from pymtl3 import *

class ChunkAdder(Component):
    def construct(s):
        s.in0 = InPort(32)
        s.in1 = InPort(32)
        s.out = OutPort(32)

        @update
        def add_logic():
            s.out @= s.in0 + s.in1
