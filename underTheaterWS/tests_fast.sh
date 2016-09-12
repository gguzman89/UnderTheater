#!/bin/bash
if [ $# -eq 0 ]; then
    ARGS="underTheaterApp"
else
    ARGS="$*"
fi
set -o xtrace
./manage.py test --settings=underTheaterWS.fast_test_settings $ARGS
