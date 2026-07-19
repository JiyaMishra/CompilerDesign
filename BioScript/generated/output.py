import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runtime.bioscript_runtime import *

dna = load_fasta("examples/gene.fasta")
rna = transcribe(dna)
protein = translate(dna)
gcvalue = gc_content(dna)
print("dna =", dna)
print("protein =", protein)
print("gcvalue =", gcvalue)