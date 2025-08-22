# 기존 코드
~~~python
# 9490_풍선팡. 풍선팡

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
#
# # sys.stdin = open("sample_input.txt", "r")
# sys.stdin = open("input.txt", "r")


def calculate_flowers(arr, r, c):
    """
    k = arr[r][c]일 때, [r][[c] 위치에서 상하좌우 k범위의 값들을 모두 더하여 return 하는 함수

    Args:
        arr (list): 각 풍선별 k값이 저장되어있는 이중 리스트
        r (int): 현재 터트릴 행
        c (int): 현재 터트릴 열

    Returns:
        int: 상하좌우 k만큼 터트렸을 때 나오는 꽃가루 수의 합
    """

    dr = [-1, 1, 0, 0]      # 행 열 delta, 순서대로 상 하 좌 우
    dc = [0, 0, -1, 1]

    flowers = arr[r][c]       # 상하좌우 얼마나 터트릴지
    popped_flowers_count = flowers      # 터진 풍선 속 꽃가루도 추가

    for i in range(4):
        for k in range(1, flowers + 1):     # 1부터 flowers까지 곱한 범위를 볼 것이므로
            nr = r + dr[i] * k  # 새로운 r과 c 계산, k범위만큼 봐야하므로 둘다 k를 곱해줘야 한다.
            nc = c + dc[i] * k

            if 0 <= nr < N and 0 <= nc < M:     # nr과 nc가 arr 안에 있다면
                popped_flowers_count += arr[nr][nc]     # 그 안에 든 꽃가루 수를 popped flowers count에 추가

    return popped_flowers_count

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N, M = map(int, input().split())  # 행, 열 길이
    arr = [list(map(int, input().split())) for _ in range(N)]  # arr 받아오기

    max_flowers = 0     # 최대값 초기화
    # 행과 열을 순회하며
    for row in range(N):
        for col in range(M):
            popped_flowers = calculate_flowers(arr, row, col)       # 해당 좌표에서의 터진 꽃가루 수 계산

            if popped_flowers > max_flowers:                # 지금까지의 max값을 넘어섰다면 update
                max_flowers = popped_flowers

    print(f'#{tc} {max_flowers}')
~~~
<br><br>

# 총평
- 전형적인 브루트포스 풀이로, 각 칸에서 상하좌우로 최대 `k`칸 합산하는 로직이 잘 구현되어 있습니다.
- 다만 `calculate_flowers()`가 전역 `N, M`에 **의존**하여 호출 시점과 입력 순서에 따라 **런타임 에러** 가능성이 있습니다(재사용성 저해).
- 매 스텝에서 **경계 체크를 반복**하며(조건문 4×k회), 작은 최적화 여지도 있습니다.
- 네이밍/도큐스트링 오타(`[r][[c]`) 등 가독성 개선 포인트가 있습니다.

# 복잡도 및 병목
- 각 칸에서 상하좌우 최대 `k`칸을 합산 → 한 칸 비용 `O(k)`, 상수 4배.
- 전체는 `O(N*M*E[k])` (E[k]는 평균 k). 최악 `k≈max(N,M)`일 때 `O(N*M*(N+M))`.
- 병목은 `calculate_flowers` 내부 루프의 **경계 체크와 인덱싱 반복**입니다.

# 보완점
## 1. 전역 의존(N, M) 제거 및 크기 추론  [중요도: High] [효과: 안정성/재사용]
- 함수 내부에서 `n, m = len(arr), len(arr[0])`로 추론하거나, 인자로 `n, m`을 받도록 변경합니다. 전역 접근을 제거해 모듈성 확보.

## 2. 경계 체크 반복 제거(최대 스텝 사전 계산)  [중요도: Med] [효과: 성능]
- 매 이동마다 `0 <= nr < n` 검사를 하기보다, **각 방향에서 가능한 최대 스텝 수**를 미리 `steps = min(k, r, n-1-r, c, m-1-c)` 형태로 계산하고 그 범위만 루프 돌면 분기 비용이 줄어듭니다.

## 3. 상수/방향 재사용 및 네이밍 정리  [중요도: Med] [효과: 가독/유지보수]
- 방향 벡터는 함수 밖 **상수**로 한 번만 정의하여 매 호출 재생성을 막습니다.
- 함수명, 변수명 의미를 명확히(`calculate_flowers` → `burst_sum`, `flowers` → `power` 등).

## 4. 타입힌트/PEP8/도큐스트링 오타 수정  [중요도: Low] [효과: 가독/유지보수]
- `List[List[int]]` 타입힌트 추가, 도큐스트링의 `[r][[c]` 오타 수정, 라인 길이와 주석 정리.

# 최종 코드 예시
~~~python
from typing import List, Tuple

# 방향: 상, 하, 좌, 우 (row_delta, col_delta)
DIRS: Tuple[Tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


def burst_sum(grid: List[List[int]], r: int, c: int) -> int:
    """
    grid[r][c] = k일 때, (r, c)에서 상/하/좌/우로 최대 k칸까지의 값을 모두 더해 반환한다.
    자기 자신(grid[r][c])도 포함한다. (in-bounds만 합산)

    Args:
        grid: 풍선 파워(정수)가 담긴 2차원 리스트
        r: 현재 행
        c: 현재 열

    Returns:
        해당 위치에서 터뜨렸을 때의 총 꽃가루 합.
    """
    n, m = len(grid), len(grid[0])
    power = grid[r][c]
    total = power  # 자기 자신 포함

    if power == 0:
        return total

    # 각 방향에서 가능한 최대 스텝 수를 사전 계산하여 불필요한 경계 체크 제거
    # 상: r, 하: n-1-r, 좌: c, 우: m-1-c
    max_steps = (min(power, r),
                 min(power, n - 1 - r),
                 min(power, c),
                 min(power, m - 1 - c))

    for (dr, dc), steps in zip(DIRS, max_steps):
        for k in range(1, steps + 1):
            total += grid[r + dr * k][c + dc * k]

    return total


def solve() -> None:
    T = int(input())
    for tc in range(1, T + 1):
        n, m = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(n)]

        best = 0
        for r in range(n):
            for c in range(m):
                s = burst_sum(grid, r, c)
                if s > best:
                    best = s

        print(f"#{tc} {best}")


if __name__ == "__main__":
    # 예시 입력 형식:
    # 1
    # 3 3
    # 1 3 1
    # 1 1 1
    # 1 1 1
    #
    # solve()
    solve()
~~~
