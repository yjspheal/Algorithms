# 1215_회문1. [S/W 문제해결 기본] 3일차 - 회문1

# import sys
#
# sys.stdin = open("input.txt")


def is_palindrome(char_list):
    """
    char_list 문자열 리스트에 대해, 회문인지 판단하여 맞다면 True 아니면 False를 반환하는 함수
    """

    return char_list == char_list[::-1]


T = 10
for tc in range(1, T + 1):
    M = int(input())  # 찾아야하는 회문의 길이
    sentences = [list(input()) for _ in range(8)]  # 8x8의 글자판이 주어진다
    sentences += list(zip(*sentences))  # 세로줄을 추가한다

    len_sentences = len(sentences)  # 16으로 고정이지만 그냥 계산
    len_row = len(sentences[0])  # 8로 고정이지만 그냥 계산

    count = 0  # 회문 갯수 계산
    for row in sentences:
        for i in range(len_row - M + 1):  # + M-1까지 회문인지 체크
            if is_palindrome(row[i: i + M]):        # 회문이라면 count + 1
                palindrome = row[i: i + M]
                count += 1

    print(f'#{tc} {count}')
