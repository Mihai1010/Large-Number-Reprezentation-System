from pymtl3 import *
from src.bigint_modules import ChunkMultiplier


def test_chunk_multiplier_basic():
    dut = ChunkMultiplier()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 7
    dut.b @= 6
    dut.sim_tick()

    assert int(dut.out) == 42


def test_chunk_multiplier_large():
    dut = ChunkMultiplier()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 0xFFFF
    dut.b @= 0x10
    dut.sim_tick()

    assert int(dut.out) == 0xFFFF0
