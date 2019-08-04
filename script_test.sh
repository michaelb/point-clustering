#!/bin/zsh

for teste in test_*
	time ./connectes.py $teste
done
echo done
