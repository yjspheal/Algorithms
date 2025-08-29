# 4864. [파이썬 S/W 문제해결 기본] 3일차 - 문자열 비교
# import sys
# sys.stdin = open("input.txt")

def brute_force(p, t):
    """
    문자열 t에서 문자열 p라는 패턴이 존재하는지 여부를 반환하는 함수
    Args:
        p (str): 찾고자 하는 패턴
        t (str): 원본 문자열
    Returns:
        int: 존재한다면 1 없다면 0을 반환
    """
    i = 0       # t의 인덱스
    j = 0       # p의 인덱스

    len_p = len(p)           # N
    len_t = len(t)           # M

    # t와 p가 일치하는지 한자리씩 확인
    while i < len_t and j < len_p:
        if t[i] == p[j]:        # 서로 같으면
            i += 1
            j += 1              # 두 인덱스에 += 1
        else:                   # 다르면
            i = i - j + 1       # 타겟 시작점은 처음 + 1로 돌아가고
            j = 0               # 패턴 시작점은 0으로 초기화

    # while을 다 돌았는데 j가 len_p라면 패턴이 존재하는 것
    if j == len_p:
        return 1
    else:
        return 0


T = int(input())
for test_case in range(1, T + 1):
    pattern = input()        # 길이 N의 문자열
    target = input()         # 길이 M의 문자열

    has_pattern = brute_force(pattern, target)
    
    print(f'#{test_case} {has_pattern}')