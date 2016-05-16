# Instruction base class

from abc import ABCMeta, abstractmethod
from AssemblerExceptions import *

# Helper function for checking if certain instruction
def isInstruct(name, asm):
    asm = asm.split(',')[0].upper().strip()
    return asm.find(name) == 0

class BaseInstruct(object):
    __metaclass__ = ABCMeta
    valid_regs = {"R0" : "000", "R1" : "001", "R2": "010", "R3" : "011", \
        "R4" : "100", "R5" : "101", "R6": "110", "R7" : "111"}

    def __init__(self, asm, line_num,label=None):
        self.asm = ' '.join(asm.strip().split()) # clean up white space
        self.label = label
        self.line_num = int(line_num)
        self.inst = None

        self.regRS = "R0"
        self.regRT = "R0"

    @abstractmethod
    def is_type(asm):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def generate_inst(self):
        pass

    def split_asm(self):
        asm = self.asm.strip()[len(self._name):]
        tmp = asm.split(",")
        cleaned = []
        for i in range(len(tmp)):
            val = tmp[i].strip()
            cleaned.append(val)
        return cleaned

    def getLabel(self):
        return self.label

    @abstractmethod
    def getPrintableInst(self):
        pass

    def getPrintableLabel(self):
        if (self.label is None):
            return ''
        return self.label + ':'

    def getLineNum(self):
        return self.line_num

    def needs_linking(self):
        return False
