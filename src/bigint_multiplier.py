from pymtl3 import *
from src.chunk_multiplier import ChunkMultiplier

class BigIntMultiplier(Component):
    def construct(s, num_chunks):
        s.num_chunks = num_chunks
        s.in0 = [InPort(32) for _ in range(num_chunks)]
        s.in1 = [InPort(32) for _ in range(num_chunks)]
        s.out = [OutPort(64) for _ in range(num_chunks*2)]

        s.multipliers = [[ChunkMultiplier() for _ in range(num_chunks)] for _ in range(num_chunks)]

        # combinarea rezultatelor
        for i in range(num_chunks):
            for j in range(num_chunks):
                s.multipliers[i][j].in0 //= s.in0[i]
                s.multipliers[i][j].in1 //= s.in1[j]

        @update
        def combine():
            result = [0]*(num_chunks*2)
            for i in range(num_chunks):
                for j in range(num_chunks):
                    result[i+j] += s.multipliers[i][j].out
            for k in range(num_chunks*2):
                s.out[k] @= result[k]
