# 4873. [파이썬 S/W 문제해결 기본] 4일차 - 반복문자 지우기

# import sys
# sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T+1):
    chars = input()         # 문자열 입력
    stack = []          # stack 초기화

    # 문자열을 순회하며
    for char in chars:
        if stack and stack[-1] == char:     # stack이 비어있지 않으며 마지막값이 지금 값과 같다면
            stack.pop()     # pop 하기
        else:
            stack.append(char)      # 아니라면 원소를 추가

    print(f'#{tc} {len(stack)}')   # 남은 stack 길이 출력