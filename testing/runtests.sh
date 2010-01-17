#!/bin/bash

TESTS="testall.py testpixmap.py testcloud.py"

for TEST in $TESTS; do
	echo "Running $TEST on reports/"
	python $TEST > $TEST.log
	echo "Running $TEST on reports2/"
	python $TEST reports2 >> $TEST.log
	if [ $? != 0 ]; then
		echo "$TEST failed" >&2
		echo "See $TEST.log for details"
		break
	fi
done
