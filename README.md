# BioScript

**A tiny language for genomics, and a real compiler underneath it.**

BioScript is a domain-specific language (DSL) that lets you describe genomic sequence operations — transcription, translation, GC content, reverse complements, FASTA loading — in a handful of plain-English-ish commands, instead of hand-writing Biopython boilerplate every time. Under the hood, BioScript is not an interpreter or a thin wrapper: it's a genuine multi-phase compiler. Source code goes through lexing, parsing, AST construction, semantic analysis, symbol table management, an intermediate representation, and finally Python code generation — the same pipeline shape you'd find in a "real" compiler class, just aimed at biology instead of machine code.

If you've ever wanted to see what a compiler actually does between "I wrote some code" and "the computer ran it," this project is a good place to look. Every phase is its own file, every phase has a single job, and you can watch a BioScript program get transformed step by step, all the way down to the generated Python that Biopython actually executes.

---

## Why this exists

Most bioinformatics scripting looks like this:

```python
from Bio.Seq import Seq
dna = Seq("ATGCGTACC")
rna = dna.transcribe()
protein = dna.translate()
```

That's fine once — but it's also five lines of setup for what is conceptually a one-line thought: "transcribe this, then translate it." BioScript lets you write the thought directly:

```bioscript
sequence dna = "ATGCGTACC"
transcribe dna -> rna
translate dna -> protein
print protein
```

The compiler takes care of turning that into correct, runnable Python with the appropriate Biopython calls. The point isn't that Biopython is hard to use — it's showing that a small, well-scoped DSL plus a real compiler pipeline can make a specialized domain feel like a first-class language.

---

## What it actually does, end to end

At a high level, a `.bio` file goes on a journey:

```
BioScript source code
        ↓
   tokens (Lexer)
        ↓
  parse tree → AST (Parser)
        ↓
  validated AST (Semantic Analysis)
        ↓
  populated Symbol Table
        ↓
  Intermediate Representation (IR)
        ↓
  generated Python code (Code Generator)
        ↓
  generated/output.py
        ↓
  executed by the Runtime (Biopython underneath)
        ↓
  your actual biological results, printed to the terminal
```

A full black-and-white version of this pipeline is included further down and as a standalone SVG in this repo (`flowchart.svg`) so you can drop it straight into slides, docs, or the repo wiki.

---

## Technology stack

- **Python 3** — the whole compiler is written in Python
- **PLY (Python Lex-Yacc)** — handles lexing and parsing, the classic way
- **Biopython** — the actual biological engine that the generated code calls into
- **Plain OOP** — AST nodes, IR instructions, and symbol table entries are all simple Python objects, deliberately kept unfancy so the compiler logic stays readable

No external services, no heavyweight frameworks — the goal was to keep every phase inspectable.

---

## Project layout

```
BioScript/
├── examples/
│   ├── sample.bio          # a basic example program
│   ├── fasta.bio           # example using FASTA loading
│   └── gene.fasta          # sample FASTA input
│
├── generated/
│   └── output.py           # the Python code the compiler produces
│
├── runtime/
│   └── bioscript_runtime.py  # the actual Biopython-backed implementations
│
├── lexer.py                # Phase 1: tokenizing
├── parser.py                # Phase 2: grammar + AST construction
├── semantic.py               # Phase 3: validation
├── symbol_table.py            # tracks every declared variable
├── ir.py                       # Phase 4: intermediate representation
├── codegen.py                    # Phase 5: Python code generation
├── executor.py                     # runs the generated program
├── main.py                          # orchestrates the whole pipeline
│
├── requirements.txt
└── README.md
```

Each compiler phase lives in its own file on purpose. If you want to understand parsing, you open `parser.py` and nothing else is competing for your attention.

---
<img width="268" height="769" alt="Screenshot 2026-07-19 at 3 28 56 PM" src="https://github.com/user-attachments/assets/7370650e-8e3b-400d-bd02-0e5e50353609" />



## Walking through each compiler phase

### 1. The Lexer (`lexer.py`)

Built with PLY's Lex module. Its only job is to turn a stream of raw characters into a stream of meaningful tokens — it doesn't know or care about grammar, just "what is this chunk of text."

