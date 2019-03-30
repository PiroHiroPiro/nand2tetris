#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re


NAME_REGEX = re.compile(r"\A[A-Za-z_.:][\w.:]*\Z")


class CodeWriter:
    def __init__(self, asm_filename: str):
        self.asm = open(asm_filename, "w")
        self.current_vm_file = None
        self.bool_count = 0
        self.call_count = 0
        self.addresses = {
            "local":    "LCL",   # Base R1
            "argument": "ARG",   # Base R2
            "this":     "THIS",  # Base R3
            "that":     "THAT",  # Base R4
            "pointer":  3,       # Edit R3, R4
            "temp":     5,       # Edit R5-12
                                 # R13-15 are free
            "static":   16,      # Edit R16-255
        }
        self._write_init()

    def __del__(self):
        self._close()

    def set_filename(self, vm_filename: str):
        self.current_vm_file = os.path.splitext(os.path.basename(vm_filename))[0]

    def write(self, line: str):
        self.asm.write(line + "\n")

    def write_arithmetic(self, operation: str):
        """Apply operation to top of stack"""

        if operation not in ["neg", "not"]:
            self._pop_stack_to_D()
        self._decrement_SP()
        self._set_A_to_stack()

        if operation == "add":
            self.write("M=M+D")
        elif operation == "sub":
            self.write("M=M-D")
        elif operation == "and":
            self.write("M=M&D")
        elif operation == "or":
            self.write("M=M|D")
        elif operation == "neg":
            self.write("M=-M")
        elif operation == "not":
            self.write("M=!M")
        elif operation in ["eq", "gt", "lt"]:  # Boolean operators
            self.write("D=M-D")
            self.write("@BOOL.%d" % self.bool_count)

            if operation == "eq":
                self.write("D;JEQ")  # if x == y => x - y == 0
            elif operation == "gt":
                self.write("D;JGT")  # if x > y => x - y > 0
            elif operation == "lt":
                self.write("D;JLT")  # if x < y => x - y < 0

            self._set_A_to_stack()
            self.write("M=0")  # False
            self.write("@ENDBOOL.%d" % self.bool_count)
            self.write("0;JMP")

            self.write("(BOOL.%d)" % self.bool_count)
            self._set_A_to_stack()
            self.write("M=-1")  # True

            self.write("(ENDBOOL.%d)" % self.bool_count)
            self.bool_count += 1
        else:
            raise ValueError("%s is an invalid operation." % operation)

        self._increment_SP()

    def write_push(self, segment: str, index: str):
        self._resolve_address(segment, index)
        if segment == "constant":
            self.write("D=A")
        else:
            self.write("D=M")
        self._push_D_to_stack()

    def write_pop(self, segment: str, index: str):
        self._resolve_address(segment, index)
        self.write("D=A")
        self.write("@R13")  # Store resolved address in R13
        self.write("M=D")
        self._pop_stack_to_D()
        self.write("@R13")
        self.write("A=M")
        self.write("M=D")

    def write_label(self, label: str):
        if not re.match(NAME_REGEX, label):
            raise ValueError("%s is an invalid label." % label)
        self.write("(%s$%s)" % (self.current_vm_file, label))

    def write_goto(self, label: str):
        self.write("@%s$%s" % (self.current_vm_file, label))
        self.write("0;JMP")

    def write_if_goto(self, label: str):
        self._pop_stack_to_D()
        self.write("@%s$%s" % (self.current_vm_file, label))
        self.write("D;JNE")

    def write_function(self, function_name: str, num_locals: int):
        if not re.match(NAME_REGEX, function_name):
            raise ValueError("%s is an invalid function name." % function_name)

        # (function)
        self.write("(%s)" % function_name)
        self.write("D=0")

        for _ in range(num_locals):
            self._push_D_to_stack()

    def write_call(self, function_name: str, num_args: int):
        return_address = function_name + ".return." + str(self.call_count)
        self.call_count += 1

        # puch return address
        self.write("@" + return_address)
        self.write("D=A")
        self._push_D_to_stack()

        # push LCL,ARG,THIS,THAT
        for address in ["@LCL", "@ARG", "@THIS", "@THAT"]:
            self.write(address)
            self.write("D=M")
            self._push_D_to_stack()

        # ARG = SP-n-5
        self.write("@SP")
        self.write("D=M")
        self.write("@" + str(num_args + 5))
        self.write("D=D-A")
        self.write("@ARG")
        self.write("M=D")

        # LCL = SP
        self.write("@SP")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")

        # goto function
        self.write("@" + function_name)
        self.write("0;JMP")

        # (return address)
        self.write("(%s)" % return_address)

    def write_return(self):
        # temporary variables
        frame = "R13"
        ret = "R14"

        # FRAME = LCL
        self.write("@LCL")
        self.write("D=M")
        self.write("@" + frame)
        self.write("M=D")

        # RET = *(FRAME - 5)
        self.write("@" + frame)
        self.write("D=M")
        self.write("@5")
        # self.write("@0")
        self.write("A=D-A")
        self.write("D=M")
        self.write("@" + ret)
        self.write("M=D")

        # *ARG = pop()
        self._pop_stack_to_D()
        self.write("@ARG")
        self.write("A=M")
        self.write("M=D")

        # SP = ARG + 1
        self.write("@ARG")
        self.write("D=M")
        self.write("@SP")
        self.write("M=D+1")

        # THAT = *(FRAME - 1)
        # THIS = *(FRAME - 2)
        # ARG = *(FRAME - 3)
        # LCL = *(FRAME - 4)
        offset = 1
        for address in ["@THAT", "@THIS", "@ARG", "@LCL"]:
            self.write("@" + frame)
            self.write("D=M")
            self.write("@" + str(offset))
            self.write("A=D-A")
            self.write("D=M")
            self.write(address)
            self.write("M=D")
            offset += 1

        # goto RET
        self.write("@" + ret)
        self.write("A=M")
        self.write("0;JMP")

    def _resolve_address(self, segment: str, index: str):
        """Resolve address to A register"""

        address = self.addresses.get(segment, None)
        if segment == "constant":
            self.write("@" + str(index))
        elif segment == "static":
            self.write("@" + self.current_vm_file + "." + str(index))
        elif segment in ["pointer", "temp"]:
            self.write("@R" + str(address + int(index)))  # Address is an int
        elif segment in ["local", "argument", "this", "that"]:
            self.write("@" + address)  # Address is a string
            self.write("D=M")
            self.write("@" + str(index))
            self.write("A=D+A")  # D is segment base
        else:
            raise ValueError("%s is an invalid segment." % segment)

    def _write_init(self):
        """Initialize asm file"""

        self.write("// bootstrap")

        # @SP = 256
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")

        # call Sys.init
        self.write_call("Sys.init", 0)

    def _push_D_to_stack(self):
        """Push from D onto top of stack, increment @SP"""

        self.write("@SP")  # Get current stack pointer
        self.write("A=M")  # Set address to current stack pointer
        self.write("M=D")  # Write data to top of stack
        self._increment_SP()  # Increment SP

    def _pop_stack_to_D(self):
        """Decrement @SP, pop from top of stack onto D"""

        self._decrement_SP()  # Decrement SP
        self.write("A=M")  # Set address to current stack pointer
        self.write("D=M")  # Get data from top of stack

    def _increment_SP(self):
        self.write("@SP")
        self.write("M=M+1")

    def _decrement_SP(self):
        self.write("@SP")
        self.write("M=M-1")

    def _set_A_to_stack(self):
        self.write("@SP")
        self.write("A=M")

    def _close(self):
        self.asm.close()
