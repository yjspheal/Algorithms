# 4843_특별한정렬. [파이썬 S/W 문제해결 기본] 2일차 - 특별한 정렬

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
#
# sys.stdin = open("input.txt", "r")
# # sys.stdin = open("input.txt", "r")

def specific_sort(arr, len_arr):
    """
    정수로 이루어진 리스트를 인자로 받아, 가장 큰 수 - 가장 작은 수 - 그다음 큰 수 - 그다음 작은 수 ...로 정렬하여 return
    단, 앞의 10개 즉 큰수 5개 / 작은 수 5개만 정렬한다.

    Args:
        arr (list): 정수로 이루어진 리스트. 정렬 전 원본
        len_arr (int): arr 길이

    Returns:
        list: 정렬된 arr의 앞 10개만 담은 list
    """

    # 선택 정렬을 위한 idx 추출

    for i in range(10):
        # 이번에 찾을 최대 or 최소의 인덱스와 값을 초기화
        target_idx = i
        target_value = arr[i]

        if i % 2 == 0:  # 짝수번째 인덱스라면 큰 수가 위치해야함
            for j in range(i, len_arr):
                if arr[j] > target_value:
                    target_value = arr[j]
                    target_idx = j

        else:  # 홀수번째 인덱스라면 작은 수가 위치해야함
            for j in range(i, len_arr):
                if arr[j] < target_value:
                    target_value = arr[j]
                    target_idx = j

        # 한번 다 돌고나면 최대 or 최소 idx가 나온다.
        # 자리를 바꿔주자
        arr[target_idx], arr[i] = arr[i], arr[target_idx]

    # 열 번이 돌고나면 앞에 10개가 정렬되어있다.
    return arr[:10]


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N = int(input())  # 정수의 갯수
    nums = list(map(int, input().split()))  # 정수 리스트

    # 정렬 후 앞 10개를 반환하는 함수를 시행한다.
    sorted_nums = specific_sort(nums, N)

    print(f'#{tc}', *sorted_nums)