It recognizes keywords like:

```
sequence   load   transcribe   translate
reverse    complement   gc   print
```

along with identifiers, string literals, and the `->` and `=` operators. Whitespace is discarded, and characters that don't belong to the language are flagged immediately rather than silently ignored.

**Example**

Input:
```bioscript
sequence dna = "ATGC"
```

Tokens produced:
```
SEQUENCE
IDENTIFIER
ASSIGN
STRING
```

### 2. The Parser (`parser.py`)

Built with PLY's Yacc module. The parser takes the token stream from the lexer and checks it against BioScript's grammar rules, building an **Abstract Syntax Tree (AST)** as it goes. This is where "is this even valid BioScript?" gets answered structurally.

Supported statement shapes:

```bioscript
sequence dna = "ATGC"
load "gene.fasta" -> dna
transcribe dna -> rna
translate dna -> protein
reverse dna -> rev
complement dna -> comp
gc dna -> gcvalue
print protein
```

Every one of these becomes an AST node, for example:

```
Node(
    type   = "translate",
    source = "dna",
    target = "protein"
)
```

### 3. The AST

The AST is the tree-shaped intermediate picture of your program before any validation happens. A declaration like:

```bioscript
sequence dna = "ATGC"
```

becomes:

```
sequence
 ├── name  = dna
 └── value = ATGC
```

It's the structural backbone every later phase reads from.

### 4. Semantic Analysis (`semantic.py`)

This is where the compiler stops asking "is this grammatically valid?" and starts asking "does this actually make sense?" It:

- Confirms every variable is declared before it's used
- Rejects references to undefined variables
- Verifies that any FASTA file being loaded actually exists on disk
- Populates the symbol table as it walks the AST

**Example of what gets caught:**

```bioscript
translate xyz -> protein
```

```
Compiler error: Undefined variable 'xyz'
```

### 5. The Symbol Table (`symbol_table.py`)

Every declared variable gets an entry recording its name, data type, simulated byte size, a simulated memory address, and its current value — deliberately mirroring the kind of bookkeeping a "real" compiler does for memory layout, even though BioScript ultimately targets Python rather than machine code.

| Variable | Datatype | Bytes | Address | Value       |
|----------|----------|-------|---------|-------------|
| dna      | sequence | 8     | 1000    | ATGCGTACC   |
| rna      | sequence | 8     | 1008    | None        |
| protein  | protein  | 8     | 1016    | None        |

The table gets printed out during compilation, so you can watch it fill in as the program is analyzed.

### 6. Intermediate Representation (`ir.py`)

Once semantic analysis passes, the AST is lowered into a flat, linear IR — a sequence of simple instructions rather than a tree. This is the phase that makes BioScript feel like a genuine compiler rather than a template engine: code generation never touches the AST directly, only the IR.

Each instruction has a shape:

```
IRInstruction(opcode, arg1, arg2, result)
```

For the earlier example, the IR looks like:

```
OPCODE         ARG1          ARG2        RESULT
DECLARE        ATGCGTACC     None        dna
TRANSCRIBE     dna           None        rna
TRANSLATE      dna           None        protein
GC             dna           None        gcvalue
PRINT          protein
```

### 7. Code Generation (`codegen.py`)

The IR gets walked one instruction at a time and turned into real, executable Python. For example:

BioScript:
```bioscript
translate dna -> protein
```

Generated Python:
```python
protein = translate(dna)
```

The output is written straight to `generated/output.py`, so you can open it and read exactly what your BioScript program compiled down to.

### 8. The Runtime (`runtime/bioscript_runtime.py`)

This is the only place Biopython actually gets called. Keeping it isolated means the compiler phases stay biology-agnostic — they just emit calls to functions like `transcribe()` or `gc_content()`, and this file is what makes those calls real:

```
create_sequence()
load_fasta()
transcribe()
translate()
reverse()
complement()
reverse_complement()
gc_content()
```

### 9. The Executor (`executor.py`)

Takes the generated `output.py`, runs it through the Python interpreter, and captures whatever it prints — the actual transcribed RNA, translated protein, GC percentage, whatever the program computed.

