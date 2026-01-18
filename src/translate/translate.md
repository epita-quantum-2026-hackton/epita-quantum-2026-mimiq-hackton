Translate module
---

This document presents the **`translate` module**, responsible for the **translation from MimiQ to QNAAsm**.

# Table of contents
- [Translate](#translate)
    - [Surface code](#surface-code)
    - [Translation](#translation)
- [`translate` module](#translate-module-1)
    - [Module architecture](#module-architecture)
- [Design choices](#design-choices)
- [Implementation details](#implementation-details)
    - [Surface code mapping](#surface-code-mapping)
    - [Translation](#translation-1)



# Translate

The **translate** stage is the final step of the MimiQ compiler.

Given a MimiQ `Circuit` and a **physical mapping** (positions on the 2D neutral-atom grid), it produces an executable **QNAasm** program.  
It inserts **resource allocation**, **routing with moves** for two-qubit gates (with **collision avoidance**), **measure/reset/conditionals**, and applies a **simple move optimization**.


## Surface code

The surface code encodes one logical qubit into a 2D-grid of 17 physical qubits: 9 data qubits and 8 ancilla qubits for a distance-3 code.

Data qubits occupy a $3\times3$ grid, while ancillas are placed between them to measure stabilizers.

Below is the layout (`D` for data qubits, `A` for ancilla qubits) of the $3\times3$ grid :

```
				|XA	|	
	|D8	|	|D7	|	|D6	|
|ZA	|	|XA	|	|ZA	|	|
	|D5	|	|D4	|	|D3	|
	|	|ZA	|	|XA	|	|ZA |
	|D2	|	|D1	|	|D0	|
	|	|XA	|	|	|	|
```

Each such **patch** represents one *logical* qubit (17 physical qubits).  
Patches are then placed on a **regular 2D-grid**, with a **fixed spacing of 8 units** between their anchor positions.  
This spacing guarantees:
- **no overlap** between physical qubits of neighbouring patches,  
- a **regular grid structure** that simplifies subsequent routing and movement planning in the translator.


## Translation

The **translation stage** converts a high-level MimiQ `Circuit` into a sequential **QNAasm program**, using the physical qubit layout provided by the surface-code mapping.  
The translator performs four main tasks: resource allocation, instruction lowering, resource cleanup, and move optimization.

### Overview

The translation process follows this structure:

1. **Resource allocation**: allocate classical registers and all physical qubits (quantum registers).
2. **Instruction lowering**: convert each MimiQ instruction into one or more QNAasm nodes.
3. **Resource cleanup**: free all allocated qubits.
4. **Move simplification**: remove redundant `Move` pairs.

The result is a QNAasm program that matches both the logical semantics of the input circuit and the physical constraints of the target architecture.

### Resource Allocation

Before translating the circuit, the translator **allocates** all the needed *classical* and *quantum* resources: it sizes and allocates the measurement register `c`, allocates the auxiliary register `drop`, and allocates all physical qubits defined in the surface-code mapping.

These allocations form the **prologue section** of the generated **QNAasm program**.

### Instruction Lowering

Each MimiQ instruction is **lowered** independently. The translation depends on the type of operation.

#### One-qubit gates
One-qubit gates are translated directly:
```
Gate(name, [position])
```
where `position` is the mapped physical location of the involved qubit.

#### Two-qubit gates

Two-qubit gates require routing because both qubits must be adjacent on the grid.

For each two-qubit operation, the translator:
1. Computes a path between the two qubits using `calculate_moves`.
2. Inserts a sequence of `Move` instructions for each step of the path.
3. If an intermediate point is occupied, a detour is computed via `move_aside`.
4. Applies the gate at the final position reached by the moved qubit.
5. Replays the moves in reverse order to return the qubit to its original position.

#### Measure

A measurement becomes:
```
Measure([position], ClassicalRegister("c", bit_index))
```
where `bit_index` corresponds to the classical bit used by the MimiQ instruction.

#### Reset

A `Reset` is expanded into:
```
Measure([position], ClassicalRegister("drop"))
Qfree([position])
Qalloc([position])
```
This ensures that the qubit is re-initialized in place.

#### IfStatement

Conditional instructions are lowered into nested `Conditional` blocks:

- The inner instruction is recursively translated.
- Multiple instructions are grouped in a `Block`.
- A `Conditional` is emitted for each tested classical bit.

#### Unsupported operations

If an instruction has arity greater than two, translation stops and returns `None`.

### Resource Cleanup

After translating all instructions, the translator frees each allocated physical qubit using:
```
Qfree([position])
```
This forms the **epilogue section** of the QNAasm program.

### Optimization

The last stage is the program optimization.

For the MimiQ compiler, we **optimize the `move`s**, by removing adjacent moves that cancel each other.


# `translate` module

The `translate` module is responsible for the translation from the QEC surface code (in MimiQ) to the QNAasm language.


## Module architecture

The architecture of the `translate` module is the following.

- [`surface_code_mapping.py`](surface_code_mapping.py)
- [`translation.py`](translation.py)


# Design choices

## Fixed surface-code tiling and spacing

We use a **fixed 17-qubit tile** for each logical qubit and place tiles on a **regular grid with spacing 8**.

This ensures:
- no overlap between neighbouring patches,
- uniformity of physical coordinates,
- simpler routing, because movements follow an orthogonal grid with known safe distances.


## Minimal routing strategy

Two-qubit gates require bringing the qubits together.  
The routing strategy is intentionally simple and deterministic, matching the implementation:
- increment/decrement `x` until aligned,
- then increment/decrement `y`.

This produces a path similar to a Manhattan path without introducing algorithmic complexity.


## Local qubit reset using a dedicated `drop` register

A **reset** is implemented as: `Measure`, `Qfree`, `Qalloc`.  
The measurement result is discarded using a dedicated **`drop` register**, which:
- avoids polluting the user's measurement register,
- simplifies semantics (the dropped bits are never read),
- mimics hardware behaviour.


## Strict separation of responsibilities

- `surface_code_mapping.py`: physical placement only.
- `translation.py`: lowering + routing.

This modularity allows replacing the layout or routing algorithm independently.


## Peephole optimization only

We restrict optimizations to removing adjacent `Move` pairs that cancel.  
No global optimization is attempted. The goal is correctness and transparency, not aggressive optimization.




# Implementation details

## Surface code mapping

This section documents the code implemented in [`surface_code_mapping.py`](surface_code_mapping.py).

The surface code encodes one logical qubit into a 2D-grid of 17 physical qubits: 9 data qubits and 8 ancilla qubits for a distance-3 code.

This file builds the physical layout of **surface-code patches**, where each logical qubit is expanded to a 17-qubit tile (9 data qubits, 8 ancilla qubits).  
It assigns a **Position** to every physical qubit and places all patches on a **regular 2D-grid** so that the translator can operate with explicit coordinates.



### `create_surface_code_mapping`

#### Description

The `create_surface_code_mapping` function physically maps a surface code for a given `qubit` to a specific `position` given as argument.

The data qubits are from position `qubit + 0` to `qubit + 8` and the ancillas from position `qubit + 9` to `qubit + 16`.   
Data qubits occupy a $3\times3$ grid, while ancillas are placed between them to measure stabilizers.


#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`qubit`|integer|Base physical index used to label the 17 sites of the tile.|
|`position`|`Position`|Anchor position of the tile; the 16 other sites are placed at fixed offsets around it.|

#### Returned Value

It returns a `dict[int, Position]` of the 17 physical indices (`qubit`, ... `qubit + 16`) mapped to their grid `Position` (17 entries).


#### Function signature

```python
def create_surface_code_mapping(qubit: int, position: Position) -> dict[int, Position]:
```

### `create_all_surface_code_mapping`

#### Description

The `create_all_surface_code_mapping` function creates a full surface code mapping for a specified number of (logical) qubits.

It places each *logical* `qubit` (17 entries in total) on the grid at column `col` and line `row`.

There is enough space between the qubits logical on the grid for all the physical qubits needed to implement one logical qubit.

We map each **logical qubit** onto a 2D-grid using row-major order.  
For a given patch index `i`, we compute its grid indices as: 
```python
col = i % square_size
row = i // square_size
```
These are **grid indices** (`column`, `row`), not physical coordinates.

The **physical anchor** of the patch is then:
```python
Position(col * 8 + 6, row * 8 + 6)
```
where:
- `8` is the **inter-patch spacing**, large enough to avoid overlaps given the patch's internal offsets (which span roughly 6 units),
- `+6` is a **global offset** ensuring non-negative coordinates and aligning the tiling with the QPU's coordinate system.  
Each patch (**logical qubit**) accounts for **17 physical qubits** (indices `i * 17` to `i * 17 + 16`).

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`qubits_count`|integer|total number of qubits in the MimiQ circuit|

#### Returned Value

It returns a `dict[int, Position]` mapping every physical qubit index of every patch to its corresponding position on the grid.


#### Function signature

```python
def create_all_surface_code_mapping(qubits_count: int) -> dict[int, Position]:
```

### `create_all_surface_code_mapping_for_circuit`

#### Description

The `create_all_surface_code_mapping_for_circuit` function creates a full surface code mapping for a given MimiQ circuit `c`.

It simply applies `create_all_surface_code_mapping` for the number of qubits of the circuit.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`c`|`Circuit`|MimiQ circuit on which we want to map surface codes to positions on the QPU grid|

#### Returned Value

It returns a `dict[int, Position]` giving the physical position of all qubits on the circuit`.


#### Function signature

```python
def create_all_surface_code_mapping_for_circuit(c: Circuit) -> dict[int, Position]:
```


## Translation

We present here the code implemented in [`translation.py`](translation.py).


This file **lowers** a **MimiQ** `Circuit` to **QNAasm**.  
It allocates the necessary classical/quantum resources translates each instruction then frees resources and runs a local peephole optimization on moves. 
Input: a MimiQ circuit and a **physical mapping** `dict[int, Position]`.  
Output: a list of QNAasm node.


### `move_aside`

#### Description

The `move_aside` function moves an obstacle qubit aside.

It computes a one-step detour for an obstacle blocking the planned path of a moving qubit.  
Using the current move (`m1`) and optionally the next move (`m2`), it chooses a lateral displacement that clears the path without breaking the movement sequence.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`m1`|`tuple` (`Position`, `Position`)|First move in the path.|
|`m2`|`Optional` `tuple` (`Position`, `Position`)|Second move in the path, may be omitted if the move is the last of the path.|

#### Returned Value

It returns a single displacement `(from, to)` of type `tuple[Position, Position]` describing where the obstacle is temporarily moved.


#### Function signature

```python
def move_aside(
    m1: tuple[Position, Position], m2: Optional[tuple[Position, Position]]
) -> tuple[Position, Position]:
```


### `calculate_moves`

#### Description

The `calculate_moves` function computes the movements needed to move a qubit in position `q1` to a position next to the qubit `q2`.

The function advances from `q1` toward `q2` by incrementing or decrementing `x` until both qubits share the same column, then does the same for `y`.  
If an intermediate position is already occupied (`position in qubits.values()`), the function first calls `move_aside` to temporarily displace the blocking qubit, then appends the planned step and continues.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`q1`|`Position`|Position of the qubit to move.|
|`q2`|`Position`|Position of the qubit we want to reach.|
|`qubits`|dictionary (integer: `Position`)|Physical positions of each qubit.|

#### Returned Value

It returns a `list[tuple[Position, Position]]`, each tuple representing a movement segment `(from, to)` in the path.


#### Function signature

```python
def calculate_moves(
    q1: Position, q2: Position, qubits: dict[int, Position]
) -> list[tuple[Position, Position]]:
```


### `remove_useless_moves`

#### Description

The `remove_useless_moves` function removes moves that are doing the exact same opposite movements one after the other.

It removes adjacent pairs of `Move` instructions that cancel each other  (a forward step immediately followed by its exact reverse).  
For instance:
```
        move {0,0} to {0,1}
        move {0,1} to {0,0}
```

After removal, the returned index may move backward to catch chained cancellations.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`instructions`|`list` of `QNAasm`|QNAasm instructions that need to be optimized.|
|`idx`|integer|position of the first move that may be removed.|

#### Returned Value

It returns a tuple `(new_instructions, new_idx)` (of type `tuple[list[QNAasm], int]`), where `new_instructions` is the updated list after simplification and `new_idx` is the next index to check.


#### Function signature

```python
def remove_useless_moves(
    instructions: list[QNAasm], idx: int
) -> tuple[list[QNAasm], int]:
```


### `optimize`

#### Description

The `optimize` function **optimizes** moves inside the resulting QNAasm program.

It repeatedly applies `remove_useless_moves` over the full instruction list to remove all immediate inverse `Move` pairs.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`instructions`|`list` of `QNAasm`|QNAasm instructions that need to be optimized.|

#### Returned Value

It returns the optimized list of QNAasm instructions (of type `list[QNAasm]`).

#### Function signature

```python
def optimize(instructions: list[QNAasm]) -> list[QNAasm]:
```


### `calculate_creg_size`

#### Description

The `calculate_creg_size` function calculates the size required for the measurement classical register of the whole circuit.

It scans all `Measure` instructions in the MimiQ circuit and returns the highest measured classical bit index plus one.  
If the circuit contains no measurement, it returns `0`.


#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`c`|`Circuit`|MimiQ circuit to translate to QNAasm|

#### Returned Value

It returns the required size of the measurement register `c` as an integer (`int`).


#### Function signature

```python
def calculate_creg_size(c: Circuit) -> int:
```


### `translate_instruction`

#### Description

The `translate_instruction` function translates a single MimiQ instruction into one or more QNAasm instructions.

The `translate_instruction` function lowers a single MimiQ instruction to one or more QNAasm instructions. Its behavior depends on the instruction type:
* 1-qubit gates: `Gate(name, [pos])`
* 2-qubit gates: routing with `Move` segments, then the gate, then reverse moves
* `Measure`: `Measure([...], ClassicalRegister("c", bit))`  
* `Reset`: `Measure` + `Qfree` + `Qalloc`  
* `IfStatement`: nested `Conditional`, wrapping multiple instructions inside a `Block`  
If the operation has unsupported arity ($> 2$), the translator aborts translation and returns `None`.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`instr`|`Instruction`|MimiQ instruction to translate.|
|`qubits`|`dict[int, Position]`|Physical positions of each qubit.|

#### Returned Value

It returns an `Optional[list[QNAasm]]`: a list of QNAasm instructions, or `None` for unsupported operations.

#### Function signature

```python
def translate_instruction(
    instr: Instruction, qubits: dict[int, Position]
) -> Optional[list[QNAasm]]:
```


### `translate`

#### Description

The `translate` function **translates** a MimiQ circuit to a QNAasm program.

The `translate` function orchestrates the full translation pipeline:  
1. allocate the measurement register `c` and the temporary `drop` register,
2. allocate all physical qubits (`Qalloc`),
3. translate each MimiQ instruction via `translate_instruction`,
4. free all qubits (`Qfree`),
5. run `optimize` on the final instruction list.

It produces a complete linear QNAasm program.

#### Function parameters

|Argument|Type|Description|
|-|-|-|
|`c`|`Circuit`|MimiQ circuit to translate.|
|`qubits`|dictionary (integer: `Position`)|Physical positions of each qubit.|

#### Returned Value

It returns the full list of QNAasm instructions (of type `list[QNAasm]`) after optimization.

#### Function signature

```python
def translate(c: Circuit, qubits: dict[int, Position]) -> list[QNAasm]:
```
