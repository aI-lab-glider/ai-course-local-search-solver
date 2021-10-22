#!/bin/bash

TESTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$TESTDIR" 
asdf install python 3.8.12
asdf local python 3.8.12
python3 -m venv test-venv
source test-venv/bin/activate
pip install -r test_requirements.txt
echo $(which python)
echo $(python --version)