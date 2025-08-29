# 1206. [S/W 문제해결 기본] 1일차 - View 

T = 10
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    # 첫줄엔 빌딩의 갯수가
    building_count = int(input())
    # 그 다음 줄엔 빌딩의 높이가
    buildings = list(map(int, input().split()))

    # 조망권 확보 세대 수
    nice_view_count = 0

    # 현재 빌딩을 기준으로 왼쪽 2개와 오른쪽 2개보다 높은 부분만 조망권이 확보됨
    # 모든 빌딩을 돌며 좌2 우2 비교
    for idx in range(2, building_count - 2):
        # 현재 빌딩 높이
        current_building = buildings[idx]

        # idx(현재 빌딩) 제외 좌우 4개 중 가장 높은 빌딩 높이 찾기
        max_building = 0
        for j in range(idx-2, idx+3):
            if j == idx:
                continue
            if buildings[j] > max_building:
                max_building = buildings[j]

        # 현재 빌딩 높이에서 max_building 뺀 값이 0 이상이면 조망권 확보세대 +
        # 아니면 0 더함
        nice_view_count += current_building - max_building if current_building - max_building >= 0 else 0

    print(f'#{tc} {nice_view_count}')