# 20230. 풍선팡 보너스게임2

# import sys
#
# sys.stdin = open("sample_in.txt")

T = int(input())
for tc in range(1, T + 1):
    N = int(input())

    row_sums = [0] * N  # 행, 열별 합 담는 리스트
    col_sums = [0] * N

    # 풍선 숫자 정보를 담은 이차원배열
    balloons = [list(map(int, input().split())) for _ in range(N)]

    for r in range(N):
        for c in range(N):
            # 합 생성
            row_sums[r] += balloons[r][c]
            col_sums[c] += balloons[r][c]

    max_score = 0
    for r in range(N):
        for c in range(N):
            score = row_sums[r] + col_sums[c] - balloons[r][c]

            if score > max_score:
                max_score = score
    print(f'#{tc} {max_score}')
