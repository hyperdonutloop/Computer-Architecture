"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
IRET = 0b00010011
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # STEP 1 - Add list properties to the CPU class to hold 256 bytes of memory and 8 general purpose registers
        self.ram = [0] * 256
        self.register = [0] * 8
        # self.running = True
        self.pc = 0 #program counter
        self.sp = 0xf3 #243 # stack pointer
        self.fl = False
        # self.HLT = 0b00000001
        # self.LDI = 0b10000010
        # self.PRN = 0b01000111
        # self.ADD = 0b10100000
        # self.MUL = 0b10100010
        # self.PUSH = 0b01000101
        # self.POP = 0b01000110
        # self.CALL = 0b01010000
        # self.RET = 0b00010011
        # self.IRET = 0b00010011
        

    def load(self):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]

        # opening filename and assigning it to program variable
        with open(filename) as program:
            # for every line in the program
            for line in program:
                # separating the #
                line = line.split('#')
                # removes spaces at the ZEROith index
                line = line[0].strip()

                if line == '':
                    continue
                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
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

    def run(self):
        """Run the CPU."""
        # STEP 3 - Implement the core of RUN
        running = True
        while running:
            # instruction = the ram AT wherever the pc is
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                # HALTS THE CPU AND EXIT THE EMULATOR
                running = False
            
            elif instruction == CALL:
                # calls a function at the ADDRESS stored in the register
                # the address of the instruction DIRECTLY after call gets pushed to stack
                # PC is set to the address stored in given register
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = self.register[operand_a]
                

            elif instruction == RET:
                # registers r6-r0 popped off stack
                # FL register popped off stack
                # return address popped off stack and stored = in PC
                # interrupts are re-enabled
                popped = self.ram[self.sp]
                self.pc = popped
                self.sp += 1
            
            elif instruction == PUSH:
                
                # r7 is the stack pointer
                # SP is the top of the stack
                # decrement the SP
                self.sp -= 1
                # copy the value in the given register to the address pointed by SP
                # taking the STACK POINTER address(index) and assigning the first argument of the instruction
                self.ram[self.sp] = self.register[operand_a]
                self.pc += 2

            elif instruction == POP:
                # Copy the value from the address pointed to by SP to the given register.
                # from the address --- to the register
                self.register[operand_a] = self.ram[self.sp]
                # Increment SP
                self.sp += 1
                self.pc += 2
            
            elif instruction == LDI:
                # LDI SETS THE VALUE OF A REGISTER TO AN INTEGER
                # the register at whatever index you are given = the value/argument 2
                self.register[operand_a] = operand_b
                self.pc += 3
            
            elif instruction == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            
            elif instruction == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            elif instruction == PRN:
                # PRINTS NUMERIC VALUE STORED IN THE GIVEN REGISTER 
                value = self.register[operand_a]
                print(value)
                self.pc += 2

            # else:
            #     print ('Invalid Instructions')
            #     running = False

# STEP 2: Add RAM functions ram_read and ram_write
    # These access the RAM inside the CPU object
    def ram_read(self, address):
        # RR should accept the address to read and return the value
        return self.ram[address]
    
    def ram_write(self, address, value):
        # RW should accept a value to write and the address to write it to
        self.ram[address] = value

# cpu = CPU()
# cpu.load()
# print(cpu.ram)