# 20739. 고대 유적 2
 
T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]  # 이중리스트로 input받음
    arr += list(map(list, zip(*arr)))  # 세로줄을 가로로 transpose하여 arr에 추가

    max_length = 0  # 가장 긴 구조물의 길이를 넣을 변수

    # arr를 순회하며
    for row in arr:
        current_length = 0  # 현재 길이 변수
        len_row = len(row)
        for i, ele in enumerate(row):  # row의 각 원소에 대해
            if ele == 1:  # 구조물이면 현재 길이 +1
                current_length += 1
                if i < len_row - 1:   # 마지막 원소가 아니라면
                    continue    # 다음 턴으로

            # 마지막 원소거나, 구조물이 아닐 떄 아래 if를 돌림
            if current_length > max_length:  # 현재 길이가 최대 길이를 넘었다면 update
                max_length = current_length

            current_length = 0  # 현재 길이 초기화

    # 젤 긴 게 1이면 노이즈라는 뜻이므로 0 출력
    if max_length == 1:
        max_length = 0

    print(f'#{tc} {max_length}')
