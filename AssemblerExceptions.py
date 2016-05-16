# Assembler exception class

class AssemblerException(Exception):

    def __init__(self, line_num, msg):
        super(AssemblerException, self).__init__(msg)
        self.line_num = line_num
        self.message = msg

    def __str__(self):
        return "On line %d: %s" (self.line_num, self.message)

    def getMessage(self):
        return self.message

    def getLineNum(self):
        return self.line_num
