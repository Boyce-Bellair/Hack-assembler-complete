#assembler with symbols complete
#create the symbol tables in a series of passes
#data structure to use: a dict
#you may want that function that craetes a tuple where index is preserved.
#Constants
DEST_DICT = {'null': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101',
'AD': '110', 'AMD': '111'}

COMP_DICT_A0 = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100', 'A': '110000',
'!D': '001101', '!A': '110001', '-D': '001111', '-A': '110011',  'D+1': '011111', 'A+1': '110111',
'D-1': '001110', 'A-1': '110010', 'D+A': '000010', 'D-A': '010011', 'A-D': '000111', 'D&A': '000000',
'D|A': '010101'}

COMP_DICT_A1 = {'M': '110000', '!M': '110001', '-M': '110011', 'M+1': '110111', 'M-1': '110010',
'D+M': '000010', 'D-M': '010011', 'M-D': '000111', 'D&M': '000000', 'D|M': '010101' }

JMP_DICT = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100',
'JNE': '101', 'JLE': '110', 'JMP': '111' }

SYMBOL_TABLE = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 
'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576 }
#Global
reg_counter = 16
from sys import argv
import math
script, filename = argv

#get file name, change extension name 
extension_drop = filename.split('.')
output_filename = extension_drop[0]
output_filename += '.hack'


txt = open(filename)
assembly_program = txt.read().splitlines()

def assembler(input_list):
    """takes a list of hack assembly instructions and translates it into Hack binary code"""
    output_list = []
    for line in input_list:
        if '@' in line:
            a_binary = a_inst_handler(line)
            output_list.append(a_binary)
        elif '=' or ';' in line:
            c_machine_code = c_inst_handler(line)
            
            output_list.append(c_machine_code)
    return output_list        
            
def c_inst_handler(input_line):
    output_str = ''
    first_three = '111'
    nul_jump_dest = '000'
    c_line = input_line
    
    if '=' in c_line:
        
        dest_str = ''
        comp_str = ''
        x = c_line.split('=') 
        dest_str = x[0]
            
        comp_str = x[1]
        dest_result = destination_trans(dest_str)
        comp_result = computation_trans(comp_str)
        c_comp_dest_out = first_three + comp_result + dest_result + nul_jump_dest
        output_str += c_comp_dest_out
    elif ';' in c_line: 
        jump_str = ''
        compu_str = ''
        y = c_line.split(';')
        compu_str = y[0]
        jump_str = y[1]
        compu_result = computation_trans(compu_str)
        jump_result = jump_trans(jump_str)
        c_jump_out = first_three + compu_result + nul_jump_dest + jump_result
        output_str += c_jump_out
    return output_str        
        
#translate assembly instructions by field
def destination_trans(destination_string):
    """translates destination field into machine code"""
    dest_input_string = destination_string
    output_str = ''
    if dest_input_string in DEST_DICT:
        output_str = DEST_DICT[dest_input_string]
    else:
        
        return "failed!"
    return output_str    
    
    


def computation_trans(computation_string):
    """ translates computational field into machine code"""
    comp_input_str = computation_string
    output_str = ''
    a_bit = ''
    if comp_input_str in COMP_DICT_A0:
        a_bit = '0'
        output_str = COMP_DICT_A0[comp_input_str]
    elif comp_input_str in COMP_DICT_A1:
        a_bit = '1'
        output_str = COMP_DICT_A1[comp_input_str]
    else: 
        return "Failed!"
    return a_bit + output_str

def jump_trans(jump_string):
    """translates the jump field into machine code"""
    jump_input = jump_string
    output_str = ''
    if jump_input in JMP_DICT:
        output_str = JMP_DICT[jump_input]
    else: 
        return "Failed!"
    return output_str



              

def a_inst_handler(a_assembly_line):
    """ changes a inst lines to short binary form with a inst code"""
    dec_num = a_assembly_line[1:] #should remove the '@'
    bin_string_a = dec_to_bin_a(int(dec_num))
    return bin_string_a
    
    
def dec_to_bin_a(n):
    """use this for actually turning a inst to bin with added zeroes"""
    length_of_inst = 15
    a_bit = str(0)
    prelim = bin(n).replace("0b", "") #turns decimal to binary
    
    zeroes_to_add = length_of_inst - len(prelim) #calculate how many leading zeroes to add
    zero_sum = ''
    for i in range(zeroes_to_add):
        
        zero_sum += str(0)
    a_inst = a_bit + zero_sum + str(prelim)
    return a_inst









def first_pass_labels(assembly_list):
    input_list = assembly_list
    line_number = 0
    for line in input_list: 
        if '(' in line:
            label = line[1:-1]
            line_number_out = label_check(label, line_number)
            #print "here is the %r for the %r" % (line_number_out, label)
            #print "removing the line from the list ..."
            del assembly_list[line_number]
            #print "Here is the new list with item removed: ", assembly_list
            
            
        line_number += 1    
    return assembly_list    
    
def second_pass_symbols(assembly_list_no_labels):
    line_number = 0
    input_list = assembly_list_no_labels
    for line in input_list:
        if '@' in line:
            value = line[1:]
            first = value[:1]
            if first.isalpha():
                #split from @ and save to a var 
                symbol = value
                #check to see if symbol is in table. Add value and symbol if not, if so, return value
                symbol_value = symbol_check(symbol, line_number)
                new_line = '@' + str(symbol_value)
                
                del assembly_list_no_labels[line_number]
                assembly_list_no_labels.insert(line_number, new_line)
        line_number += 1                    
    return assembly_list_no_labels    

def label_check(symbol, line_number):
    """check to see if symbol is in table. If it is, return the corresponging value
  if it isn't, add the symbol to the list with value and return the corresponding value"""
    if symbol in SYMBOL_TABLE:
        return SYMBOL_TABLE[symbol]
        
    else:
        SYMBOL_TABLE[symbol] = line_number    
        return line_number
        
def symbol_check(symbol, line_number):
    """check to see if symbol is in table. If it is, return the corresponging value
  if it isn't, add the symbol to the list with value and return the corresponding value"""
    global reg_counter
    if symbol in SYMBOL_TABLE:
        return SYMBOL_TABLE[symbol]
        
    else:
        
        SYMBOL_TABLE[symbol] = reg_counter
        reg_counter += 1  
        return reg_counter - 1        
               

def remove_comments(assembly_program):
    line_list_no_comments = []
    internal_assembly_list = assembly_program
    for line in internal_assembly_list:
        if '/' not in line:
            line_list_no_comments.append(line)
    return line_list_no_comments         

def remove_white_blank(line_list_no_comments):
    line_list_no_empty_strings = []
    line_list = line_list_no_comments
    for string in line_list:
        if string != "":
            trim_line = string.strip()
            line_list_no_empty_strings.append(trim_line)
    return line_list_no_empty_strings

def create_list(file):
    """creates the list of assembly lines with comments and blank lines removed"""
    assembly_program = file
    no_comment = remove_comments(assembly_program)    
    ready_to_go = remove_white_blank(no_comment)   
    return ready_to_go
    
def write_file(final_output):
    """writes the compiled code to an external file"""
    f = open(output_filename, 'w')
    for line in final_output:
        f.write(str(line) + '\n')
    f.close()      
    
first_pass_in = create_list(assembly_program)
second_pass_in = first_pass_labels(first_pass_in)
symbols_resolved = second_pass_symbols(second_pass_in)
final_output = assembler(symbols_resolved)
write_file(final_output)

