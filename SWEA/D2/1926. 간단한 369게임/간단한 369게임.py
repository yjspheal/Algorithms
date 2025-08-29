# 1926. 간단한 369게임

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")

# T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
# for tc in range(1, T + 1):
"""
3, 6, 9가 들어가는 부분을 -로 치환하는 로직
"""

# 369 진행할 숫자 끝 수
N = int(input())

for n in range(1, N + 1):
    # n을 string화
    n = str(n)

    # n의 글자수를 순회하며
    for i in range(len(n)):
        # 369에 해당하는 수
        count_369 = n.count('3') + n.count('6') + n.count('9')

    # 369가 있는 수였다면
    if count_369:
        print('-' * count_369, end = ' ')
    else:   # 없었다면 숫자 그대로 출력
        print(n, end = ' ')
        
