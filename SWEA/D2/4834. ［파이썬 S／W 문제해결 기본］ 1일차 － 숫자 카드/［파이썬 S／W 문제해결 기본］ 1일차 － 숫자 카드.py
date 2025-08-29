# 4834. [파이썬 S/W 문제해결 기본] 1일차 - 숫자 카드

# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    cards = input()  # 각 카드가 공백없이 문자열로 들어옴

    card_count = [0] * 10       # 카드 갯수 저장할 10개짜리 리스트

    # 가장 많은 카드 수와 카드를 저장할 변수 초기화
    max_card_count = 0
    max_card = 0

    # 카드들을 순회하며
    for card in cards:
        card = int(card)            # int 화
        card_count[card] += 1       # 카드 한장마다 갯수 + 1

        # 만약 maximum 갯수를 넘었다면
        if card_count[card] > max_card_count:
            max_card_count = card_count[card]      # 업데이트
            max_card = card     # card 도 업데이트

        # 만약 동일하다면, 숫자가 큰 쪽이 max_card
        elif card_count[card] == max_card_count and card > max_card:
            max_card = card     # card 도 업데이트


    print(f'#{test_case} {max_card} {max_card_count}')
