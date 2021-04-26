@ECHO off

ECHO STARTING CCOMPILER

compile.exe

ECHO STARTING PROGRAM

FOR /F "tokens=* delims=" %%x in (root_dir) DO cd %%x

CD umoria
CD Debug

umoria.exe