class IRInstruction:

    def __init__(self, opcode, arg1=None, arg2=None, result=None):
        self.opcode = opcode
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        return (
            f"{self.opcode:15}"
            f"{str(self.arg1):15}"
            f"{str(self.arg2):15}"
            f"{str(self.result)}"
        )


class IRGenerator:

    def __init__(self):
        self.instructions = []

    def generate(self, ast):

        self.instructions = []

        for node in ast:

            method = getattr(self, f"visit_{node.type}")

            method(node)

        return self.instructions

    def visit_sequence(self, node):

        self.instructions.append(
            IRInstruction(
                "DECLARE",
                node.value,
                None,
                node.name
            )
        )

    def visit_transcribe(self, node):

        self.instructions.append(
            IRInstruction(
                "TRANSCRIBE",
                node.source,
                None,
                node.target
            )
        )

    def visit_translate(self, node):

        self.instructions.append(
            IRInstruction(
                "TRANSLATE",
                node.source,
                None,
                node.target
            )
        )

    def visit_reverse(self, node):

        self.instructions.append(
            IRInstruction(
                "REVERSE",
                node.source,
                None,
                node.target
            )
        )

    def visit_complement(self, node):

        self.instructions.append(
            IRInstruction(
                "COMPLEMENT",
                node.source,
                None,
                node.target
            )
        )

    def visit_gc(self, node):

        self.instructions.append(
            IRInstruction(
                "GC",
                node.source,
                None,
                node.target
            )
        )
    def visit_load(self, node):

     self.instructions.append(
        IRInstruction(
            "LOAD_FASTA",
            node.filename,
            None,
            node.target
        )
    )


    def visit_print(self, node):

        self.instructions.append(
            IRInstruction(
                "PRINT",
                node.value
            )
        )

    def display(self):

        print("\n========== INTERMEDIATE CODE ==========\n")

        print(f"{'OPCODE':15}{'ARG1':15}{'ARG2':15}RESULT")

        print("-" * 60)

        for instruction in self.instructions:
            print(instruction)
if __name__ == "__main__":

    from parser import parser

    code = """

    sequence dna = "ATGCGTACC"

    transcribe dna -> rna

    translate dna -> protein

    print protein

    """

    ast = parser.parse(code)

    ir = IRGenerator()

    ir.generate(ast)

    ir.display()