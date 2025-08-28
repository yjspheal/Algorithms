# 피드백
## 작성 코드
~~~python
# 1949. [모의 SW 역량테스트] 등산로 조성

def update_longest(l):
    """
    루트의 길이 l이 기존 최장 길이(전역 변수)보다 높다면 최장 길이를 업데이트하는 함수
    """
    global longest_route

    if l > longest_route:
        longest_route = l


def find_route(r, c, route_length, is_worked):
    """
    현재 지도의 좌표와 공사 여부를 인자로 받아, 다음 이동할 위치를 계속 찾아가며
    하나의 루트를 찾아내는 재귀함수
    Args:
        r (int): 현재 위치의 행 좌표
        c (int): 현재 위치의 열 좌표
        route_length (int): 현재까지 거쳐온 루트의 길이
        is_worked (bool): 공사 했는지 여부 표시 bool
    """

    for i in range(4):  # 상하좌우를 돌며
        nr = r + dr[i]  # 새 좌표 계산
        nc = c + dc[i]

        if (
                0 <= nr < LENGTH and 0 <= nc < LENGTH and  # 다음 위치가 범위에 들고
                not visited[nr][nc]  # 방문한 적이 없다면
        ):

            if mountains[nr][nc] < mountains[r][c]:  # 현재 위치보다 봉우리가 낮다면
                visited[nr][nc] = True  # 여기 방문 완
                find_route(nr, nc, route_length + 1, is_worked)  # 새 좌표, 길이+1, 공사진행여부유지 후 재귀
                visited[nr][nc] = False  # 여기 방문 취소

            elif mountains[nr][nc] >= mountains[r][c] and is_worked is False:  # 봉우리는 높지만 공사를 아직 안 했다면
                height_diff = mountains[nr][nc] - mountains[r][c]  # 높이 차 계산

                if WORK_DEPTH > height_diff:  # 공사 가능 깊이가 높이 차보다 크다면
                    origin = mountains[nr][nc]
                    mountains[nr][nc] = mountains[r][c] - 1  # 다음 높이를 현재높이 - 1로 만들고 함수를 돌린다

                    visited[nr][nc] = True  # 여기 방문 완
                    find_route(nr, nc, route_length + 1, True)
                    visited[nr][nc] = False  # 여기 방문 취소

                    mountains[nr][nc] = origin  # 다시 돌아와~

                # 아니면 계산할 필요가 없다...

    else:  # 언젠가는 공사도 하고 사방이 현재위치보다 높아져서 for문을 못 도는 때가 온다
        update_longest(route_length)
        return


T = int(input())

dr = [-1, 1, 0, 0]  # 상하좌우 델타
dc = [0, 0, -1, 1]

for tc in range(1, T + 1):

    # 지도 한 변의 길이, 최대 공사 가능 깊이
    LENGTH, WORK_DEPTH = map(int, input().strip().split())

    mountains = [list(map(int, input().split())) for _ in range(LENGTH)]  # 산 정보 담을 리스트

    highest_height = 0  # 젤 높은 산 높이
    highest_spots = set()  # 젤 높은 산의 좌표 담을 set

    for idx_row, row in enumerate(mountains):
        for idx_col, mountain in enumerate(row):

            if mountain > highest_height:  # 젤높은 키를 갱신했다면
                highest_height = mountain
                highest_spots = set()  # 지금까지 담은 젤 높은 키 집합을 리셋하고
                highest_spots.add((idx_row, idx_col))  # 좌표를 추가

            elif mountain == highest_height:  # 동일하다면 좌표만 추가
                highest_spots.add((idx_row, idx_col))

    longest_route = 0  # 젤 긴 루트 길이

    # 젤 높은 산들의 좌표를 돌며
    for h_r, h_c in highest_spots:
        visited = [[False] * LENGTH for _ in range(LENGTH)]  # 방문여부
        visited[h_r][h_c] = True  # 여기 방문 완
        find_route(h_r, h_c, 1, False)  # 아직 안 했으니까 공사여부 False

    print(f'#{tc} {longest_route}')
~~~
<br><br>

