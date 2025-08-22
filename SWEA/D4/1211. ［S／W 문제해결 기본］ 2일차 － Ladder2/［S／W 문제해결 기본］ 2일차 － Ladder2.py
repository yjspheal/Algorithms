# 1211. [S/W 문제해결 기본] 2일차 - Ladder2

# import sys
#
# sys.stdin = open('input.txt')


def down_ladder(arr, c):
    """
    arr[0][c] 지점에서 사다리를 내려가는 루트에 드는 길이를 구하여 return
    Args:
        arr (list): 1, 0으로 이루어진 100x100 행렬
        c (int): 시작점의 x값
    Returns:
        int: 루트 길이
    """
    r = 0  # 시작점의 행
    route_length = 0  # 루트의 길이 계산

    while r < 100:  # 바닥에 닿기 전까지
        if arr[r][c - 1] == 1:  # 왼쪽에 길이 있다면
            while arr[r][c - 1] == 1:  # 왼쪽 끝까지 간다
                c -= 1
                route_length += 1  # 루트 길이에 1 추가

        elif arr[r][c + 1] == 1:  # 오른쪽에 길이 있다면
            while arr[r][c + 1] == 1:  # 오른쪽 끝까지 간다
                c += 1
                route_length += 1  # 루트 길이에 1 추가

        r += 1  # 아래로 한칸 간다
        route_length += 1  # 루트 길이에 1 추가

        while r < 100 and arr[r][c - 1] == 0 and arr[r][c + 1] == 0:  # 바닥이 아니고 양쪽이 벽이라면
            r += 1
            route_length += 1  # 사다리가 나오거나 받가이 나올 때까지 밑으로 간다

    return route_length


T = 10
for _ in range(1, T + 1):
    tc = input()
    ladder = []  # 사다리 정보를 담은 이차원 배열

    for __ in range(100):  # 사다리는 100x100
        # 양쪽에 벽을 하나씩 둔다(셀렉션)
        ladder.append([0] + list(map(int, input().split())) + [0])

    start_points = []  # 시작점 인덱스들을 모을 리스트
    for i in range(101):
        if ladder[0][i] == 1:  # 시작점이라면 인덱스 추가
            start_points.append(i)

    # 초기값 설정
    shortest_length = down_ladder(ladder, start_points[0])
    shortest_x = start_points[0]

    for start_point in start_points[1:]:  # 첫번째 건 위에서 했으므로
        current_length = down_ladder(ladder, start_point)  # 이번 start point의 루트 길이

        if current_length < shortest_length:  # 더 짧다면 루트 길이와 x를 업데이트
            shortest_length = current_length
            shortest_x = start_point

    print(f'#{tc} {shortest_x - 1}')  # 앞에 셀렉션 제외
