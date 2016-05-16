# Register instruction subclass

from BaseInstruct import *
from abc import ABCMeta, abstractmethod
from AssemblerExceptions import *

class RegInst(BaseInstruct):
    __metaclass__ = ABCMeta
    _op = "1111"
    _name = ""
    _funct = ""

    def __init__(self, asm, line_num,label=None):
        super(RegInst, self).__init__(asm, line_num,label)
        self.regRD = "R0"

    @abstractmethod
    def is_type(asm):
        pass

    def parse(self):
        args = self.split_asm()
        if (len(args) != self._num_args):
            raise AssemblerException(self.line_num, "Incorrect instruction format for '%s'" % (self.asm))

        for i in range(len(args)):
            args[i] = args[i].upper()
            if (not BaseInstruct.valid_regs.has_key(args[i])):
                raise AssemblerException(self.line_num, "Invalid register '%s'" % (args[i]))

        self.regRD = args[0]
        self.regRS = args[1]

        if (len(args) >= 3):
            self.regRT = args[2]


    def generate_inst(self):
        valid_regs = super(RegInst, self).valid_regs

        return self._op + valid_regs[self.regRS] + valid_regs[self.regRT] + valid_regs[self.regRD] + self._funct


    def getPrintableInst(self):
        tmp = "%s %s, %s" % (self._name, self.regRD, self.regRS)
        if self._num_args >= 3:
            tmp += ', %s' % (self.regRT)
        return tmp




class HaltInst(RegInst):

    _funct = "001"
    _op = '0000'
    _name = "HALT"
    _num_args = 1


    def parse(self):
        args = self.split_asm()
        if (len(args) != self._num_args):
            raise AssemblerException(self.line_num, "Incorrect number of arguments for '%s'" % (self.asm))

        self.regRD = "R0"
        self.regRS = "R0"
        self.regRT = "R0"

    def getPrintableInst(self):
        return self._name

    @staticmethod
    def is_type(asm):
        return isInstruct(HaltInst._name, asm)


class NopInst(RegInst):

    _funct = "000"
    _op = '0000'
    _name = "NOP"
    _num_args = 1

    def parse(self):
        args = self.split_asm()
        if (len(args) != self._num_args):
            raise AssemblerException(self.line_num, "Incorrect number of arguments for '%s'" % (self.asm))

        self.regRD = "R0"
        self.regRS = "R0"
        self.regRT = "R0"

    def getPrintableInst(self):
        return self._name

    @staticmethod
    def is_type(asm):
        return isInstruct(NopInst._name, asm)


class AddInst(RegInst):
    _funct = "000"
    _name = "ADD"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(AddInst._name, asm)


class SubInst(RegInst):
    _funct = "001"
    _name = "SUB"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(SubInst._name, asm)


class SraInst(RegInst):
    _funct = "010"
    _name = "SRA"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(SraInst._name, asm)


class SrlInst(RegInst):
    _funct = "011"
    _name = "SRL"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(SrlInst._name, asm)


class SllInst(RegInst):
    _funct = "100"
    _name = "SLL"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(SllInst._name, asm)


class AndInst(RegInst):
    _funct = "101"
    _name = "AND"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(AndInst._name, asm)


class OrInst(RegInst):
    _funct = "110"
    _name = "OR"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(OrInst._name, asm)
