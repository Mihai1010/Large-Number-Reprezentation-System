from pymtl3 import *
from bigint_adder import BigIntAdder
from bigint_multiplier import BigIntMultiplier
from config import CHUNK_WIDTH

class BigIntALU( Component ):
    def construct( s, num_chunks=4, width=CHUNK_WIDTH ):
        s.in0 = [InPort(width) for _ in range(num_chunks)]
        s.in1 = [InPort(width) for _ in range(num_chunks)]
        s.sum_out = [OutPort(width) for _ in range(num_chunks)]
        s.carry_out = OutPort(1)
        s.prod_out = [OutPort(2*width) for _ in range(num_chunks*2)]

        s.adder = BigIntAdder(num_chunks=num_chunks, width=width)
        s.multiplier = BigIntMultiplier(num_chunks=num_chunks, width=width)

        # Conectare intrări ieșiri
        for i in range(num_chunks):
            s.adder.in0[i] //= s.in0[i]
            s.adder.in1[i] //= s.in1[i]
            s.sum_out[i] //= s.adder.sum_out[i]
        s.carry_out //= s.adder.carry_out

        for i in range(num_chunks):
            s.multiplier.in0[i] //= s.in0[i]
            s.multiplier.in1[i] //= s.in1[i]
            for j in range(num_chunks*2):
                s.prod_out[j] //= s.multiplier.prod_out[j]
