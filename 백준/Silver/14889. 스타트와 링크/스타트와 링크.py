# 14889 스타트와 링크

import sys
input = sys.stdin.readline
import itertools

def cal_players_synergy(arr, comb):
    """
    선수간 시너지 정보가 들은 arr에 대해, comb에 들은 인덱스 번호(재료번호)에 따른 시너지 합을 계산하여 리턴하는 함수
    Args:
        arr (list): 숫자를 인자로 갖는 이차원 배열
        comb (tuple): 사용할 재료의 번호들
    Returns:
        int: 시너지합
    """

    synergy = 0
    # comb가 123이었다면 각 재료 두개씩 시너지를 확인해야하므로 12, 23, 13을 체크
    for i1, i2 in itertools.combinations(comb, 2):
        synergy += arr[i1][i2]
        synergy += arr[i2][i1]  # i1i2와 i2i1은 다르다

    return synergy



N = int(input())  # NxN행렬의 길이
players = [list(map(int, input().rstrip().split())) for _ in range(N)]  # 선수 정보가 담긴 이차원 배열

# 최초 최소합 초기화
min_sub = float('inf')
already_checked_combs = set()       # 이미 체크한 comb 확인용

# 나머지 반절 조합을 계산하기 위한 리스트
base_comb = list(range(N))

# 절반을 조합하여 만들기
for half_comb in itertools.combinations(range(N), N // 2):
    comb1 = half_comb
    if comb1 in already_checked_combs:      # 이미 봤던거라면, 즉 정반대 조합을 통해 체크했더라면
        continue

    comb2 = tuple([num for num in range(N) if num not in comb1])       # 0 ~ N-1 중 comb1에 안 들은 조합 계산

    synergy1 = cal_players_synergy(players, comb1)
    synergy2 = cal_players_synergy(players, comb2)

    # abs 안 쓰고 하려고 이렇게씀
    current_sub = synergy1 - synergy2 if synergy1 > synergy2 else synergy2 - synergy1

    # min_sub 업데이트
    if current_sub < min_sub:
        min_sub = current_sub

    # 이미 봤다는 확인용 set에 추가. comb1는 어차피 다시 돌아오지 않으므로 넣을 필요 없다
    already_checked_combs.add(tuple(comb2))

print(min_sub)