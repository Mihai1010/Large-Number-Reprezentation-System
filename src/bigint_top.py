from pymtl3 import *
from src.bigint_adder import BigIntAdder
from src.bigint_multiplier import BigIntMultiplier

class BigIntALU(Component):
    def construct(s, num_chunks):
        s.num_chunks = num_chunks
        s.in0 = [InPort(32) for _ in range(num_chunks)]
        s.in1 = [InPort(32) for _ in range(num_chunks)]
        s.sum_out = [OutPort(32) for _ in range(num_chunks)]
        s.product_out = [OutPort(64) for _ in range(num_chunks*2)]

        s.adder = BigIntAdder(num_chunks)
        s.multiplier = BigIntMultiplier(num_chunks)

        for i in range(num_chunks):
            s.adder.in0[i] //= s.in0[i]
            s.adder.in1[i] //= s.in1[i]
            s.sum_out[i] //= s.adder.out[i]

            s.multiplier.in0[i] //= s.in0[i]
            s.multiplier.in1[i] //= s.in1[i]

        for i in range(num_chunks*2):
            s.product_out[i] //= s.multiplier.out[i]
