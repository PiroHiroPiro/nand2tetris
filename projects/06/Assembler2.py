#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re

A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3

A_BINARY = '0%s\n'
C_BINARY = '111%s%s%s\n'

class Parser:
    def __init__(self, asm):
        self.asm = [self._remove_comment(line).strip() for line in asm if self._remove_comment(line).strip()]
        self.index = -1
        self.line = ''
        self.dest = 'null'
        self.comp = 'null'
        self.jump = 'null'

    def nextLine(self):
        if len(self.asm) - 1 > self.index:
            self.index += 1
            self.line = self.asm[self.index]
            return True
        else:
            self.index = -1
            self.line = ''
            return False

    def rmLabel(self):
            _ = self.asm.pop(self.index)
            line_number = self.index
            self.index -= 1
            return line_number

    def commandType(self):
        if re.match('@.*$', self.line):
            return A_COMMAND
        elif re.match('\(.*\)$', self.line):
            return L_COMMAND
        elif re.match('([ADM]{1,3})?=?[AD!\-\+01&\|M]+;?([JEQGLTNMP]{3})?$', self.line):
            return C_COMMAND

    def symbol(self):
        return re.sub('[@\(\)]', '', self.line).strip()

    def parse(self):
        parsed_list = ['', '', '']
        if self.line.find('=') == -1:
            self.line = '=' + self.line
        if self.line.find(';') == -1:
            self.line = self.line + ';'
        parsed_list[0], tmp = self.line.split('=')
        parsed_list[1:3] = tmp.strip().split(';')
        self.dest = parsed_list[0].strip() if parsed_list[0] != '' else 'null'
        self.comp = parsed_list[1].strip() if parsed_list[1] != '' else 'null'
        self.jump = parsed_list[2].strip() if parsed_list[2] != '' else 'null'

    def dest2bin(self):
        return Code.dest(self.dest)

    def comp2bin(self):
        return Code.comp(self.comp)

    def jump2bin(self):
        return Code.jump(self.jump)

    def _remove_comment(self, line):
        idx = line.find('//')
        if idx == -1:
            return line
        return line[:idx]

class Code:
    DEST_DICT = {
        "null": "000",
        "M": "001",
        "D": "010",
        "A": "100",
        "MD": "011",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    COMP_DICT = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    JUMP_DICT = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }

    @staticmethod
    def dest(mnemonic):
        return Code.DEST_DICT[mnemonic]

    @staticmethod
    def comp(mnemonic):
        return Code.COMP_DICT[mnemonic]

    @staticmethod
    def jump(mnemonic):
        return Code.JUMP_DICT[mnemonic]

class SymbolTable:
    def __init__(self):
        self.symbol_table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
        for i in range(0,16):
            label = "R" + str(i)
            self.symbol_table[label] = i
        self.variable_cursor = 16 - 1

    def addEntry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        return symbol in self.symbol_table

    def nextAddress(self):
        self.variable_cursor += 1
        return self.variable_cursor

    def getAddress(self, symbol):
        return self.symbol_table[symbol]

class Assembler:
    def __init__(self, asm_file_name):
        try:
            self.asm_file_name = asm_file_name
            target = asm_file_name[:asm_file_name.index('.asm')]
            self.hack_file_name = target + '.hack'
            asms = ''
            with open(self.asm_file_name, mode='r') as asmf:
                asms = asmf.read().split('\n')
            self.hack_file = open(self.hack_file_name, mode='w')
            self.parser = Parser(asms)
            self.st = SymbolTable()
        except:
            print('No such file or directory.')
            del self

    def __del__(self):
        try:
            self.hack_file.close()
        except:
            pass

    def _labelSearch(self):
        while self.parser.nextLine():
            if self.parser.commandType() == L_COMMAND:
                symbol = self.parser.symbol()
                line_number = self.parser.rmLabel()
                self.st.addEntry(symbol, line_number)

    def _variableSearch(self):
        while self.parser.nextLine():
            if self.parser.commandType() == A_COMMAND:
                symbol = self.parser.symbol()
                if not re.match('[0-9]+$', symbol) and not self.st.contains(symbol):
                    address = self.st.nextAddress()
                    self.st.addEntry(symbol, address)

    def assemble(self):
        self._labelSearch()
        self._variableSearch()
        while self.parser.nextLine():
            binary = ''

            command_type = self.parser.commandType()
            if command_type == A_COMMAND:
                symbol = self.parser.symbol()
                if re.match('[0-9]+$', symbol):
                    address = int(symbol)
                else:
                    address = self.st.getAddress(symbol)
                binary = A_BINARY % format(address, '015b')

            elif command_type == C_COMMAND:
                self.parser.parse()
                binary = C_BINARY % (self.parser.comp2bin(), self.parser.dest2bin(), self.parser.jump2bin())
            else:
                continue

            self.hack_file.write(binary)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("asm", help="required : please set asm file", type=str)
    args = parser.parse_args()
    asm = args.asm.strip()

    assembler = Assembler(asm)
    assembler.assemble()
