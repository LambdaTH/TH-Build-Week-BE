"""CPU functionality."""

import sys

branchTable ={
    HALT: halt_op,
    PRINT: print_op,
    ADD: add_op,
    PUSH: push_op,
    POP: pop_op,
    CALL: call_op,
    RET: ret_op
}
# create functions for each activity

def halt_op ():
    self.HALT = True
def pop_op():
    self.reg[operand_a] = self.ram_read(self.reg[self.sp])
    self.reg[self.sp] += 1
def push_op():
    self.reg[self.sp] -= 1
    value = self.reg[operand_a]
    address = self.reg[self.sp]
    self.raw_write(address, value)
def prn_op():
    print(self.reg[operand_a])
def ldi_op():
    self.reg[operand_a] = operand_b
def mul_op():
    self.alu("MUL", operand_a, operand_b)
def call_op():
    pass
def ret_op():
    pass


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.HALTED = False
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py <filename>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as instructions:
                # read each instruction line
                for line in instructions:
                    # split each line into instructions and comments
                    split_instruction_line = line.split("#")
                    
                    # remove whitespace
                    one_and_zeroes = split_instruction_line[0].strip()

                    # ignore blank lines / comment only lines
                    if len(one_and_zeroes) == 0:
                        continue

                    # set the number to an integer of base 2
                    instruction = int(one_and_zeroes, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
            # for add operation
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # for mulitplication operation
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def ram_read(self , MAR):
        return self.ram[MAR]

    def raw_write(self , MAR , MDR):
        self.reg[MAR] = MDR
        

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        while not self.HALTED:
            IR = self.ram[self.pc]
            # LDI = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # mask the remaining aspect of the code and then right shift
            # so it basically becomes the first value in IR * 2^1 + second value in IR*2^0
            operands = (IR  >> 6 ) & 0b11000000
            # if IR == HLT:
            #     self.HALTED = True
            # elif IR == LDI:
            #     self.reg[operand_a] = operand_b
            # elif IR == PRN:
            #     print(self.reg[operand_a])
            # elif IR == MUL:
            #     self.alu("MUL", operand_a, operand_b)
            # elif IR == PUSH:
            #     self.reg[self.sp] -= 1
            #     value = self.reg[operand_a]
            #     address = self.reg[self.sp]
            #     self.raw_write(address, value)
            # elif IR == POP:
            #     self.reg[operand_a] = self.ram_read(self.reg[self.sp])
            #     self.reg[self.sp] += 1
            # else:
            #     print(f"Unknown Instruction {IR:08b}")
            #     sys.exit(1)
            self.pc += operands + 1
            
    