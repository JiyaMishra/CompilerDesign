import sys

from parser import parser
from semantic import SemanticAnalyzer
from ir import IRGenerator
from codegen import CodeGenerator
from executor import Executor


def compile_bioscript(filename):

    

    with open(filename, "r") as file:
        source = file.read()

    print("\n========== BIOSCRIPT COMPILER ==========\n")

    

    print("Parsing...")

    ast = parser.parse(source)

    print("Parsing completed.")

   

    print("\nSemantic Analysis...")

    analyzer = SemanticAnalyzer()

    symbol_table = analyzer.analyze(ast)

    print("Semantic Analysis completed.")

    symbol_table.display()

    

    print("\nGenerating Intermediate Representation...")

    ir = IRGenerator()

    ir.generate(ast)

    ir.display()

 

    print("\nGenerating Python code...")

    generator = CodeGenerator()

    generator.generate(ast)

    generator.save()

    print("Python code generated.")

   

    executor = Executor()

    executor.execute()


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage:")

        print("python main.py examples/sample.bio")

        sys.exit(1)

    compile_bioscript(sys.argv[1])