from pymtl3 import *
from PyMTL.config import CHUNK_WIDTH

class ChunkAdder( Component ):
    def construct( s, width=CHUNK_WIDTH ):
        s.in0 = InPort(width)
        s.in1 = InPort(width)
        s.cin = InPort(1)
        s.out = OutPort(width)
        s.cout = OutPort(1)

        @update
        def add_logic():
            sum_val = s.in0 + s.in1 + s.cin
            s.out @= sum_val & ((1<<width)-1)
            s.cout @= sum_val >> width
