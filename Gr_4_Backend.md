README of the group 4 "team **Backend**"
---

This document presents the work of the **Backend** team, which is part of the class project.

It presents the **members** of the team **Backend**, the parts of **specifications** they were responsible for and the **modules** finally written by the **Backend** team.


# Members
The members of the Backend team are:
- BRAVO Cyril
- DERVAL Louis-Maël
- ESPRIMONT Théo
- HÉLIAS Alexandre
- REHS Clément
- VIGNERON Loïc

The **group leader** is Lous-Maël DERVAL.

# Specifications
The **Backend** team was essentially in charge of sections "**3.4 Physical Mapping to a Neutral-Atom Architecture**" and "**3.5 Hardware Instruction Generation**" of the specifications.

## Physical Mapping to a Neutral-Atom Architecture
### Specification extract
> **3.4 Physical Mapping to a Neutral-Atom Architecture**
>
> The compiler must map the surface-code operations onto a **2D neutral-atom array** under the following constraints:
> * Neutral atoms are arranged in a **2D grid** with limited > nearest-neighbour interactions.
> * Only single and two-qubits gates are supported.
> * Atoms can be physically moved but with a cost in time scaling linearly on the distance.
> 
> The mapping module must:
> 1. Assign each surface-code patch to a region in the NAQC array.
> 2. Schedule atom movement when required.
> 3. Decompose surface-code operations into hardware-native gates.

### Assigned task
We receive the different gates applied on physical qubits from the QEC layer. We decompose gates that were added during the QEC layer which are not supported by the hardware. Then we organize physical qubits to reduce the number of SWAP gates and atom movements. When needed, we have to schedule these SWAP gates and atom movements.

## Hardware Instruction Generation
### Specification Extract
> **3.5 Hardware Instruction Generation**
> 
> The final compilation stage must produce a device-executable instruction > sequence
> including:
> * **Native single and two-qubit gates.**
> * **Atom movement operations.**
> * **Measurement operations.**
> * **Atoms allocations/deallocations**
> * **Atom reset**
>
> The output format must follow the specification provided in the course framework.

### Assigned task
Finally, we want to generate hardware instructions in an easy to read and parse format so that the device does not have much work to apply them.

# Modules
Each module has its own documentation file (`module.md`, with `module` beeing the name of the module). Please refer to them for more detail.

The **Backend** team worked on the following modules
- `qnaasm`
- `translate`
- `utils`
    * `classical_register.py`
    * `position.py`

## `qnaasm`
This module is responsible for the definition of the **QNAasm** language: **Quantum Neutral Atom Assembly language**.  
Its documentation file can be found at `qnaasm/qnaasm.md`.

## `translate`
This module is responsible for the translation of **mimiQ** code to **QNAasm**.  
Its documentation file can be found at `translate/translate.md`.

# Backend overview
**Input**:
-	Logical qubits encoded with surface codes
-	Gates on logical qubits, only one and two qubits gates

**Output**:
-	Physical qubits, with their positions
-	Gates on physical qubits

# Illustration
H gate:
```
				XA		
	D8		D7		D6	
ZA		XA		ZA		
	D5		D4		D3	
		ZA		XA		ZA
	D2		D1		D0	
		XA				
```
```
				|XA	|	
	|D8	|	|D7	|	|D6	|
|ZA	|	|XA	|	|ZA	|	|
	|D5	|	|D4	|	|D3	|
	|	|ZA	|	|XA	|	|ZA |
	|D2	|	|D1	|	|D0	|
	|	|XA	|	|	|	|
```