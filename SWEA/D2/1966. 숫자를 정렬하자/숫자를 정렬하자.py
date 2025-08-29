# 1966_숫자를정렬하자.

def bubble_sort(arr, n):
    """
    버블정렬하는 함수
    Args:
        arr(list): 숫자 리스트
        n (int): 리스트 길이
    Returns:
        list: 정렬된 리스트
    """
    # 앞자리부터 순회하며
    for i in range(n, 1, -1):  # 매 순회마다 가장 오른쪽값이 채워지므로 상한값이 1씩 줆
        for j in range(1, i):
            if arr[j] < arr[j - 1]:  # 이전것보다 값이 작다면
                arr[j], arr[j - 1] = arr[j - 1], arr[j]  # swap

    return arr


def select_sort(arr, n):
    """
    선택정렬하는 함수
    Args:
        arr(list): 숫자 리스트
        n (int): 리스트 길이
    Returns:
        list: 정렬된 리스트
    """
    for i in range(n, 1, -1):  # 매 순회마다 가장 오른쪽값이 채워지므로 상한값이 1씩 줆
        max_idx = 0  # 최대 인덱스 지정
        for j in range(i):
            if arr[j] > arr[max_idx]:  # j번쨰 원소 값이 더 크다면
                max_idx = j  # max idx 업데이트

        arr[i - 1], arr[max_idx] = arr[max_idx], arr[i - 1]

    return arr


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N = int(input())  # 들어올 숫자의 갯수
    nums = list(map(int, input().split()))  # 숫자 리스트 받기

    # sorted_nums = bubble_sort(nums, N)
    sorted_nums = select_sort(nums, N)

    print(f'#{tc}', *sorted_nums)
