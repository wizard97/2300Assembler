# 2300Assembler
A Python Assembler for Cornell's ECE 2300 Class. This will create the Verilog instruction RAM for the processor based on the assembly text file.

## Example Assembly Code
```
# This is a comment
myLabel: # This is a label
    # Feel free to indent
    SUB R0, R0, R0
    LB R1, 5(R0) #load 5th byte from memory
    ADDI R1, R1, 1
BEQ R0, R0, myLabel # Same as BEQ R0, R0, -4
```

## How to use:
Make sure you have Python installed
Download zip and unpack
Drag the .asm file you want to assemble (ex: "lab5iramHRM.asm") into folder
Start Python shell in the same directory
On mac in terminal that would be something like this:
```
> cd ~/path/to/2300assembler
# Start Python
> python
```
 
### To assemble "lab5iramHRM.asm" in Python shell:
```
>>> import Assembler
>>> a = Assembler.Assembler("lab5iramHRM.asm") # Select input file
>>> a.assemble() # Assemble it, make sure no errors, check if warnings
>>> a.genVLogiram("myiram.v") # Will create Verilog file "myiram.v" in same directory
```
