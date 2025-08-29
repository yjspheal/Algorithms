# 5097_회전. [파이썬 S/W 문제해결 기본] 6일차 - 회전
 

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())        # N: 자연수 갯수, M: 뒤로 보내는 작업 횟수
    nums = list(map(int, input().split()))  # 수 리스트

    print(f'#{tc} {nums[M % N]}')