## 총평
- 강점
  - DFS 백트래킹 구조가 명확하며, “한 번만 공사(깎기)” 제약을 `is_worked` 플래그로 깔끔히 표현.
  - 공사 시 인접 칸을 `현재높이-1`로 바로 깎는 전략은 각 분기에서 최장 경로를 노리는 합리적 그리디 + 백트래킹 조합.
  - 방문 관리와 원복(restore) 로직이 올바르게 배치되어 사이드이펙트 최소화.
- 개선 필요
  - 전역변수(`longest_route`) 의존, 상수처럼 보이는 `LENGTH`, `WORK_DEPTH`를 대문자/전역으로 취급 → 테스트 케이스 루프와 섞여 가독성 저하.
  - `highest_spots`는 집합(set)일 필요가 없어 오버헤드. 한 번씩만 추가되는 좌표이므로 리스트가 적절.
  - 함수/변수 네이밍과 타입힌트/도큐스트링이 부족해 유지보수성 저하(`is_worked` → `used_dig` 등 도메인 용어 일관성).
  - `for-else`는 파이썬 숙련자 외엔 가독성 저하 가능. “막다른 길” 처리 분리를 고려.
- 병목/리스크
  - 최악의 경우 DFS 분기가 많아질 수 있음(격자 전체 단순 경사에 가까운 경우). 다만 SWEA 제약(N≤8, K≤5)에서는 실용적으로 충분.
  - 매 시작점마다 `visited` 새로 생성. N이 작아 성능 문제는 적지만 로컬 재사용 패턴으로 미세 개선 여지.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 시작점 수를 H라 할 때, 각 시작점에서 백트래킹 분기가 최대 4, 경로 길이 최대 N²이므로 이론상 상한은 지수적이지만, 방문 체크로 경로 길이가 상한 N²로 제한되며 실제 입력 범위에선 충분히 수렴.
- 공간 복잡도: `visited` O(N²), 재귀 깊이 최대 O(N²). 입력 제약에서 안전.
- 병목 지점: `find_route` 내부의 4방 탐색 루프와 공사 분기. 불필요한 조건/조회 최소화가 체감 성능에 기여.
<br><br>

## 보완점
### 1. 전역 상태 제거 및 캡슐화  [중요도: High] [효과: 가독, 안정성]
- **근거(Reasoning):** `longest_route`, `LENGTH`, `WORK_DEPTH`, `dr/dc` 등 전역 의존은 테스트/재사용/버그 추적을 어렵게 합니다. 테스트 케이스마다 값이 바뀌므로 지역화가 바람직합니다.
- **결론(Refactor 코드):**
~~~python
from typing import List, Tuple

def solve_case(n: int, k: int, mountains: List[List[int]]) -> int:
    dr, dc = (-1, 1, 0, 0), (0, 0, -1, 1)
    best = 0

    def dfs(r: int, c: int, length: int, used_dig: bool, visited: List[List[bool]]) -> None:
        nonlocal best
        moved = False
        cur_h = mountains[r][c]

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if visited[nr][nc]:
                continue

            nh = mountains[nr][nc]
            if nh < cur_h:
                visited[nr][nc] = True
                dfs(nr, nc, length + 1, used_dig, visited)
                visited[nr][nc] = False
                moved = True
            elif not used_dig:
                diff = nh - cur_h
                if k > diff:                    # d >= diff+1 <= k
                    origin = nh
                    mountains[nr][nc] = cur_h - 1
                    visited[nr][nc] = True
                    dfs(nr, nc, length + 1, True, visited)
                    visited[nr][nc] = False
                    mountains[nr][nc] = origin
                    moved = True

        if not moved:
            if length > best:
                best = length
~~~
<br><br>

### 2. 시작점 수집 로직 단순화(한 번의 최대값 탐색 후 좌표 수집)  [중요도: Med] [효과: 가독]
- **근거:** set 리셋/추가보다 “최대 높이 계산 → 동일 좌표 수집” 2-pass가 읽기 쉽고 비용이 매우 작음. 중복 좌표가 없으므로 list로 충분.
- **결론(예시 코드):**
~~~python
max_h = max(max(row) for row in mountains)
starts: List[Tuple[int, int]] = [
    (r, c)
    for r in range(n)
    for c in range(n)
    if mountains[r][c] == max_h
]
~~~
<br><br>

