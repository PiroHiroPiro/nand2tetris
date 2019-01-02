// ----------  StackTest ----------
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.0
D;JEQ
@SP
A=M
M=0
@ENDBOOL.0
0;JMP
(BOOL.0)
@SP
A=M
M=-1
(ENDBOOL.0)
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.1
D;JEQ
@SP
A=M
M=0
@ENDBOOL.1
0;JMP
(BOOL.1)
@SP
A=M
M=-1
(ENDBOOL.1)
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.2
D;JEQ
@SP
A=M
M=0
@ENDBOOL.2
0;JMP
(BOOL.2)
@SP
A=M
M=-1
(ENDBOOL.2)
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.3
D;JLT
@SP
A=M
M=0
@ENDBOOL.3
0;JMP
(BOOL.3)
@SP
A=M
M=-1
(ENDBOOL.3)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.4
D;JLT
@SP
A=M
M=0
@ENDBOOL.4
0;JMP
(BOOL.4)
@SP
A=M
M=-1
(ENDBOOL.4)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.5
D;JLT
@SP
A=M
M=0
@ENDBOOL.5
0;JMP
(BOOL.5)
@SP
A=M
M=-1
(ENDBOOL.5)
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.6
D;JGT
@SP
A=M
M=0
@ENDBOOL.6
0;JMP
(BOOL.6)
@SP
A=M
M=-1
(ENDBOOL.6)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.7
D;JGT
@SP
A=M
M=0
@ENDBOOL.7
0;JMP
(BOOL.7)
@SP
A=M
M=-1
(ENDBOOL.7)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@BOOL.8
D;JGT
@SP
A=M
M=0
@ENDBOOL.8
0;JMP
(BOOL.8)
@SP
A=M
M=-1
(ENDBOOL.8)
@SP
M=M+1

// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
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

// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
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

// neg
@SP
M=M-1
@SP
A=M
M=-M
@SP
M=M+1

// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M&D
@SP
M=M+1

// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M|D
@SP
M=M+1

// not
@SP
M=M-1
@SP
A=M
M=!M
@SP
M=M+1

// ------------------------------
