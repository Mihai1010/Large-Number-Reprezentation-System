#!/usr/bin/env python3
"""
Script pentru rularea tuturor testelor și afișarea rezultatelor
"""
import sys
import os

# Setează PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("RULARE TESTE - Large Number Representation System")
print("="*60)
print()

# Import teste
from tests.test_bigint_adder import test_bigint_adder_2chunks
from tests.test_chunk_ops import test_chunk_adder_basic, test_chunk_subtractor_basic, test_chunk_multiplier_basic
from tests.test_bigint_multiplier import test_bigint_multiplier_2chunks
from tests.test_bigint_top import test_bigint_alu_sum_and_product

tests = [
    ("test_chunk_adder_basic", test_chunk_adder_basic),
    ("test_chunk_subtractor_basic", test_chunk_subtractor_basic),
    ("test_chunk_multiplier_basic", test_chunk_multiplier_basic),
    ("test_bigint_adder_2chunks", test_bigint_adder_2chunks),
    ("test_bigint_multiplier_2chunks", test_bigint_multiplier_2chunks),
    ("test_bigint_alu_sum_and_product", test_bigint_alu_sum_and_product),
]

passed = 0
failed = 0
skipped = 0
errors = 0

for test_name, test_func in tests:
    print(f"\nRunning {test_name}...")
    print("-" * 60)
    try:
        test_func()
        if "skip" in test_name.lower() or "BigInt" in test_name and "Adder" not in test_name:
            print(f"⚠️  TEST SKIPPED: {test_name}")
            skipped += 1
        else:
            print(f"✅ TEST PASSED: {test_name}")
            passed += 1
    except AssertionError as e:
        print(f"❌ TEST FAILED: {test_name}")
        print(f"   Error: {e}")
        failed += 1
    except Exception as e:
        print(f"❌ TEST ERROR: {test_name}")
        print(f"   Error: {e}")
        errors += 1

print("\n" + "="*60)
print("SUMAR TESTE")
print("="*60)
print(f"✅ Passed:  {passed}")
print(f"❌ Failed:  {failed}")
print(f"⚠️  Skipped: {skipped}")
print(f"🔥 Errors:  {errors}")
print(f"📊 Total:   {len(tests)}")
print("="*60)

if failed > 0 or errors > 0:
    sys.exit(1)
