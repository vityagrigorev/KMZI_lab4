from itertools import cycle
from itertools import product

import Image
import time
LEN = 256

def message_to_bin(message):

    message = bytes(message)
    len_message = len(message)

    binlen = bin(len_message)[2:]
    if len(binlen) < 8:
        binlen = '0' * (8 - len(binlen)) + binlen
        
    binmessage = []
    binmessage.append(binlen)

    for x in message:
        part = bin(ord(x))[2:]
        partlen = len(part)
        if (partlen < 8):
            part = '0' * (8 - partlen) + part
        binmessage.append(part)        
    return b''.join(binmessage)

def hide_message(message, image): #, outfile
    
    binmessage = message_to_bin(message)
    image = Image.open(image)   
            
    pix = image.load()
    sizex, sizey = image.size
    
    if len(binmessage) > (sizex * sizey):
        raise Exception ("Very small image")
    
    next_index = product(range(sizex), range(sizey))

    for m in binmessage:
        index = next(next_index)
        r, g, b, a = pix[index]
        last_bit = bin(b)[-1:]
        if m == '0':
            if last_bit == '1':
                b -= 1
        elif m == '1':
            if last_bit == '0':
                b += 1
        
        pix[index] = r,g,b,a
    
    #image.save(outfile)
    image.save('step_image.png', 'png')


Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

def add_key_round(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]

def bytes_sub(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = Sbox[s[i][j]]

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

x = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ x(a[0] ^ a[1])
    a[1] ^= t ^ x(a[1] ^ a[2])
    a[2] ^= t ^ x(a[2] ^ a[3])
    a[3] ^= t ^ x(a[3] ^ u)

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    for i in range(4):
        u = x(x(s[i][0] ^ s[i][2]))
        v = x(x(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)

def round_encode(matrix_state, key_matrix):
    bytes_sub(matrix_state)
    shift_rows(matrix_state)
    mix_columns(matrix_state)
    add_key_round(matrix_state, key_matrix)

Rcon = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

def text2matrix(text):
    text = [ord(i) for i in text]
    state = []

    for i in range(4):
        state.append(text[i::4])
    return state

def matrix2text(matrix):
    result = []
    for i in range(4):
        for j in range(4):
            result.append(matrix[j][i])
    return ''.join([chr(i) for i in result])

class AES:

    def __init__(self, AES_key):
        self.change_key(AES_key)

    def change_key(self, AES_key):
        self.key_round = text2matrix(AES_key)

        for i in range(4, 4 * 11):
            self.key_round.append([])
            if i % 4 == 0:
                byte = self.key_round[i - 4][0]        \
                     ^ Sbox[self.key_round[i - 1][1]]  \
                     ^ Rcon[i / 4]
                self.key_round[i].append(byte)

                for j in range(1, 4):
                    byte = self.key_round[i - 4][j]    \
                         ^ Sbox[self.key_round[i - 1][(j + 1) % 4]]
                    self.key_round[i].append(byte)
            else:
                for j in range(4):
                    byte = self.key_round[i - 4][j]    \
                         ^ self.key_round[i - 1][j]
                    self.key_round[i].append(byte)

    def encode(self, data):
        self.plain_state = text2matrix(data)

        add_key_round(self.plain_state, self.key_round[:4])

        for i in range(1, 10):
            round_encode(self.plain_state, self.key_round[4 * i : 4 * (i + 1)])

        bytes_sub(self.plain_state)
        shift_rows(self.plain_state)
        add_key_round(self.plain_state, self.key_round[40:])

        return matrix2text(self.plain_state)

def full_encode(value, Vig_key):
    return ''.join(map(lambda x: chr((ord(x[0]) + ord(x[1])) % LEN), zip(value, cycle(Vig_key))))
    
def main(data, Vig_key, AES_key, image):

    data_from_Vig = full_encode(data, Vig_key)
    time.sleep(1)
    print 'Encryption Vigineer was successful'
    AES_key = AES_key[0:len(AES_key)-1]
    
    if len(AES_key) != 16:
        print "length of key must be 16"
        
    my_AES = AES(AES_key)
    
    encoded_aes = my_AES.encode(data_from_Vig)
    final_value = encoded_aes
    time.sleep(1)
    print 'Encryption AES was successful'
    
    hide_message(final_value, image)
    
    f = open('step_image.png', 'rb')
    res = f.read()
    
    time.sleep(1)
    print 'Encryption LSB was successful'
    
    return res
if __name__ == "__main__":
    main()
