from pymtl3 import *
from config import CHUNK_WIDTH

class ChunkSubtractor( Component ):
    def construct( s, width=CHUNK_WIDTH ):
        s.in0 = InPort(width)
        s.in1 = InPort(width)
        s.bin_ = InPort(1)
        s.out = OutPort(width)
        s.bout = OutPort(1)

        @update
        def sub_logic():
            diff = s.in0 - s.in1 - s.bin_
            s.out @= diff & ((1<<width)-1)
            s.bout @= 1 if diff < 0 else 0
