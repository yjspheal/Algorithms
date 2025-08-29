# 4869. [파이썬 S/W 문제해결 기본] 4일차 - 종이붙이기

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.

def factorial(n):
    """
    주어진 양의 정수 n의 팩토리얼 값을 계산하여 반환합니다.

    Args:
        n (int): 팩토리얼을 계산할 양의 정수.

    Returns:
        int: n의 팩토리얼 값(n!).

    Raises:
        ValueError: n이 0보다 작은 경우 발생.

    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1

    Note:
        - 0!은 1로 정의됩니다.
        - n이 0보다 작은 경우 예외를 발생시켜야 합니다(필요시).
    """
    fact = 1
    for i in range(1, n+1):
        fact *= i

    return  fact
    


for test_case in range(1, T + 1):
    """
    # 작은 세로 종이로 만들 수 있는 모든 경우를 계산한 후, 거기서 큰 종이나 작은 가로 종이 2개로 대체될 수 있는 경우를 찾는다.
    # 1 1 1 1 1
    # 5! / 5! * 2^0 + 4!/3!1! * 2^1 + 3!/1!2! * 2 ^ 2 ...
    """

    # 가로 길이를 input받음
    row_length = int(input()) // 10

    # 로직 구현
    case_count = 0 # 경우의 수 계산 변수 초기화
    # 큰 종이는 길이 2씩 차지하므로 range 범위를 //2로 제한
    for big_paper in range(row_length // 2 + 1):
        # 작은 종이의 갯수는 총 길이 - 2 * 큰종이
        small_paper = row_length - 2 * big_paper
        whole_paper = small_paper + big_paper   # 총 종이 수

        case_count += factorial(whole_paper) // (factorial(small_paper) * factorial(big_paper)) * 2 ** (big_paper)
    print(f'#{test_case} {case_count}')