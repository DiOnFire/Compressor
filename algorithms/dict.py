import math


def encode(path: str) -> None:
    with open(path, 'r') as file:
        contents = file.readline()
        letters = []

        # parse all character to make a dict of all characters used
        for char in contents:
            if char not in letters:
                letters.append(char)

        # first byte -- dictionary length
        final_string_bits = to_byte(len(letters))
        # adding dictionary itself
        for char in letters:
            final_string_bits += to_byte(ord(char))

        # encoding content and dumping it in final string  
        for char in contents:
            final_string_bits += encode_with_dict_len(letters.index(char), len(letters))

        # creating a file where encoded string will be stored
        open(f"{path.replace('.txt', '')}_encoded.txt", 'w').write(final_string_bits)


def decode(path: str) -> None:
    with open(path, 'r') as file:
        contents = file.readline()
        dictionary = {}

        # getting first byte -> dictionary length
        dict_len = int(contents[contents[:8].find('1'):8], 2)

        # parsing dictionary bytes and making a python dict variable out of them
        counter = 0
        for i in range(8, dict_len * 8 + 1, 8):
            dictionary[f'{encode_with_dict_len(counter, dict_len)}'] = chr(int(contents[i:i + 8], 2))
            counter += 1
        
        decoded_string = ''

        # calculating the number of bits that are needed for one symbol to be stored
        step = math.ceil(math.log2(dict_len))

        # parsing contents and decoding them with the dictionary created above
        for i in range(dict_len * 8 + 8, len(contents), step):
            decoded_string += dictionary[contents[i:i+step]]
        # creating a file where decoded string will be stored
        open(f"{path.replace('_encoded.txt', '')}_decoded.txt", 'w').write(decoded_string)
       

def to_byte(_int: int) -> str:
    byte = format(_int, 'b')
    while len(byte) < 8:
        byte = '0' + byte
    return byte


def encode_with_dict_len(index: int, dict_len: int) -> str:
    output = format(index, 'b')
    while len(output) < math.log2(dict_len):
        output = '0' + output
    return output
