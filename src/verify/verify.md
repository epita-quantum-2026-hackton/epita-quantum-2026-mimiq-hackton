Verify module
---

This document presents the **`verify` module**, responsible for the static **verification of QNAasm programs** before execution.



# Table of contents
- [Verify](#verify)
  - [Purpose](#purpose)
  - [Overview](#overview)
- [`verify` module](#verify-module-1)
  - [Module architecture](#module-architecture)
- [Design choices](#design-choices)
  - [Visitor-based verification](#visitor-based-verification)
- [Implementation details](#implementation-details)
  - [`Verifier` (visitor)](#verifier-visitor)
  - [`verify`](#verify)
- [Example](#example)



# Verify

## Purpose

The **verify stage** ensures that a QNAasm program is **correct and physically realizable** before execution on a neutral-atom device.  
It checks resource correctness, movement rules, neighbor constraints, and classical register usage.


## Overview

The **verifier** traverses instructions, prints errors to stderr, and returns `True` if no violation is detected.  
It also enforces that all qubits are deallocated at the end of the program.

### Checks per instruction

- **Calloc**: register must not already exist.
- **Qalloc**: targets must be free.
- **Qfree**: targets must contain a qubit.
- **Move**: start must contain a qubit; end must be free; both must be neighbors.
- **Gate**: 1-2 targets; if 2, must be neighbors.
- **Measure**: qubits must exist; register index/size must match.
- **Conditional**: register must exist; cannot change registers or qubits.




# `verify` module

## Module architecture

The architecture of the `verify` module is the following.

- [`verifier.py`](verifier.py)
- [`verification.py`](verification.py)



# Design choices

## Visitor-based verification

Using the **Visitor pattern** centralizes verification logic and keeps QNAasm instruction classes simple.



# Implementation details

## `Verifier` (visitor)

The `Verifier` class implements a concrete Visitor that verifies QNAasm programs.  
It is implemented in [`verifier.py`](verifier.py).

The `Verifier` stores classical registers, live qubit positions, and an error flag.  
Errors are printed via `set_error(msg)`.

### Structure

```
Verifier
    cregs
    qubits
    error
```

|Attribute|Type|Description|
|-|-|-|
|`cregs`|dictionary|Classical registers of the QNAasm program to verify.|
|`qubits`|set|Set of currently allocated qubit positions.|
|`error`|boolean|Error Flag. `False` by default.|


The class contains **methods** and **visiting methods**.

```
set_error(msg: str)
visit_block(e: "Block")
visit_calloc(e: "Calloc")
visit_conditional(e: "Conditional")
visit_gate(e: "Gate")
visit_measure(e: "Measure")
visit_move(e: "Move")
visit_qalloc(e: "Qalloc")
visit_qfree(e: "Qfree")
visit_qnaasm(e: "QNAasm")
```

|Method|Description|
|-|-|
|`set_error(msg: str)`|Set an error message.|
|`visit_block(e: "Block")`|Visit a `Block`.|
|`visit_calloc(e: "Calloc")`|Visit a `Calloc`.|
|`visit_conditional(e: "Conditional")`|Visit a `Conditional`.|
|`visit_gate(e: "Gate")`|Visit a `Gate`.|
|`visit_measure(e: "Measure")`|Visit a `Measure`.|
|`visit_move(e: "Move")`|Visit a `Move`.|
|`visit_qalloc(e: "Qalloc")`|Visit a `Qalloc`.|
|`visit_qfree(e: "Qfree")`|Visit a `Qfree`.|
|`visit_qnaasm(e: "QNAasm")`|Visit a `QNAasm`.|

### Class signature

```python
class Verifier(Visitor):
```

## `verify`

The `verify` function runs the **verifier** on each instruction and checks that no qubit remains allocated.  
It is implemented in [`verification.py`](verification.py).

It is the entry point of the verify module. 

### Function parameters

|Argument|Type|Description|
|-|-|-|
|`instructions`|`list` of `QNAasm`|All the instructions that compose the circuit.|

### Returned value

The function returns a boolean indicating if the verified circuit is valid and can be executed in nearest neighbors (`True`).

### Function signature

```python
def verify(instructions: list[QNAasm]) -> bool:
```



# Example

An example can be found and run in the [`verify_a_qnaasm_circuit.ipynb`](../examples/verify_a_qnaasm_circuit.ipynb) notebook.
