# 13458 시험감독

import sys

input = sys.stdin.readline
# sys.stdin = open("input.txt")

import math

# 시험장의 수
N = int(input())

# 각 시험장에 있는 응시자 수
arr = list(map(int, input().rstrip().split()))

# 주감독관 시야ㅂ 부감독관 시야
B, C = map(int, input().rstrip().split())

tester = 0

for students in arr:
    students -= B  # 총시험관 1명
    tester += 1

    if students > 0:
        if students % C == 0:
            tester += students // C
        else:
            tester += students // C + 1

print(tester)
