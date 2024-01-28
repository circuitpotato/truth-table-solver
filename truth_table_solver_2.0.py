# Visit downtothecircuits.com for more information
# Code by: circuit_potato

# Truth Table Solver 2.0: This program takes in the outputs of an N input truth table and simplifies the boolean expression
# The simplified boolean expression is then expressed in Verilog/VHDL Syntax. The program runs on a GUI on Tkinter

from tkinter import Tk, Label, Button, Entry, Canvas, Scrollbar, Frame, messagebox
from sympy import simplify_logic, sympify

# Global variables
truth_table_input = None
truth_table_input_max = 9   # maximum no. of truth table inputs
truth_table_symbols = None
button_values = []

# truth table GUI/labels global size
label_width = 27
label_pad_x = 13
label_pad_y = 15
font_size = 10

# output GUI/labels global size
output_label_width = 59
output_label_padx = 10
output_label_pady = 10

# copy button global size
button_padx = 10
button_pady = 5


def button2_pressed():
    # Configure row and column weights for expansion
    canvas2.yview_moveto(0)  # Set the initial view position of the canvas to the top
    canvas2.grid(row=5, column=0, columnspan=3, sticky="nsew")
    scrollbar2.grid(row=5, column=3, sticky="nsew")
    canvas2.create_window((0, 0), window=content_frame2)

    button_values_list = [int(item) if item in ['1'] else item for item in button_values]
    my_simplified_expression = get_simplified_expression(truth_table_symbols, str(truth_table_input), button_values_list)
    get_verilog_output(my_simplified_expression)
    get_vhdl_output(my_simplified_expression)


def get_inputs():
    global truth_table_input, truth_table_symbols, button_values

    # get inputs from user
    input_value = number_entry.get()
    symbols_value = string_entry.get()

    # Validate the user input
    if (input_value.isnumeric() and 2 <= int(input_value) <= truth_table_input_max) and (symbols_value.isalpha() == 1) and (len(set(symbols_value)) == len(symbols_value)) and (len(symbols_value) == int(input_value)):
        truth_table_input = int(input_value)  # save values into global variables
        truth_table_symbols = symbols_value
        print_truth_table(truth_table_input, truth_table_symbols)
        button_values = create_toggle_buttons(truth_table_input)

    else:
        messagebox.showerror("Error", "Invalid input! \na) Truth Table Inputs: Enter a number between 2 to " + str(truth_table_input_max) + " \nb) Truth Table Symbols: Enter with respect to the number of inputs (E.g. ABCD, DCBA, aAc, cba)")


def print_truth_table(tt_inputs, tt_symbols):
    global label_width, label_pad_x, label_pad_y, font_size

    # Configure row and column weights for expansion
    canvas.yview_moveto(0)  # Set the initial view position of the canvas to the top
    canvas.grid(row=2, column=0, columnspan=3, sticky="nsew")
    scrollbar.grid(row=2, column=3, sticky="nsew")
    canvas.create_window((0, 0), window=content_frame)

    # display instructions guide for truth table
    instructions_label = Label(content_frame, text=f"Please select (toggle) your truth table output values and press submit: ", width=0, padx=label_pad_x, pady=label_pad_y, anchor="center")
    instructions_label.grid(row=3, columnspan=2, sticky="nsew")
    instructions_label.configure(font=("Arial", font_size, "bold italic"), foreground="green")

    # display name labels
    name_label = Label(content_frame, text=f"{tt_symbols}", width=label_width, relief="raised", padx=label_pad_x, pady=label_pad_y, anchor="center")
    name_label.grid(row=4, column=0, sticky="nsew")
    name_label.configure(font=("Arial", font_size, "bold"), foreground="red")
    name_label2 = Label(content_frame, text=f"Z", width=label_width, relief="raised", padx=label_pad_x, pady=label_pad_y, anchor="center")
    name_label2.grid(row=4, column=1, sticky="nsew")
    name_label2.configure(font=("Arial", font_size, "bold"), foreground="red")

    # display truth table
    truth_table_label = []
    for i in range(2 ** tt_inputs):
        num_bits = tt_inputs
        binary_number = bin(i)[2:].zfill(num_bits)
        label = Label(content_frame, text=f"{binary_number}", width=label_width, relief="raised", padx=label_pad_x, pady=label_pad_y, anchor="center")
        label.grid(row=(5+i), column=0, sticky="nsew")
        label.configure(font=("Arial", font_size, "bold"), foreground="black")
        truth_table_label.append(label)

    # Update the scrollable region
    update_scroll_region(None)


