# 5188. [파이썬 S/W 문제해결 구현] 2일차 - 최소합

# import sys
# 
# sys.stdin = open('input.txt')

def min_sum_dfs(r, c, arr, curr_sum, N):
    """
    오른쪽 혹은 밑으로 가며 우하단까지 도달.
    지금까지 루트의 최소합을 업데이트한다.

    Args:
        r: 행
        c: 열
        arr: 배열
        curr_sum: 현재까지 루트의 합
        N: 배열의 행열 길이

    """
    global min_sum

    if r == N - 1 and c == N - 1:  # 마지막에 도달했다면
        min_sum = min(min_sum, curr_sum)  # 최소합 업데이트
        return  # 끝

    # 마지막 아니면 이동해야함
    if c < N - 1:  # 오른쪽 끝이 아니라면
        min_sum_dfs(r, c + 1, arr, curr_sum + arr[r][c + 1], N)  # 오른쪽으로 가보자

    if r < N - 1:  # 맨 아래가 아니라면
        min_sum_dfs(r + 1, c, arr, curr_sum + arr[r + 1][c], N)  # 밑으로 가보자


T = int(input())
for tc in range(1, T + 1):
    len_data = int(input())  # 가로세로칸수
    data = [list(map(int, input().split())) for _ in range(len_data)]  # 숫자 담을 이차원 배열

    min_sum = float('inf')

    min_sum_dfs(0, 0, data, data[0][0], len_data)

    print(f'#{tc} {min_sum}')
