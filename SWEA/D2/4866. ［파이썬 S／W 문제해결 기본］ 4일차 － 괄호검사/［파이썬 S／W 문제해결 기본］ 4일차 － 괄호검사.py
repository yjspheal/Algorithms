# 4866. [파이썬 S/W 문제해결 기본] 4일차 - 괄호검사

# import sys
#
# sys.stdin = open('input.txt')


def check_valid_bracket(chars):
    """
    chars에서 중괄호, 소괄호가 제대로 짝을 이뤘는지 검사하는 함수
    Args:
        chars (str): 한 줄의 문자열
    Returns:
        boolean:  정상 -> True, 비정상 -> False
    """
    stack = []  # stack 초기화
    open_bracket_set = ('(', '{')
    close_bracket_set = (')', '}')
    bracket_dict = {')': '(', '}': '{'}  # 닫는 괄호 : 여는 괄호만 있으면 됨

    # chars를 순회하며
    for char in chars:
        if char in open_bracket_set:  # 여는 괄호면 push
            stack.append(char)
        elif char in close_bracket_set:  # 닫는 괄호면
            if not stack:  # 근데 스택이 비어있으면
                return False  # 비정상

            last_bracket = stack.pop()  # 스택의 마지막값이
            if last_bracket != bracket_dict[char]:  # 닫는 괄호(char)와 매치되는 여는 괄호가 아니라면
                return False  # 비정상

    # 다 돌았는데 stack이 남아있다면 비정상, 안남아있다면 정상을 return
    return False if stack else True


T = int(input())
for tc in range(1, T + 1):
    sentence = input()      # 한 줄의 문자열 입력
    result = 1 if check_valid_bracket(sentence) else 0    # 괄호 맞는지 체크, True면 1 False면 0으로 변경

    print(f'#{tc} {result}')

