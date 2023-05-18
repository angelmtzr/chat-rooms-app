import socket

HOST = "localhost"
PORT = 5004
KEY = 14


def caesar_cipher(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            ciphertext += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext


def caesar_decipher(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isupper():
            plaintext += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            plaintext += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            plaintext += char
    return plaintext


def auth_service():
    username = input("Username: ")
    password = input("Password: ")
    return f"auth {username} {password}"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[+] Connected to server on {HOST}:{PORT}")
        # TODO: Handle different services
        req = auth_service()
        print(f"[+] Client request (decrypted): {req}")
        req = caesar_cipher(req, KEY)
        s.send(req.encode())
        print(f"[+] Request sent to server (encrypted): {req}")
        res = s.recv(1024).decode()
        print(f"[+] Response from server (encrypted): {res}")
        res = caesar_decipher(res, KEY)
        print(f"[+] Server response (decrypted): {res}")


if __name__ == "__main__":
    main()
