# Large-Number-Reprezentation-System

## 1. Introducere

Aritmetica cu precizie arbitrară reprezintă o componentă esențială în domenii
precum criptografia, simulările numerice de înaltă precizie și calculul științific.
Operațiile pe numere foarte mari (peste 64 de biți) nu pot fi realizate eficient
folosind doar instrucțiunile standard ale procesorului, motiv pentru care sunt
necesare arhitecturi hardware dedicate.

Acest proiect propune implementarea operațiilor aritmetice fundamentale
(adunare, scădere și înmulțire) pentru numere mari, utilizând PyMTL – un
Hardware Construction Language bazat pe Python – pentru a simula comportamentul
unui accelerator FPGA, fără a necesita hardware fizic.

---

## 2. Obiectivul proiectului

Scopul proiectului este de a demonstra:
- cum pot fi implementate operații aritmetice cu precizie mare folosind o
  arhitectură hardware modulară;
- cum se pot verifica aceste operații prin testbench-uri dedicate;
- separarea clară dintre implementare hardware și verificare.

Proiectul este realizat exclusiv prin simulare și se concentrează pe corectitudine
funcțională, nu pe optimizare de performanță.

---

## 3. Cerința proiectului (formulată clar)

Se cere implementarea următoarelor componente:

### 3.1 Operații de bază pe chunk
- Adunare pe un chunk cu semnal de carry
- Scădere pe un chunk cu semnal de borrow
- Înmulțire pe un chunk

Un *chunk* reprezintă o porțiune fixă a unui număr mare (de exemplu 32 biți).

### 3.2 Operații pe numere mari
- Reprezentarea numerelor mari ca vectori de chunk-uri
- Implementarea adunării pe mai mulți chunk-uri
- Implementarea înmulțirii pe mai mulți chunk-uri folosind metoda schoolbook

Carry-ul și borrow-ul trebuie propagate corect între chunk-uri.

### 3.3 Verificare
- Crearea de testbench-uri pentru fiecare modul
- Testarea corectitudinii pentru:
  - cazuri normale
  - cazuri limită (overflow, valori maxime, zero)
- Compararea rezultatelor cu o implementare software de referință (Python)

---

## 4. Tehnologii utilizate

- **Python 3.10+**
- **PyMTL3** – Hardware Construction Language
- **pytest** – framework pentru testare automată

Nu este utilizat hardware FPGA real.

---

## 5. Structura proiectului

.
├── src/
│ └── bigint_modules.py
│ # Implementarea modulelor PyMTL:
│ # - ChunkAdder
│ # - ChunkSubtractor
│ # - ChunkMultiplier
│ # - BigIntAdder
│ # - BigIntMultiplier
│
├── testbench/
│ ├── test_chunk_adder.py
│ ├── test_chunk_subtractor.py
│ ├── test_chunk_multiplier.py
│ ├── test_bigint_add.py
│ └── test_bigint_mul.py
│
├── requirements.txt
└── README.md

yaml
Copy code

---

## 6. Descrierea implementării

### 6.1 Reprezentarea numerelor mari
Numerele mari sunt reprezentate ca liste de chunk-uri de dimensiune fixă.
Fiecare chunk este procesat de un modul hardware dedicat.

### 6.2 Module PyMTL
- **ChunkAdder** – adună două chunk-uri și un carry de intrare
- **ChunkSubtractor** – scade două chunk-uri cu borrow
- **ChunkMultiplier** – realizează produsul a două chunk-uri
- **BigIntAdder** – realizează adunarea pe mai mulți chunk-uri
- **BigIntMultiplier** – realizează înmulțirea schoolbook

Fiecare modul este descris folosind semantică hardware (semnale, actualizări
sincrone).

---

## 7. Verificare și testare

Pentru fiecare modul există un testbench dedicat care:
- instanțiază modulul PyMTL;
- aplică vectori de test;
- compară rezultatul cu o referință software Python.

Testele sunt complet automate și pot fi rulate folosind `pytest`.

---

## 8. Instalare

```bash
pip install pymtl3 pytest
9. Rulare teste
bash
Copy code
pytest testbench/
Toate testele trebuie să fie marcate ca PASSED pentru ca implementarea să
fie considerată corectă.

10. Ce demonstrează acest proiect
Utilizarea unui Hardware Construction Language (PyMTL)

Implementarea logicii hardware pentru aritmetică cu precizie mare

Propagarea corectă a carry-ului și borrow-ului

Separarea implementării de verificare (design vs. testbench)

Structurarea unui proiect HDL/HCL într-un repository GitHub

11. Limitări
Nu este utilizat un FPGA real

Nu sunt implementați algoritmi avansați (Karatsuba, FFT)

Accentul este pus pe corectitudine, nu pe performanță

12. Posibile extensii
Implementarea multiplicării Karatsuba

Suport pentru aritmetică modulară (Montgomery)

Generarea de cod HDL (Verilog) din PyMTL

Analiză de performanță și resurse

13. Concluzie
Acest proiect oferă o implementare clară, modulară și verificată a aritmeticii
cu precizie arbitrară folosind PyMTL. Structura și documentația sunt concepute
pentru a respecta cerințele academice ale fazei de implementare HDL/HCL