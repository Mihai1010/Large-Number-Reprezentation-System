from pymtl3 import *
from chunk_adder import ChunkAdder
from config import CHUNK_WIDTH

class BigIntAdder( Component ):
    def construct( s, num_chunks=4, width=CHUNK_WIDTH ):
        s.in0 = [InPort(width) for _ in range(num_chunks)]
        s.in1 = [InPort(width) for _ in range(num_chunks)]
        s.sum_out = [OutPort(width) for _ in range(num_chunks)]
        s.carry_out = OutPort(1)

        s.adders = [ChunkAdder(width=width) for _ in range(num_chunks)]

        @update
        def sum_logic():
            carry = 0
            for i in range(num_chunks):
                s.adders[i].in0 @= s.in0[i]
                s.adders[i].in1 @= s.in1[i]
                s.adders[i].cin @= carry
                s.sum_out[i] @= s.adders[i].out
                carry = s.adders[i].cout
            s.carry_out @= carry
