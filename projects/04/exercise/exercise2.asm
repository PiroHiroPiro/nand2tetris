// 1. goto 50
  @goto
  0;JMP
// 2. if D==0 then goto 123
  @123
  D;JEQ
// 3. if D<9 then goto 123
  @9
  D=D-A
  @123
  D;JLT
// 4. if RAM[12]>0 then goto 50
  @12
  D=M
  @50
  D;JGT
// 5. if sum>0 then goto 50
  @sum
  D=M
  @50
  D;JGT
// 6. if x[1]<= 0 then goto NEXT
  @x
  A=M+1
  D=M
  @NEXT
  D;JLE
