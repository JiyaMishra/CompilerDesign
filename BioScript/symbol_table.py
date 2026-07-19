class SymbolTable:
    def __init__(self):
        self.table = {}
        self.next_address = 1000

    def insert(self, name, data_type, value=None):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared.")

        self.table[name] = {
            "datatype": data_type,
            "value": value,
            "address": self.next_address,
            "bytes": 8
        }

        self.next_address += 8

    def exists(self, name):
        return name in self.table

    def lookup(self, name):
        return self.table.get(name)

    def update(self, name, value):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared.")

        self.table[name]["value"] = value

    def display(self):
        print("\n========== SYMBOL TABLE ==========\n")

        print(
            "{:<15} {:<15} {:<10} {:<10} {}".format(
                "Variable",
                "Datatype",
                "Bytes",
                "Address",
                "Value"
            )
        )

        print("-" * 70)

        for name, info in self.table.items():
            print(
                "{:<15} {:<15} {:<10} {:<10} {}".format(
                    name,
                    info["datatype"],
                    info["bytes"],
                    info["address"],
                    info["value"]
                )
            )
if __name__ == "__main__":

    st = SymbolTable()

    st.insert("dna", "sequence", "ATGCGTA")

    st.insert("rna", "sequence")

    st.insert("protein", "sequence")

    st.display()