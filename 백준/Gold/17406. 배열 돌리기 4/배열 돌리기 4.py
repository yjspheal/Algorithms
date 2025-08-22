# 배열 돌리기 4

import sys

input = sys.stdin.readline
# sys.stdin = open('input.txt')

import itertools
from copy import deepcopy


def rotate_clockwise_arr(arr, mid_r, mid_c, s):
    """
    arr[mid_r][mid_c]를 중심으로, s길이만큼 시계방향으로 1만큼 rotate하는 함수

    Args:
        arr (list): 숫자로 이루어진 이중리스트
        mid_r (int): 중심이 될 행의 인덱스
        mid_r (int): 중심이 될 열의 인덱스
        s (int): rotate시킬 범위

    Notes:
        arr 원본을 변환합니다.
    """
    for i in range(1, s + 1):
        # 좌 상 우 하 인덱스
        left = mid_c - i
        top = mid_r - i
        right = mid_c + i
        bottom = mid_r + i

        # 일단 빼서 저장. 하나씩 돌리며 덮어씌우므로 첫번째 값은 따로 저장해준다.
        left_top = arr[top][left]

        # 왼쪽줄 끌어올리기
        for r in range(top + 1, bottom + 1):
            arr[r - 1][left] = arr[r][left]

        # 아랫줄 왼쪽으로 당기기
        for c in range(left + 1, right + 1):
            arr[bottom][c - 1] = arr[bottom][c]

        # 오른쪽 끌어내리기
        for r in range(bottom - 1, top - 1, -1):
            arr[r + 1][right] = arr[r][right]

        # 윗줄 오른쪽으로 당기기
        for c in range(right - 1, left - 1, -1):
            arr[top][c + 1] = arr[top][c]

        arr[top][left + 1] = left_top  # 빠진값 채워주기


# NxM, 회전연산 수 K
N, M, K = map(int, input().rstrip().split())

# 배열 받기
nums = [list(map(int, input().rstrip().split())) for _ in range(N)]
nums_copy = deepcopy(nums)      # 원본 저장용

rotates = []    # 연산들. permutation 용
# K번의 연산
for _ in range(K):
    temp_row, temp_col, temp_step = map(int, input().split())

    rotates.append((temp_row, temp_col, temp_step))

# 최소합 할당
min_sum = float('inf')


for perm in itertools.permutations(rotates):
    for row, col, step in perm:
        # 인덱스 맞춰주기
        rotate_clockwise_arr(nums, row - 1, col - 1, step)

    # 업데이트
    for i in range(len(nums)):
        if sum(nums[i]) < min_sum:
            min_sum = sum(nums[i])

    nums = deepcopy(nums_copy)        # 다시 원본으로 변경

print(min_sum)
