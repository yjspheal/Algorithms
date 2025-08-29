# 2001. 파리 퇴치

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# # sys.stdin = open("input.txt", "r")
# sys.stdin = open("input.txt", "r")

def catch_flies(arr, r, c):
    """
    arr[r][c], arr[r + M-1][c], arr[r][c + M-1], arr[r + M-1][c + M-1] 범위 내의 모든 원소 값을 더하여 return
    M은 global에 선언되어있음

    Args:
         arr (list): 이차원 배열
         r (int): 타겟 행
         c (int): 타겟 열
         M (int): 계산할 범위

    Returns:
        int: 모든 원소값을 더한 값

    Notes:
        arr는 NxN행렬 이다.
    """

    count = 0
    # arr를 순회하며 잡는 모기 수를 더한다
    for i in range(r, r + M):
        for j in range(c, c + M):
            count += arr[i][j]

    return count

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N, M = map(int, input().split())        # 행렬 크기, 파리채 길이

    fly_arr = [list(map(int, input().split())) for _ in range(N)]       # 파리 정보 담은 arr

    max_flies_count = 0     # 제일 많이 잡은 파리 수

    # +M 한 곳까지의 범위를 봐야하므로 아래와 같이 범위 지정
    for row in range(N - M + 1):
        for col in range(N - M + 1):
            flies_count = catch_flies(fly_arr, row, col)

            if flies_count > max_flies_count:       # 만약 현재 잡은 파리 수가 최대치 갱신했다면 update
                max_flies_count = flies_count

    print(f'#{tc} {max_flies_count}')