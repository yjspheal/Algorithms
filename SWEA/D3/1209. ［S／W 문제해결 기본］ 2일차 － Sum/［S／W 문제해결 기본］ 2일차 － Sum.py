# 1209. [S/W 문제해결 기본] 2일차 - Sum

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# # sys.stdin = open("sample_input.txt", "r")
# sys.stdin = open("input.txt", "r")

T = 10      # 10개 테케로 고정
N = 100     # N x N의 N은 100으로 고정

# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for _ in range(1, T + 1):
    tc = int(input())       # 테케 번호가 들어옴

    arr = [tuple(map(int, input().split())) for _ in range(N)]    # 튜플을하면 머라도 나아지지ㅣ않읗까?

    # 모든것의 최대합 초기화
    max_sum = 0

    # 대각선 합 초기화
    right_diagonal_sum = 0
    left_diagonal_sum = 0

    # 하나는 고정된 채로 나머지 하나가 도는 루프 생성
    for i in range(N):
        row_sum = 0
        col_sum = 0
        for j in range(N):
            # 그럼 한번에 가로합과 세로합을 볼 수 있다
            row_sum += arr[i][j]
            col_sum += arr[j][i]

            # 대각 위치에 해당한다면 대각합 ㄱㄱ
            if i == j:
                right_diagonal_sum += arr[i][j]
            if i == N - 1 - j:
                left_diagonal_sum += arr[i][j]

        # 현재 sum들 중 하나라도 최대를 갱신한 게 있으면 업데이트
        for num in [row_sum, col_sum, right_diagonal_sum, left_diagonal_sum]:
            if num > max_sum:
                max_sum = num

    print(f'#{tc} {max_sum}')