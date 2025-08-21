# 9490_풍선팡. 풍선팡

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
#
# # sys.stdin = open("sample_input.txt", "r")
# sys.stdin = open("input.txt", "r")


def calculate_flowers(arr, r, c):
    """
    k = arr[r][c]일 때, [r][[c] 위치에서 상하좌우 k범위의 값들을 모두 더하여 return 하는 함수

    Args:
        arr (list): 각 풍선별 k값이 저장되어있는 이중 리스트
        r (int): 현재 터트릴 행
        c (int): 현재 터트릴 열

    Returns:
        int: 상하좌우 k만큼 터트렸을 때 나오는 꽃가루 수의 합
    """

    dr = [-1, 1, 0, 0]      # 행 열 delta, 순서대로 상 하 좌 우
    dc = [0, 0, -1, 1]

    flowers = arr[r][c]       # 상하좌우 얼마나 터트릴지
    popped_flowers_count = flowers      # 터진 풍선 속 꽃가루도 추가

    for i in range(4):
        for k in range(1, flowers + 1):     # 1부터 flowers까지 곱한 범위를 볼 것이므로
            nr = r + dr[i] * k  # 새로운 r과 c 계산, k범위만큼 봐야하므로 둘다 k를 곱해줘야 한다.
            nc = c + dc[i] * k

            if 0 <= nr < N and 0 <= nc < M:     # nr과 nc가 arr 안에 있다면
                popped_flowers_count += arr[nr][nc]     # 그 안에 든 꽃가루 수를 popped flowers count에 추가

    return popped_flowers_count

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N, M = map(int, input().split())  # 행, 열 길이
    arr = [list(map(int, input().split())) for _ in range(N)]  # arr 받아오기

    max_flowers = 0     # 최대값 초기화
    # 행과 열을 순회하며
    for row in range(N):
        for col in range(M):
            popped_flowers = calculate_flowers(arr, row, col)       # 해당 좌표에서의 터진 꽃가루 수 계산

            if popped_flowers > max_flowers:                # 지금까지의 max값을 넘어섰다면 update
                max_flowers = popped_flowers

    print(f'#{tc} {max_flowers}')
