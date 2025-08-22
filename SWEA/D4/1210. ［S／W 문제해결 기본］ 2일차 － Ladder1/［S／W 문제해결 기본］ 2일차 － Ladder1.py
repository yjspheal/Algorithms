# 1210. [S/W 문제해결 기본] 2일차 - Ladder1

"""
idea
1. 도착지에서 시작해서 거슬러 올라간다.
2. 좌 or 우를 만난다면 막힐 때까지, 즉 1인동안 해당 방향으로 계속 이동
3. 막히면, 좌우를 만날 때까지 올라간다.
4. 행이 0이되면 해당 col값을 출력

[제약 사항]
한 막대에서 출발한 가로선이 다른 막대를 가로질러서 연속하여 이어지는 경우는 없다.
"""

def climb_ladder(arr, end_c):
    """
    0(벽), 1(길), 2(도착점)로 이루어진 이차원 리스트 arr에 대해서, 1만을 이어서 2에 도달하게 되는 루트의 시작점의 col값을 반환
    단, 경로는 위에서 아래로만 진행되어야 함

    Args:
        arr (list): 0, 1, 2로 이루어진 이차원 리스트
        end_c (int): 도착점의 열 값

    Returns:
        int: 시작점의 col 값
    """
    N = 100     # 총 행 수

    r = N - 1      # 현재는 마지막줄이므로 99에 위치
    c = end_c   # 현재 col 위치

    # 방금까지 왼쪽으로 왔으면 오른쪽에 길이 있는 것이 당연
    # 그렇게 가면 무한으로 도므로 방지용 변수 제작
    going_right = False
    going_left = False

    while r > 0:    # 행이 0이 되면 끝
        # 왼쪽에 길이 있다면
        if 0 <= c - 1 < N and arr[r][c - 1] == 1 and not going_right:
            # 끝까지 간다
            while True:
                going_left = True
                c -= 1
                if c == 0 or arr[r][c-1] == 0:      # 열이 0, 즉 왼쪽 끝에 도달했거나 벽에 막히게되면 break
                    r -= 1 if r > 0 else 0     # 첫줄이 아니라면 1 올라간다
                    break

        # 오른쪽에 길이 있다면
        # print(r, c)
        if 0 <= c + 1 < N and arr[r][c + 1] == 1 and not going_left:
            # 끝까지 간다
            while True:
                going_right = True
                c += 1
                if c == 99 or arr[r][c+1] == 0:      # 열이 99, 즉 오른쪽 끝에 도달했거나 벽에 막히게되면 break
                    r -= 1 if r > 0 else 0     # 첫줄이 아니라면 1 올라간다
                    break

        # 좌우가 막혔다면 위로 올라감. 다만 이번엔 막힐 때까지가 아닌, 다음 좌우가 나올 때까지.
        while (r > 0) and (c == 0 and arr[r][c+1] == 0) or (c == 99 and arr[r][c-1] == 0) or (1 <= c < N and arr[r][c-1] == 0 and arr[r][c+1] == 0):
        # 너무 긴데...?
            going_left = going_right = False    # 로 초기화
            r -= 1
            if r == 0:  # 첫 행에 도달했다면 break
                break

    # 현재 c가 출발 c가 된다.
    return c

T = 10  # 테케 10으로 고정
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    _ = int(input())  # 테케 번호와 동일
    ladder = [list(map(int, input().split())) for _ in range(100)]  # 사다리 정보 담긴 이차원 배열

    # 도착점 찾기
    end_col = 0
    for c in range(100):
        if ladder[-1][c] == 2:      # 2는 항상 마지막줄에있으므로
            end_col = c

    # 첫 col값 찾기
    start_col = climb_ladder(ladder, end_col)

    print(f'#{tc} {start_col}')
