# 1953 탈주범 검거
"""
흉악범 탈주 후 1시간 후 맨홀로 뛰어들어감
현재 k시간 지남
지금 있을 수 있는 위치 수 계산할 것
"""


def track_criminal(r, c, spent_time):
    """
    현재 위치를 인자로 받아, 다음 위치를 다시 인자로 넣는 재귀함수
    K 시간이 지난 시점에, 도착 arr를 True로 만든다.

    Returns:

    """

    # 거쳐가는 순간 범죄자 가능 위치 True로
    if criminal_spot[r][c] > K + 1 - spent_time:
        # 다른곳에서 계산할것이다.
        return
    else:
        criminal_spot[r][c] = K + 1 - spent_time      # 남은 루트의 길이를 저장

    if spent_time == K:  # K시에 도달했다면
        # criminal_spot[r][c] = True      # 범죄자 가능 위치 True로
        # criminal_spot[r][c] = 1      # 범죄자 가능 위치 True로
        return  # 끝

    else:  # 아직이면 계속 돌려
        ele = underground[r][c]
        delta_list = turnel[underground[r][c]]
        # delta_list =
        for dr, dc in delta_list:  # 델타를 돌며
            nr = r + dr  # 새 위치 계산
            nc = c + dc

            a = 1
            pass
            # 범위에 들고 0이 아니
            if (
                    0 <= nr < LEN_ROW and  # 범위에 들고
                    0 <= nc < LEN_COL and
                    underground[nr][nc] and  # 0이 아니며
                    (-dr, -dc) in turnel[underground[nr][nc]]  # 그 터널이랑 이어진 모양새라면
            ):
                track_criminal(nr, nc, spent_time + 1)  # 도둑 보내
            else:  # 벗어나면
                continue  # 다음으로


T = int(input())
turnel = {
    # 1: [(-1, 0), (1, 0), (0, -1), (0, 1)],  # 상하좌우
    1: [(0, 1), (1, 0), (0, -1), (-1, 0)],  # 우하좌상
    2: [(-1, 0), (1, 0)],  # 상하
    3: [(0, -1), (0, 1)],  # 좌우
    4: [(-1, 0), (0, 1)],  # 상우
    5: [(1, 0), (0, 1)],  # 하우
    6: [(1, 0), (0, -1)],  # 하좌
    7: [(-1, 0), (0, -1)],  # 상좌
}

for tc in range(1, T + 1):
    # 첫 줄에는 지하 터널 지도의 세로 크기 N, 가로 크기 M, 맨홀 뚜껑이 위치한장소의 세로 위치 R, 가로 위치 C, 그리고 탈출 후 소요된 시간 K 이 주어진다.
    LEN_ROW, LEN_COL, R, C, K = map(int, input().split())

    underground = [list(map(int, input().split())) for _ in range(LEN_ROW)]

    # 범죄자 스팟 저장할 array
    criminal_spot = []
    for _ in range(LEN_ROW):
        # criminal_spot.append([False] * LEN_COL)
        criminal_spot.append([0] * LEN_COL)

    # 범죄자 돌리기. 초기는 R C 1시간
    track_criminal(R, C, 1)

    # 범죄자 수 계산
    spot_count = 0
    for i in range(LEN_ROW):
        for j in range(LEN_COL):
            spot_count += 1 if criminal_spot[i][j] else 0

    print(f'#{tc} {spot_count}')
