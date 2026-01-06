# Group 3: Error correction

In this group we are working on the error correction code in Julia.

In the file [`surface_code_3.ipynb`](./surface_code_3.ipynb), you will find the different functions to test a custom circuit.

In the file [`correct_circuit.jl`](./correct_circuit.jl), you can input a certain circuit file (`*.pb`), and it will output the physically corrected version using surface code with a distace 3.
To run it, execute:
```bash
$ julia correct_circuit.jl ghz.pb
```
It will output the file `[circuit-name]-corrected.pb`.

Available gates: H, X, Z, CX, SWAP, T, Measure.

Note: the T gate is approximately working, but it shouldn't.

Circuit execution:
After creating the corrected circuit, run
```bash
$ julia execute_corrected_circuit.jl ghz.pb 
[ Info: Listening on: 127.0.0.1:1444, thread id: 1
[ Info: Please login in your browser at http://127.0.0.1:1444
[ Info: Server on 127.0.0.1:1444 closing
Sending job execution of 'ghz.pb'...
Sending job execution of 'ghz-corrected.pb'...
Wating results of 'ghz.pb'...
Wating results of 'ghz-corrected.pb'...

Results:

Logical results (ghz.pb):
Dict{BitString, Int64}(bs"00" => 503, bs"11" => 497)

Physical_corrected (ghz-corrected.pb):
Dict("00" => 46, "11" => 54)
```
by giving in argument the name of the original circuit.

This will run bot the logical and corrected circuit.