#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os


# DEFINE CONSTANT
COMMENT = '//'
VM_EXT = '.vm'
ASM_EXT = '.asm'


def raise_exception(message: str):
    raise ValueError(message)


class Parser:
    def __init__(self, vm_filename: str):
        with open(vm_filename, mode='r') as vm_file:
            text = vm_file.read().split('\n')
        self.lines = [self._remove_comment(line) for line in text if self._remove_comment(line).strip()]
        self.index = 0
        self.command = []

    def next_line(self) -> bool:
        if len(self.lines) > self.index:
            self.command = self.lines[self.index].split(' ')
            self.index += 1
            return True
        else:
            self.index = 0
            self.command = []
            return False

    def command_type(self) -> str:
        command = self.argn(0)
        if command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        elif command in ['push']:
            return 'C_PUSH'
        elif command in ['pop']:
            return 'C_POP'
        elif command in ['label']:
            return 'C_LABEL'
        elif command in ['goto']:
            return 'C_GOTO'
        elif command in ['if-goto']:
            return 'C_IF'
        elif command in ['function']:
            return 'C_FUNCTION'
        elif command in ['RETURN']:
            return 'C_RETURN'
        elif command in ['call']:
            return 'C_CALL'
        else:
            raise_exception('%s is an invalid command.' % command)

    def argn(self, n: int) -> str:
        if len(self.command) <= n:
            return ''
        return self.command[n]

    def _remove_comment(self, line: str) -> str:
        comment_idx = line.find(COMMENT)
        if comment_idx == -1:
            clean_line = line.strip()
        else:
            clean_line = line[:comment_idx].strip()
        return clean_line


class CodeWriter:
    def __init__(self, asm_filename: str):
        self.asm = open(asm_filename, 'w')
        self.current_vm_file = None
        self.bool_count = 0  # Number of boolean comparisons so far
        self.addresses = self._address_dict()

    def __del__(self):
        self.close()

    def set_filename(self, vm_filename: str):
        self.current_vm_file = os.path.splitext(os.path.basename(vm_filename))[0]

    def write(self, line: str):
        self.asm.write(line + '\n')

    def write_arithmetic(self, operation: str):
        '''Apply operation to top of stack'''

        if operation not in ['neg', 'not']:  # Binary operator
            self._pop_stack_to_D()
        self._decrement_SP()
        self._set_A_to_stack()

        if operation == 'add':  # Arithmetic operators
            self.write('M=M+D')
        elif operation == 'sub':
            self.write('M=M-D')
        elif operation == 'and':
            self.write('M=M&D')
        elif operation == 'or':
            self.write('M=M|D')
        elif operation == 'neg':
            self.write('M=-M')
        elif operation == 'not':
            self.write('M=!M')
        elif operation in ['eq', 'gt', 'lt']:  # Boolean operators
            self.write('D=M-D')
            self.write('@BOOL.%d' % self.bool_count)

            if operation == 'eq':
                self.write('D;JEQ')  # if x == y, x - y == 0
            elif operation == 'gt':
                self.write('D;JGT')  # if x > y, x - y > 0
            elif operation == 'lt':
                self.write('D;JLT')  # if x < y, x - y < 0

            self._set_A_to_stack()
            self.write('M=0')  # False
            self.write('@ENDBOOL.%d' % self.bool_count)
            self.write('0;JMP')

            self.write('(BOOL.%d)' % self.bool_count)
            self._set_A_to_stack()
            self.write('M=-1')  # True

            self.write('(ENDBOOL.%d)' % self.bool_count)
            self.bool_count += 1
        else:
            raise_exception('%s is an invalid operation.' % operation)

        self._increment_SP()

    def write_push_pop(self, command: str, segment: str, index: str):
        self._resolve_address(segment, index)
        if command == 'C_PUSH':  # load M[address] to D
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self._push_D_to_stack()
        elif command == 'C_POP':  # load D to M[address]
            self.write('D=A')
            self.write('@R13')  # Store resolved address in R13
            self.write('M=D')
            self._pop_stack_to_D()
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        else:
            raise_exception('%s is an invalid command.' % command)

    def _resolve_address(self, segment: str, index: str):
        '''Resolve address to A register'''

        address = self.addresses.get(segment)
        if segment == 'constant':
            self.write('@' + str(index))
        elif segment == 'static':
            self.write('@' + self.current_vm_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + int(index)))  # Address is an int
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + address)  # Address is a string
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A')  # D is segment base
        else:
            raise_exception('%s is an invalid segment.' % segment)

    def _address_dict(self):
        return {
            'local':    'LCL',   # Base R1
            'argument': 'ARG',   # Base R2
            'this':     'THIS',  # Base R3
            'that':     'THAT',  # Base R4
            'pointer':  3,       # Edit R3, R4
            'temp':     5,       # Edit R5-12
                                 # R13-15 are free
            'static':   16,      # Edit R16-255
        }

    def _push_D_to_stack(self):
        '''Push from D onto top of stack, increment @SP'''

        self.write('@SP') #  Get current stack pointer
        self.write('A=M')  # Set address to current stack pointer
        self.write('M=D')  # Write data to top of stack
        self._increment_SP()  # Increment SP

    def _pop_stack_to_D(self):
        '''Decrement @SP, pop from top of stack onto D'''

        self._decrement_SP()  # Decrement SP
        self.write('A=M')  # Set address to current stack pointer
        self.write('D=M')  # Get data from top of stack

    def _increment_SP(self):
        self.write('@SP')
        self.write('M=M+1')

    def _decrement_SP(self):
        self.write('@SP')
        self.write('M=M-1')

    def _set_A_to_stack(self):
        self.write('@SP')
        self.write('A=M')

    def _close(self):
        self.asm.close()


