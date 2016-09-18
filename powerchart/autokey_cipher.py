

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt_message(message: str) -> bytearray:
    ciphertext = bytearray('\0\0\0\0', 'ascii')
    key = 0xAB

    for character in message:
        byte = key ^ ord(character)
        key = byte
        ciphertext.append(byte)

    return ciphertext


def decrypt_message(ciphertext: bytes) -> bytearray:
    message = bytearray()
    key = 0xAB

    # Skip the first 4 bytes (this is basically the 0's we also append to messages)
    for byte in ciphertext[4:]:
        character = key ^ byte
        key = byte
        message.append(character)

    return message
