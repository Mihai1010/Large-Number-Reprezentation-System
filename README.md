# Large-Number-Reprezentation-System

1. Filosofia Proiectului: "Divide et Impera"
Computerele moderne sunt limitate de dimensiunea registrelor hardware (de obicei 32 sau 64 de biți). Când vrem să calculăm valori astronomice sau chei criptografice, aceste registre devin neîncăpătoare.Soluția adoptată în acest proiect este segmentarea (chunking):Nu privim un număr ca pe o singură entitate, ci ca pe un lanț de segmente de câte 32 de biți.Fiecare segment este tratat ca o cifră într-o bază mult mai mare ($2^{32}$).Logica de calcul este transpusă de la nivel elementar (biți) la nivel de blocuri (chunks).

2. Strategia Hardware (Modelare PyMTL3)
În design-ul de hardware, am construit ierarhia de jos în sus, imitând modul în care un procesor modular este asamblat într-un mediu real (FPGA/ASIC).

A. Elementele de Bază (Atomii)
În loc să construim un sistem monolitic, am creat unități mici și specializate: ChunkAdder și ChunkMultiplier. Acestea sunt „muncitorii” care execută operația doar pe „felia” lor de date, fără să vadă imaginea de ansamblu.

B. Scalabilitatea prin Agregare (BigIntALU)
Pentru a obține rezultatul final, am implementat o structură ierarhică unde componentele comunică între ele:

Adunarea: Se face prin alinierea segmentelor. Fiecare segment își primește datele și calculează suma locală.

Înmulțirea: Folosește o abordare de tip "produs cartezian". Fiecare segment din primul număr este înmulțit cu fiecare segment din al doilea număr, iar rezultatele sunt redistribuite în funcție de ponderea lor pozițională.

3. Validarea Design-ului (Strategia de Testare)
Hardware-ul nu permite erori de logică fără costuri mari. Prin urmare, am implementat o suită de teste unitare care simulează comportamentul fizic:

Simularea Ciclului de Viață: Testele nu verifică doar o funcție, ci „elaborează” circuitul, îi aplică un grup de reguli de simulare și îi dau un semnal de „reset”, exact ca la pornirea unui procesor real.

Verificarea prin Hexadecimal: Folosim reprezentarea HEX pentru a vizualiza clar cum se comportă fiecare „chunk” de 32 de biți în interiorul unui număr mare.

Integritatea Datelor: Testele confirmă că atunci când adunăm două structuri complexe de segmente, rezultatul se păstrează corect aliniat, asigurând că logica de „leagătură” dintre componentele hardware funcționează.

4. Strategia Software și Paralelizarea (CUDA/GPU)
Când mutăm problema pe GPU, filosofia se schimbă de la "ierarhie de componente" la "paralelism masiv".

Conceptul de "Little Endian" în Memorie
Pentru a facilita calculele, numerele sunt stocate cu segmentul cel mai puțin semnificativ la început (index 0). Aceasta este o decizie strategică: ne permite să propagăm transportul (carry) de la stânga la dreapta într-un mod natural pentru procesarea digitală.

JIT Compilation (Just-In-Time)
Folosind Numba, codul Python este tradus direct în instrucțiuni mașină pentru placa video (PTX). Aceasta oferă un echilibru între flexibilitatea scrierii codului în Python și viteza brută a unui procesor NVIDIA.

5. Provocări Tehnice Rezolvate
Puntea Software-Hardware: Am creat un sistem de „packing/unpacking” (conversie chunks <-> întregi). Acesta funcționează ca un translator între lumea flexibilă a Python-ului (care poate gestiona orice număr) și lumea rigidă a hardware-ului (unde totul trebuie să aibă o dimensiune fixă de biți).

Gestiunea Overflow-ului: Am prevăzut arhitectura astfel încât rezultatele intermediare ale înmulțirii să aibă spațiu dublu (64 de biți), prevenind pierderea de informație înainte de agregarea finală.
