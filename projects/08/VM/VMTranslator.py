#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os

from parser import Parser
from code_writer import CodeWriter


# DEFINE CONSTANT
VM_EXT = ".vm"
ASM_EXT = ".asm"


class VMTranslator:
    def __init__(self, src: str):
        self.asm_file, self.vm_files = self._parse_files(src)
        print("Translate to %s." % self.asm_file)
        self.code_writer = CodeWriter(self.asm_file)

    def translates(self):
        for vm_file in self.vm_files:
            self._translate(vm_file)

    def _parse_files(self, file_path: str) -> (str, list):
        if not os.path.exists(file_path):
            raise IOError("No such file or directory.")

        if os.path.isfile(file_path) and file_path.endswith(VM_EXT):
            asm_file = file_path.replace(VM_EXT, ASM_EXT)
            vm_files = [file_path]

        elif os.path.isdir(file_path):
            dir_path = file_path[:-1] if file_path[-1] == "/" else file_path
            asm_file = dir_path + "/" + os.path.basename(dir_path) + ASM_EXT
            vm_files = self._find_all_files_with_ext(dir_path, "vm")
        else:
            raise IOError("No such file or directory.")

        return asm_file, vm_files

    def _find_all_files_with_ext(self, dir_path: str, ext: str) -> list:
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
        self.code_writer.write("// ----------  %s ----------" % self.code_writer.current_vm_file)

        while parser.next_line():
            self.code_writer.write("// " + parser.command_line())

            if parser.command_type() == "C_ARITHMETIC":
                self.code_writer.write_arithmetic(parser.argn(0))
            elif parser.command_type() == "C_PUSH":
                self.code_writer.write_push(parser.argn(1), parser.argn(2))
            elif parser.command_type() == "C_POP":
                self.code_writer.write_pop(parser.argn(1), parser.argn(2))
            elif parser.command_type() == "C_LABEL":
                self.code_writer.write_label(parser.argn(1))
            elif parser.command_type() == "C_GOTO":
                self.code_writer.write_goto(parser.argn(1))
            elif parser.command_type() == "C_IF_GOTO":
                self.code_writer.write_if_goto(parser.argn(1))
            elif parser.command_type() == "C_FUNCTION":
                self.code_writer.write_function(parser.argn(1), int(parser.argn(2)))
            elif parser.command_type() == "C_CALL":
                self.code_writer.write_call(parser.argn(1), int(parser.argn(2)))
            elif parser.command_type() == "C_RETURN":
                self.code_writer.write_return()

            self.code_writer.write("")  # empty line
        self.code_writer.write("// ------------------------------\n")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("vm", help="required : please set path of vm file or directory include vm file", type=str)
    args = argparser.parse_args()
    target = args.vm.strip()
    vm_translator = VMTranslator(target)
    vm_translator.translates()
