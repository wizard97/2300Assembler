# Branching instructions subclass

from ImmInstructs import *
from BaseInstruct import *
from abc import ABCMeta, abstractmethod
from AssemblerExceptions import *

class BranchInst(ImmInstruct):
    __metaclass__ = ABCMeta
    _name = ""
    _op = ""

    def __init__(self, asm, line_num,label=None):
        super(BranchInst, self).__init__(asm, line_num,label)
        # Offset
        self.IMM = None
        # Label
        self.branch_to = None

    @abstractmethod
    def is_type(asm):
        pass

    def parse(self):
        args = self.split_asm()

        args[0] = args[0].upper()
        args[1] = args[1].upper()

        if (len(args) != self._num_args or \
            not BaseInstruct.valid_regs.has_key(args[0]) or \
            not BaseInstruct.valid_regs.has_key(args[1])):
            raise AssemblerException(self.line_num, "Invalid arguments for '%s'" % (self.asm))

        #offset
        if (isInt(args[2])):
            if (int(args[2]) < super(BranchInst, self)._min_imm or int(args[2]) > super(BranchInst, self)._max_imm):
                raise AssemblerException(self.line_num, "Unable to jump by '%s' offset, IMM is out of range" % (args[2]))
            else:
                self.IMM = int(args[2])
                self.branch_to = None

        else:
            # label
            self.branch_to = args[2]
            self.IMM = None

        self.regRT = args[0]
        self.regRS = args[1]

    def generate_inst(self):
        # Make sure linker has run
        assert self.IMM is not None
        valid_regs = BaseInstruct.valid_regs
        return self._op + valid_regs[self.regRS] + valid_regs[self.regRT] + self.int_2comp(6, self.IMM)

    def set_IMM(self, imm):
        imm = int(imm)
        if (imm < super(BranchInst, self)._min_imm or imm > super(BranchInst, self)._max_imm):
            raise AssemblerException(self.line_num, "Unable to jump by '%s' offset, IMM is out of range" % (str(imm)))
            return
        self.IMM = imm

    def needs_linking(self):
        return self.IMM is None

    def getImmLabel(self):
        return self.branch_to

    def getPrintableInst(self):
        l = self.getImmLabel()
        if l is None:
            l = str(self.IMM)
        return "%s %s, %s, %s" % (self._name, self.regRT, self.regRS, l)


class BeqInst(BranchInst):
    _name = "BEQ"
    _op = "1000"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(BeqInst._name, asm)

class BneInst(BranchInst):
    _name = "BNE"
    _op = "1001"
    _num_args = 3

    @staticmethod
    def is_type(asm):
        return isInstruct(BneInst._name, asm)


class BranchSinReg(BranchInst):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def is_type(asm):
        pass

    def parse(self):
        args = self.split_asm()

        args[0] = args[0].upper()

        if (len(args) != self._num_args or not BaseInstruct.valid_regs.has_key(args[0])):
            raise AssemblerException(self.line_num, "Invalid arguments for '%s'" % (self.asm))

        #offset
        if (isInt(args[1])):
            if (int(args[1]) < super(BranchInst, self)._min_imm or int(args[1]) > super(BranchInst, self)._max_imm):
                raise AssemblerException(self.line_num, "Unable to jump by '%s' offset, IMM is out of range" % (args[1]))
                return
            else:
                self.IMM = int(args[1])
                self.branch_to = None

        else:
            # label
            self.branch_to = args[1]
            self.IMM = None

        self.regRT = "R0"
        self.regRS = args[0]


    def getPrintableInst(self):
        l = self.getImmLabel()
        if l is None:
            l = str(self.IMM)
        return "%s %s, %s" % (self._name, self.regRS, l)

class BgezInst(BranchSinReg):
    _name = "BGEZ"
    _op = "1010"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(BgezInst._name, asm)


class BltzInst(BranchSinReg):
    _name = "BLTZ"
    _op = "1011"
    _num_args = 2

    @staticmethod
    def is_type(asm):
        return isInstruct(BltzInst._name, asm)
