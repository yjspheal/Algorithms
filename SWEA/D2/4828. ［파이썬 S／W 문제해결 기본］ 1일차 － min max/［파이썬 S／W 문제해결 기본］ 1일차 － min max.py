# 4828. [파이썬 S/W 문제해결 기본] 1일차 - min max


# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())

    nums = list(map(int, input().split()))  # 숫자 리스트 생성

    # 최소값 최대값 초기화
    mini = nums[0]
    maxi = nums[0]

    # nums 를 순회하며
    for num in nums:
        # maxi 와 mini 업데이트
        if num > maxi:
            maxi = num
        if num < mini:
            mini = num

    print(f'#{test_case} {maxi - mini}')
