// ----------  BasicLoop ----------
// 1 : push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// 2 : pop local 0
@LCL
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

// 3 : label LOOP_START
(BasicLoop.LOOP_START)

// 4 : push argument 0
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

// 5 : push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// 6 : add
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

// 7 : pop local 0
@LCL
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

// 8 : push argument 0
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

// 9 : push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// 10 : sub
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

// 11 : pop argument 0
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

// 13 : if-goto LOOP_START
@SP
M=M-1
A=M
D=M
@BasicLoop.LOOP_START
D;JNE

// 14 : push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// ------------------------------
