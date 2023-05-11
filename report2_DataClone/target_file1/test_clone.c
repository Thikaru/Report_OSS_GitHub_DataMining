#include <stdio.h>

int main() {
  char a[] = "TEST\n";

  // same(1)
  print("TEST\n");
  // same(1)
  print("%s", a);

  // same(2)
  int num[10], i;
  for (i = 0; i < 10; i++) {
    num[i] = i;
  }

  // same(3)
  for (i = 0; i < 10; i++) {
    printf("num[%d] = %d\n", i, num[i]);
  }

  // same(4)
  for (i = 0; i < 10; i++) {
    num[i] = i * i;
  }

  // same(4)
  for (i = 0; i < 10; i++) {
    num[i] = i * i;
  }

  // same(4)
  for (i = 0; i < 10; i++) {
    num[i] = i * i;
  }

  // same(3)
  for (i = 0; i < 10; i++) {
    printf("num[%d]", i);
    printf(" ");
    printf("=");
    printf(" ");
    printf("%d", num[i]);
    printf("\n");
  }

  // same(4)
  for (i = 0; i < 10; i++) {
    num[i] = num[i] * i;
  }

  // same(4)
  for (i = 0; i < 10; i++) {
    num[i] = num[i] * num[i];
  }

  // same(3)
  for (i = 0; i < 10; i++) {
    printf("num[%d] = %d\n", i, num[i]);
  }
}