// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// @KBD = 24576
// @SCREEN = 16384
// 8191 = 512 * 256 / 16 - 1

// while (0 == 0) {
//   if (KBD != 0) {
//     color = -1
//   } else {
//     color = 0
//   }
//   i = 0
//   while (i < 8192) {
//     SCREEN + i = color
//   }
// }

    @SCREEN
    D=A
    @8191
    D=D+A
    @SCREEN_END
    M=D
(INIT)
    @KBD
    D=M
    @BLACK
    D;JNE
    @WHITE
    D;JEQ
(BLACK)
    @color
    M=-1
    @DRAW_INIT
    0;JMP
(WHITE)
    @color
    M=0
(DRAW_INIT)
    @SCREEN
    D=A
    @addr
    M=D
(DRAW)
    @addr
    D=A
    @SCREEN_END
    D=D-M
    @INIT
    D;JGT
    @color
    D=M
    @addr
    A=M
    M=D
    @addr
    M=M+1
    @DRAW
    0;JMP
