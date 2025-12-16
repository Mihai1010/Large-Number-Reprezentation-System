from pymtl3 import *
from src.bigint_modules import ChunkAdder


def test_chunk_adder_basic():
    dut = ChunkAdder()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 10
    dut.b @= 20
    dut.carry_in @= 0
    dut.sim_tick()

    assert int(dut.out) == 30
    assert int(dut.carry_out) == 0


def test_chunk_adder_with_carry():
    dut = ChunkAdder()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 0xFFFFFFFF
    dut.b @= 1
    dut.carry_in @= 0
    dut.sim_tick()

    assert int(dut.out) == 0
    assert int(dut.carry_out) == 1
