# DECAF20-Parser
This repository contains a simple scanner and parser for the [DECAF language](https://anoopsarkar.github.io/compilers-class/decafspec.html), written in Python.


## Architecture
The project follows a modular, object-oriented design to represent the language's grammar:

- Parser.py: The core engine implementing recursive descent logic.

- Individual classes for every statement and expression type in the abstract syntax tree (e.g., ReturnStmt.py, BreakStmt.py, Variable.py).

- Type.py module to handle base types and array structures.

## Technical Highlights
- Hand-written parsing logic to handle context-free grammar without reliance on external generator tools.
  - There is a mismatch with operator associativity; the parser is left recursive. This was a deliberate decision to prioritize passing the required academic test cases and meeting the defined project scope in time rather than introducing the complexity of a full right-recursive transformation.

- Tree structure is dynamically contstructed and maintains the semantic relationship between code elements.

- Basic syntactic validation to identify malformed Decaf source files during the parsing phase and throw syntax errors.

## Running the Scanner

``` bash
python main.py [.decaf file]
```
Output is a printed list of the parse tree or errors.
