# 1949. [모의 SW 역량테스트] 등산로 조성

# import sys
# 
# sys.stdin = open('input.txt')


def update_longest(l):
    """
    루트의 길이 l이 기존 최장 길이(전역 변수)보다 높다면 최장 길이를 업데이트하는 함수
    """
    global longest_route

    if l > longest_route:
        longest_route = l


def find_route(r, c, route_length, is_worked):
    """
    현재 지도의 좌표와 공사 여부를 인자로 받아, 다음 이동할 위치를 계속 찾아가며
    하나의 루트를 찾아내는 재귀함수
    Args:
        r (int): 현재 위치의 행 좌표
        c (int): 현재 위치의 열 좌표
        route_length (int): 현재까지 거쳐온 루트의 길이
        is_worked (bool): 공사 했는지 여부 표시 bool
    """

    for i in range(4):  # 상하좌우를 돌며
        nr = r + dr[i]  # 새 좌표 계산
        nc = c + dc[i]

        if (
                0 <= nr < LENGTH and 0 <= nc < LENGTH and  # 다음 위치가 범위에 들고
                not visited[nr][nc]  # 방문한 적이 없다면
        ):

            if mountains[nr][nc] < mountains[r][c]:  # 현재 위치보다 봉우리가 낮다면
                visited[nr][nc] = True  # 여기 방문 완
                find_route(nr, nc, route_length + 1, is_worked)  # 새 좌표, 길이+1, 공사진행여부유지 후 재귀
                visited[nr][nc] = False  # 여기 방문 취소

            elif mountains[nr][nc] >= mountains[r][c] and is_worked is False:  # 봉우리는 높지만 공사를 아직 안 했다면
                height_diff = mountains[nr][nc] - mountains[r][c]  # 높이 차 계산

                if WORK_DEPTH > height_diff:  # 공사 가능 깊이가 높이 차보다 크다면
                    origin = mountains[nr][nc]
                    mountains[nr][nc] = mountains[r][c] - 1  # 다음 높이를 현재높이 - 1로 만들고 함수를 돌린다

                    visited[nr][nc] = True  # 여기 방문 완
                    find_route(nr, nc, route_length + 1, True)
                    visited[nr][nc] = False  # 여기 방문 취소

                    mountains[nr][nc] = origin  # 다시 돌아와~

                # 아니면 계산할 필요가 없다...


    else:  # 언젠가는 공사도 하고 사방이 현재위치보다 높아져서 for문을 못 도는 때가 온다
        update_longest(route_length)
        return


T = int(input())

dr = [-1, 1, 0, 0]  # 상하좌우 델타
dc = [0, 0, -1, 1]

for tc in range(1, T + 1):

    # 지도 한 변의 길이, 최대 공사 가능 깊이
    LENGTH, WORK_DEPTH = map(int, input().strip().split())

    mountains = [list(map(int, input().split())) for _ in range(LENGTH)]  # 산 정보 담을 리스트

    highest_height = 0  # 젤 높은 산 높이
    highest_spots = set()  # 젤 높은 산의 좌표 담을 set

    for idx_row, row in enumerate(mountains):
        for idx_col, mountain in enumerate(row):

            if mountain > highest_height:  # 젤높은 키를 갱신했다면
                highest_height = mountain
                highest_spots = set()  # 지금까지 담은 젤 높은 키 집합을 리셋하고
                highest_spots.add((idx_row, idx_col))  # 좌표를 추가

            elif mountain == highest_height:  # 동일하다면 좌표만 추가
                highest_spots.add((idx_row, idx_col))

    longest_route = 0  # 젤 긴 루트 길이

    # 젤 높은 산들의 좌표를 돌며
    for h_r, h_c in highest_spots:
        visited = [[False] * LENGTH for _ in range(LENGTH)]  # 방문여부
        visited[h_r][h_c] = True  # 여기 방문 완
        find_route(h_r, h_c, 1, False)  # 아직 안 했으니까 공사여부 False

    print(f'#{tc} {longest_route}')
