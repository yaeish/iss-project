def permutate(original, permutation):
    return [original[i - 1] for i in permutation]

def shift_left(bits, n):
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def s_box_lookup(sbox, bits):
    row = int(f"{bits[0]}{bits[3]}", 2)
    col = int(f"{bits[1]}{bits[2]}", 2)
    return [int(x) for x in f"{sbox[row][col]:02b}"]

def fk(bits, key):
    left, right = bits[:4], bits[4:]
    expanded_permuted = permutate(right, EP)
    xor_result = xor(expanded_permuted, key)
    left_sbox = s_box_lookup(S0, xor_result[:4])
    right_sbox = s_box_lookup(S1, xor_result[4:])
    combined_sbox = left_sbox + right_sbox
    permuted_4 = permutate(combined_sbox, P4)
    return xor(left, permuted_4) + right

def bits_to_char(bits):
    return chr(int(''.join(map(str, bits)), 2))

def char_to_bits(char):
    return [int(bit) for bit in f"{ord(char):08b}"]

def sdes_encrypt_char(plain_char, k1, k2):
    plaintext = char_to_bits(plain_char)

    print("\nEncryption:")
    ip = permutate(plaintext, IP)
    print(f"IP: {ip}")
    
    first_fk = fk(ip, k1)
    print(f"fk1: {first_fk}")
    
    switched = first_fk[4:] + first_fk[:4]
    print(f"Switch: {switched}")
    
    second_fk = fk(switched, k2)
    print(f"fk2: {second_fk}")
    
    cipher_bits = permutate(second_fk, IP_INV)
    cipher_char = bits_to_char(cipher_bits)
    print(f"Cipher Text: {cipher_char} (bits: {cipher_bits})")
    
    return cipher_char

def sdes_encrypt(plaintext, key_char):
    key = char_to_bits(key_char) + [0] * 2  # Adjust key to be 10 bits

    print("Key Generation:")
    key_permuted = permutate(key, P10)
    print(f"P10: {key_permuted}")
    
    left_half, right_half = key_permuted[:5], key_permuted[5:]
    left_half = shift_left(left_half, 1)
    right_half = shift_left(right_half, 1)
    k1 = permutate(left_half + right_half, P8)
    print(f"K1: {k1}")
    
    left_half = shift_left(left_half, 2)
    right_half = shift_left(right_half, 2)
    k2 = permutate(left_half + right_half, P8)
    print(f"K2: {k2}")
    
    encrypted_text = ''
    for char in plaintext:
        encrypted_char = sdes_encrypt_char(char, k1, k2)
        encrypted_text += encrypted_char
        
    return encrypted_text

# Permutation and S-box tables
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

# Test with sample plaintext and key
plaintext = 'HELLO'  # Example plaintext
key_char = 'A'       # Example key character

cipher_text = sdes_encrypt(plaintext, key_char)
print("Final Cipher Text:", cipher_text)