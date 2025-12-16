import numpy as np
from numba import cuda, uint64

# --- CONFIGURĂRI CONSTANTE ---
CHUNK_SIZE = 32
MASK = (1 << CHUNK_SIZE) - 1
TPB = 256  # Threads Per Block

# --- IMPLEMENTARE CPU (Referință) ---
def cpu_mul(A, B):
    n = len(A)
    R = [0] * (2 * n)
    for i in range(n):
        carry = 0
        for j in range(n):
            res = R[i + j] + (A[i] * B[j]) + carry
            R[i + j] = res & MASK
            carry = res >> CHUNK_SIZE
        R[i + n] += carry
    return R

# --- IMPLEMENTARE GPU (Kernel CUDA) ---
@cuda.jit
def gpu_mul_kernel(A, B, R, n):
    tx = cuda.grid(1)
    if tx < n:
        val_A = A[tx]
        for j in range(n):
            # Folosim atomic.add pentru a evita Race Conditions la înmulțire
            cuda.atomic.add(R, tx + j, val_A * B[j])