# 2105. [모의 SW 역량테스트] 디저트 카페

# import sys
# 
# sys.stdin = open('sample_input.txt')

T = int(input())


def cal_unique_desserts(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    네 좌표를 돌며 디저트 종류 수를 return
    겹치는 게 있다면 -1을 반환한다
    """

    ate_desserts = set()  # 이미 먹은 디저트 종류 저장

    # 네 방향에 대해서 계산
    # 우하
    for x, y in zip(range(x1, x2), range(y1, y2)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  #이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 좌하
    for x, y in zip(range(x2, x3), range(y2, y3, -1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 좌상
    for x, y in zip(range(x3, x4, -1), range(y3, y4, -1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 우상
    for x, y in zip(range(x4, x1, -1), range(y4, y1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장


    return len(ate_desserts)  # 종류 return


def find_cafe_route(r, c):
    """
    해당 지점에서 시계방향으로 돌 수 있는 모든 영역을 찾아내어 리스트로 반환하는 함수
    """

    available_routes = []

    for i in range(1, N - max(r, c) + 1):  # 하우로 얼마나 이동가능?
        nr = r + i
        nc = c + i
        # 원랜 델타 썼었는데 생각해보니까 필요없음

        if 0 <= nr < N and 0 <= nc < N:  # 범위에 든다면

            for j in range(1, N - min(nr, nc) + 1):  # 하좌로 더 가자
                nr2 = nr + j
                nc2 = nc - j

                if 0 <= nr2 < N and 0 <= nc2 < N:  # 범위에 든다면
                    nr3 = nr2 - i  # nr2에서 좌상으로 i만큼 이동한 게 셋째 꼭지점
                    nc3 = nc2 - i

                    if 0 <= nr3 < N and 0 <= nc3 < N:  # 범위에 든다면

                        available_routes.append((r, c, nr, nc, nr2, nc2, nr3, nc3))

    return available_routes


# 하우, 하좌, 상좌, 상우 시계방향 회전 델타 생성
cross_delta = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

for tc in range(1, T + 1):
    N = int(input())  # 행렬 길이

    cafes = [list(map(int, input().split())) for _ in range(N)]  # 카페 정보 담은 이차원배열

    max_desserts = -1  # 디저트를 가장 많이 먹을 떄의 디저트 수

    for row in range(N - 2):  # 아래에서 2줄은 시계 루트 불가능
        for col in range(1, N - 1):  # 좌우 1줄씩 불가능
            routes = find_cafe_route(row, col)  # 가능한 루트 계산

            for rout in routes:
                current_desserts = cal_unique_desserts(*rout)

                if current_desserts > max_desserts:  # 크다면 업데이트
                    max_desserts = current_desserts

    print(f'#{tc} {max_desserts}')
