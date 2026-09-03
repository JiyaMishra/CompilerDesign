from Bio.Seq import Seq
from Bio import SeqIO



def create_sequence(sequence):

    return Seq(sequence)



def transcribe(sequence):

    return sequence.transcribe()



def translate(sequence):

    trimmed = sequence[:len(sequence) - (len(sequence) % 3)]
    return trimmed.translate()



def reverse(sequence):

    return sequence[::-1]



def complement(sequence):

    return sequence.complement()



def reverse_complement(sequence):

    return sequence.reverse_complement()



def gc_content(sequence):

    sequence = str(sequence)

    if len(sequence) == 0:
        return 0.0

    gc = sequence.count("G") + sequence.count("C")

    return round(gc * 100 / len(sequence), 2)

def load_fasta(filename):

    record = SeqIO.read(filename, "fasta")

    return record.seq
if __name__ == "__main__":

    dna = create_sequence("ATGCGTACC")

    print("DNA :", dna)

    print("RNA :", transcribe(dna))

    print("Protein :", translate(dna))

    print("Reverse :", reverse(dna))

    print("Complement :", complement(dna))

    print("Reverse Complement :", reverse_complement(dna))

    print("GC Content :", gc_content(dna), "%")