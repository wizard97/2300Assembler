# Immediate instruction subclass

from BaseInstruct import *
from abc import ABCMeta, abstractmethod
from AssemblerExceptions import *

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class ImmInstruct(BaseInstruct):
    __metaclass__ = ABCMeta

    _name = ""
    _op = ""

    _max_imm = 31
    _min_imm = -32

    def __init__(self, asm, line_num,label=None):
        super(ImmInstruct, self).__init__(asm, line_num,label)
        self.IMM = 0

    @abstractmethod
    def is_type(asm):
        pass

    def parse(self):
        args = self.split_asm()
        if (len(args) != self._num_args):
            raise AssemblerException(self.line_num, "Invalid number of arguments for '%s'" % (self.asm))

        args[0] = args[0].upper()
        args[1] = args[1].upper()

        if (not BaseInstruct.valid_regs.has_key(args[0]) or \
            not BaseInstruct.valid_regs.has_key(args[1]) or \
            not (isInt(args[2]) and int(args[2]) >= self._min_imm and int(args[2]) <= self._max_imm)):
            raise AssemblerException(self.line_num, "Invalid instruction '%s'" % (self.asm))

        self.regRT = args[0]
        self.regRS = args[1]
        self.IMM = int(args[2])

    def generate_inst(self):
        valid_regs = super(ImmInstruct, self).valid_regs
        return self._op + valid_regs[self.regRS] + valid_regs[self.regRT] + self.int_2comp(6, self.IMM)

    def getPrintableInst(self):
        return "%s %s, %s, %d" % (self._name, self.regRT, self.regRS, self.IMM)

    @staticmethod
    def int_2comp(bits, value):
        if value < 0:
            value = ( 1<<bits ) + value
        formatstring = '{:0%ib}' % bits
        return formatstring.format(value)

    def getIMM(self):
        return self.IMM


class AddiInst(ImmInstruct):
    _name = "ADDI"
    _op = "0101"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(AddiInst._name, asm)


class AndiInst(ImmInstruct):
    _name = "ANDI"
    _op = "0110"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(AndiInst._name, asm)


class OriInst(ImmInstruct):
    _name = "ORI"
    _op = "0111"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(OriInst._name, asm)


class MemImmInst(ImmInstruct):
    __metaclass__ = ABCMeta

    def parse(self):
        args = self.split_asm()

        args[0] = args[0].upper()

        if (len(args) != self._num_args or not BaseInstruct.valid_regs.has_key(args[0])):
            raise AssemblerException(self.line_num, "Invalid instruction arguments for '%s'" % (self.asm))

        self.regRT = args[0]

        im = args[1].split('(')[0].strip()
        rs = args[1].split('(')[1].split(')')[0].strip().upper()

        if (not (isInt(im) and int(im) >= self._min_imm and int(im) <= self._max_imm and BaseInstruct.valid_regs.has_key(rs))):
            raise AssemblerException(self.line_num, "IMM of '%s' is invalid or out of bounds" % (self.asm))

        self.regRS = rs
        self.IMM = int(im)


    def getPrintableInst(self):
        return "%s %s, %d(%s)" % (self._name, self.regRT, self.IMM, self.regRS)

class SbInst(MemImmInst):
    _name = "SB"
    _op = "0100"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(SbInst._name, asm)


class LbInst(MemImmInst):
    _name = "LB"
    _op = "0010"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(LbInst._name, asm)
