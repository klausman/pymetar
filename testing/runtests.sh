#!/bin/bash

TESTS="testall.py testpixmap.py"

for TEST in $TESTS; do
	python $TEST > $TEST.log
	if [ $? != 0 ]; then
		echo "$TEST failed" >&2
		echo "See $TEST.log for details"
		break
	fi
done
