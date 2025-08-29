# 16546. Baby-gin_실습
 
import itertools


def is_run(chars):
    """
    세 숫자로 이루어진 문자열 chars에 대해, 해당 세 숫자가 연속인지 판단하여 결과를 return하는 함수
    Args:
        chars (str): 세 숫자로 이루어진 문자열
    Returns:
        boolean: 연속이라면 True, 아니면 False
    """

    n1 = int(chars[0])
    n2 = int(chars[1])
    n3 = int(chars[2])

    return (n1 + 1) == n2 == (n3 - 1)


def is_triplet(chars):
    """
    세 숫자로 이루어진 문자열 chars에 대해, 해당 세 숫자가 모두 동일한지 판단하여 결과를 return하는 함수
    Args:
        chars (str): 세 숫자로 이루어진 문자열
    Returns:
        boolean: 동일하다면 True, 아니면 False
    """

    return chars[0] == chars[1] == chars[2]

T = int(input())
for tc in range(1, T + 1):
    cards = list(map(str, input().strip()))         # 여섯 개의 숫자로 이루어진 문자열

    result = 'false'
    for six_chars in itertools.permutations(cards):

        front_3chars = ''.join(six_chars[:3])
        behind_3chars = ''.join(six_chars[3:])

        if (
                (is_run(front_3chars) or is_triplet(front_3chars))              # 앞 3개가 run이거나 triplet
                and (is_run(behind_3chars) or is_triplet(behind_3chars))        # 뒤 3개가 run이거나 triplet
        ):
            result = 'true'                                                     # 인 경우가 하나라도 존재한다면 true
            break

    print(f'#{tc} {result}')