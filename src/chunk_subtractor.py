from pymtl3 import *

class ChunkSubtractor(Component):
    def construct(s):
        s.in0 = InPort(32)
        s.in1 = InPort(32)
        s.out = OutPort(32)
        s.borrow = OutPort(1)

        @update
        def comb_logic():
            if s.in0 < s.in1:
                s.out @= (1 << 32) + s.in0 - s.in1
                s.borrow @= 1
            else:
                s.out @= s.in0 - s.in1
                s.borrow @= 0
