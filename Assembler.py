#!/usr/bin/env python
#title           :Assembler.py
#description     :Assembler for 2300 assembly, creates verilog iram from assembly
#author          :D. Aaron Wisner (daw268@cornell.edu)
#date            :5/9/16
#version         :1.3
#usage           :run from python shell
#notes           :
#==============================================================================


from RegInstructs import *
from ImmInstructs import *
from BranchInstructs import *
from AssemblerExceptions import *

class Assembler(object):

    ill_chars = [';', ' ', ':', ',', '#']

    supported_insts = [OriInst, AndiInst, AddiInst, SbInst, LbInst, \
        AddInst, SubInst, SraInst, SrlInst, SllInst, AndInst, OrInst, \
        BeqInst, BneInst, BgezInst, BltzInst,
        NopInst, HaltInst]


    def __init__(self, input):
        self.input = input
        self.reset()
        print "Using asm source: '%s'" % (input)

    def reset(self):
        self.asm = []
        self.insts = []
        self.warnings = []

    def assemble(self):
        try:
            self.reset()
            print "Parsing..."
            self.parse()
            print "Creating instructions..."
            self.gen_insts()
            if (len(self.insts) > 128):
                raise AssemblerException(self.insts[128].getLineNum(), \
                    "Max number of instructions exceeded (%d currently)" % (len(self.insts)))
            print "Linking..."
            self.link()
            print "Done!"
        except AssemblerException as e:
            self.error(e.getMessage(), e.getLineNum())
            return

        print "_______RESULTING INSTRUCTIONS________\n"
        branches = 0
        for x in self.insts:
            print x.generate_inst() + '  // ' + x.getPrintableLabel() + ' ' + x.asm
            if isinstance(x, BranchInst):
                branches += 1

        if (len(self.getWarnings())):
            print "\nWarnings:"
            for w in self.getWarnings():
                print "Line %d: %s" % (w[0], w[1])

        print "\nDone: %d instructions (%d branches)" % (len(self.insts), branches)
        print "Run genVLogiram() to generate Verilog .v file"


    def parse(self):
        self.asm = []
        lines = open(self.input, "r").readlines()
        label = None
        i=0
        for i in range(len(lines)):
            # Remove all comments
            c = lines[i].split('#')[0].strip()

            #is there a label?
            pos = c.find(':')
            if (pos != -1):
                if (label is not None):
                    self._addWarning(i, "Ignoring redundant label '%s'" % (label))
                label = c[:pos]
                bad_chars = False
                # Look for bad chars
                for ch in self.ill_chars:
                    if (label.find(ch) >= 0):
                        bad_chars = True
                        break

                if (len(label) == 0 or bad_chars):
                    raise AssemblerException(i+1, "Invalid label '%s'" % (label))

            if (pos < 0):
                inst = c.strip()
            else:
                inst = c[pos+1:].strip()
            if (len(inst) > 0):
                self.asm.append([inst, label, i+1])
                label = None
        # spurrious label?
        if (label is not None):
            self.asm.append(["NOP", label, i+1])
            self._addWarning(i+1, "Spurious label '%s', appending a NOP so label can be resolved" % (label))

        return self.asm

    def gen_insts(self):
        self.insts = []

        for a in self.asm:
            inst = None

            for i in self.supported_insts:
                if (i.is_type(a[0])):
                    # found inst
                    inst = i
                    break
            if (inst is None):
                raise AssemblerException(a[2], "Unknown instruction '%s'" % a[0])

            tmp = inst(a[0], a[2], a[1])
            tmp.parse()
            self.insts.append(tmp)
        return self.insts


    def link(self):
        # create symbols table
        symbols = {}
        for i in range(len(self.insts)):
            inst = self.insts[i]
            label = inst.getLabel()
            if (label is not None):
                if symbols.has_key(label):
                    raise AssemblerException(inst.getLineNum(), "Exisiting label for '%s'" % label)

                symbols[label] = (i, self.insts[i])

        # Resolve symbols
        for i in range(len(self.insts)):
            inst = self.insts[i]
            if (inst.needs_linking()):
                try:
                    imm = symbols[inst.getImmLabel()][0] - i - 1
                except KeyError:
                    raise AssemblerException(inst.getLineNum(), \
                        "Unable to resolve label '%s'" % (inst.getImmLabel()))
                try:
                    inst.set_IMM(imm)
                except AssemblerException: #can we reach it we PC overflow?
                    try:
                        fw = 127 + symbols[inst.getImmLabel()][0] - i
                        rev = symbols[inst.getImmLabel()][0] - 129 - i
                        if (abs(fw) <= abs(rev)):
                            imm2 = fw
                        else:
                            imm2 = rev
                        inst.set_IMM(imm2)
                        self._addWarning(inst.getLineNum(),
                            "Using PC overflow to jump (%d) to label '%s' on line: %d" % \
                            (imm2, inst.getImmLabel(), symbols[inst.getImmLabel()][1].getLineNum()))
                    except AssemblerException: #Guess we couldnt
                        raise AssemblerException(inst.getLineNum(), \
                            "Branch to label '%s' (line %d) is unreachable (IMM = %d)" % \
                            (inst.getImmLabel(), symbols[inst.getImmLabel()][1].getLineNum(), imm))



    def print_asm(self):
        for a in self.asm:
            if (a[1] is not None):
                print a[1] + ': ' + a[0]
            else:
                print a[0]


    def error(self, msg, line):
        self.reset()
        print "Error on line %d in '%s': %s" % (line, self.input, msg)

    def _addWarning(self, line, msg):
        tup = (line, msg)
        self.warnings.append(tup)

    def getWarnings(self):
        return self.warnings


    def genVLogiram(self, output):
        out = open(output, "w")
        template = open("iramTemplate.txt", "r").read()
        name = output.split('.')[0]
        lines = []
        for i in range(len(self.insts)):
            lines.append("mem[%d] <= 16'b%s; // %s  %s" % \
                (i, self.insts[i].generate_inst(), self.insts[i].getPrintableLabel(), self.insts[i].asm))
        out.write(template % (name, "\n      ".join(lines), i+1))
        print "Created '%s' Verilog file with module name '%s'" % (output, name)
