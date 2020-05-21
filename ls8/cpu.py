"""CPU functionality."""

import sys

PUSH = 0b01000101
POP = 0b01000110

SP = 7
STACK_START = 0xF4

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # STEP 1 - Add list properties to the CPU class to hold 256 bytes of memory and 8 general purpose registers
        self.ram = [0] * 256
        self.register = [0] * 8
        self.running = True
        self.pc = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.register[SP] = STACK_START

    def load(self):
        """Load a program into memory."""
        filename = './examples/print8.ls8'
        
        if len(sys.argv) == 2:
            filename = sys.argv[1]

        address = 0
        

        with open(filename) as program:
            for ins in program:
                ins = ins.split('#')
                ins = ins[0].strip()

                if ins == '':
                    continue
                self.ram[address] = int(ins, 2)
                address += 1


        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")
    
    def halt(self):
        self.running = False

    # STEP 2: Add RAM functions ram_read and ram_write
    # These access the RAM inside the CPU object
    def ram_read(self, address):
        # RR should accept the address to read and return the value
        return self.ram[address]
    
    def ram_write(self, address, value):
        # RW should accept a value to write and the address to write it to
        self.ram[address] = value

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
        # wherever the pc is, this is storing it into the Instruction Register
        IR = self.pc
        

        while self.running:
            instruction = self.ram[IR]
            
            if instruction == self.LDI:
                # LDI SETS THE VALUE OF A REGISTER TO AN INTEGER
                reg_num = self.ram[IR + 1]
                value = self.ram[IR + 2]
                self.register[reg_num] = value
                IR += 3
            
            elif instruction == self.PRN:
                # PRINTS NUMERIC VALUE STORED IN THE GIVEN REGISTER 
                reg_num = self.ram[IR + 1]
                value = self.register[reg_num]
                print(value)
                IR += 2
            
            elif instruction == self.MUL:
                self.alu('MUL', self.ram[IR + 1], self.ram[IR + 2])
                IR += 3
            
            elif instruction == PUSH:
                # decrement the SP
                self.register[SP] -= 1
                # get resgister number
                reg_num = self.ram[IR + 1]
                self.ram[self.register[SP]] = self.register[reg_num]
                self.pc += 2
            
            elif instruction == POP:
                reg_num = self.ram_read(self.pc+1)

                # stack_address = self.register[SP]
                # stack_value = self.ram[stack_address]
                # self.register[reg_num] = stack_value
                self.register[SP] += 1
                self.pc +=2

            elif instruction == self.HLT:
                # HALTS THE CPU AND EXIT THE EMULATOR
                self.halt()

            else:
                print ('Invalid Instructions')
                self.halt()
