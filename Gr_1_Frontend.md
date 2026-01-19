# Group 1: Input Handling

This document presents the work of the **Frontend** team, which handles the initial steps of the project.

All parts of the code in this team are written in **Julia**.
## Members

- GROS Théo
- BOURAS Kelyan
- SEFRIN Quentin
- ELBAZ Geoffrey
- EDDE Yohann
- DOURIEZ Eliott

The group leader is Théo GROSS

## Specifications

The **Frontend** team was essentially in charge of the sections "**3.1 Input Handling**" and "**3.2 Logical Circuit Extraction**"

> Input Handling : Implementing a module to accept the quantum circuit expressed using the MIMIQ framework. This module must validate the input, ensuring that only single and two-qubit gates are present. It must reject or warn about any unsupported gates. 
>
>Logical Circuit Extraction : Translating the validated physical-level circuit into a logical (idealized) circuit representation. The final output of this stage is an internal Intermediate Representation (IR) suitable for the error-correction encoding stage.

## Files

- [`src/frontend/InputHandling.jl`](src/frontend/InputHandling.jl), which contains the necessary functions to filter the circuit before w try to apply a surface code to it.
- [`src/frontend/filter_circuit.jl`](src/frontend/filter_circuit.jl), which checks a `.pb` circuit before calling the main function in `InputGHandling.jl` to filter the circuit and save it.
- [`src/frontend/runtests.jl`](src/frontend/runtests.jl), which contains some tests for the fronted.

## Usage

### Filter and save and IR of a circuit

You can filter a circuit and save its intermediate representation
```jl
$ julia filter_circuit.jl "input_circuit.pb"
Loading circuit from 'circuits/ghz.pb'...
Saving new circuit to 'circuits/ghz-filtered.pb'...
Filtered circuit:
       ┌─┐
q[1]: ╶┤H├─●─╴
       └─┘┌┴┐
q[2]: ╶───┤X├╴
          └─┘
```
