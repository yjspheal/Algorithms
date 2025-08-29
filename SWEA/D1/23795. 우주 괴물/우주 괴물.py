# 23795_우주괴물 
  
"""
0 - 빈칸, 1 - 벽, 2 - 괴물
괴물은 상하좌우로 광선을 발사하며, 벽에 막하지 않는 곳까지 뻗어나간다.
안전한 빈 칸의 수를 구하라.
"""


def count_warning_areas(arr, len_arr, r, c):
    """
    행 열 길이가 len_arr인 이차원배열 arr에 대해, arr[row][col]를 기준으로
    상하좌우에서 벽(1)에 막히기 전까지의 빈 칸(0)의 수를 구하여 retur
    """

    warning_counts = 0  # 위험한 칸의 수

    dr = [-1, 1, 0, 0]
    dc = [0, 0, 1, -1]  # 행 열 델타 정의

    for i in range(4):
        k = 1
        while True:
            nr = r + dr[i] * k  # 새로운 r
            nc = c + dc[i] * k  # 새로운 c

            if 0 <= nr < len_arr and 0 <= nc < len_arr and arr[nr][nc] == '0':  # 범위에 있고 빈 칸이라면
                warning_counts += 1  # count + 1
                k += 1  # 다음 칸으로
            else:
                break

    return warning_counts


T = int(input())  # 테케 수
for tc in range(1, T + 1):
    N = int(input())  # NxN
    space = [list(input().split()) for _ in range(N)]  # 우주 정보가 들어있는 이차원배열

    empty_areas = 0  # 빈 칸 수
    warning_empty_areas = 0  # 위험 칸 수(없어도 되지만 밑에 밑줄그어지지말라고..)

    # space를 순회하며
    for row in range(N):
        for col in range(N):
            if space[row][col] == '0':  # 빈칸이라면
                empty_areas += 1
            elif space[row][col] == '2':  # 괴물이라면
                # 위험한 칸 계산
                warning_empty_areas = count_warning_areas(space, N, row, col)

    print(f'#{tc} {empty_areas - warning_empty_areas}')
