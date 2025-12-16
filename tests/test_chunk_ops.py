import pytest
from pymtl3 import *
from src.chunk_adder import ChunkAdder
from src.chunk_subtractor import ChunkSubtractor
from src.chunk_multiplier import ChunkMultiplier
from src.config import CHUNK_WIDTH

def test_chunk_adder_basic():
    dut = ChunkAdder()
    dut.in0 @= 0xFFFF
    dut.in1 @= 0x0001
    dut.cin @= 0
    dut.sim_tick()
    assert dut.out == 0x0000
    assert dut.cout == 1

def test_chunk_subtractor_basic():
    dut = ChunkSubtractor()
    dut.in0 @= 0x0000
    dut.in1 @= 0x0001
    dut.bin_ @= 0
    dut.sim_tick()
    assert dut.out == 0xFFFFFFFF & ((1<<CHUNK_WIDTH)-1)
    assert dut.bout == 1

def test_chunk_multiplier_basic():
    dut = ChunkMultiplier()
    dut.in0 @= 0xFFFF
    dut.in1 @= 0x0002
    dut.sim_tick()
    assert dut.out == 0x1FFFE
