import os 
from symbol_table import SymbolTable


class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = SymbolTable()

    # -----------------------------
    # Analyze Entire AST
    # -----------------------------
    def analyze(self, ast):

        for node in ast:

            method_name = f"visit_{node.type}"

            method = getattr(self, method_name, self.generic_visit)

            method(node)

        return self.symbol_table

    # -----------------------------
    # Default Visitor
    # -----------------------------
    def generic_visit(self, node):
        raise Exception(f"No semantic rule for {node.type}")

    # -----------------------------
    # sequence dna = "ATGC"
    # -----------------------------
    def visit_sequence(self, node):

        dna = node.value.upper()

        for base in dna:

            if base not in "ATGC":
                raise Exception(
                    f"Invalid DNA sequence '{dna}'. "
                    "Only A, T, G and C are allowed."
                )

        self.symbol_table.insert(
            node.name,
            "sequence",
            dna
        )

    # -----------------------------
    # transcribe dna -> rna
    # -----------------------------
    def visit_transcribe(self, node):

        if not self.symbol_table.exists(node.source):
            raise Exception(
                f"Variable '{node.source}' not declared."
            )

        self.symbol_table.insert(
            node.target,
            "sequence"
        )

    # -----------------------------
    # translate dna -> protein
    # -----------------------------
    def visit_translate(self, node):

        if not self.symbol_table.exists(node.source):
            raise Exception(
                f"Variable '{node.source}' not declared."
            )

        self.symbol_table.insert(
            node.target,
            "protein"
        )

    # -----------------------------
    # reverse dna -> rev
    # -----------------------------
    def visit_reverse(self, node):

        if not self.symbol_table.exists(node.source):
            raise Exception(
                f"Variable '{node.source}' not declared."
            )

        self.symbol_table.insert(
            node.target,
            "sequence"
        )

    # -----------------------------
    # complement dna -> comp
    # -----------------------------
    def visit_complement(self, node):

        if not self.symbol_table.exists(node.source):
            raise Exception(
                f"Variable '{node.source}' not declared."
            )

        self.symbol_table.insert(
            node.target,
            "sequence"
        )

    # -----------------------------
    # gc dna -> gcvalue
    # -----------------------------
    def visit_gc(self, node):

        if not self.symbol_table.exists(node.source):
            raise Exception(
                f"Variable '{node.source}' not declared."
            )

        self.symbol_table.insert(
            node.target,
            "float"
        )

    # -----------------------------
    # print dna
    # -----------------------------
    def visit_print(self, node):

        if not self.symbol_table.exists(node.value):
            raise Exception(
                f"Variable '{node.value}' not declared."
            )
    def visit_load(self, node):

      if not os.path.exists(node.filename):
        raise Exception(
            f"FASTA file '{node.filename}' not found."
        )

      self.symbol_table.insert(
        node.target,
        "sequence"
    )
if __name__ == "__main__":

    from parser import parser

    code = """

    sequence dna = "ATGCGTA"

    transcribe dna -> rna

    translate dna -> protein

    reverse dna -> rev

    complement dna -> comp

    gc dna -> gcvalue

    print protein

    """

    ast = parser.parse(code)

    analyzer = SemanticAnalyzer()

    symbol_table = analyzer.analyze(ast)

    symbol_table.display()