#!/bin/bash

STUDENT=$(cd "$1" 2> /dev/null && pwd -P)
TESTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$TESTDIR"
source ./test-venv/bin/activate
python -m pytest --timeout 300 --show-exceptions -p grading --points --student "${STUDENT}" --teacher "${TESTDIR}"