#!/bin/sh

INPUT_PB="$1"

if [ -z "$INPUT_PB" ]; then
  echo "Missing input protobuff file" 1>&2
  exit 1
fi

BASE="${INPUT_PB%.pb}"
CORRECTED_PB="${BASE}-corrected.pb"
OUTPUT_QNAASM="${BASE}.qnaasm"

{
  echo QNA Compiler:
  echo -- Checking input
  if ! [ -f "$INPUT_PB" ]; then
    echo "$INPUT_PB" does not exist
    exit 2
  fi
  if [ "$BASE" = "$INPUT_PB" ]; then
    echo Invalid file name "$INPUT_PB"
    exit 2
  fi
  echo -- Applying QEC
  julia src/qec/correct_circuit.jl "$INPUT_PB"
  echo -- Translating to QNAasm
  python src/translate/translate_corrected_circuit.py "$CORRECTED_PB" 1>"${OUTPUT_QNAASM}"
  echo Compilation terminated
  echo Result stored inside "$OUTPUT_QNAASM"
} 1>&2
