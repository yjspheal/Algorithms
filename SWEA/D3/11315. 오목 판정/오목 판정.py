# 11315_오목판정. 오목 판정
"""
idea
첫줄부터 돌면서, 돌을 만나면  우 우하 하 좌하 네 방향을 탐색하며 오목여부를 계산한다
"""
# import sys
#
# sys.stdin = open('input.txt')


def check_omok(arr):
    """
    arr를 돌며, 가로 세로 대각선 방향으로 O가 연속 다섯 개 있는지 여부를 판단하여 return
    Args:
        arr(list): .과 O로 이루어진 이차원 리스트
    Returns:
        str: 다섯개 있다면 YES, 없다면 NO를 반환
    """
    dr = [0, 1, 1, 1]
    dc = [1, 1, 0, -1]  # 우 우하 하 좌하 델타

    n = N  # 바둑판 한줄 길이

    # 바둑판을 돌며
    for r in range(n):
        for c in range(n):
            if arr[r][c] == 'o':  # 돌이면
                current_mok = 1  # 현재 연속 돌에 1 할당

                for i in range(4):  # 네가지 방향 탐색
                    for k in range(1, 5):   # 현재 다음부터 4개까지만 연속인지 보면 됨
                        nr = r + dr[i] * k
                        nc = c + dc[i] * k

                        if 0 <= nr < N and 0 <= nc < N and arr[nr][nc] == 'o':      # 바둑판 안에 있고 또 돌이면
                            current_mok += 1    # 목 + 1

                        else:
                            break   # 아닌 순간 바로 break하여 다음 방향 탐색

                    else:   # 다섯개를 다 봤는데 break가 안 됐다면 오목
                        return 'YES'

    # 리턴이 한번도 안 됐다면, 즉 오목이 없다는 것
    else:
        return 'NO'


T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    baduk = [list(input()) for _ in range(N)]

    result = check_omok(baduk)
    print(f'#{tc} {result}')
