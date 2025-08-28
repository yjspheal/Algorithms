# 피드백
## 작성 코드
~~~python
# 9490_풍선팡 

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

## 총평
- 강점
  - 문제 정의를 반영한 직관적 구현(델타 배열로 4방 탐색).
  - 중복 합산 없이 중심 셀을 한 번만 더하는 올바른 합산 로직.
- 개선 필요
  - `calculate_flowers` 내부에서 전역처럼 `N, M`을 참조(외부 루프에서만 정의) → 함수 독립성/안정성 저하.
  - Docstring 오타(`[[c]`) 및 주석 문장과 실제 동작의 표현 불일치(“곱한 범위” 등).
  - 타입 힌트, 도큐스트링의 파라미터/반환 설명 형식화 필요.
- 병목/리스크
  - 시간 복잡도: 각 칸마다 최대 `4 * arr[r][c]` 만큼 전진하여 누적 → 전체 O(N*M*K_avg), 최악 O(N*M*K_max).
  - 내부 이중 루프에서 경계 체크 분기와 곱셈(`dr[i] * k`)이 매 스텝 수행되어 상수항 부담.
<br><br>

## 복잡도 및 병목
- 현재 구현
  - 시간 복잡도: O(N*M*K_avg). (K_avg는 전체 평균 풍선 값, 최악은 K_max)
  - 공간 복잡도: O(1).
  - 병목 지점: `calculate_flowers`의 이중 루프(방향 4 × k칸 전진) 및 매 스텝 경계 체크.
- 개선 방향
  - 행/열 별 누적합(prefix sum)을 미리 구축하면, 각 칸의 상·하·좌·우 구간 합을 O(1)로 얻을 수 있어 전체 O(N*M)로 개선 가능.
  - 또한 함수 내부에서 배열 크기를 직접 구해 전역 의존 제거 → 안정성/재사용성 향상.
<br><br>

## 보완점
### 1. 전역 의존 제거 및 타입 힌트/도큐스트링 정비  [중요도: High] [효과: 안정성, 가독성]
- **이유(Reasoning)**  
  - `calculate_flowers`가 외부의 `N, M`에 의존하면, 동일 함수를 다른 맥락에서 호출할 때 버그 위험이 큼.  
  - `len(arr)`, `len(arr[0])`로 경계를 계산하면 함수 독립성과 재사용성이 확보됨.  
  - 타입 힌트 및 일관된 도큐스트링은 유지보수성 향상.
- **결론/코드**
~~~python
from typing import List

def calculate_flowers_naive(arr: List[List[int]], r: int, c: int) -> int:
    """arr[r][c] = k일 때, (r, c)에서 상·하·좌·우로 거리 k까지의 값을 모두 더한 합(중심 포함)을 반환."""
    n, m = len(arr), len(arr[0])
    dr = (-1, 1, 0, 0)
    dc = (0, 0, -1, 1)

    k = arr[r][c]
    s = k  # 중심 포함
    for i in range(4):
        for d in range(1, k + 1):
            nr, nc = r + dr[i] * d, c + dc[i] * d
            if 0 <= nr < n and 0 <= nc < m:
                s += arr[nr][nc]
    return s
~~~
<br><br><br>

### 2. 행·열 누적합(prefix sums)로 O(N*M)로 최적화  [중요도: High] [효과: 성능]
- **이유(Reasoning)**  
  - 각 칸 (r, c)에서 필요한 값은 상/하/좌/우 “선분” 합.  
  - 행 누적합 `row_ps[r][j] = arr[r][0..j-1] 합`, 열 누적합 `col_ps[c][i] = arr[0..i-1][c] 합`을 미리 계산하면,  
    - 좌( c-k .. c-1 ), 우( c+1 .. c+k ), 상( r-k .. r-1 ), 하( r+1 .. r+k ) 구간 합을 각각 O(1)에 얻을 수 있음.  
  - 중심은 한 번만 더하고, 사방은 중심 제외 구간으로 정확히 잘라 합산.  
  - 전체 시간: prefix 구축 O(N*M) + 모든 칸 조회 O(N*M) ⇒ O(N*M). 공간 O(N*M).
- **결론/코드**
~~~python
from typing import List