class VMTranslator:
    def __init__(self, src: str):
        self.asm_file, self.vm_files = self._parse_files(src)
        self.code_writer = CodeWriter(self.asm_file)

    def translates(self):
        for vm_file in self.vm_files:
            self._translate(vm_file)

    def _parse_files(self, file_path: str) -> (str, list):
        if not os.path.exists(file_path):
            print('No such file or directory.')
            return '', []

        if os.path.isfile(file_path) and file_path.endswith(VM_EXT):
            asm_file = file_path.replace(VM_EXT, ASM_EXT)
            vm_files = [file_path]

        elif os.path.isdir(file_path):
            dir_path = file_path[:-1] if file_path[-1] == '/' else file_path
            asm_file = dir_path + '/' + os.path.basename(dir_path) + ASM_EXT
            vm_files = _find_all_files_with_ext(dir_path, 'vm')

        return asm_file, vm_files

    def _find_all_files_with_ext(dir_path: str, ext: str) -> list:
        ext_files = []
        suffix = os.extsep + ext.lower()
        for cur_dir, _, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(suffix):
                    ext_files.append(os.path.join(cur_dir, file))
        return ext_files

    def _translate(self, vm_file: str):
        parser = Parser(vm_file)
        self.code_writer.set_filename(vm_file)
        self.code_writer.write('// ----------  %s ----------' % self.code_writer.current_vm_file)

        while parser.next_line():
            self.code_writer.write('// ' + ' '.join(parser.command))
            if parser.command_type() == 'C_PUSH':
                self.code_writer.write_push_pop('C_PUSH', parser.argn(1), parser.argn(2))
            elif parser.command_type() == 'C_POP':
                self.code_writer.write_push_pop('C_POP', parser.argn(1), parser.argn(2))
            elif parser.command_type() == 'C_ARITHMETIC':
                self.code_writer.write_arithmetic(parser.argn(0))

            self.code_writer.write('')
        self.code_writer.write('// ------------------------------')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("vm", help="required : please set path of vm file or directory include vm file", type=str)
    args = parser.parse_args()
    target = args.vm.strip()
    vm_translator = VMTranslator(target)
    vm_translator.translates()
