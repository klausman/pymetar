#!/bin/bash

TESTS="testall.py testpixmap.py testcloud.py testskycond.py"
SETDIR="reports/"
SETS="set-2007-10-14  set-2010-01-17 set-2010-10-31"

for TEST in $TESTS; do
	for SET in $SETS; do
		echo "Running $TEST on $SETDIR/$SET"
		python2 $TEST $SETDIR/$SET > logs/$TEST-$SET.log
		if [ $? != 0 ]; then
			echo "$TEST on $SETDIR/$SET failed" >&2
			echo "See logs/$TEST-$SET.log for details"
			break
		fi
	done
done
