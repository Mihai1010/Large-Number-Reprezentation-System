import pytest
from pymtl3 import *
from src.bigint_multiplier import BigIntMultiplier

def test_bigint_multiplier_2chunks():
    dut = BigIntMultiplier(num_chunks=2)
    dut.in0[0] @= 0x0001
    dut.in0[1] @= 0x0002
    dut.in1[0] @= 0x0003
    dut.in1[1] @= 0x0004
    dut.sim_tick()
    # Schoolbook multiplication: 2 chunks x 2 chunks
    expected = [3, 10, 8, 0]  # manual calculation
    for i in range(4):
        assert dut.prod_out[i] == expected[i]
