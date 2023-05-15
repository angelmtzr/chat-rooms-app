#include <ctype.h>
#include "../includes/encrypt.h"

void caesar_cipher(const char *plaintext, char *ciphertext, int shift) {
  char c;
  for (int i = 0; plaintext[i] != '\0'; i++) {
    c = plaintext[i];
    if (isupper(c)) {
      ciphertext[i] = (char) (((int) c + (int) shift - 65) % 26 + 65);
    } else if (islower(c)) {
      ciphertext[i] = (char) (((int) c + (int) shift - 97) % 26 + 97);
    } else {
      ciphertext[i] = c;
    }
  }
}

void caesar_decipher(const char *ciphertext, char *plaintext, int shift) {
  char c;
  for (int i = 0; ciphertext[i] != '\0'; i++) {
    c = ciphertext[i];
    if (isupper(c)) {
      plaintext[i] = (char) (((int) c - (int) shift - 65 + 26) % 26 + 65);
    } else if (islower(c)) {
      plaintext[i] = (char) (((int) c - (int) shift - 97 + 26) % 26 + 97);
    } else {
      plaintext[i] = c;
    }
  }
}