### 3. 불변 상수/네이밍/PEP8/타입힌트 정비  [중요도: Med] [효과: 가독, 유지보수]
- **근거:** `is_worked`→`used_dig`, `LENGTH/WORK_DEPTH`→`n/k` 등 도메인 용어와 소문자 지역변수는 PEP8에 부합. 타입힌트와 간결한 도큐스트링은 의도를 명확히 함.
- **결론(스니펫):**
~~~python
def dfs(r: int, c: int, length: int, used_dig: bool, visited: List[List[bool]]) -> None:
    """현재 (r,c)에서 시작하여 최장 등산로 갱신을 시도한다."""
    ...
~~~
<br><br>

### 4. for-else 제거로 “막다른 길” 의도 명확화  [중요도: Low] [효과: 가독]
- **근거:** `for-else`는 파이썬 특성에 익숙하지 않으면 오해될 수 있음. `moved` 플래그로 종료처리를 분리하면 읽기 쉬움.
- **결론:** 위 ①의 `moved` 처리 참조.
<br><br>

### 5. 미세 최적화: 지역 변수 캐싱/조건 순서  [중요도: Low] [효과: 성능(미세)]
- **근거:** 재귀의 핵심 루프에서 `mountains[r][c]`를 `cur_h`로 캐싱, 경계/방문 체크를 먼저 수행해 분기 비용을 줄임(파이썬 인터프리터에서 미세하지만 누적 효과).
- **결론:** ① 스니펫 반영됨.
<br><br>

## 최종 코드 예시
~~~python
from typing import List, Tuple

def solve_case(n: int, k: int, mountains: List[List[int]]) -> int:
    """
    SWEA 1949 등산로 조성: 한 격자에서 시작해 인접 4방으로 strictly 하강하며,
    전체 경로 중 정확히 한 번만 최대 k 깊이까지 '깎기'를 허용할 때 만들 수 있는 최장 경로 길이.
    """
    dr, dc = (-1, 1, 0, 0), (0, 0, -1, 1)
    best = 0

    def dfs(r: int, c: int, length: int, used_dig: bool, visited: List[List[bool]]) -> None:
        nonlocal best
        moved = False
        cur_h = mountains[r][c]

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if visited[nr][nc]:
                continue

            nh = mountains[nr][nc]
            if nh < cur_h:
                visited[nr][nc] = True
                dfs(nr, nc, length + 1, used_dig, visited)
                visited[nr][nc] = False
                moved = True
            elif not used_dig:
                diff = nh - cur_h
                # 깎기 깊이 d는 1..k이고, nh - d < cur_h 이려면 d > diff이므로 k > diff여야 함.
                if k > diff:
                    origin = nh
                    mountains[nr][nc] = cur_h - 1  # 가장 유리한 높이로 깎기
                    visited[nr][nc] = True
                    dfs(nr, nc, length + 1, True, visited)
                    visited[nr][nc] = False
                    mountains[nr][nc] = origin
                    moved = True

        if not moved:
            if length > best:
                best = length

    # 시작점(최고 봉우리) 수집: 2-pass로 단순 명료
    max_h = max(max(row) for row in mountains)
    starts: List[Tuple[int, int]] = [
        (r, c)
        for r in range(n)
        for c in range(n)
        if mountains[r][c] == max_h
    ]

    for sr, sc in starts:
        visited = [[False] * n for _ in range(n)]
        visited[sr][sc] = True
        dfs(sr, sc, 1, False, visited)

    return best


# --- 입력/출력 래퍼 ---
import sys
input = sys.stdin.readline

T = int(input().strip())
for tc in range(1, T + 1):
    n, k = map(int, input().split())
    mountains = [list(map(int, input().split())) for _ in range(n)]
    ans = solve_case(n, k, mountains)
    print(f'#{tc} {ans}')
~~~
