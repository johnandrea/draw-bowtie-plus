@echo off

if exist draw-bowtie-plus.exe del draw-bowtie-plus.exe

pyinstaller --onefile draw-bowtie-plus.py

rmdir /q /S build
del draw-bowtie-plus.spec

move /y dist\draw-bowtie-plus.exe .

rmdir /q /S dist
