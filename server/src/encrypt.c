#include <ctype.h>
#include "../includes/encrypt.h"

void caesar_cipher(const char *plaintext, char *ciphertext, int shift) {
  if (plaintext == NULL || ciphertext == NULL)
    return;

  int len = strlen(plaintext);
  int uppercaseA = (int) 'A';
  int lowercaseA = (int) 'a';

  for (int i = 0; i < len; i++) {
    char c = plaintext[i];

    if (isalpha(c)) {
      int base = isupper(c) ? uppercaseA : lowercaseA;
      int offset = ((int) c - base + shift) % 26;
      ciphertext[i] = (char) (base + offset);
    } else {
      ciphertext[i] = c;
    }
  }
  ciphertext[len] = '\0';
}

void caesar_decipher(const char *ciphertext, char *plaintext, int shift) {
  if (ciphertext == NULL || plaintext == NULL)
    return;

  int len = strlen(ciphertext);
  int uppercaseA = (int) 'A';
  int lowercaseA = (int) 'a';

  for (int i = 0; i < len; i++) {
    char c = ciphertext[i];

    if (isalpha(c)) {
      int base = isupper(c) ? uppercaseA : lowercaseA;
      int offset = ((int) c - base - shift + 26) % 26;
      plaintext[i] = (char) (base + offset);
    } else {
      plaintext[i] = c;
    }
  }
  plaintext[len] = '\0';
}