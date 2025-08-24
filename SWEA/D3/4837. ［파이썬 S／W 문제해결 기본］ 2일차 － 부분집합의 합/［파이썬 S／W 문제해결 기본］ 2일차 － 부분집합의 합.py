# 4837. [파이썬 S/W 문제해결 기본] 2일차 - 부분집합의 합


import itertools

T = int(input().rstrip())
A = list(range(1, 13))
for tc in range(1, T+1):
    # N = 부분집합 원소의 수, 부분집합의 합 K
    N, K = map(int, input().split())
    count_K_sets = 0

    for subset in itertools.combinations(A, N):
        if sum(subset) == K:
            count_K_sets += 1

    print(f'#{tc} {count_K_sets}')
