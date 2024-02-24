# truth_table_solver_2.0.py
### Introduction:
1. https://downtothecircuits.com/?p=2754
2. This is a GUI based version of the truth table solver.
3. This GUI can run up to 9 inputs (but I honestly don't reccommend it because too many logic inputs has its disadvantages)

# truth_table_solver.py
### Introduction:
1. Visit https://downtothecircuits.com/?p=2677 for more information (currently on maintenance)
2. This python program solves a truth table based on user input from the python terminal locally.
3. It's not the prettiest of graphics (I'm no web developer) --> but hey it works just fine for me
4. This only converts the truth table to boolean algebra to primitives (or basic gates not including special gates like NAND, XOR, XNOR etc)

### Packages used: 
1. sympy

### Instructions:
1. download relevant packages
2. run the program :) Yes it's that easy

### Packages used:
1. tkinter
2. sympy

### Instructions:
1. download relevant packages:
2. run the program :) more user friendly than version 1 of truth table solver

# To do List / Future Improvements
1. I made some changes to truth_table_solver 1.0 and 2.0 to accomodate reserved symbols (O, S, I, N, E, Q) in SymPy 
   - Some "reserved" symbols:
      - O: for big O notation
      - S: S class
      - I: Imaginary
      - N: evaluates expression in floating point
      - E: Euler's number
      - Q: rational number
      - For more information: https://docs.sympy.org/latest/modules/abc.html#
2. Support gates other than primitives (E.g. NOR, XOR, NAND)

