from pymtl3 import *
from src.chunk_adder import ChunkAdder

class BigIntAdder(Component):
    def construct(s, num_chunks=2):
        s.num_chunks = num_chunks

        # Vector de intrări și ieșiri
        s.in0 = InPort(32*num_chunks)
        s.in1 = InPort(32*num_chunks)
        s.out = OutPort(32*num_chunks)

        # Cream un list de adders
        s.adders = [ChunkAdder() for _ in range(num_chunks)]

        for i in range(num_chunks):
            s.adders[i].in0 //= s.in0[i*32:(i+1)*32]
            s.adders[i].in1 //= s.in1[i*32:(i+1)*32]
            s.out[i*32:(i+1)*32] //= s.adders[i].out
