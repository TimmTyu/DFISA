'''
this is interpreter for DFISA (DiForm Instruction Set Architecture)
'''
class DFISA:
    def __init__(self,program):
        self.pc = 0
        self.flags = {"NF":0,"ZF":0}
        self.regs = [0] * 15
        self.acc = 0
        self.mem = program + [0] * (0xFF - len(program))
        self.running = 1
    def fetch(self):
        inst = self.mem[self.pc]
        self.pc += 1
        return(inst & 0XFF)
    def exe(self):
        inst = self.fetch()
        if inst == 0x6A: #mov r,i
            reg = self.fetch()
            num = self.fetch()
            self.regs[reg] = num
        elif inst == 0xD4: #mov r,r
            reg = self.fetch()
            reg2 = self.fetch()
            self.regs[reg] = self.regs[reg2]
        elif inst == 0xF5: #add i
            num = self.fetch()
            self.acc += num
            self.flags["ZF"] = 1 if self.acc == 0 else 0
            self.flags["NF"] = 1 if self.acc < 0 else 0
        elif inst == 0xFD: #sub i
            num = self.fetch()
            self.acc -= num
            self.flags["ZF"] = 1 if self.acc == 0 else 0
            self.flags["NF"] = 1 if self.acc < 0 else 0
        elif inst == 0x56: #lda r
            reg = self.fetch()
            self.regs[reg] = self.acc
        elif inst == 0xAF: #sta i
            num = self.fetch()
            self.acc = num
        elif inst == 0xA6: #sta r
            reg = self.fetch()
            self.acc = self.regs[reg]
        elif inst == 0xE9: #ldm r
            memdt = self.mem[self.fetch()]
            reg = self.fetch()
            self.regs[reg] = memdt
        elif inst == 0xFA:  # stm i
            addr = self.fetch()
            num = self.fetch()
            self.mem[addr] = num
        elif inst == 0xFB:  # stm r
            addr = self.fetch()
            reg = self.fetch()
            self.mem[addr] = self.regs[reg]
        elif inst == 0xF9: #syscall
            if self.regs[0] == 0xFA:
                print(chr(self.regs[1]))
        elif inst == 0xFF: #halt
            self.running = 0
        else: #nop
            pass
    def going(self):
        return(self.running)  
C = DFISA([0x6A,0x00,0xFA,0x6A,0x01,0x41,0xF9,0xFF])
while C.going():
    C.exe()
'''
C = DFISA([0x6A,0x00,0xFA,0x6A,0x01,0x68,0xF9,0x6A,0x01,0x65,0xF9,0x6A,0x01,0x6C,0xF9,0x6A,
0x01,0x6C,0xF9,0x6A,0x01,0x6F,0xF9,0x6A,0x01,0x20,0xF9,0x6A,0x01,0x77,0xF9,0x6A,0x01,0x6F,
0xF9,0x6A,0x01,0x72,0xF9,0x6A,0x01,0x6C,0xF9,0x6A,0x01,0x64,0xF9,0x6A,0x01,0x0A,0xF9,0xFF])
while C.going():
    C.exe()
'''
