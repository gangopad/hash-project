#From https://rosettacode.org/wiki/MD5/Implementation#Python

import pickle
import math
import sys 
import os 
 
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
 
constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
 
init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
 
functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]
 
index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]
 
A = []
B = []
C = []
D = []

adj_list = {}

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF
 
def md5(message):
 
    message = bytearray(message) #copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message)%64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')
 
    hash_pieces = init_values[:]
 
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF

            #Gather hash data
            str_hash = str(chunk)
            if (str_hash, d, a) not in adj_list:
                adj_list[(str_hash, d, a)] = 1
            else:
                adj_list[(str_hash, d, a)] += 1

            if (str_hash, new_b, b) not in adj_list:
                adj_list[(str_hash, new_b, b)] = 1
            else:
                adj_list[(str_hash, new_b, b)] += 1

            if (str_hash, b, c) not in adj_list:
                adj_list[(str_hash, b, c)] = 1
            else:
                adj_list[(str_hash, b, c)] += 1

            if (str_hash, c, d) not in adj_list:
                adj_list[(str_hash, c, d)] = 1
            else:
                adj_list[(str_hash, c, d)] += 1

            a, b, c, d = d, new_b, b, c

        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF
 
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))
 
def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))
 
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

# Run 
bin_dir = sys.argv[1]
for filename in absoluteFilePaths(bin_dir):
    with open(filename, 'rb') as cur_file:
        bit_str = cur_file.read()
        #print(md5_to_hex(md5(bit_str)))
        md5(bit_str)

    with open("md5states.pickle", 'wb') as out_file:
        out_file.write(pickle.dumps(adj_list))

