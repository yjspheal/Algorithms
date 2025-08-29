# 12712_파리퇴치3. 파리퇴치3

# import sys
#
# sys.stdin = open("input.txt", "r")


def catch_flies(arr, r, c, catch_size, len_arr):
    """
    arr[r][c]에서 크기 m짜리 파리채를 + , x자로 휘둘렀을 때 최대로 죽인 파리 수를 return

    Args:
        arr (list): 파리 정보가 담긴 이차원 배열
        r, c (int): 파리채의 중심이 될 행, 열값
        m (int): 파리채 크기
        n (int): arr 길이

    Returns:
        int: 최대로 죽인 파리 수
    """
    # 잡은 파리 수 초기화(십자든 대각이든 중심은 잡음)
    plus_catch = x_catch = arr[r][c]

    # 십자와 대각용 delta 설정
    # 순서대로 상 하 좌 우 좌상 우상 좌하 우하
    dr = [-1, 1, 0, 0, -1, -1, 1, 1]
    dc = [0, 0, -1, 1, -1, 1, -1, 1]

    # + 모양 처리 (상, 하, 좌, 우)
    for k in range(1, catch_size):
        for j in range(8):  # 십자 이동방향 4가지 + 대각 4가지
            nr = r + dr[j] * k  # 1범위 상하좌우 2범위 상하좌우 ... k범위 상하좌우를 돈다
            nc = c + dc[j] * k

            # 새로운 행과 열이 arr 범위에 있으면
            if 0 <= nr < len_arr and 0 <= nc < len_arr:

                if j < 4:  # j = 0 1 2 3은 십자용 delta
                    plus_catch += arr[nr][nc]  # 십자용 합에 더함
                else:  # 4 5 6 7은 x용 delta
                    x_catch += arr[nr][nc]

    # 둘 중 큰 것을 return한다
    return plus_catch if plus_catch > x_catch else x_catch


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, M = map(int, input().split())  # NxN의 N, 파리채 크기 M
    flies = [list(map(int, input().split())) for _ in range(N)]  # 파리 정보를 담은 arr

    # 젤 크게 잡은 파리 수 초기화
    max_fly = 0

    # 모든 행과 열을 돌며 max값을 찾는다
    for row in range(N):
        for col in range(N):
            catched_fly = catch_flies(flies, row, col, M, N)  # 이번에 잡은 파리 수 계산

            if catched_fly > max_fly:  # 만약 이번에 잡은 파리 수가 max를 넘기면 update
                max_fly = catched_fly

    print(f"#{test_case} {max_fly}")