### 10. `main.py` — the conductor

This file ties every phase together in order: read source → parse → semantic check → build symbol table → generate IR → generate code → write `output.py` → execute it. It's the single entry point you actually run.

---

## Language features, at a glance

| Feature | Syntax | What it does |
|---|---|---|
| Sequence declaration | `sequence dna = "ATGC"` | Defines a new sequence variable |
| FASTA loading | `load "gene.fasta" -> dna` | Reads a sequence in from a FASTA file via Biopython |
| Transcription | `transcribe dna -> rna` | DNA → RNA |
| Translation | `translate dna -> protein` | DNA → protein |
| Reverse | `reverse dna -> rev` | Reverses the sequence |
| Complement | `complement dna -> comp` | Base-pair complement |
| Reverse complement | (runtime-level) | Reverse + complement combined |
| GC content | `gc dna -> gcvalue` | Calculates GC percentage |
| Print | `print protein` | Outputs a variable's value |

---

## FASTA support

BioScript can pull sequences straight from a FASTA file rather than making you paste raw strings into your source code.

Sample FASTA:
```
>Example_Gene
ATGCGTACCGGTAACTGATCGATCGATCG
```

BioScript:
```bioscript
load "examples/gene.fasta" -> dna
```

Compiles to:
```python
dna = load_fasta("examples/gene.fasta")
```

---

## A full run, start to finish

**Input (`examples/gene.bio`):**
```bioscript
load "examples/gene.fasta" -> dna
transcribe dna -> rna
translate dna -> protein
gc dna -> gcvalue
print protein
```

**What the compiler generates (`generated/output.py`):**
```python
dna = load_fasta("examples/gene.fasta")
rna = transcribe(dna)
protein = translate(dna)
gcvalue = gc_content(dna)
print(protein)
```

**What you see when it runs:**
```
dna = ...
protein = ...
gcvalue = ...
```

Every stage of that transformation — tokens, AST, symbol table, IR — is inspectable along the way if you want to see the intermediate steps rather than just the final output.

---

## Design decisions worth knowing about

- **Source-to-source, not source-to-machine-code.** BioScript compiles to Python rather than bytecode or assembly, because the goal was to demonstrate compiler *architecture*, not build a production interpreter from scratch.
- **Biopython does the biology.** The compiler never reimplements transcription or translation logic itself — it generates calls into a well-tested runtime library instead, which keeps the compiler's job purely about language processing.
- **Every phase is isolated.** Lexing doesn't know about semantics, semantics doesn't know about code generation, and so on. This makes each file individually readable and testable.
- **An IR layer exists on purpose**, even though a simpler compiler could skip straight from AST to Python. Having it in between is what makes this feel like an actual compiler pipeline rather than a template substitution script.
- **The symbol table tracks simulated memory details** (byte size, address) even though none of that maps to anything real in the Python output — it's there to mirror how compilers for real, low-level languages manage identifiers.

---

## What's already working

- A complete custom DSL for genomic sequence analysis
- A full compiler pipeline: lexer → parser → AST → semantic analysis → symbol table → IR → codegen
- Semantic validation with clear error messages
- FASTA file loading
- DNA/RNA/protein sequence operations
- GC content analysis
- A clean, modular structure that's easy to extend

## Where it could go next

- Control flow: `if` / `else`, `foreach`, `while`
- User-defined functions
- Batch processing of multi-sequence FASTA files
- Sequence alignment and motif searching
- Restriction enzyme analysis
- Optimization passes over the IR
- AST visualization tooling
- Better diagnostics — line numbers and column positions in error messages
- Support for more bioinformatics formats: FASTQ, GenBank

---

## Getting started

```bash
git clone <your-repo-url>
cd BioScript
pip install -r requirements.txt
python main.py examples/sample.bio
```

The generated Python will land in `generated/output.py`, and the executor will run it and print your results straight to the terminal.

---

## Closing thought

BioScript is small on purpose. It's not trying to be a production bioinformatics platform — it's trying to show, clearly and completely, what happens between "a person writes a line of code" and "a computer does the thing." Biology just happened to be an interesting domain to point a compiler at.
