import time
import numpy as np
import matplotlib.pyplot as plt
from numba import cuda, uint64

# Importăm funcțiile și constantele din fișierul nostru gpu_mul.py
from gpu_mul import cpu_mul, gpu_mul_kernel, MASK, TPB

plt.style.use('ggplot')

def run_detailed_benchmark(num_chunks):
    num_chunks = int(num_chunks)

    # 1. Generare Date
    data_A = np.random.randint(0, MASK, size=num_chunks, dtype=np.uint64)
    data_B = np.random.randint(0, MASK, size=num_chunks, dtype=np.uint64)
    list_A = data_A.tolist()
    list_B = data_B.tolist()

    # 2. Măsurare CPU
    start_cpu = time.perf_counter()
    _ = cpu_mul(list_A, list_B)
    end_cpu = time.perf_counter()
    time_cpu = end_cpu - start_cpu

    # 3. Măsurare GPU (Transfer Host -> Device)
    start_transfer = time.perf_counter()
    d_A = cuda.to_device(data_A)
    d_B = cuda.to_device(data_B)
    d_R = cuda.device_array(num_chunks * 2, dtype=np.uint64)
    cuda.synchronize()
    end_transfer = time.perf_counter()
    
    transfer_time = end_transfer - start_transfer

    # 4. Măsurare GPU (Calcul Kernel)
    threads = TPB
    blocks = (num_chunks + (threads - 1)) // threads

    start_compute = time.perf_counter()
    gpu_mul_kernel[blocks, threads](d_A, d_B, d_R, num_chunks)
    cuda.synchronize()
    end_compute = time.perf_counter()
    
    compute_time = end_compute - start_compute

    # 5. Măsurare GPU (Transfer Device -> Host)
    start_read = time.perf_counter()
    _ = d_R.copy_to_host()
    cuda.synchronize()
    end_read = time.perf_counter()
    
    total_transfer = transfer_time + (end_read - start_read)
    total_gpu = total_transfer + compute_time

    return time_cpu, total_gpu, total_transfer, compute_time

# --- RULARE SIMULARE ---
sizes = np.unique(np.logspace(1, 3.5, num=30, dtype=int))
cpu_times = []
gpu_times = []
transfer_times = []
compute_times = []

print(f"Generare date ÎNMULȚIRE pentru {len(sizes)} intervale...")

for s in sizes:
    c, g, t, comp = run_detailed_benchmark(s)
    cpu_times.append(c)
    gpu_times.append(g)
    transfer_times.append(t)
    compute_times.append(comp)

# ==========================================
#               GENERARE GRAFICE
# ==========================================

# --- GRAFIC 1: GENERAL (Performanță Scalabilă) ---
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(sizes, cpu_times, label='CPU (Secvențial)', color='#e74c3c', linewidth=2.5, marker='o', markersize=5)
ax.plot(sizes, gpu_times, label='GPU (Total)', color='#2ecc71', linewidth=2.5, marker='s', markersize=5)
ax.fill_between(sizes, cpu_times, gpu_times, where=(np.array(gpu_times) < np.array(cpu_times)), 
                interpolate=True, color='#2ecc71', alpha=0.1, label='Avantaj GPU')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Dimensiune Număr (Chunks)', fontsize=12, fontweight='bold')
ax.set_ylabel('Timp (Secunde) - Scară Log', fontsize=12, fontweight='bold')
ax.set_title('1. Performanță Generală: CPU vs GPU (Înmulțire)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, which="both", ls="-", alpha=0.3)
plt.tight_layout()
plt.show()

# --- FUNCȚIE PENTRU BARE ---
def plot_fancy_bar(size_idx, title_prefix):
    s = sizes[size_idx]
    c = cpu_times[size_idx]
    g = gpu_times[size_idx]
    speedup = c / g if g > 0 else 0
    
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(['CPU', 'GPU'], [c, g], color=['#c0392b', '#27ae60'], alpha=0.9, width=0.5)
    ax.set_title(f"{title_prefix}: {s} chunks", fontsize=13)
    ax.set_ylabel('Timp (s)', fontsize=11)
    
    max_h = max(c, g)
    ax.set_ylim(0, max_h * 1.3)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 1.02*h, f'{h:.5f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')

    txt = f"GPU {speedup:.1f}x mai rapid" if speedup > 1 else f"CPU {(1/speedup):.1f}x mai rapid"
    ax.text(0.5, max_h * 1.1, txt, ha='center', fontsize=11, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    plt.tight_layout()
    plt.show()

# --- GRAFICELE 2, 3, 4 ---
plot_fancy_bar(0, "2. Număr Mic")
plot_fancy_bar(len(sizes) // 2, "3. Număr Mediu")
plot_fancy_bar(-1, "4. Număr Masiv")

# --- GRAFIC 5: LATENCY VS THROUGHPUT (Stacked Bar Normalizat) ---
idx_small = 0
idx_large = -1

t_small = transfer_times[idx_small]
c_small = compute_times[idx_small]
t_large = transfer_times[idx_large]
c_large = compute_times[idx_large]

total_small = t_small + c_small
total_large = t_large + c_large

pct_t_small = (t_small / total_small) * 100
pct_c_small = (c_small / total_small) * 100

pct_t_large = (t_large / total_large) * 100
pct_c_large = (c_large / total_large) * 100

fig, ax = plt.subplots(figsize=(10, 8))
bar_width = 0.5
indices = [0, 1]

labels = [
    f'Număr Mic\n(Transfer Dominant)\nTimp Total: {total_small:.6f}s', 
    f'Număr Masiv\n(Calcul Dominant)\nTimp Total: {total_large:.4f}s'
]

transfer_pcts = [pct_t_small, pct_t_large]
compute_pcts = [pct_c_small, pct_c_large]

p1 = ax.bar(indices, transfer_pcts, bar_width, label='Transfer Date (PCIe)', color='#e74c3c', edgecolor='white', linewidth=1)
p2 = ax.bar(indices, compute_pcts, bar_width, bottom=transfer_pcts, label='Calcul Efectiv (Kernel)', color='#2ecc71', edgecolor='white', linewidth=1)

ax.set_ylabel('Distribuția Timpului (%)', fontsize=12, fontweight='bold')
ax.set_title('5. Anatomia Execuției: Unde se pierde timpul?', fontsize=14, pad=10)
ax.set_xticks(indices)
ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
ax.set_ylim(0, 100)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=12)

for i in range(2):
    if transfer_pcts[i] > 5:
        ax.text(i, transfer_pcts[i]/2, f"{transfer_pcts[i]:.1f}%", 
                ha='center', va='center', color='white', fontweight='bold', fontsize=12)
    
    if compute_pcts[i] > 5:
        ax.text(i, transfer_pcts[i] + compute_pcts[i]/2, f"{compute_pcts[i]:.1f}%", 
                ha='center', va='center', color='white', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.show()