import sys
input = sys.stdin.readline

N = int(input())
nums = list(map(int,input().split()))

i = 0
result = {}
for idx in range(21):
  result[idx] = 0

result[nums[0]] = 1

while i < N - 2:
  i += 1
  res = {}
  for n in range(21):
    res[n] = 0
    try:
      res[n] += result[n + nums[i]]
    except:
      pass

    try:
      res[n] += result[n - nums[i]]
    except:
      pass

  result = res

print(result[nums[-1]])