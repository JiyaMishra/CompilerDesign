import os


class CodeGenerator:
    def __init__(self):
        self.lines = []

    # -----------------------------------------
    # Generate Python Code from AST
    # -----------------------------------------
    def generate(self, ast):

        self.lines = []

        # Runtime import
        self.lines.append("import sys")
        self.lines.append("import os")
        self.lines.append("")
        self.lines.append("sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))")
        self.lines.append("")
        self.lines.append("from runtime.bioscript_runtime import *")
        self.lines.append("")
       

        for node in ast:
            method_name = f"visit_{node.type}"

            if hasattr(self, method_name):
                getattr(self, method_name)(node)
            else:
                raise Exception(f"No code generator for node '{node.type}'")

        return "\n".join(self.lines)

    # -----------------------------------------
    # sequence dna = "ATGC"
    # -----------------------------------------
    def visit_sequence(self, node):
        self.lines.append(
            f'{node.name} = create_sequence("{node.value}")'
        )

    # -----------------------------------------
    # transcribe dna -> rna
    # -----------------------------------------
    def visit_transcribe(self, node):
        self.lines.append(
            f"{node.target} = transcribe({node.source})"
        )

    # -----------------------------------------
    # translate dna -> protein
    # -----------------------------------------
    def visit_translate(self, node):
        self.lines.append(
            f"{node.target} = translate({node.source})"
        )

    # -----------------------------------------
    # reverse dna -> rev
    # -----------------------------------------
    def visit_reverse(self, node):
        self.lines.append(
            f"{node.target} = reverse({node.source})"
        )

    # -----------------------------------------
    # complement dna -> comp
    # -----------------------------------------
    def visit_complement(self, node):
        self.lines.append(
            f"{node.target} = complement({node.source})"
        )

    # -----------------------------------------
    # gc dna -> gcvalue
    # -----------------------------------------
    def visit_gc(self, node):
        self.lines.append(
            f"{node.target} = gc_content({node.source})"
        )
    def visit_load(self, node):

      self.lines.append(
        f'{node.target} = load_fasta("{node.filename}")'
    )
    # -----------------------------------------
    # print variable
    # -----------------------------------------
    def visit_print(self, node):
        self.lines.append(
            f'print("{node.value} =", {node.value})'
        )

    # -----------------------------------------
    # Save generated Python
    # -----------------------------------------
    def save(self, filename="output.py"):

     generated_folder = os.path.join(
        os.path.dirname(__file__),
        "generated"
    )

     os.makedirs(generated_folder, exist_ok=True)

     filepath = os.path.join(
        generated_folder,
        filename
    )

     code = "\n".join(self.lines)

     with open(filepath, "w", encoding="utf-8") as file:
        file.write(code)

     print(f"\nGenerated file saved to:\n{filepath}")
    


# ------------------------------------------------
# Testing
# ------------------------------------------------

if __name__ == "__main__":

    from parser import parser
    from semantic import SemanticAnalyzer

    code = """
    sequence dna = "ATGCGTACC"

    transcribe dna -> rna

    translate dna -> protein

    reverse dna -> rev

    complement dna -> comp

    gc dna -> gcvalue

    print dna

    print rna

    print protein

    print rev

    print comp

    print gcvalue
    """

    # Parse
    ast = parser.parse(code)

    # Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # Code Generation
    generator = CodeGenerator()

    generated_code = generator.generate(ast)

    print("\n========== GENERATED PYTHON ==========\n")
    print(generated_code)

    # Save generated file
    generator.save()