import pytest
from pymtl3 import *
from src.bigint_adder import BigIntAdder

def test_bigint_adder_2chunks():
    dut = BigIntAdder(num_chunks=2)
    dut.in0[0] @= 0xFFFFFFFF
    dut.in0[1] @= 0x00000001
    dut.in1[0] @= 0x00000001
    dut.in1[1] @= 0x00000002
    dut.sim_tick()
    assert dut.sum_out[0] == 0x00000000
    assert dut.sum_out[1] == 0x00000004
    assert dut.carry_out == 0
