// ----------  FibonacciSeries ----------
// 1 : push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 2 : pop pointer 1
@R4
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 3 : push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// 4 : pop that 0
@THAT
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 5 : push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// 6 : pop that 1
@THAT
D=M
@1
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 7 : push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 8 : push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// 9 : sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1

// 10 : pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 11 : label MAIN_LOOP_START
(FibonacciSeries.MAIN_LOOP_START)

// 12 : push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 13 : if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@FibonacciSeries.COMPUTE_ELEMENT
D;JNE

// 14 : goto END_PROGRAM
@FibonacciSeries.END_PROGRAM
0;JMP

// 15 : label COMPUTE_ELEMENT
(FibonacciSeries.COMPUTE_ELEMENT)

// 16 : push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 17 : push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 18 : add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1

// 19 : pop that 2
@THAT
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 20 : push pointer 1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1

// 21 : push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// 22 : add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1

// 23 : pop pointer 1
@R4
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 24 : push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 25 : push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// 26 : sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1

// 27 : pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// 28 : goto MAIN_LOOP_START
@FibonacciSeries.MAIN_LOOP_START
0;JMP

// 29 : label END_PROGRAM
(FibonacciSeries.END_PROGRAM)

// ------------------------------
