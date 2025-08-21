import sys
input = sys.stdin.readline

N, row, col = map(int,input().split())

num = 0

while N > 0:
  num += (row // 2 **(N-1) * 2 **(N-1) * 2 ** N) + (col // 2 **(N-1) * 2 **(N-1)* 2 **(N-1))
  row %= 2 **(N-1)
  col %= 2 **(N-1)
  N -= 1

print(num)