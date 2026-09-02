import sys
from runtime.bioscript_runtime import *

dna = load_fasta("examples/gene.fasta")
rna = transcribe(dna)
protein = translate(dna)
rev = reverse(dna)
comp = complement(dna)
gcvalue = gc_content(dna)

print("rna =", rna)
print("protein =", protein)
print("rev =", rev)
print("comp =", comp)
print("gcvalue =", gcvalue)