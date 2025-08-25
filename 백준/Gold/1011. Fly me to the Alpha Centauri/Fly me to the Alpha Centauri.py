import sys
input = sys.stdin.readline

Test = int(input())
distance = [0]*Test

for t in range(Test):
  start, end = map(int,input().split())
  distance[t] = end - start

def count_run(D):
  if D < 4:
    return D

  for k in range(2,D):
    if D <= k ** 2:           # = (k*(k+1)) // 2 + ((k-1)*k) // 2
      return k + (k-1)          

    elif D <= k ** 2 + k:
      return k + (k-1) + 1

for d in distance:
  print(count_run(d))