def max_pollen_with_prefix(arr: List[List[int]]) -> int:
    """행/열 누적합을 이용해 모든 칸에서의 폭발 합을 O(1) 조회, 전체 O(N*M)로 최대값 계산."""
    n, m = len(arr), len(arr[0])

    # 1) 행/열 누적합 구축
    row_ps = [[0]*(m+1) for _ in range(n)]
    col_ps = [[0]*(n+1) for _ in range(m)]
    for r in range(n):
        rp = row_ps[r]
        for c in range(m):
            rp[c+1] = rp[c] + arr[r][c]
            col_ps[c][r+1] = col_ps[c][r] + arr[r][c]

    def range_row_sum(r: int, c1: int, c2: int) -> int:
        """열 범위 [c1, c2] 합 (경계 자동 클램프)."""
        c1_ = max(0, c1)
        c2_ = min(m-1, c2)
        if c1_ > c2_:
            return 0
        ps = row_ps[r]
        return ps[c2_+1] - ps[c1_]

    def range_col_sum(c: int, r1: int, r2: int) -> int:
        """행 범위 [r1, r2] 합 (경계 자동 클램프)."""
        r1_ = max(0, r1)
        r2_ = min(n-1, r2)
        if r1_ > r2_:
            return 0
        ps = col_ps[c]
        return ps[r2_+1] - ps[r1_]

    # 2) 모든 칸에 대해 상/하/좌/우 합(중심 제외 구간)을 O(1)로 계산
    ans = 0
    for r in range(n):
        for c in range(m):
            k = arr[r][c]
            center = k

            left  = range_row_sum(r, c - k, c - 1)
            right = range_row_sum(r, c + 1, c + k)
            up    = range_col_sum(c, r - k, r - 1)
            down  = range_col_sum(c, r + 1, r + k)

            total = center + left + right + up + down
            if total > ans:
                ans = total
    return ans
~~~
<br><br><br>

### 3. 메인 루프 정리 및 I/O 분리  [중요도: Med] [효과: 가독성, 유지보수성]
- **이유(Reasoning)**  
  - 문제 풀이 구조를 “입력 → 계산 → 출력”으로 명확히 분리하면 테스트/재사용이 쉬움.  
  - 최대값 갱신은 `max()` 활용으로 간결화 가능.
- **결론/코드**
~~~python
def solve_case(arr):
    # 최적(누적합) 버전 사용
    return max_pollen_with_prefix(arr)

def main():
    import sys
    input = sys.stdin.readline
    T = int(input().strip())
    for tc in range(1, T + 1):
        N, M = map(int, input().split())
        arr = [list(map(int, input().split())) for _ in range(N)]
        ans = solve_case(arr)
        print(f'#{tc} {ans}')
~~~
<br><br><br>

### 4. 주석·도큐스트링 표현 개선  [중요도: Low] [효과: 가독성]
- **이유(Reasoning)**  
  - Docstring 오타(`[[c]`)와 “곱한 범위” 같은 표현은 오해 소지.  
  - “거리 k까지의 선분 합(중심 포함)” 등으로 명료하게 기술.
- **결론/코드(예시)**  
  - 위 코드들의 도큐스트링 및 주석을 반영(이미 수정된 표현 사용).
<br><br>

## 최종 코드 예시
~~~python
from typing import List

def max_pollen_with_prefix(arr: List[List[int]]) -> int:
    """
    각 칸 (r, c)에서 k = arr[r][c]일 때,
    상·하·좌·우 방향으로 '거리 k까지'의 선분 값(중심 제외)을 합산하고,
    중심 arr[r][c]을 한 번 더해 얻는 총합의 최댓값을 O(N*M) 시간에 구한다.
    """
    n, m = len(arr), len(arr[0])

    # 행/열 누적합 구축
    row_ps = [[0]*(m+1) for _ in range(n)]
    col_ps = [[0]*(n+1) for _ in range(m)]
    for r in range(n):
        rp = row_ps[r]
        for c in range(m):
            rp[c+1] = rp[c] + arr[r][c]
            col_ps[c][r+1] = col_ps[c][r] + arr[r][c]

    def range_row_sum(r: int, c1: int, c2: int) -> int:
        c1_ = max(0, c1)
        c2_ = min(m-1, c2)
        if c1_ > c2_:
            return 0
        ps = row_ps[r]
        return ps[c2_+1] - ps[c1_]

    def range_col_sum(c: int, r1: int, r2: int) -> int:
        r1_ = max(0, r1)
        r2_ = min(n-1, r2)
        if r1_ > r2_:
            return 0
        ps = col_ps[c]
        return ps[r2_+1] - ps[r1_]
