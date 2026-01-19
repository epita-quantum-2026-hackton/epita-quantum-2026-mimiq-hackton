#!/bin/sh

CMD="$1"

if [ -z "$CMD" ]; then
  echo "Missing command" 1>&2
  exit 1
fi

case "$CMD" in
  compile) bash /home/mimiq/app/src/qnac.sh $2;;
  notebook) python -m jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser /home/mimiq/app/src;;
  *) {
    echo "Unkown command '$CMD'" 1>&2
    exit 1
  };;
esac
