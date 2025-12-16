import pytest
from pymtl3 import *
from src.bigint_top import BigIntALU

def test_bigint_alu_sum_and_product():
    dut = BigIntALU(num_chunks=2)
    dut.in0[0] @= 0x0001
    dut.in0[1] @= 0x0002
    dut.in1[0] @= 0x0003
    dut.in1[1] @= 0x0004
    dut.sim_tick()
    # Test adunare
    assert dut.sum_out[0] == 0x0004
    assert dut.sum_out[1] == 0x0007
    # Test multiplicare
    expected_prod = [3, 10, 8, 0]
    for i in range(4):
        assert dut.prod_out[i] == expected_prod[i]
