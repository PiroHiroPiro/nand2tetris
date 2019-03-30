#!/usr/bin/env python3
# -*- coding: utf-8 -*-

COMMENT = "//"


class Parser:
    def __init__(self, vm_filename: str):
        with open(vm_filename, mode="r") as vm_file:
            text = vm_file.read().split("\n")
        self.lines = [self._remove_comment(line) for line in text if self._remove_comment(line).strip()]
        self.line_index = 0
        self.command = []

    def next_line(self) -> bool:
        if len(self.lines) > self.line_index:
            self.command = self.lines[self.line_index].split(" ")
            self.line_index += 1
            return True
        else:
            self.line_index = 0
            self.command = []
            return False

    def command_type(self) -> str:
        command = self.argn(0)
        if self.command == 'push':
            return "C_PUSH"
        elif self.command == 'pop':
            return "C_POP"
        elif self.command == 'label':
            return "C_LABEL"
        elif self.command == 'goto':
            return "C_GOTO"
        elif self.command == 'if-goto':
            return "C_IF""
        elif self.command == 'function':
            return "C_FUNCTION"
        elif self.command == 'return':
            return "C_RETURN"
        elif self.command == 'call':
            return "C_CALL"
        elif self.command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return "C_ARITHMETIC"
        else:
            raise ValueError("%s is an invalid command." % command)

    def argn(self, n: int) -> str:
        if len(self.command) <= n:
            raise ValueError("arg%d is not exist." % n)
        return self.command[n]

    def command_line(self) -> str:
        return "%d : %s" % (self.line_index, " ".join(self.command))

    def _remove_comment(self, line: str) -> str:
        comment_idx = line.find(COMMENT)
        if comment_idx == -1:
            clean_line = line.strip()
        else:
            clean_line = line[:comment_idx].strip()
        return clean_line
