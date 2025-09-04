# 5189. [파이썬 S/W 문제해결 구현] 2일차 - 전자카트

# import sys
# 
# sys.stdin = open('input.txt')


def go_cart(curr_sector, curr_sum, arr, N):
    """
    현재 방문중인 위치와 현재까지 배터리 사용량을 인자로 받아 다음곳으로 이동하여 배터리 사용량을 업데이트하는 dfs

    Args:
        curr_sector: 현재 위치
        curr_sum: 현재까지 사용량
        arr: 이차원배열

    Returns:

    """
    global visited, min_sum

    # 이미 최소값을 넘어섰다면 더 볼 것 없음 끝
    if curr_sum > min_sum:
        return

    # 사무실로 돌아왔다면 업데이트하고 끝
    if visited[1] is True:
        min_sum = min(min_sum, curr_sum)
        return

    # 2번부터 N번까지 관리구역 중
    for next_sector in range(2, N + 1):
        # 아직 방문하지 않은 곳이라면
        if not visited[next_sector]:
            visited[next_sector] = True  # 방문했다치고
            go_cart(next_sector, curr_sum + arr[curr_sector][next_sector], arr, N)  # 가보자고

            visited[next_sector] = False  # 방문취소

    # 2번부터 N번까지 다 갔으면
    if visited[2:] == [True] * (N - 1):
        # 사무실로 가자
        visited[1] = True
        go_cart(1, curr_sum + arr[curr_sector][1], arr, N)  # 가보자고
        visited[1] = False



T = int(input())
for tc in range(1, T + 1):
    len_data = int(input())  # 전체 구역의 길이. 2번부터 N번까지 관리구역 번호이다.
    data = [None] + [[None] + list(map(int, input().split())) for _ in range(len_data)]

    visited = [False] * (len_data + 1)  # 방문 여부
    min_sum = float('inf')  # 최소합

    go_cart(1, 0, data, len_data)

    print(f'#{tc} {min_sum}')
