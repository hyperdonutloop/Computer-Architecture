"""CPU functionality."""

import sys

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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    def halt(self):
        self.running = False

    # STEP 2: Add RAM functions ram_read and ram_write
    # These access the RAM inside the CPU object
    def ram_read(self, address):
        # RR should accept the address to read and return the value
        return self.ram[address]
    
    def ram_write(self, address, payload):
        # RW should accept a value to write and the address to write it to
        self.ram[address] = payload

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
        IR = self.pc

        while self.running:
            instruction = self.ram[IR]
            
            if instruction == self.LDI:
                reg_num = self.ram[IR + 1]
                value = self.ram[IR + 2]
                self.register[reg_num] = value
                IR += 3
            
            elif instruction == self.PRN:
                reg_num = self.ram[IR + 1]
                value = self.register[reg_num]
                print(value)
                IR += 2

            elif instruction == self.HLT:
                self.halt()

            else:
                print ('Invalid Instructions')
                self.halt()


        
        pass
