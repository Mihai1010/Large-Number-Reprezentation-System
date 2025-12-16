import pytest
from pymtl3 import *
from src.bigint_adder import BigIntAdder

def test_bigint_adder_2chunks():
    dut = BigIntAdder(num_chunks=2)
    dut.elaborate()
    dut.apply(DefaultPassGroup())
    dut.sim_reset()
    
    # Test simple addition: 1 + 1 = 2
    dut.in0 @= 0x00000001_00000001  # 64-bit: chunk[1]=1, chunk[0]=1
    dut.in1 @= 0x00000001_00000001  # 64-bit: chunk[1]=1, chunk[0]=1
    dut.sim_eval_combinational()
    expected_out = 0x00000002_00000002  # chunk[1]=2, chunk[0]=2
    print(f"Input 0: {hex(dut.in0)}")
    print(f"Input 1: {hex(dut.in1)}")
    print(f"Output:  {hex(dut.out)}")
    print(f"Expected: {hex(expected_out)}")
    assert dut.out == expected_out

if __name__ == "__main__":
    print("Running test_bigint_adder_2chunks...")
    try:
        test_bigint_adder_2chunks()
        print("✅ TEST PASSED: test_bigint_adder_2chunks")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
