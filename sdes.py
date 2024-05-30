IP = [2,6,3,1,4,8,5,7]
InvIP = [4,1,3,5,7,2,8,6]
P10 = [3,5,2,7,4,10,1,9,8,6]
P8 = [6,3,7,4,8,5,10,9]
P4 = [2,4,3,1]
EP = [4,1,2,3,2,3,4,1]

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

def permutate(input, permutation):
    result = [0] * len(permutation)
    for i in range(len(permutation)):
        result[i] = input[permutation[i] - 1]
    return result

def leftshift_helper(half_input, count):
    return half_input[count:] + half_input[:count]

def leftshift(input, count):
    # Split array into left and right
    left = input[:len(input)//2]
    right = input[len(input)//2:]

    # left shift each section
    left = leftshift_helper(left, count)
    print(f"Key Expansion (After LS-{count}, Left): ", left)

    right = leftshift_helper(right, count)
    print(f"Key Expansion (After LS-{count}, right): ", right)


    return left + right

def xor_helper(bit1, bit2):
    b1 = True if bit1 == 1 else False
    b2 = True if bit2 == 1 else False
    return 1 if (not b1 and b2) or (b1 and not b2) else 0

def xor(input1, input2):
    result = [0] * len(input1)
    for i in range(len(input1)):
        result[i] = xor_helper(input1[i], input2[i])
    return result

def binary_to_decimal(bit_array):
    result = 0
    for i in range(len(bit_array)):
        result += pow(2, len(bit_array) - 1 - i) * bit_array[i]
    return result

def decimal_to_binary(input, size):
    result = []
    
    if input == 0:
        result.append(0)
    
    while input > 0:
        bit = input % 2
        result.append(bit)
        input = input // 2

    # Reverse the result to get the correct binary order
    result.reverse()
    
    if size is not None and size > len(result):
        result = ([0] * (size - len(result))) + result
    
    return result

def sbox(input, s_box):
    row = binary_to_decimal([input[0], input[3]])
    col = binary_to_decimal([input[1], input[2]])
    subsitution = s_box[row][col]
    return decimal_to_binary(subsitution, len(input) // 2)


def string_to_binary_array(str):
    result = [[0] * 8] * len(str)
    
    for i in range(len(str)):
        result[i] = decimal_to_binary(ord(str[i]), 8)

    return result

def char_to_binary_array(char):
    result = decimal_to_binary(ord(char), 8)
    return result

def key_expansion(key_array):
    # P10
    state = permutate(key_array, P10)
    print("Key Expansion (After P10): ", state)

    state = leftshift(state, 1)

    k1 = permutate(state, P8)
    print("Key Expansion (After P8) (k1): ", k1)

    state = leftshift(state, 2)

    k2 = permutate(state, P8)
    print("Key Expansion (After P8) (k2): ", k2)

    return [k1, k2]

def single_char_sdes_encryption(char, key):
    keys = key_expansion(key)
    state = char_to_binary_array(char)

    # IP
    state = permutate(state, IP)
    print("After IP: ", state)

    left = state[:4]
    right = state[4:]

    state = f(left, right, keys[0])
    print("After fk(k1): ", state)

    left = state[:4]
    right = state[4:]
    
    state = f(right, left, keys[1])
    print("After fk(k2): ", state)

    # InvIP
    state = permutate(state, InvIP)
    print("After InvIP: ", state)

    return chr(binary_to_decimal(state))

def single_char_sdes_decryption(char, key):
    keys = key_expansion(key)
    state = char_to_binary_array(char)

    # IP
    state = permutate(state, IP)
    print("After IP: ", state)

    left = state[:4]
    right = state[4:]

    state = f(left, right, keys[1])
    print("After fk(k2): ", state)

    left = state[:4]
    right = state[4:]
    
    state = f(right, left, keys[0])
    print("After fk(k1): ", state)

    # InvIP
    state = permutate(state, InvIP)
    print("After InvIP: ", state)

    return chr(binary_to_decimal(state))


def f(left, right, key):
    # EP on right
    temp = permutate(right, EP)
    print("fk (After EP): ", temp)


    # XOR on right with key
    temp = xor(temp, key)
    print("fk (After XOR, right): ", temp)


    # SBOX
    temp_l = temp[:4]
    temp_r = temp[4:]

    temp_l = sbox(temp_l, S0)
    temp_r = sbox(temp_r, S1)

    temp = temp_l + temp_r
    print("fk (After SBOX): ", temp_l, ", ", temp_r)

    # P4
    temp = permutate(temp, P4)
    print("fk (After P4): ", temp)


    # XOR with left
    left = xor(left, temp)
    print("fk (After XOR, left): ", left)

    return left + right

def sdes_encryption(plaintext, key):
    result = ""

    for i in range(len(plaintext)):
        result += single_char_sdes_encryption(plaintext[i], key)
    
    return result

def sdes_decryption(ciphertext, key):
    result = ""

    for i in range(len(ciphertext)):
        result += single_char_sdes_decryption(ciphertext[i], key)
    
    return result

plaintext = input("Enter your plaintext: ")

cipher = sdes_encryption(plaintext, [0,1,0,1,1,0,0,1,1,1])

decrypted = sdes_decryption(cipher, [0,1,0,1,1,0,0,1,1,1])

# print("Plaintext: ", plaintext)
# print("Cipher text: ", cipher)
print("Decrypted text: ", decrypted)