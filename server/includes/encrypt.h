#ifndef CHAT_ROOMS_SERVER_ENCRYPT_H
#define CHAT_ROOMS_SERVER_ENCRYPT_H

void caesar_cipher(const char *plaintext, char *ciphertext, int shift);
void caesar_decipher(const char *ciphertext, char *plaintext, int shift);

#endif //CHAT_ROOMS_SERVER_ENCRYPT_H
