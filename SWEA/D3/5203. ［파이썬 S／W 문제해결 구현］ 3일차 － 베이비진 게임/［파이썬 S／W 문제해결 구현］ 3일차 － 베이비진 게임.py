# 5203. [파이썬 S/W 문제해결 구현] 3일차 - 베이비진 게임
# 
# import sys
# 
# sys.stdin = open('input.txt')

import itertools


def is_run(c_list):
    """
    세 숫자로 이루어진 리스트에 대해, 해당 세 숫자가 연속인지 판단하여 결과를 return하는 함수
    Args:
        chars (list): 세 숫자로 이루어진 문자열
    Returns:
        boolean: 연속이라면 True, 아니면 False
    """
    c_list.sort()

    return (c_list[0] + 1) == c_list[1] == (c_list[2] - 1)


def is_triplet(c_list):
    """
    세 숫자로 이루어진 리스트에 대해, 해당 세 숫자가 모두 동일한지 판단하여 결과를 return하는 함수
    Args:
        c_list (list): 세 숫자로 이루어진 리스트
    Returns:
        boolean: 동일하다면 True, 아니면 False
    """

    return c_list[0] == c_list[1] == c_list[2]


T = int(input())
for tc in range(1, T + 1):
    cards = list(map(int, input().split()))

    p1 = cards[0::2]  # 각 카드 부여
    p2 = cards[1::2]

    p2_complete = p1_complete = False
    for i in range(2, len(p1)):  # 3 4 5 6 장만 체크(i는 인덱스)
        # 마지막 카드 전까지에서 2개 뽑아서
        for comb in itertools.combinations(list(range(i)), 2):
            # 합쳐서 체크
            p1_cards = [p1[i]] + [p1[cnum] for cnum in comb]
            p2_cards = [p2[i]] + [p2[cnum] for cnum in comb]

            if is_triplet(p1_cards) or is_run(p1_cards):
                p1_complete = True
                break   # 1은 선플레이어이므로 break 바로 해도 됨

            if is_triplet(p2_cards) or is_run(p2_cards):
                p2_complete = True

        # p1이 완성했다면
        if p1_complete:
            ans = 1
            break

        # p2가 완성했다면
        elif p2_complete:
            ans = 2
            break

    else:
        # 아무도 완성하지 못했다면
        ans = 0

    print(f'#{tc} {ans}')
