# lab5hrm.asm
#
# This program computes the "heartrate" as an input on IOC, and displays
# it on IOF--IOG. Each transition on the LSB of IOC is considered a
# heartbeat.

# Set registers R0, R2 to zero. R0 shall always be 0, R2 stores observed
# number of heartbeats
SUB  R0, R0, R0
SUB  R2, R2, R2

# Initialise loop variables here
SUB  R7, R7, R7
SUB  R6, R6, R6
# R5 = 0xFF
ADDI R5, R0, -1
# R5 = 0x7F
SRL  R5, R5

# Read input from IOC (this is only to set the initial input,
# instruction is never revisited in the monitoring loop/cycle)
LB   R3, -5(R0)
# Only concerned with the last bit
ANDI R3, R3, 1

monitor_loop:
# Read input again from IOC
LB   R4, -5(R0)
# Again, only concerned with the last bit
ANDI R4, R4, 1
# Check if previous reads are the same
ADD  R3, R4, R3
# R3 will be even parity if the reads were the same, odd parity if they
# were different
ANDI R3, R3, 1
# Only record a positive transition
AND  R3, R3, R4
# increment R2
ADD  R2, R2, R3
# Copy the current read (R4) to the previous read (R3)
ADD  R3, R4, R0
# Decrement R7, i.e. loop 256 times, 0 -> 255 -> 0
ADDI R7, R7, -1
# If R7 is not 0, go back to monitor_loop
BNE  R7, R0, monitor_loop
# Decrement R6, i.e. loop 256 times, 0 -> 255 -> 0
ADDI R6, R6, -1
# If R6 is not 0, go back to monitor_loop
BNE  R6, R0, monitor_loop
# Decrement R5, i.e. loop 128 times, 127 -> 0
ADDI R5, R5, -1
# If R5 is not 0, go back monitor_loop
BNE  R5, R0, monitor_loop

# R2 stores the number of heartbeats observed in the sampling interval.
# The sampling interval is (((256*8)*256+256*2)*128+128*2) = 67,174,656
# cycles at a 10 MHz clock, i.e. 6.7 seconds.
# Check if the number of pulses measured is less than 30.
ADDI R4, R2, -30
# If the number of pulses observed is less than 30, skip the next
# instruction (i.e. go to multiply_by_two)
BLTZ R4, multiply_by_two
# Otherwise, set the number of observed pulses to 29 (sets upper bound
# on heartrate to 259)
ADDI R2, R0, 29
multiply_by_two:
# Multiply the number of observed pulses by two. This changes the
# allowed values of R2 to be even numbers between 0 and 58 (inclusive)
SLL  R2, R2

# There is a certain amount of cheating involved here. The microprocessor
# simply looks up the BPM  conversion from memory. This can be done
# because the memory (lab5dram.v) sets memory addresses at 0 through 59
# with corresponding heartrates, in big endian format.
# Typically, in a real processor, we would use the initial instructions
# to set the memory to these values. This will, however, take up
# multiple instructions per value (at least one to initialise, and one
# to store, 2 instructions * 60 values gives at least 120 instructions
# from an available 128), and we don't have that kind of space in our
# iram.

# Load the upper byte to be displayed on the 7-segments
# (the two most significant digits in the BPM)
LB   R3, 0(R2)
# And write it to the corresponding 7 segment (IOF)
SB   R3, -2(R0)
# Load the lower byte to be displayed on the 7-segments
# (the two least significant digits in the BPM)
LB   R3, 1(R2)
# And write it to the corresponding 7 segment (IOG)
SB   R3, -1(R0)
