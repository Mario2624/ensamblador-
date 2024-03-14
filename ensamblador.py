instruction_table = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

dest_table = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111',
}

jump_table = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


symbol_table = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576,
    'END': 24,
    'addr': 17,
    'LOOP': 10,
    'n': 16
}

def tokenize(line):
    line = line.strip()
    if line.startswith('@'):
        return [line]
    else:
        return line.split()
    
def translate_instruction(instruction):
    if instruction.startswith('@'):
        address = instruction[1:]
        if address.isdigit():  # Verificar si es un número
            address_binary = format(int(address), '015b')
            return '0' + address_binary.zfill(15)
        else:
            if address in symbol_table:
                address_value = symbol_table[address]
                address_binary = format(address_value, '015b')
                return '0' + address_binary.zfill(15)
            else:
                address_binary = format(int(address), '015b')
                return '0' + address_binary.zfill(15)
    elif ';' in instruction:
        comp, jump = instruction.split(';')
        comp_binary = instruction_table[comp].zfill(7)
        jump_binary = jump_table[jump].zfill(3)
        return '111' + comp_binary + '000' + jump_binary
    elif '=' in instruction:
        dest, comp = instruction.split('=')
        dest_binary = dest_table[dest].zfill(3)
        comp_binary = instruction_table[comp].zfill(7)
        if '0' * 7 in comp_binary:  
            comp_binary = comp_binary.replace('0' * 7, '')  
        return '111' + comp_binary + dest_binary + '000'
    else:
        symbol = instruction.split('(')[1].split(')')[0] if '(' in instruction else instruction
        return '111' + instruction_table[symbol_table[symbol]].zfill(7) + '000'





def assemble(source_code, output_file):
    binary_code = []

    for line in source_code:
        tokens = tokenize(line)

        if not tokens or tokens[0].startswith('//'):
            continue

        instruction_binary = translate_instruction(tokens[0])
        binary_code.append(instruction_binary.zfill(16))

    with open(output_file, 'w') as f:
        for instruction_binary in binary_code:
            f.write(instruction_binary + '\n')


# para probarlo solo se borra lo que hay en el source_code y se le pone el que sse quiera pasar a binario
# Ejemplo de uso en este caso use  el de Rect.asm ingeniero  es lo que se encuentra en el source_code 
source_code = [
    '@R0',
    'D=M',
    '@END',
    'D;JLE',
    '@n',
    'M=D',
    '@SCREEN',
    'D=A',
    '@addr',
    'M=D',
    '@addr',
    'A=M',
    'M=-1',
    '@addr',
    'D=M',
    '@32',
    'D=D+A',
    '@addr',
    'M=D',
    '@n',
    'M=M-1',
    'D=M',
    '@LOOP',
    'D;JGT',
    '@END',
    '0;JMP'
]


assemble(source_code, 'output.hack')
