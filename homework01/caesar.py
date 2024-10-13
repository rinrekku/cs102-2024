"""Module for Caesar encryption"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for b in plaintext:
        symbol = ""

        if ord("A") <= ord(b) <= ord("Z"):
            symbol = chr((ord(b) - ord("A") + shift) % (ord("Z") - ord("A") + 1) + ord("A"))
        elif ord("a") <= ord(b) <= ord("z"):
            symbol = chr((ord(b) - ord("a") + shift) % (ord("z") - ord("a") + 1) + ord("a"))
        else:
            symbol = b
        ciphertext += symbol

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for b in ciphertext:
        symbol = ""

        if ord("A") <= ord(b) <= ord("Z"):
            symbol = chr((ord(b) - ord("A") - shift) % (ord("Z") - ord("A") + 1) + ord("A"))
        elif ord("a") <= ord(b) <= ord("z"):
            symbol = chr((ord(b) - ord("a") - shift) % (ord("z") - ord("a") + 1) + ord("a"))
        else:
            symbol = b
        plaintext += symbol

    return plaintext
