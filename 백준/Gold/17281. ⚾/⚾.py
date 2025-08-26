# 17281. 야구공

import sys
# import time
#
# # 측정 시작
# start_time = time.time()

input = sys.stdin.readline
# sys.stdin = open('input.txt')

import itertools

# 몇 이닝 진행할지
N = int(input())
baseballs = [list(map(int, input().rstrip().split())) for _ in range(N)]

GAME_PLAYER = 9


def play_baseball(arr, s_player):
    """
    이번 이닝의 각 선수별 점수를 인자로 받아, start_player 부터 시작했을 때 점수와 다음 시작 player 를 return

    Args:
        arr (list): 0 1 2 3 4 값으로 이루어진 숫자 일차원 리스트
        s_player (int): 시작 선수의 idx
    Returns:
        (tuple): (score, 다음 start_player)로 이루어진 튜플

    Notes:
        0 - 아웃, 1 - 안타, 2 - 2루타, 3 - 3루타, 4 - 홈런
        각 이닝은 아웃 3번을 맞는 즉시 끝남.
    """
    global score

    base_status = 0

    out_count = 0

    # 현재 주자 = 시작 주자로 초기화
    c_player = s_player

    # 아웃이 3번 나기 전까지
    while out_count < 3:
        # 이번 주자가 침
        hit = arr[c_player]

        if hit == 0:  # 아웃이면 아웃+1
            out_count += 1

        else:
            score += 1  # 일단 점수로 쳐

            base_status = (base_status << 1) | 1  # <<1 하고 마지막 자리에 1 꽂기
            base_status <<= (hit - 1)  # (hit-1)만큼 왼쪽 쉬프트
            base_status &= 0b111  # 마지막 3비트만 남기기

        c_player = (c_player + 1) % GAME_PLAYER  # 0 ~ 8 인덱스를 계속 돌기

    # 비트연산으로 아직 홈에 들어오지 못한 애들은 뺴기
    non_home = bin(base_status).count('1')

    score -= non_home

    return c_player % GAME_PLAYER


max_score = 0  # 젤 큰 점수 초기화

# 선수들 2번부터 9번까지 다 순열 돌려
# 돌리지마 오래걸려..

perms = itertools.permutations(range(2, 10))
for perm in perms:
    player_perm = list(perm[:3]) + [1] + list(perm[3:])  # 1번을 4번타자로 고정
    # player_perm = [2, 3, 4, 1, 5, 6, 7, 9, 8]

    current_player = 0  # 첫번째 player의 idx
    score = 0
    # 모든 이닝 진행
    for inning in baseballs:
        current_inning_hits = [inning[p - 1] for p in player_perm]
        # current_inning_hits = [2, 4, 3, 1, 0, 2, 1, 0, 3]
        current_player = play_baseball(current_inning_hits, current_player)

    # max_score 업데이트
    max_score = score if score > max_score else max_score

print(max_score)
# # 측정 끝
# end_time = time.time()
#
# print("총 실행 시간:", end_time - start_time, "초")
