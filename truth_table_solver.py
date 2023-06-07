# Visit downtothecircuits.com for more information
# Code by: circuit_potato

# Truth Table Solver: This program takes in the outputs of an N input truth table and simplifies the boolean expression
# The simplified boolean expression is then expressed in Verilog/VHDL Syntax

from sympy import simplify_logic, sympify


# Request for no. of inputs in truth table from user
def get_truth_table_inputs():
    n = input("Enter the number of inputs to truth table (+ve integers only): ")  # no. of inputs to truth table
    while (n.isnumeric() == 0) or (int(n) <= 1):  # check if input from user is a positive number
        n = input("Re-enter the number of inputs to truth table (+ve integers only): ")
    return n


# Request for symbols of truth table with respect to no. of inputs from user
def get_truth_table_symbols(truth_table_input):
    symbols_instruction = "Enter the truth table symbols with respect to the no. of inputs (E.g. ABCD, DCBA, aAc, cba): "
    while True:
        truth_table_symbols = input(symbols_instruction)

        # check if symbols entered by user has no repeating letters
        if (truth_table_symbols.isalpha() == 1) & (len(set(truth_table_symbols)) == len(truth_table_symbols)) & (int(truth_table_input) == len(truth_table_symbols)):
            break
        else:
            symbols_instruction = "Re-enter the truth table symbols: "
    return truth_table_symbols


# Request for truth table outputs from user
def get_truth_table_outputs(inputs_of_truth_table):
    largest_truth_table_input = (2**int(inputs_of_truth_table))-1
    num_digits = len(bin(largest_truth_table_input)) - 2    # number of digits needed for the binary representation
    truth_table_outputs = [0]*(largest_truth_table_input+1)
    for i in range(largest_truth_table_input+1):
        binary = format(i, '0{}b'.format(num_digits))
        outputs_instruction = "Enter the output "
        while True:
            truth_table_outputs_temp = input(outputs_instruction + "of truth table " + binary + " ('0', '1', 'x' or 'X' ) : ")
            if (truth_table_outputs_temp == "0") or (truth_table_outputs_temp == "1"):
                truth_table_outputs[i] = int(truth_table_outputs_temp)
                break
            elif (truth_table_outputs_temp == "x") or (truth_table_outputs_temp == "X"):
                truth_table_outputs[i] = truth_table_outputs_temp
                break
            else:
                outputs_instruction = "Re-enter the output of "
    return truth_table_outputs


# Simplify the boolean expression of truth table from SOP
def get_simplified_expression(input_symbols, tt_inputs, tt_outputs):
    decimal_inputs = 2 ** (int(tt_inputs))
    sop_str = ""
    sop_str_dont_care = ""
    for x in range(decimal_inputs):
        if (tt_outputs[x] == 1) or (tt_outputs[x] == "X") or (tt_outputs[x] == "x"):
            binary_input = bin(x)[2:]
            padded_binary = binary_input.zfill(int(tt_inputs))
            input_symbols_index = 0

            sop_temp = ""
            for y in padded_binary:
                if y == "0":
                    sop_temp = sop_temp + "~" + str(input_symbols[input_symbols_index]) + "&"
                elif y == "1":
                    sop_temp = sop_temp + str(input_symbols[input_symbols_index]) + "&"
                input_symbols_index = input_symbols_index + 1
            sop_temp = sop_temp[:-1]  # remove last character of string

            if tt_outputs[x] == 1:
                sop_str = sop_str + " | " + sop_temp
            else:
                sop_str_dont_care = sop_str_dont_care + " | " + sop_temp
    sop_str = sop_str[2:]  # remove first character of string
    sop_str_dont_care = sop_str_dont_care[2:]  # remove first character of string
    expression = sympify(sop_str)
    simplified_expression = simplify_logic(expression)  # simplify expression
    if ("x" in tt_outputs) or ("X" in tt_outputs):
        expression_dont_care = sympify(sop_str_dont_care)
        simplified_expression_dont_care = simplify_logic(simplified_expression, dontcare=expression_dont_care)
        simplified_expression_dont_care = str(simplified_expression_dont_care)
        final_simplified_expression = simplified_expression_dont_care
        print("Simplified Boolean Expression dont care: Z = " + simplified_expression_dont_care)
    else:
        simplified_expression = str(simplified_expression)
        final_simplified_expression = simplified_expression
        print("Simplified Boolean Expression: Z = " + simplified_expression)

    return final_simplified_expression


# Translate simplified boolean expression to Verilog Syntax
def get_verilog_output(expression_str):
    print("Verilog equivalent: ")
    print("assign Z = " + expression_str + ";")


# Translate simplified boolean expression to VHDL syntax
def get_vhdl_output(expression_str):
    # Find the index of the first occurrence of "~"
    index = expression_str.find("~")
    while index != -1:
        if expression_str[index] == "~":
            expression_str = expression_str[:index] + '-' + expression_str[index + 1:]
            expression_str = expression_str[:index] + "(" + expression_str[index] + expression_str[
                index + 1] + ")" + expression_str[index + 2:]
            index = expression_str.find("~")

    expression_str = expression_str.replace("&", "and")
    expression_str = expression_str.replace("|", "or")
    expression_str = expression_str.replace("-", "not ")
    print("VHDL equivalent: ")
    print("Z <= " + expression_str + ";")


# main code
truth_table_inputs = get_truth_table_inputs()                                                                   # get no. of truth table inputs (> 1)
print("\n")                                                                                                     # just a spacer
my_symbols = get_truth_table_symbols(truth_table_inputs)                                                        # get symbols of inputs (E.g. ABC, DCBA)
print("\n")

my_truth_table_outputs = get_truth_table_outputs(truth_table_inputs)                                            # get outputs of truth table with respect to inputs ("0", "1", "x", or "X")
print("\n")
my_simplified_expression = get_simplified_expression(my_symbols, truth_table_inputs, my_truth_table_outputs)    # get simplified boolean expression
print("\n")
get_verilog_output(my_simplified_expression)                                                                    # Verilog equivalent
print("\n")
get_vhdl_output(my_simplified_expression)                                                                       # VHDL equivalent
print("\n")