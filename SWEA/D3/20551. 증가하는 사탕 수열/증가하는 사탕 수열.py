# 20551. 증가하는 사탕 수열

# import sys
# 
# sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    candies = list(map(int, input().split()))
    len_candies = len(candies)
    remain_candies = [0] * len_candies  # 마지막 상자에 들어있을 사탕 리스트

    s_idx = 0  # 캔디 체크 시작 idx

    is_possible = True
    while s_idx < len_candies:  # s_idx가 범위를 벗어나기 전까지
        min_gap = float('inf')
        min_gap_idx = -1

        for i in range(s_idx, len_candies):  # s_idx에서 끝까지 돌며
            min_candy = i + 1  # 최소 1 2 3 4 5 ... 가 가능해야 조건을 만족시킬 수 있음

            gap = candies[i] - min_candy
            if gap < 0:  # 음수가 됐다면 불가능으로 break
                is_possible = False
                break

            if gap <= min_gap:  # 갱신됐다면
                min_gap = gap
                min_gap_idx = i

        else:  # break가 안 됐다면 리스트 업데이트 후 다음으로
            # 해당하는 인덱스 + 1 해줘야 최소 사탕 갯수
            # 에다가 min_gap까지 다 더해줘야 사탕을 '최소'로 먹을 수 있음
            remain_candies[s_idx:(min_gap_idx + 1)] = [j + min_gap + 1 for j in range(s_idx, min_gap_idx + 1)]
            s_idx = min_gap_idx + 1  # 시작 위치 조정

            continue  # 다음으로

        break  # for문에서 break가 됐으면 바로 나갈 수 있게

    eat_candies = sum([i - j for i, j in zip(candies, remain_candies)])

    print(f'#{tc} {eat_candies if is_possible else -1}')
