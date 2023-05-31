#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#ifndef ENCRYPT_H
#define ENCRYPT_H

char *caesar_cipher(const char *text, int shift) {
  char *encrypted_text = malloc(strlen(text) * sizeof(char));
  char c;
  for (int i = 0; text[i] != '\0'; i++) {
    c = text[i];
    if (isupper(c)) {
      encrypted_text[i] = (char) (((int) c + (int) shift - 65) % 26 + 65);
    } else if (islower(c)) {
      encrypted_text[i] = (char) (((int) c + (int) shift - 97) % 26 + 97);
    } else {
      encrypted_text[i] = c;
    }
  }
  encrypted_text[strlen(text)] = '\0';
  return encrypted_text;
}

char *caesar_decipher(const char *encrypted_text, int shift) {
  char *decrypted_text = malloc(strlen(encrypted_text) * sizeof(char));
  char c;
  for (int i = 0; encrypted_text[i] != '\0'; i++) {
    c = encrypted_text[i];
    if (isupper(c)) {
      decrypted_text[i] = (char) (((int) c - (int) shift - 65 + 26) % 26 + 65);
    } else if (islower(c)) {
      decrypted_text[i] = (char) (((int) c - (int) shift - 97 + 26) % 26 + 97);
    } else {
      decrypted_text[i] = c;
    }
  }
  decrypted_text[strlen(encrypted_text)] = '\0';
  return decrypted_text;
}

#endif //ENCRYPT_H
