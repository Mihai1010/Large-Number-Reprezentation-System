import pytest
from pymtl3 import *
from src.chunk_adder import ChunkAdder
from src.chunk_subtractor import ChunkSubtractor
from src.chunk_multiplier import ChunkMultiplier
from src.config import CHUNK_WIDTH

def test_chunk_adder_basic():
    dut = ChunkAdder()
    dut.elaborate()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()
    
    dut.in0 @= 0xFFFFFFFF
    dut.in1 @= 0x00000001
    dut.sim_eval_combinational()
    
    print(f"ChunkAdder: {hex(dut.in0)} + {hex(dut.in1)} = out={hex(dut.out)}")
    # Note: Simple addition without carry - result wraps around
    expected = (0xFFFFFFFF + 0x00000001) & 0xFFFFFFFF
    assert dut.out == expected

def test_chunk_subtractor_basic():
    dut = ChunkSubtractor()
    dut.elaborate()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()
    
    dut.in0 @= 0x00000005
    dut.in1 @= 0x00000003
    dut.sim_eval_combinational()
    
    print(f"ChunkSubtractor: {hex(dut.in0)} - {hex(dut.in1)} = out={hex(dut.out)}, borrow={dut.borrow}")
    assert dut.out == 0x00000002
    assert dut.borrow == 0

def test_chunk_multiplier_basic():
    dut = ChunkMultiplier()
    dut.elaborate()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()
    
    dut.in0 @= 0x0000FFFF
    dut.in1 @= 0x00000002
    dut.sim_eval_combinational()
    
    print(f"ChunkMultiplier: {hex(dut.in0)} * {hex(dut.in1)} = {hex(dut.out)}")
    assert dut.out == 0x0001FFFE

if __name__ == "__main__":
    print("Running test_chunk_adder_basic...")
    try:
        test_chunk_adder_basic()
        print("✅ TEST PASSED: test_chunk_adder_basic\n")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"❌ TEST ERROR: {e}\n")
    
    print("Running test_chunk_subtractor_basic...")
    try:
        test_chunk_subtractor_basic()
        print("✅ TEST PASSED: test_chunk_subtractor_basic\n")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"❌ TEST ERROR: {e}\n")
    
    print("Running test_chunk_multiplier_basic...")
    try:
        test_chunk_multiplier_basic()
        print("✅ TEST PASSED: test_chunk_multiplier_basic\n")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"❌ TEST ERROR: {e}\n")
