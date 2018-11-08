// 1.sum=0
    @sum
    M=0
// 2.j=j+1
    @j
    M=M+1
// q=sum+12-j
    @sum
    D=M
    @q
    M=D
    @12
    D=A
    @q
    M=M+D
    @j
    D=M
    @q
    M=M+D
// arr[3]=-1
  @arr
  A=M+3
  M=-1
// arr[j]=0
  @j
  D=M
  @arr
  A=A+D
  M=0
// arr[j]=17
  @j
  D=M
  @arr
  D=A+D
  @tmp
  M=D
  @17
  D=A
  @tmp
  A=M
  M=D
