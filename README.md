## Pascal Compiler

This is a Pascal Compiler written in Python 2.7.11. As such please follow the directions
below to run the compiler.

### Dependencies

In order to add native enumeration states found in C# and Java, I used a python package
called **AEnum**. To install the right version of **AEnum** please have **pip** installed
and run the following command:

`pip install -r requirements.txt`

This will install Aenum into your Python Package Manager.

### Running the Compiler

All pascal files are located in the `pascal_files` directory. For a list of the following
pascal files please see the image below:

![pascal files][pascal_file.png]

To run the Compiler simply run the `compiler_simulator.py` file in the terminal. See below for an example.

`python compiler_simulator.py pascal_files/arrays.pas`

### Compiler Info

The `compiler_simulator.py` script executes the following modules in order:

- `tokenizer.py` -> Contains the Scanner
- `parser_module.py` -> Contains the Parser
- `emulator_module.py` -> Contains the Emulator

Other files include:

- `byte_manager.py` -> Allows the compiler to create bytearray and unpack it
- `symbol.py` -> Module holds an instance of a `Symbol` object entry for the Symbol table
