from pymtl3 import *
from config import CHUNK_WIDTH

class ChunkMultiplier( Component ):
    def construct( s, width=CHUNK_WIDTH ):
        s.in0 = InPort(width)
        s.in1 = InPort(width)
        s.out = OutPort(2*width)

        @update
        def mul_logic():
            s.out @= s.in0 * s.in1
