# Group 3: Error correction

This document presents the work of the **Quantum Error Correction** team.

It presents the **members** of the team QEC, the parts of **specifications** they were responsible for and the modules finally written by the **QEC** team (and how to use it).

All parts of the code in this team are written in **Julia**.

## Members

- BARDOUIL Maxime François [maxime-francois.bardouil@epita.fr](mailto:maxime-francois.bardouil@epita.fr)
- DIAMANT Arnaud [arnaud.diamant@epita.fr](mailto:arnaud.diamant@epita.fr)
- DJERMOUNE Kylian [kylian.djermoune@epita.fr](mailto:kylian.djermoune@epita.fr)
- FLORION Thomas [thomas.florion@epita.frr](mailto:thomas.florion@epita.fr)
- HAY--KERGROHENN Quentin [quentin.hay-kergrohenn@epita.fr](mailto:quentin.hay-kergrohenn@epita.fr)
- NAJI Hamza [hamza.naji@epita.fr](mailto:hamza.naji@epita.fr)

## Specifications

The **QEC** team was essentially in charge of the section "**3.3 Error Correction Layer (Surface Code)**":

> The compiler must:
> 1. Encode each logical qubit using a surface-code patch, with variable size.
>      - Translate each logical operation into physical operations supported by a
> NAQC.
> 2. Schedule stabilizer/QEC rounds to maintain code integrity during > computation.
> 3. Track error-correction overhead:
>      - Extra qubits (ancilla patches)
> 
> The final output of this stage must be a fully error-protected logical circuit expressed
> as surface-code instructions.


**Available gates: H, X, Z, CX, SWAP, T, Measure.**

**Note 1**: the T gate is probably **not stable**. It worked for our tests, but it is basically a T gate applied on the data qubit in the center of the surface code.\
**Note 2**: every gate must be single qubit (except CX) (for example, a Measure will be on qubit n and bit n, but not ranges of qubits like n:m to bits n:m).\
**Note 3**: Noise is not available. To add noise, you must open the corrected circuit in another python / julia script, add noise, and resave the corrected circuit (as shown in [`src/qec/surface_code_3.ipynb`](src/qec/surface_code_3.ipynb), in `Test GHZ state with error`).

## Files

- [`src/qec/surface_code_3.ipynb`](src/qec/surface_code_3.ipynb), you will find the different functions to test a custom circuit. This is a Julia notebook made for testing purpose.

- [`src/qec/correct_circuit.jl`](src/qec/correct_circuit.jl), you can input a certain circuit file (`*.pb`), and it will output the physically corrected version using surface code with a distace 3.

- [`src/qec/execute_corrected_circuit.jl`](src/qec/execute_corrected_circuit.jl), you can input a certain circuit file (`*.pb`), it will verify if there is the `[filename]-corrected.pb` associated file, and it will run them on Mimiq emulator.

- [`src/qec/create_ghz.jl`](src/qec/create_ghz.jl): create `ghz.pb` when run, a very simple GHZ circuit of 2 qubits with measure.

- `ghz.pb` / `ghz-corrected.pb`: files to test default circuits. created with [`src/qec/create_ghz.jl`](src/qec/create_ghz.jl) and [`src/qec/correct_circuit.jl`](src/qec/correct_circuit.jl).

## Usage

### Create a circuit

You can generate a ghz circuit of 2 qubits with:
```jl
$ julia create_ghz.jl
       ┌─┐   ┌─┐
q[1]: ╶┤H├─●─┤M├───╴
       └─┘┌┴┐└╥┘┌─┐
q[2]: ╶───┤X├─╫─┤M├╴
          └─┘ ║ └╥┘
              ║  ║
c:    ════════╩══╩═
              1  2

Created file ghz.pb
```

### Create the corrected circuit
```bash
$ julia correct_circuit.jl [filename].pb
```
It will output the file `[filename]-corrected.pb`.

### Circuit execution:
```bash
$ julia execute_corrected_circuit.jl [filename].pb 
[ Info: Listening on: 127.0.0.1:1444, thread id: 1
[ Info: Please login in your browser at http://127.0.0.1:1444
[ Info: Server on 127.0.0.1:1444 closing
Sending job execution of '[filename].pb'...
Sending job execution of '[filename]-corrected.pb'...
Wating results of '[filename].pb'...
Wating results of '[filename]-corrected.pb'...

Results:

Logical results ([filename].pb):
Dict{BitString, Int64}(bs"00" => 503, bs"11" => 497)

Physical_corrected ([filename]-corrected.pb):
Dict("00" => 46, "11" => 54)
```

This will run both the logical and corrected circuit.