def create_toggle_buttons(num_buttons):
    global label_width, label_pad_x, label_pad_y, font_size
    button_values_final = []

    def toggle_value(my_button):
        current_value = my_button.cget("text")
        if current_value == "0":
            my_button.config(text="1")
        elif current_value == "1":
            my_button.config(text="X")
        else:
            my_button.config(text="0")

        # Update the list with the button's current value
        button_values_final[buttons.index(my_button)] = my_button.cget("text")

    # display truth table output buttons for user to toggle
    buttons = []
    for i in range(2**num_buttons):
        # whitespace = Label(content_frame, text=f"", padx=10, pady=5)
        # whitespace.grid(row=(5 + i), column=4, padx=100, sticky="nsew")
        button = Button(content_frame, text=f"0", width=label_width, relief="solid", padx=label_pad_x, pady=label_pad_y)
        button.grid(row=(5 + i), column=1, sticky="nsew")
        button.config(command=lambda b=button: toggle_value(b))
        button.configure(font=("Arial", font_size, "bold"), foreground="black")
        buttons.append(button)
        button_values_final.append("0")  # Initialize the list with "0" values

    # Show truth table output submit button
    output_submit_button = Button(root, text="Submit", padx=button_padx, pady=button_pady, command=button2_pressed)
    output_submit_button.grid(row=4, column=2, sticky="nsew")

    # Return the button values
    return button_values_final


# this function splits a string if it exceeds a certain length
def split_string(sentence_str):
    string_length = 70
    if len(sentence_str) <= string_length:
        return sentence_str  # Return the original string as a single element list

    split_strings = []
    remaining_text = sentence_str

    while len(remaining_text) > string_length:
        split_line = remaining_text[:string_length]  # Extract the first 30 characters
        split_strings.append(split_line)
        remaining_text = remaining_text[string_length:]  # Remove the split portion from the remaining text

    # Append the remaining text as the last split string
    split_strings.append(remaining_text)
    return "\n".join(split_strings)  # Join the split strings using newline character


def replace_letters_with_lowercase(input_string):
    replaced_letters = []
    for char in ['O', 'S', 'I', 'N', 'E', 'Q']:
        if char in input_string:
            replaced_letters.append(char)
            input_string = input_string.replace(char, char.lower())

    replaced_letters = [char.lower() for char in replaced_letters]
    return input_string, replaced_letters


def invert_case_of_replaced_letters(input_string, letters_to_check):
    print(letters_to_check)
    for char in input_string:
        if char in letters_to_check:
            inverted_char = char.upper()
            input_string = input_string.replace(char, inverted_char)

    return input_string


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

    sop_str, replaced_letters = replace_letters_with_lowercase(sop_str)
    sop_str_dont_care, replaced_letters_dont_care = replace_letters_with_lowercase(sop_str_dont_care)

    expression = sympify(sop_str)
    simplified_expression = simplify_logic(expression)  # simplify expression

    if ("x" in tt_outputs) or ("X" in tt_outputs):
        expression_dont_care = sympify(sop_str_dont_care)
        simplified_expression_dont_care = simplify_logic(simplified_expression, dontcare=expression_dont_care)
        simplified_expression_dont_care = str(simplified_expression_dont_care)
        final_simplified_expression = simplified_expression_dont_care
        final_simplified_expression = invert_case_of_replaced_letters(final_simplified_expression, replaced_letters_dont_care)

        # simplified equivalent dont care (title)
        simplified_label1 = Label(content_frame2, text=f"Simplified Boolean Expression dont care: ")
        simplified_label1.grid(row=0, column=0, sticky="nsew")
        simplified_label1.configure(font=("Arial", font_size, "bold italic"), foreground="brown")

        # simplified equivalent dont care (output expression)
        simplified_dont_care_output = f"Z = {final_simplified_expression}"
        split_simplified_dont_care_output = split_string(simplified_dont_care_output)
        simplified_label2 = Label(content_frame2, text=split_simplified_dont_care_output, width=output_label_width, padx=10, pady=10, relief="solid")
        simplified_label2.grid(row=1, column=0, sticky="we")
        simplified_label2.configure(font=("Arial", font_size, "bold"), foreground="black")

        # copy button
        simplified_copy_button = Button(content_frame2, text=f"copy", command=lambda: copy_to_clipboard(simplified_dont_care_output), padx=button_padx, pady=button_pady)
        simplified_copy_button.grid(row=2, column=0, sticky="e")

    else:
        simplified_expression = str(simplified_expression)
        final_simplified_expression = simplified_expression
        final_simplified_expression = invert_case_of_replaced_letters(final_simplified_expression,
                                                                      replaced_letters)

        # simplified equivalent (title)
        simplified_label1 = Label(content_frame2, text="Simplified Boolean Expression: ")
        simplified_label1.grid(row=0, column=0, sticky="nsew")
        simplified_label1.configure(font=("Arial", font_size, "bold italic"), foreground="brown")

        # simplified equivalent (expression)
        simplified_output = "Z = " + final_simplified_expression
        split_simplified_output = split_string(simplified_output)
        simplified_label2 = Label(content_frame2, text=split_simplified_output, width=output_label_width, padx=10, pady=10, relief="solid")
        simplified_label2.grid(row=1, column=0, sticky="we")
        simplified_label2.configure(font=("Arial", font_size, "bold"), foreground="black")

        # copy button
        simplified_copy_button = Button(content_frame2, text=f"copy", command=lambda: copy_to_clipboard(simplified_output), padx=button_padx, pady=button_pady)
        simplified_copy_button.grid(row=2, column=0, sticky="e")

    return final_simplified_expression


