# 1258_행렬찾기. [S/W 문제해결 응용] 7일차 - 행렬찾기 D4

T = int(input())
for tc in range(1, T + 1):
    N = int(input())  # NxN
    chemicals = [list(map(int, input().split())) for _ in range(N)]

    sizes = []  # 서브 matrix 크기 담을 리스트

    # 화학물질 통이 겹칠 수 없다
    dr = [0, 1]  # 우 좌
    dc = [1, 0]

    for r in range(N):
        for c in range(N):
            if chemicals[r][c] > 0:  # 화학 칸이면
                nr, nc = r, c
                while 0 <= nr + 1 < N and chemicals[nr + 1][c] > 0:  # 화학칸일 때까지 아래로
                    nr += 1

                while 0 <= nc + 1 < N and chemicals[r][nc + 1] > 0:  # 화학칸일 때까지 오른
                    nc += 1

                # 사각형을 모두 0화
                for i in range(r, nr + 1):
                    for j in range(c, nc + 1):
                        chemicals[i][j] = 0

                row = nr - r + 1  # 사이즈 계산
                col = nc - c + 1

                sizes.append((row * col, row, col))

    sizes.sort()  # 맨 앞 값 기준으로 sort

    print(f'#{tc} {len(sizes)}', end=' ')
    for size in sizes:
        print(size[1], size[2], end=' ')

    print()
