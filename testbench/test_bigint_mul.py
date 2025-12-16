from pymtl3 import *
from src.bigint_modules import BigIntMultiplier


def test_bigint_mul_1_chunk():
    dut = BigIntMultiplier(nchunks=1)
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a[0] @= 7
    dut.b[0] @= 6
    dut.sim_tick()

    assert int(dut.out[0]) == 42


def test_bigint_mul_2_chunks_simple():
    dut = BigIntMultiplier(nchunks=2)
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a[0] @= 2
    dut.a[1] @= 0

    dut.b[0] @= 3
    dut.b[1] @= 0

    dut.sim_tick()

    assert int(dut.out[0]) == 6
    assert int(dut.out[1]) == 0
