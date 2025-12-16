from pymtl3 import *
from chunk_multiplier import ChunkMultiplier
from config import CHUNK_WIDTH

class BigIntMultiplier( Component ):
    def construct( s, num_chunks=4, width=CHUNK_WIDTH ):
        s.in0 = [InPort(width) for _ in range(num_chunks)]
        s.in1 = [InPort(width) for _ in range(num_chunks)]
        s.prod_out = [OutPort(2*width) for _ in range(num_chunks*2)]

        s.multipliers = [[ChunkMultiplier(width=width) for _ in range(num_chunks)] for _ in range(num_chunks)]

        @update
        def mul_logic():
            # Zero output
            for i in range(num_chunks*2):
                s.prod_out[i] @= 0
            # Schoolbook multiplication
            for i in range(num_chunks):
                for j in range(num_chunks):
                    s.prod_out[i+j] @= s.prod_out[i+j] + s.in0[i]*s.in1[j]
