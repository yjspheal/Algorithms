#  5202. [파이썬 S/W 문제해결 구현] 3일차 - 화물 도크

# import sys
# 
# sys.stdin = open('input.txt')

from collections import deque

T = int(input())
for tc in range(1, T + 1):
    N = int(input())  # 신청서

    q = []

    for _ in range(N):  # 모든 신청 정보 담기
        q.append(list(map(int, input().split())))

    q.sort(key=lambda x: x[1])  # 끝나는 값 기준으로 sort
    q = deque(q)

    work = 0  # 작업한 횟수
    past_end = 0  # 이전 작업이 0시에 끝났다고 가정
    while q:
        curr_start, curr_end = q.popleft()
        if curr_start >= past_end:  # 저번 작업 끝난 이후라면
            work += 1  # 작업하고
            past_end = curr_end  # 종료 시간을 업데이트한다

    print(f'#{tc} {work}')
