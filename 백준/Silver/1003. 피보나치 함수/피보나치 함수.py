import sys
input = sys.stdin.readline

T = int(input())
nums = [0] * T

for t in range(T):
  nums[t] = int(input())

def fibo_01(n):
  if n == 0:
    return 1, 0
  elif n == 1:
    return 0, 1

  fibo = [0] * n #T번까지 피보나치

  fibo[0] = 1;fibo[1]=1
  for i in range(2,n):   #피보나치 만들기
    fibo[i] = fibo[i-1] + fibo[i-2]

  return fibo[-2], fibo[-1]

zeros = []
ones = []

for num in nums:
  z, o = fibo_01(num)
  zeros.append(z);ones.append(o)

for i in range(T):
  print(zeros[i], ones[i])