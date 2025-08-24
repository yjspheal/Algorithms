# 11092. 최대 최소의 간격

T = int(input())
for tc in range(1, T + 1):
    N = int(input())

    arr = list(map(int, input().split()))

    min_idx = max_idx = 0
    # arr를 순회하며
    for i in range(N):
        # 작은 수가 여러개이면 먼저 나오는 위치
        if arr[i] < arr[min_idx]:
            min_idx = i

        # 큰 수가 여러 개이면 마지막으로 나오는 위치
        if arr[i] >= arr[max_idx]:
            max_idx = i

    print(f'#{tc} {abs(min_idx - max_idx)}')
