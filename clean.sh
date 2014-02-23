#!/bin/bash
rm -R ../../photos/
make clean -C src/
if [ -f "*.out" ]; then
	rm *.out
fi
rm main
if [ -f "*.png" ]; then
	rm *.png
fi