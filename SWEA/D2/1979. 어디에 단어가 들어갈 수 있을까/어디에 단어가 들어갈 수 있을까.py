# 1979. 어디에 단어가 들어갈 수 있을까

# import sys
#
# sys.stdin = open('input.txt')


def count_K_length_word(arr, k):
    """
    arr의 각 줄을 돌며, 연속되는 1의 갯수가 정확히 k개인 것의 갯수를 세서 return
    Args:
        arr (list): 0 또는 1을 원소로 갖는 이차원 배열
        k (int): 타겟 길이
    Returns:
        int: 연속되는 1의 길이가 k인 것의 갯수
    """

    k_count = 0  # k인 단어 갯수
    n = N  # 한 줄당 길이

    for line in arr:  # arr의 각 줄을 돌며
        current_length = 0  # 현재 연속되는 1의 길이

        for i, ele in enumerate(line):  # 각 줄의 원소를 돌며
            if ele == 1:  # 흰색이면
                current_length += 1  # 현재 길이에 1을 늘린다

            if ele == 0 or i == n - 1:  # 검정색이거나, 마지막이라면
                if current_length == k:  # 현재 길이가 정확히 k라면
                    k_count += 1  # k인 단어 갯수에 1을 늘린다

                current_length = 0  # 길이 초기화

    return k_count


T = int(input())
for tc in range(1, T + 1):
    N, K = map(int, input().split())
    crossword = [list(map(int, input().split())) for _ in range(N)]  # 단어퍼즐 정보
    crossword += list(map(list, zip(*crossword)))

    result = count_K_length_word(crossword, K)

    print(f'#{tc} {result}')