# Translate simplified boolean expression to Verilog Syntax
def get_verilog_output(expression_str):
    # verilog equivalent (title)
    verilog_label1 = Label(content_frame2, text=f"Verilog equivalent: ")
    verilog_label1.grid(row=3, column=0, sticky="nsew")
    verilog_label1.configure(font=("Arial", font_size, "bold italic"), foreground="brown")

    # verilog equivalent (expression)
    verilog_output = "assign Z = " + expression_str + ";"
    split_verilog_output = split_string(verilog_output)
    verilog_label2 = Label(content_frame2, text=split_verilog_output, width=output_label_width, padx=output_label_padx, pady=output_label_pady, relief="solid")
    verilog_label2.grid(row=4, column=0, sticky="we")
    verilog_label2.configure(font=("Arial", font_size, "bold"), foreground="black")

    # copy button
    verilog_copy_button = Button(content_frame2, text=f"copy", command=lambda: copy_to_clipboard(verilog_output), padx=button_padx, pady=button_pady)
    verilog_copy_button.grid(row=5, column=0, sticky="e")


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

    # vhdl equivalent (title)
    vhdl_label1 = Label(content_frame2, text=f"VHDL equivalent: ")
    vhdl_label1.grid(row=6, column=0, sticky="nsew")
    vhdl_label1.configure(font=("Arial", font_size, "bold italic"), foreground="brown")

    # verilog equivalent (expression)
    vhdl_output = "Z <= " + expression_str + ";"
    split_vhdl_output = split_string(vhdl_output)
    vhdl_label2 = Label(content_frame2, text=split_vhdl_output, width=output_label_width, padx=10, pady=10, relief="solid")
    vhdl_label2.grid(row=7, column=0, sticky="we")
    vhdl_label2.configure(font=("Arial", font_size, "bold"), foreground="black")

    # copy button
    vhdl_copy_button = Button(content_frame2, text=f"copy", command=lambda: copy_to_clipboard("Z <= " + expression_str + ";"), padx=button_padx, pady=button_pady)
    vhdl_copy_button.grid(row=8, column=0, sticky="e")


def copy_to_clipboard(text):
    root.clipboard_clear()  # Clear the clipboard contents
    root.clipboard_append(text)  # Append the new text to the clipboard
    messagebox.showinfo("Copied!", "Text has been copied to the clipboard.")


# main code
root = Tk()
root.title("Truth Table GURU 2.0 :)")

# Show truth table inputs GUI (inputs)
number_label = Label(root, text=f"No. of Truth Table Inputs (+ve integers only):", padx=10, pady=5)
number_label.grid(row=0, column=0, sticky="nsew")
number_entry = Entry(root)
number_entry.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

# Show truth table symbols GUI (inputs)
string_label = Label(root, text=f"Truth Table Symbols (E.g. ABCD, DCBA, aAc, cba): ", padx=10, pady=5)
string_label.grid(row=1, column=0, sticky="nsew")
string_entry = Entry(root)
string_entry.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

# Show Submit Button
BUTTON = Button(root, text=f"Submit", command=get_inputs, padx=button_padx, pady=button_pady)
BUTTON.grid(row=1, column=2, sticky="nsew")

# Create a Canvas and Scrollbar (only displayed after submit button)
canvas = Canvas(root)
canvas2 = Canvas(root)

# generate scrollbars
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar2 = Scrollbar(root, orient="vertical", command=canvas2.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas2.configure(yscrollcommand=scrollbar2.set)

# Create a Frame to contain the content
content_frame = Frame(canvas)
content_frame2 = Frame(canvas2)


# Update the scrollable region when the content frame changes its size
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)  # Set the initial view position of the canvas to the top


def update_scroll_region2(event):
    canvas2.configure(scrollregion=canvas2.bbox("all"))
    canvas2.yview_moveto(0)  # Set the initial view position of the canvas to the top


# configure the scrollbar to update properly
content_frame.bind("<Configure>", update_scroll_region)
content_frame2.bind("<Configure>", update_scroll_region2)

root.mainloop()
