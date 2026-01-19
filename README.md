# MimiQ Hackton: QNA Compiler
Quantum Circuit Compilation with Surface-Code Error Correction for Neutral-Atom Hardware, project developed by the EPITA QUANTUM major.

## How to Run?

There are multiple ways to do so. Firstly, you can install all Python and Julia dependencies needed by the project and manually run the script `src/qnac.sh` with a protobuff circuit file path as argument. Its corrected version and the resulting QNAasm program will be generated next to it. You may need to add the results of `$(pwd)/src` to your `PYTHONPATH`.

The easiest way for now is to use the docker image.

### Use the Docker Image

The docker image is based on `python:3.13.11-trixie`.

It exposes the port 8888 to run Python and Julia notebooks and accessed it from a navigator.

You will have to add a volume to the container in order to access to the generated files from your system.

To use the image, you need to build it with
```bash
docker build -t mimiq:1.0 .
```

Then you can run
```bash
docker run --rm -it -p 8888:8888 -v "$(pwd)/circuits:/home/mimiq/app/circuits" mimiq:1.0 <COMMAND> [ARGUMENTS...]
```
to run a command.

The available commands are:

- `compile <circuit.pb>`: compile the given protobuff circuit to a QNAasm circuit.
- `notebook`: start the jupyter notebook server in the container.
