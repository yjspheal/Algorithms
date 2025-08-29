# 4839_이진탐색. [파이썬 S/W 문제해결 기본] 2일차 - 이진탐색

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")


def count_binary_search(num, target):
    """
    주어진 범위 [1, num]에서 이진탐색을 진행하여 target을 찾을 때까지 진행해야하는 이진탐색의 횟수를 반환

    Args:
        num (int): 탐색 범위의 상한값
        target (int): 찾고자 하는 목표값

    Returns:
        int: target 페이지를 찾기 위해 실행된 binary_search 호출 횟수.
    """

    # 초기 탐색 구간의 하한과 상한을 정함. 책은 1쪽부터이므로 1로로
    l, r = 1, num

    # 탐색 횟수 초기화
    binary_count = 0
    # mid는 target이 아닌 값으로 초기화
    mid = 0

    # mid가 target이 되는 순간까지 진행할 것
    while mid != target:
        mid = int((l + r) / 2)  # 기준이 될 중간 페이지는 c= int((l+r)/2)로 계산한다.

        if target > mid:  # target이 절반값보다 크다면 l을 업데이트
            l = mid
        else:  # target이 절반값보다 작다면 r을 업데이트
            r = mid

        binary_count += 1       # 탐색 횟수 += 1

    return binary_count


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.

for test_case in range(1, T + 1):
    pages, target_A, target_B = map(int, input().split())

    # 각 search 횟수 계산
    search_count_A = count_binary_search(pages, target_A)
    search_count_B = count_binary_search(pages, target_B)

    # 승자 계산
    if search_count_A < search_count_B:
        winner = 'A'
    elif search_count_A > search_count_B:
        winner = 'B'
    else:  # 비김
        winner = 0

    print(f'#{test_case} {winner}')
