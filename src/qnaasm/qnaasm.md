QNAasm module
---

This document presents the **`qnaasm` module**, which defines the **QNAasm language**.



# Table of contents
- [QNAasm language](#QNAasm-language)
    - [Motivations](#motivations)
    - [Core Instructions](#core-instructions)
- [`qnaasm` module](#qnaasm-module-1)
    - [Module architecture](#module-architecture)
- [Design choices](#design-choices)
    - [Visitor Design Pattern](#visitor-design-pattern)
    - [QNAasm (Abstract Base Class)](#qnaasm-abstract-base-class)
- [Implementation details](#implementation-details)
    - [Block](#block)
    - [Calloc](#calloc)
    - [Classical Register](#classical-register)
    - [Conditional](#conditional)
    - [Gate](#gate)
    - [Measure](#measure)
    - [Move](#move)
    - [Nodes](#nodes)
    - [Position](#position)
    - [Pretty Printer](#pretty-printer)
    - [Qalloc](#qalloc)
    - [Qfree](#qfree)
    - [QNAasm](#qnaasm)
    - [Visitor](#visitor)
- [Example](#example)



# QNAasm language

The **QNAasm** or **Quantum Neutral Atom Assembly** language is the **target language** of the compiler.

It is a low-level language designed for **neutral atom** computers.

The language is inspired by classical assembly languages: it provides explicit instructions for resource allocation, movement, gate application, and measurement.  
Each instruction corresponds to a physical operation or a control structure that the hardware can interpret.

## Motivations

We need a language to represent a program executable by a neutral atom QPU.

We choose to implement the following instruction for a language named **QNAasm**:

* **Gate**: to represent a one or multiple qubits gate.
* **Move**: to move a qubit from a position to another.
* **Qalloc**: to allocate a qubit at a given position.
* **Qfree**: to deallocate a qubit at a given position.
* **Calloc**: to allocate a classical register of a given size.
* **Measure**: to measure a qubit at a given position inside a classical register.
* **Conditional**: to execute an instruction if the value of a classical register matches a given value.
* **Block**: to store multiple instructions inside one usually used inside Conditional instructions.

A **program** is a list of **QNAasm instructions**.


## Core Instructions

### Block instructions

A **block instruction** groups multiple instructions together, typically used inside conditionals.

*Syntax:*
```QNAasm
intr1
intr2
...
intrN
```

> `instr1`, `instr2`, ..., `instrN` are `N` $\in \mathbb{N}^*$ instructions composing the block.

*Example:*  
```
    {
      move {3,1} to {4,1}
      move {3,0} to {3,1}
      move {3,1} to {3,2}
      gate CX {3,2},{3,3}
      move {3,2} to {3,1}
      move {3,1} to {3,0}
      move {4,1} to {3,1}
    }
```
The previous example shows a list of instruction grouped within a block (between the curly brackets `{...}`).


### Calloc Instruction

A **calloc instruction** allocates a classical register with a given name and size.

*Syntax:*
```QNAasm
calloc creg_name[size]
```
> `creg_name` is the name of the classical register on which we allocate `size` data.

*Example:*  
```QNAasm
calloc creg[4]
```
`calloc creg[4]` allocates a classical register named `creg` of size 4.


### Conditional instruction

A **conditional instruction** executes an instruction only if the classical register matches a given value.

*Syntax:*
```QNAasm
if creg = value then
  instruction
```

> `creg` is the name of the classical register we compare with `value`.  
> `instruction` is the instruction to execute (which can be a single instruction or multiple instruction regrouped within a block for example).

*Example:*  
```QNAasm
if c[0] = 1 then
  gate X {0,0}
```
The previous code applies instruction `gate X {0, 0}` if classical register `c[0]` equals `1`.


### Gate instruction

The **gate instruction** applies a quantum gate to one or more qubits at specified positions.

*Syntax:*
```QNAasm
gate name targets
```

> `name` is the name of the gate to apply.  
> `targets` is the list of the positions of the qubits on which we want to apply the gate.

*Examples:*  
*single-qubit Gate*  
```QNAasm
gate H {3,1}
```
`gate H {3,1}` applies a H gate on qubit at position `{3,1}`.

*Multiple-qubits Gate: a 2-qubits Gate*  
```QNAasm
gate CX {0,0} {1,0}
```
`gate CX {0,0} {1,0}` applies a controlled-X gate between two qubits (qubit target 1 is at position `{0,0}`, and qubit target 2 is at position `{1,0}`).


### Measure instruction

The **measure instruction** measures one or more qubits and stores the result in a classical register.

*Syntax:*
```QNAasm
measure targets creg
```

> `targets` is the list of the positions of the qubits we want to measure.  
> `creg` is the name of the classical register used to store the classical result of the quantum measure.

*Example:*  
```QNAasm
measure {0,0} {1,0} to creg
```
`measure {0,0} {1,0} to creg` measures two qubits (measured qubit 1 is at position `{0,0}`, and measured qubit 2 is at position `{1,0}`) and stores results in `creg`.


### Move instruction

The **move instruction** moves a qubit from its current position to a new position in the neutral-atom grid.  

*Syntax:*
```QNAasm
move start_position end_position
```

> `start_position` is the start position of the qubit to move (source position).  
> `end_position` is the end position of the qubit to move (destination position).  

*Example:*  
`move {0,0} {1,0}` moves a qubit from `{0,0}` to `{1,0}`.

*Note:*  
The name `move` is inspired from classical assembly sets.


### Qalloc instruction

The **qalloc instruction** allocates quantum resources (qubits) at given positions.  

*Syntax:*
```QNAasm
qalloc targets
```

> `targets` is the list of the positions of the qubits we want to allocate.  

*Examples:*  
*Single qubit allocation*  
```QNAasm
qalloc {0,0}
```
`qalloc {0,0}` allocates one qubit at position `{0,0}`.


*Multiple qubit allocation: a 2-qubit allocation*  
```QNAasm
qalloc {0,0} {1,0}
```
`qalloc {0,0} {1,0}` allocates two qubits at positions `{0,0}` and `{1,0}`.

*Note:*  
The name `qalloc` is the quantum analogy to `calloc`.


### Qfree instruction

The **qfree instruction** deallocates quantum resources at given positions. 

*Syntax:*
```QNAasm
qfree targets
```

> `targets` is the list of the positions of the qubits we want to deallocate.  

*Examples:*  
*Free single qubit*
```QNAasm
qfree {0,0}
```
`qfree {0,0}` frees the qubit at position `{0,0}`.

*Free multiple qubits*
```QNAasm
qfree {0,0},{0,5}
```
`qfree {0,0},{0,5}` frees the qubits at position `{0,0}` and `{0,5}`.

*Note:*  
The name `qfree` is the quantum analogy to `free`.



# `qnaasm` module

The `qnaasm` module is responsible for the definition and implementation of the QNAasm language.


## Module architecture

The architecture of the `qnaasm` module is the following:
- `block.py`
- `calloc.py`
- `conditional.py`
- `gate.py`
- `measure.py`
- `move.py`
- `nodes.py`
- `pretty_printer.py`
- `qalloc.py`
- `qfree.py`
- `qnaasm.py`
- `visitor.py`



# Design choices

## Visitor Design Pattern

The **visitor design pattern** is used to keep QNAasm instructions simple by separating their data from the operations applied to them.

Each class representing an instruction only stores its attributes, while visitors implement behaviors like printing.  
This makes the code easier to maintain and extend because new operations can be added without changing the instruction classes. Every instruction provides an `accept(visitor)` method that calls the appropriate `visit_*` method in the visitor.

## QNAasm (Abstract Base Class)

The `QNAasm` class is the **abstract base class** for all QNAasm instructions.  
It is implemented in `qnaasm.py`.

Every instruction inherits from `QNAasm` and implements the `accept(visitor)` method to support the **Visitor pattern**.



# Implementation details

## Block

The `Block` class represents a **block of instructions**.  
It is implemented in [`block.py`](block.py).

A **block** stores a list of instructions and is commonly used within Conditional instructions.

### Structure

```
Block
    instructions
```

|Attribute|Type|Description|
|-|-|-|
|`instructions`|`list` of `QNAasm`|instructions to execute inside the block|

### Class signature

```python
class Block(QNAasm):
    def __init__(self, instructions: list[QNAasm]):
```


## Calloc

The `Calloc` class represents a **calloc instruction**.  
It is implemented in [`calloc.py`](calloc.py).

A **calloc instruction** is a classical memory allocation instruction.
It allocates a classical register with a given name and size.

### Structure

```
Calloc
    name
    size
```

|Attribute|Type|Description|
|-|-|-|
|`name`|string|name of the register|
|`size`|integer|size of the register|

### Class signature

```python
class Calloc(QNAasm):
    def __init__(self, name: str, size: int):
```


## Classical Register
The `ClassicalRegister` class represents a **classical register** or a **specific bit** within such a register.  
It is implemented in [`classical_register.py`](classical_register.py).

A **classical register** is used to store classical data.
I may refer either to:
- either an entire named register (`idx = None`) ;
- or a specific indexed bit inside the register  (`idx` set to an integer). 

### Structure

```
ClassicalRegister
    name
    idx
```

|Attribute|Type|Description|
|-|-|-|
|`name`|string|name of the register|
|`idx`|integer or `None`|Optional index referring to a specific classical bit|

### Class signature

```python
class ClassicalRegister:
    def __init__(self, name: str, idx: Optional[int] = None):
```


## Conditional

The `Conditional` class represents a **conditional instruction**.  
It is implemented in [`conditional.py`](conditional.py).

A **conditional instruction** executes a quantum or classical instruction only if a classical register matches a given value.

### Structure

```
Conditional
    creg
    value
    instruction
```

|Attribute|Type|Description|
|-|-|-|
|`creg`|`ClassicalRegister`|classical register to test|
|`value`|integer|value to match the register against|
|`instruction`|`QNAasm`|instruction to execute on match|

### Class signature
```python
class Conditional(QNAasm):
    def __init__(self, creg: ClassicalRegister, value: int, instruction: QNAasm):
```


## Gate

The `Gate` class represents a **gate instruction**.  
It is implemented in [`gate.py`](gate.py).

A **gate instruction** applies a quantum gate to one or more qubits.  
Targets are specified as positions in the neutral-atom grid.

### Structure

```
Gate
    name
    targets
```

|Attribute|Type|Description|
|-|-|-|
|`name`|string|name of the gate|
|`targets`|`list` of `Position`|positions of the qubits on which to apply the gate|

### Class signature

```python
class Gate(QNAasm):
    def __init__(self, name: str, targets: list[Position]):
```


## Measure

The `Measure` class represents a **measure instruction**.  
It is implemented in [`measure.py`](measure.py).

A **measure instruction** measures one or more qubits at given positions and stores the result in a classical register.

### Structure

```
Measure
    targets
    creg
```

|Attribute|Type|Description|
|-|-|-|
|`targets`|`list` of `Position`|positions of the qubits to measure|
|`creg`|`ClassicalRegister`|classical register inside which to store the result of the measure|

### Class signature

```python
class Measure(QNAasm):
    def __init__(self, targets: list[Position], creg: ClassicalRegister):
```


## Move

The `Move` class represents a **move instruction**.  
It is implemented in [`move.py`](move.py).

A **move instruction** moves a qubit from one position to another in the neutral-atom array.  

### Structure

```
Move
    start
    end
```

|Attribute|Type|Description|
|-|-|-|
|`start`|`Position`|initial position of the qubit|
|`end`|`Position`|new position of the qubit|

### Class signature

```python
class Move(QNAasm):
    def __init__(self, start: Position, end: Position):
```


## Nodes

The [`nodes.py`](nodes.py) file aggregates all instruction classes for easier imports.

```python
from qnaasm.nodes import (
    Block,
    Calloc,
    Conditional,
    Gate,
    Measure,
    Move,
    Qalloc,
    Qfree,
    QNAasm,
)
```


## Position
The `Position` class represents a **position** on the 2D atom-grid.  
It is implemented in [`position.py`](position.py).

A **position** is a pair of coordinate over the x and y axis on the 2D atom-grid. 

### Structure

```
Position
    x
    y
```

|Attribute|Type|Description|
|-|-|-|
|`x`|integer|x-axis coordinate|
|`y`|integer|y-axis coordinate|

### Class signature

```python
class Position:
    def __init__(self, x: int, y: int):
```


## Pretty Printer

The `PrettyPrinter` class implements a concrete Visitor that prints QNAasm programs in a human-readable format with indentation for nested structures.  
It is implemented in [`pretty_printer.py`](pretty_printer.py).

### Structure

```
PrettyPrinter
    level
```

|Attribute|Type|Description|
|-|-|-|
|`level`|integer|level of indentation (0 by default)|

### Class signature

```python
class PrettyPrinter(Visitor):
    def __init__(self):
```


## Qalloc

The `Qalloc` class represents a **qalloc instruction**.  
It is implemented in [`qalloc.py`](qalloc.py).

A **qalloc instruction** allocates a quantum resource (qubit) at a given position in the neutral-atom grid.


### Structure

```
Qalloc
    targets
```

|Attribute|Type|Description|
|-|-|-|
|`targets`|`list` of `Position`|positions where a qubit must be allocated|


### Class signature

```python
class Qalloc(QNAasm):
    def __init__(self, targets: list[Position]):
```


## Qfree

The `Qfree` class represents a **qfree instruction**.  
It is implemented in [`qfree.py`](qfree.py).

A **qfree instruction** deallocates a quantum resource (qubit) at a given position in the neutral-atom grid.

### Structure

```
Qfree
    targets
```

|Attribute|Type|Description|
|-|-|-|
|`targets`|`list` of `Position`|positions where a qubit must be deallocated|

### Class signature

```python
class Qfree(QNAasm):
    def __init__(self, targets: list[Position]):
```


## QNAasm

The `QNAasm` class is the **abstract base class** for all QNAasm instructions.  
It is implemented in [`qnaasm.py`](qnaasm.py).

Every instruction inherits from `QNAasm` and implements the `accept(visitor)` method to support the **Visitor pattern**.


### Structure

```
QNAasm
```

|Attribute|Type|Description|
|-|-|-|
|.|.|*No attributes*|

The class is very basic and just inherits from `ABC` metaclass and has an `accept` method to accept visitors.

### Class signature

```python
class QNAasm(ABC):
```


## Visitor

The `Visitor` class defines the interface for visiting QNAasm instructions.  
It is implemented in [`visitor.py`](visitor.py).

Visitors allow operations (like printing) to be applied without modifying instruction classes.

### Structure
```
Visitor
```

This class has no attribute but has many visit methods.

|Method|Description|
|-|-|
|`visit_block(e: Block)`|Visit a Block instruction|
|`visit_calloc(e: Calloc)`|Visit a Calloc instruction|
|`visit_conditional(e: Conditional)`|Visit a Conditional instruction|
|`visit_gate(e: Gate)`|Visit a Gate instruction|
|`visit_measure(e: Measure)`|Visit a Measure instruction|
|`visit_move(e: Move)`|Visit a Move instruction|
|`visit_qalloc(e: Qalloc)`|Visit a Qalloc instruction|
|`visit_qfree(e: Qfree)`|Visit a Qfree instruction|
|`visit_qnaasm(e: QNAasm)`|Generic visit method|


### Class signature

```python
class Visitor(ABC):
    def visit_block(self, e: "Block"):
    def visit_calloc(self, e: "Calloc"):
    def visit_conditional(self, e: "Conditional"):
    def visit_gate(self, e: "Gate"):
    def visit_measure(self, e: "Measure"):
    def visit_move(self, e: "Move"):
    def visit_qalloc(self, e: "Qalloc"):
    def visit_qfree(self, e: "Qfree"):
```



# Example

An example can be found and run in the [`write_qnaasm_circuits.ipynb`](../examples/write_qnaasm_circuits.ipynb) notebook.
