# [파이썬 S/W 문제해결 기본] 3일차 - 글자수

# import sys
# sys.stdin = open('input.txt')

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    str1 = set(input())     # 길이가 N인 문자열 1, 1개씩만 있으면 되므로 set처리
    str2 = input()          # 길이가 M인 문자열 2


    # str2에 들어있는 문자별 갯수를 저장할 dict 초기화
    char_dict = {}
    
    max_count = 0   # 제일 큰 횟수 저장

    for char in str2:   # str2에 있는 문자가
        if char in str1:        # str1에도 있다면
            # dict의 value에 +1을 해준다. 만약 없었다면 0 + 1 = 1을 넣는다.
            char_dict[char] = char_dict.get(char, 0) + 1

            if char_dict[char] > max_count:     # max값을 넘겼다면
                max_count = char_dict[char]     # update
    
    print(f'#{test_case} {max_count}')