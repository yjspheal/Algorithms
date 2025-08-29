# 6190_정곤이의단조증가하는수 

# import sys
# 
# sys.stdin = open('s_input.txt')


def is_monotone(num):
    """
    들어온 숫자가 단조증가인지 여부를 판단하는 함수
    Args:
        num (int): 정수 여러자리로 이루어진 문자열
    Returns:
        boolean: T / F
    """

    while num > 0:
        after = num % 10
        before = (num // 10) % 10
        if after < before:
            return False

        num //= 10  # 한자리 줄이기

    return True


T = int(input())
for tc in range(1, T + 1):
    N = int(input())  # 정수 갯수
    nums = list(map(int, input().split()))  # 정수로 이루어진 일차원 배열

    nums.sort()  # 최대 1000개이므로 그냥 정렬하자
    # nums = bubble_sort(nums)

    max_monotone = -1  # 최대 단조증가 수 초기화

    i = N - 2  # 초기 앞 수의 인덱스
    while i >= 0:  # 앞 수가 범위 내이고, 단조증가 수를 찾기 전까지
        for j in range(N - 1, i, -1):  # 뒤 수의 인덱스
            current_num = nums[i] * nums[j]
            if current_num < max_monotone:      # 이번 곱에서, 이미 최대 단조수보다 작아졌다면
                break
            # if is_monotone(str(current_num)):  # 단조증가면
            if is_monotone(current_num):  # 단조증가면
                if max_monotone < current_num:
                    max_monotone = current_num

        i -= 1  # 앞자리 수를 하나 앞당긴다

    print(f'#{tc} {max_monotone}')
