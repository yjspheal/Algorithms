# 4835. [파이썬 S/W 문제해결 기본] 1일차 - 구간합 
def sum_list(arr):
    """
    주어진 리스트의 모든 원소를 합하여 return 하는 함수

    Args:
        arr (list): 주어진 리스트

    Returns:
        int: 모든 원소의 합

    Notes:
        arr 의 모든 원소는 정수로 이루어져있다
    """

    # 반환할 합의 값
    result = 0

    for num in arr:
        result += num

    return result


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    # 정수의 갯수 _와, 합칠 구간의 갯수 section_length
    _, section_length = map(int, input().split())

    digit_list = list(map(int, input().split()))

    # 최대 최소값 초기화 = 맨 처음 구간합
    min_sum = max_sum = sum_list(digit_list[:section_length])

    # 모든 구간을 순회하며 sum 값을 업데이트
    for i in range(len(digit_list) - section_length + 1):
        current_sum = sum_list(digit_list[i:(i + section_length)])

        if current_sum > max_sum:  # current가 max_sum을 넘겼다면
            max_sum = current_sum
        if current_sum < min_sum:  # current가 min_sum보다 작다면
            min_sum = current_sum

    print(f'#{test_case} {max_sum - min_sum}')
