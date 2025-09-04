# 2115. [모의 SW 역량테스트] 벌꿀채취

# import sys
# 
# sys.stdin = open('input.txt')

def cal_max_square(arr, C):
    """
    일차원 리스트를 인자로 받아, 원소합이 C 이하인 경우인 부분집합의 제곱합의 최대값을 return하는 함수
    Args:
        arr: 일차원 리스트

    Returns:
        int: 조건 만족하는 부분집합의 제곱합의 최대값
    """

    len_arr = len(arr)

    max_subset_sum = 0

    # 1000...(k+1자리) 전까지 순회하며
    for i in range(1, 1 << len_arr):
        subset = []
        current_sum = 0     # 현재 합

        for j in range(len_arr):
            if i & (1 << j):    # i의 j번째 자리가 1이라면
                current_sum += arr[j]   # arr의 j번째 숫자를 더한다
                subset.append(arr[j])       # 부분지합 생성

        if current_sum <= C:    # 합이 C 이하라면
            max_subset_sum = max(max_subset_sum, sum([i**2 for i in subset]))

    return max_subset_sum


def find_honey_pair(arr, N, M, C):
    """
    작업자 A의 위치를 좌상단부터 하나씩 늘려가며 작업량 계산 후, B가 위치할 수 있는 모든 경우의 수를 계산
    최대 작업량을 update해가는 함수

    Args:
        arr (list): 1~9 자연수로 이루어진 이중리스트
        N (int): arr의 행,열 길이
        M (int): 연속으로 선택할 수 있는 수
        C (int): 최대 꿀 양

    Returns:
        None

    Notes:
        전역변수 max_sum을 직접 업데이트합니다.
    """
    global max_sum

    # A가 가능한 위치 구하기
    for r_A in range(N):  # A가 있는 행부터 전체를 돌 것
        for c_A in range(N):
            c_end_A = min(c_A+M-1, N-1)     # M개 선택 vs 끝까지

            cand_A = arr[r_A][c_A:(c_end_A + 1)]        # 선택한 M 범위의 리스트에서

            sum_A = cal_max_square(cand_A, C)   # 합이 C 이하인 최대의 부분집합

            # B가 가능한 위치 구하기
            for r_B in range(r_A, N):  # A가 있는 행부터 전체를 돌 것
                for c_B in range(N):

                    if r_B == r_A and c_B <= c_end_A:  # 이미 A가 먹은 곳이라면 다음으로
                        continue

                    # A와 똑같이 열 끝값 구하기
                    c_end_B = min(c_B + M - 1, N - 1)  # M개 선택 vs 끝까지

                    cand_B = arr[r_B][c_B:(c_end_B + 1)]  # 선택한 M 범위의 리스트에서

                    sum_B = cal_max_square(cand_B, C)  # 합이 C 이하인 최대의 부분집합

                    max_sum = max(max_sum, sum_A + sum_B)  # max_sum 업데이트


T = int(input())
for tc in range(1, T + 1):
    # 꿀통 리스트 크기, 선택할 연속 꿀통 수, 꿀 채취 가능 양
    len_honey, conti, max_honey = map(int, input().split())
    honey = [list(map(int, input().split())) for _ in range(len_honey)]  # 꿀통 정보 담은 이중 리스트

    max_sum = 0
    find_honey_pair(honey, len_honey, conti, max_honey)

    print(f'#{tc} {max_sum}')
