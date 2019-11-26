import binascii
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)
def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def load():
    address = 0
    try:
        print('----====&')
        with open('wishing_well_prophecy.txt',) as instructions:
            lines_from_2 = instructions.readlines()[2:]
            for lines in lines_from_2:
                # if lines[:7] != '0000000':
                    # print(lines)
                value = chr(int(lines, 2))
                print(value)


    except FileNotFoundError:
        print('File does not Exist')
    
                            
                          
load()