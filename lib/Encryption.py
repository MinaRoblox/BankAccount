alphabet = ['!', '@', '#', '$', '%', '^', '&', '*', "/", "¿", "?", " ",
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
            'm', 'n', "ñ", 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
            'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
            'á', "Á", "e", "É", "í", "Í", "ó", "Ó", "ú", "Ú", 
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            "{", "}", "(", ")", ".", ","]  # <- added digits to alphabet

combos = ["5UN/", ")dg(6$)", "f+1-¡", "h,so1T.{[oi]}"]

def get_combo(key):
    if 0 <= key <= 492:
        return combos[0]
    elif 493 <= key <= 940:
        return combos[1]
    elif 941 <= key <= 1486:
        return combos[2]
    elif 1487 <= key <= 2956:
        return combos[3]
    else:
        return "8BY98N4Y384NFYU398K0UW9!"

def Encrypt(key, value):
    combo = get_combo(key)
    encryptedString = ""
    grb = value[2] if len(value) >= 3 else '!'  # fallback if too short

    for letter in value:
        if letter not in alphabet:
            raise ValueError(f"Unsupported character in input: '{letter}'")

        pos = alphabet.index(letter)
        let = combo[3]
        encryptedString += grb + combo + let + f"{pos + 31:03}"  # fixed length

    return encryptedString

def Decrypt(key, encryptedString):
    combo = get_combo(key)
    decrypted = ""
    i = 0
    combo_len = len(combo)

    while i < len(encryptedString):
        if i + 1 + combo_len + 1 + 3 > len(encryptedString):
            raise ValueError("Encrypted string is malformed or incomplete.")

        grb = encryptedString[i]
        i += 1

        enc_combo = encryptedString[i:i + combo_len]
        if enc_combo != combo:
            raise ValueError(f"Combo mismatch: expected {combo}, got {enc_combo}")
        i += combo_len

        let = encryptedString[i]
        i += 1

        num_str = encryptedString[i:i + 3]
        if not num_str.isdigit():
            raise ValueError(f"Expected digits at position {i}, got '{num_str}'")
        pos = int(num_str) - 31
        if pos < 0 or pos >= len(alphabet):
            raise ValueError(f"Invalid position: {pos}")
        decrypted += alphabet[pos]
        i += 3

    return decrypted
