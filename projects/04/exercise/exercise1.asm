// 1. Set D to A-1
  D=A-1
// 2. Set both A and D to A+1
  D=A+1
  A=D
// 3. Set D to 19
  @19
  D=A
// 4. D++
  D=D+1
// 5. D=RAM[128]
  @128
  D=M
// 6. Set RAM[1234] to D-1
  @1234
  M=D-1
// 7. Set RAM[24] to 432
  @432
  D=A
  @24
  M=D
// 8. Add 1 to RAM[10] and store the result in D
  @10
  D=M+1
