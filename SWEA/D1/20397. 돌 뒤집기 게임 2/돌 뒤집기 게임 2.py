# 20397. 돌 뒤집기 게임 2 

def switch_stones(arr, mid, scope):
    """
    arr에서, mid를 중심으로 scope만큼 벌어져있는 각각의 원소들이
    서로 같다면 뒤집고, 다른 색이면 유지하여 다시 arr를 반환하는 함수
    Args:
        arr (list): 0과 1로 이루어진 리스트
        mid (int): 중심이 될 원소의 인덱스
        scope (int): mid에서 얼마나 떨어져있는가
    Returns:
        list: 일부 뒤집거나 유지된 arr
    """
    len_arr = len(arr)  # arr의 길이

    # 만약 범위를 벗어난다면 scope를 조정한다
    if mid - scope < 0:
        scope = mid
    if mid + scope >= len_arr:
        scope = len_arr - mid - 1  # mid + scope < len_arr 가 mid + scope <= len_arr - 1 이 되므로

    for idx in range(1, scope + 1):
        before = arr[mid - idx]
        after = arr[mid + idx]
        # 서로 같다면
        # if arr[mid - idx] == arr[mid + idx]:
        if before == after:
            # 둘 다 뒤집어준다
            arr[mid - idx] = arr[mid + idx] = (after + 1) % 2

    return arr


T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())  # 돌의 수 N, 뒤집기 횟수 M
    stones = list(map(int, input().split()))  # N 개의 돌의 상태


    for _ in range(M):  # M번에 걸쳐
        i, j = map(int, input().split())  # i번째 돌을 사이에 두고 마주보는 j개의 돌에 대해~
        result = switch_stones(stones, i - 1, j)        # i번쨰이므로 인덱스는 -1

    print(f'#{tc}', *result)