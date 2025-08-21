s_number = list(range(1,31))

for time in range(28):
  student = int(input())
  del s_number[s_number.index(student)]

for s in s_number:
  print(s)