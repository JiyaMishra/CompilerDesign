import os


class CodeGenerator:
    def __init__(self):
        self.lines = []

    
    def generate(self, ast):

        self.lines = []

        
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

   
    def visit_sequence(self, node):
        self.lines.append(
            f'{node.name} = create_sequence("{node.value}")'
        )

    
    def visit_transcribe(self, node):
        self.lines.append(
            f"{node.target} = transcribe({node.source})"
        )

  
    def visit_translate(self, node):
        self.lines.append(
            f"{node.target} = translate({node.source})"
        )

    
    def visit_reverse(self, node):
        self.lines.append(
            f"{node.target} = reverse({node.source})"
        )

    
    def visit_complement(self, node):
        self.lines.append(
            f"{node.target} = complement({node.source})"
        )

    
    def visit_gc(self, node):
        self.lines.append(
            f"{node.target} = gc_content({node.source})"
        )
    def visit_load(self, node):

      self.lines.append(
        f'{node.target} = load_fasta("{node.filename}")'
    )
    
    def visit_print(self, node):
        self.lines.append(
            f'print("{node.value} =", {node.value})'
        )

 
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
    




if __name__ == "__main__":

    from parser import parser
    from semantic import SemanticAnalyzer

    code = """
    load "examples/gene.fasta" -> dna
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

    
    ast = parser.parse(code)

    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    
    generator = CodeGenerator()

    generated_code = generator.generate(ast)

    print("\n========== GENERATED PYTHON ==========\n")
    print(generated_code)

    
    generator.save()