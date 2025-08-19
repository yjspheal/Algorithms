# 1094 막대기

import sys
input = sys.stdin.readline

X = int(input().rstrip())

count = 0
# 어차피 2의 지수, 1 2 4 8 .. 이중에 필요한거 하나씩 골라서 만들게된다
for k in [64, 32, 16, 8 , 4, 2, 1]:
    if X >= k:
        X -= k
        count += 1

print(count)