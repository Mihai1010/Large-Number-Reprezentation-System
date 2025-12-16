from pymtl3 import *
from src.bigint_modules import BigIntAdder


def test_bigint_add_2_chunks():
    dut = BigIntAdder(nchunks=2)
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a[0] @= 0xFFFFFFFF
    dut.a[1] @= 0x00000001

    dut.b[0] @= 1
    dut.b[1] @= 0

    dut.sim_tick()

    assert int(dut.out[0]) == 0
    assert int(dut.out[1]) == 2


def test_bigint_add_no_carry():
    dut = BigIntAdder(nchunks=2)
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a[0] @= 10
    dut.a[1] @= 20

    dut.b[0] @= 5
    dut.b[1] @= 6

    dut.sim_tick()

    assert int(dut.out[0]) == 15
    assert int(dut.out[1]) == 26
