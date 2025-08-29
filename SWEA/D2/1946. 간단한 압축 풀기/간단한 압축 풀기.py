# 1946_간단한압축풀기. 간단한 압축 풀기

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# # sys.stdin = open("input.txt", "r")
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    # 채울 알파벳 갯수
    N = int(input())

    print(f'#{tc}')

    current_line_length = 0     # 10번 넘지 않도록, 각 줄에 현재 몇개까지 적혔는지 작성
    for _ in range(N):      # N번동안 input
        alphabet, count = input().split()
        count = int(count)  # str -> int화

        for i in range(count):
            print(alphabet, end = '')
            current_line_length += 1
            if current_line_length == 10:   # 10개 다 채웠으면
                print()         # 다음 줄로 끊고
                current_line_length = 0     # 다시 현재 줄 0으로 초기화

    # 이번 테케 끝났으면 다시 줄바꿈
    print()