import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runtime.bioscript_runtime import *

dna = create_sequence("ATGCGTACC")
rna = transcribe(dna)
protein = translate(dna)
rev = reverse(dna)
comp = complement(dna)
gcvalue = gc_content(dna)
print("dna =", dna)
print("rna =", rna)
print("protein =", protein)
print("rev =", rev)
print("comp =", comp)
print("gcvalue =", gcvalue)