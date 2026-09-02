"""
BioScript Visualization

Standalone visualization tool for the existing BioScript compiler.

This file DOES NOT modify the existing compiler pipeline.
It reads the same .bio source file and uses the existing:
    parser.py
    semantic.py
    symbol_table.py
    ir.py

It generates:
    visuals/ast.png
    visuals/symbol_table.png
    visuals/ir_flow.png
    visuals/pipeline_overview.png

Usage:
    python visualizer.py examples/sample.bio
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import networkx as nx

from parser import parser
from semantic import SemanticAnalyzer
from ir import IRGenerator


# --------------------------------------------------
# Output directory
# --------------------------------------------------

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "visuals"
)


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_figure(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)

    fig.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)

    print(f"Created: {path}")


# --------------------------------------------------
# AST Visualization
# --------------------------------------------------

def render_ast(ast):

    graph = nx.DiGraph()

    root = "program"

    graph.add_node(
        root,
        label="PROGRAM",
        kind="root"
    )

    for index, node in enumerate(ast, start=1):

        statement_id = f"statement_{index}"

        graph.add_node(
            statement_id,
            label=node.type.upper(),
            kind="statement"
        )

        graph.add_edge(
            root,
            statement_id
        )

        # Every Node stores its data directly
        # inside __dict__.
        for attr_index, (key, value) in enumerate(
            node.__dict__.items(),
            start=1
        ):

            if key == "type":
                continue

            attribute_id = (
                f"statement_{index}_{attr_index}"
            )

            value_text = str(value)

            if len(value_text) > 35:
                value_text = (
                    value_text[:32] + "..."
                )

            graph.add_node(
                attribute_id,
                label=f"{key} = {value_text}",
                kind="attribute"
            )

            graph.add_edge(
                statement_id,
                attribute_id
            )

    # --------------------------------------------------
    # Position nodes manually.
    #
    # This is intentional because the project's AST
    # is a flat list of Node objects rather than a
    # recursive tree.
    # --------------------------------------------------

    pos = {
        root: (0, 0)
    }

    statement_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data["kind"] == "statement"
    ]

    attribute_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data["kind"] == "attribute"
    ]

    spacing = max(
        2.5,
        len(statement_nodes) * 0.45
    )

    for i, statement_id in enumerate(
        statement_nodes
    ):

        y = -i * spacing

        pos[statement_id] = (
            -1.8,
            y
        )

        children = list(
            graph.successors(statement_id)
        )

        for j, child_id in enumerate(children):

            child_y = (
                y
                - (
                    j
                    - (len(children) - 1) / 2
                ) * 0.75
            )

            pos[child_id] = (
                2.2,
                child_y
            )

    # Safety fallback
    for node in attribute_nodes:

        if node not in pos:

            pos[node] = (
                2.2,
                -len(pos)
            )

    fig_height = max(
        5.5,
        len(ast) * 1.7
    )

    fig, ax = plt.subplots(
        figsize=(13, fig_height)
    )

    ax.axis("off")

    root_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data["kind"] == "root"
    ]

    statement_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data["kind"] == "statement"
    ]

    attribute_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data["kind"] == "attribute"
    ]

    # Edges
    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        arrows=True,
        arrowsize=16,
        width=1.2,
        node_size=0
    )

    # Program node
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=root_nodes,
        node_size=2600,
        node_shape="o",
        node_color="lightgray",
        ax=ax
    )

    # Statement nodes
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=statement_nodes,
        node_size=3000,
        node_shape="s",
        node_color="lightblue",
        ax=ax
    )

    # Attribute nodes
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=attribute_nodes,
        node_size=2500,
        node_shape="o",
        node_color="lightyellow",
        ax=ax
    )

    labels = nx.get_node_attributes(
        graph,
        "label"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=labels,
        font_size=9,
        ax=ax
    )

    ax.set_title(
        "BioScript AST Visualization",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    save_figure(
        fig,
        "ast.png"
    )


# --------------------------------------------------
# Symbol Table Visualization
# --------------------------------------------------

def render_symbol_table(symbol_table):

    rows = []

    for name, info in symbol_table.table.items():

        rows.append([
            name,
            info.get("datatype", ""),
            info.get("bytes", ""),
            info.get("address", ""),
            info.get("value", "")
        ])

    if not rows:

        rows = [
            ["(empty)", "", "", "", ""]
        ]

    fig, ax = plt.subplots(
        figsize=(
            12,
            1 + max(
                2.5,
                len(rows) * 0.65
            )
        )
    )

    ax.axis("off")

    columns = [
        "Variable",
        "Datatype",
        "Bytes",
        "Address",
        "Value"
    ]

    table = ax.table(
        cellText=rows,
        colLabels=columns,
        loc="center",
        cellLoc="center",
        colLoc="center",
        colWidths=[
            0.18,
            0.18,
            0.12,
            0.18,
            0.34
        ]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    for cell in table.get_celld().values():

        cell.set_edgecolor("gray")

    ax.set_title(
        "BioScript Symbol Table",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    save_figure(
        fig,
        "symbol_table.png"
    )


# --------------------------------------------------
# IR Visualization
# --------------------------------------------------

def render_ir(instructions):

    fig, ax = plt.subplots(
        figsize=(
            12,
            max(
                5.5,
                len(instructions) * 1.15
            )
        )
    )

    ax.axis("off")

    if not instructions:

        ax.text(
            0.5,
            0.5,
            "No IR instructions",
            ha="center",
            va="center",
            fontsize=14
        )

        ax.set_title(
            "BioScript IR Flow",
            fontsize=16,
            fontweight="bold"
        )

        save_figure(
            fig,
            "ir_flow.png"
        )

        return

    x = 0.5
    top = 0.93

    step = min(
        0.16,
        0.82 / max(
            1,
            len(instructions) - 1
        )
    )

    for index, instruction in enumerate(
        instructions,
        start=1
    ):

        y = (
            top
            - (index - 1) * step
        )

        arg1 = (
            "-"
            if instruction.arg1 is None
            else str(instruction.arg1)
        )

        arg2 = (
            "-"
            if instruction.arg2 is None
            else str(instruction.arg2)
        )

        result = (
            "-"
            if instruction.result is None
            else str(instruction.result)
        )

        label = (
            f"{index}. {instruction.opcode}\n"
            f"ARG1: {arg1}    "
            f"ARG2: {arg2}    "
            f"RESULT: {result}"
        )

        box = FancyBboxPatch(
            (0.08, y - 0.045),
            0.84,
            0.09,
            boxstyle="round,pad=0.012",
            linewidth=1.2,
            edgecolor="gray",
            facecolor="whitesmoke",
            transform=ax.transAxes
        )

        ax.add_patch(box)

        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=9,
            transform=ax.transAxes
        )

        # Arrow to next instruction
        if index < len(instructions):

            next_y = (
                top
                - index * step
            )

            ax.annotate(
                "",
                xy=(
                    x,
                    next_y + 0.055
                ),
                xytext=(
                    x,
                    y - 0.055
                ),
                xycoords=ax.transAxes,
                textcoords=ax.transAxes,
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=1.2
                )
            )

    ax.set_title(
        "BioScript Intermediate Representation (IR) Flow",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    save_figure(
        fig,
        "ir_flow.png"
    )


# --------------------------------------------------
# Pipeline Visualization
# --------------------------------------------------

def render_pipeline():

    stages = [
        "SOURCE CODE",
        "LEXER",
        "PARSER / AST",
        "SEMANTIC ANALYSIS",
        "IR GENERATION",
        "CODE GENERATION",
        "EXECUTION"
    ]

    fig, ax = plt.subplots(
        figsize=(13, 3.5)
    )

    ax.axis("off")

    left = 0.03
    width = 0.115
    gap = 0.025
    y = 0.42

    for i, stage in enumerate(stages):

        x = (
            left
            + i * (width + gap)
        )

        box = FancyBboxPatch(
            (x, y),
            width,
            0.18,
            boxstyle="round,pad=0.012",
            linewidth=1.2,
            edgecolor="gray",
            facecolor="whitesmoke",
            transform=ax.transAxes
        )

        ax.add_patch(box)

        ax.text(
            x + width / 2,
            y + 0.09,
            stage,
            ha="center",
            va="center",
            fontsize=8.5,
            fontweight="bold",
            transform=ax.transAxes
        )

        if i < len(stages) - 1:

            ax.annotate(
                "",
                xy=(
                    x + width + gap - 0.003,
                    y + 0.09
                ),
                xytext=(
                    x + width + 0.003,
                    y + 0.09
                ),
                xycoords=ax.transAxes,
                textcoords=ax.transAxes,
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=1.2
                )
            )

    ax.set_title(
        "BioScript Compiler Pipeline",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    save_figure(
        fig,
        "pipeline_overview.png"
    )


# --------------------------------------------------
# Main Visualization Process
# --------------------------------------------------

def build_visualizations(filename):

    ensure_output_dir()

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        source = file.read()

    print(
        "\n========== BIOSCRIPT VISUALIZER ==========\n"
    )

    print(
        f"Source: {filename}\n"
    )

    # -----------------------------
    # Parsing
    # -----------------------------

    print("Parsing source...")

    ast = parser.parse(source)

    if ast is None:

        raise RuntimeError(
            "Parsing failed; no AST was produced."
        )

    print(
        f"AST created: {len(ast)} statement(s)"
    )

    # -----------------------------
    # Semantic Analysis
    # -----------------------------

    print(
        "Running semantic analysis..."
    )

    analyzer = SemanticAnalyzer()

    symbol_table = analyzer.analyze(ast)

    print(
        f"Symbol table created: "
        f"{len(symbol_table.table)} symbol(s)"
    )

    # -----------------------------
    # IR Generation
    # -----------------------------

    print("Generating IR...")

    ir_generator = IRGenerator()

    instructions = ir_generator.generate(ast)

    print(
        f"IR created: "
        f"{len(instructions)} instruction(s)\n"
    )

    # -----------------------------
    # Generate visuals
    # -----------------------------

    render_ast(ast)

    render_symbol_table(
        symbol_table
    )

    render_ir(
        instructions
    )

    render_pipeline()

    print(
        "\nVisualization complete."
    )

    print(
        f"All images are in:\n{OUTPUT_DIR}"
    )


# --------------------------------------------------
# Command Line Entry Point
# --------------------------------------------------

def main():

    if len(sys.argv) != 2:

        print("Usage:")
        print(
            "  python visualizer.py "
            "examples/sample.bio"
        )

        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):

        print(
            f"Error: source file not found: "
            f"{filename}"
        )

        sys.exit(1)

    try:

        build_visualizations(
            filename
        )

    except Exception as exc:

        print(
            f"\nVisualization failed: {exc}"
        )

        sys.exit(1)


if __name__ == "__main__":

    main()