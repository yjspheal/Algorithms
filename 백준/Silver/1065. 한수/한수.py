import sys
input = sys.stdin.readline

N = int(input())

def hansu(lst):
  if len(lst) == 1:
    #print(lst, end = '  ')
    return True

  diff = int(lst[0]) - int(lst[1])
  for i in range(1, len(lst)-1):
    if int(lst[i]) - int(lst[i+1]) != diff:
      return False

  #print(lst, end = '  ')
  return True

hs = 0
for num in range(1,N+1):
  num = list(str(num))
  for i in range(len(num)):
    num[i] = int(num[i])
  if hansu(num) == True:
    hs += 1
    #print(hs)

print(hs)