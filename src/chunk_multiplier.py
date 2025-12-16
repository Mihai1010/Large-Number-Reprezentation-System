from pymtl3 import *

class ChunkMultiplier(Component):
    def construct(s):
        s.in0 = InPort(32)
        s.in1 = InPort(32)
        s.out = OutPort(64)

        @update
        def comb_logic():
            s.out @= zext(s.in0, 64) * zext(s.in1, 64)
