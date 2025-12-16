from pymtl3 import *
from src.bigint_modules import ChunkSubtractor


def test_chunk_subtractor_basic():
    dut = ChunkSubtractor()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 50
    dut.b @= 20
    dut.borrow_in @= 0
    dut.sim_tick()

    assert int(dut.out) == 30
    assert int(dut.borrow_out) == 0


def test_chunk_subtractor_with_borrow():
    dut = ChunkSubtractor()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()

    dut.a @= 0
    dut.b @= 1
    dut.borrow_in @= 0
    dut.sim_tick()

    assert int(dut.out) == 0xFFFFFFFF
    assert int(dut.borrow_out) == 1
