# 4881. [파이썬 S/W 문제해결 기본] 5일차 - 배열 최소 합

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")


def sum_down(row, current_sum):
    # 계속 update할 최소합
    global min_sum
    # 지금까지 더한 합이 이미 min_sum을 넘으면 break
    if current_sum >= min_sum:
        return
    

    # 모든 행에서 하나씩 골랐으면 min_sum 갱신
    if row == N:
        min_sum = current_sum
        return

    # 0 ~ N-1 열까지,
    for col in range(N):
        # 아직 고르지 않은 열만 하나씩 골라서 재귀로 내려감
        if not visited[col]:              # col열이 아직 선택 안 됐으면
            visited[col] = True           # col열 선택 표시
            sum_down(row + 1, current_sum + arr[row][col])  # 다음 행으로, 합계 갱신해서 재귀호출
            visited[col] = False          # 함수 복귀 시, 선택 취소해서 다른 조합도 탐색하게 함

    
T = int(input())
for tc in range(1, T+1):
    N = int(input())        # NxN 숫자 배열
    arr = []
    for _ in range(N):
        arr.append(list(map(int, input().split())))


    min_sum = float('inf')    # 최소 합계 초기값
    visited = [False] * N     # 각 열의 선택여부 리스트
    sum_down(0, 0)            # 0행부터, 합계 0에서 시작

    print(f'#{tc} {min_sum}')
