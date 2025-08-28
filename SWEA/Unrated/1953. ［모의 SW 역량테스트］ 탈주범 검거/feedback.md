# 피드백
## 작성 코드
~~~python
# 1953 탈주범 검거
"""
흉악범 탈주 후 1시간 후 맨홀로 뛰어들어감
현재 k시간 지남
지금 있을 수 있는 위치 수 계산할 것
"""


def track_criminal(r, c, spent_time):
    """
    현재 위치를 인자로 받아, 다음 위치를 다시 인자로 넣는 재귀함수
    K 시간이 지난 시점에, 도착 arr를 True로 만든다.

    Returns:

    """

    # 거쳐가는 순간 범죄자 가능 위치 True로
    if criminal_spot[r][c] > K + 1 - spent_time:
        # 다른곳에서 계산할것이다.
        return
    else:
        criminal_spot[r][c] = K + 1 - spent_time      # 남은 루트의 길이를 저장

    if spent_time == K:  # K시에 도달했다면
        # criminal_spot[r][c] = True      # 범죄자 가능 위치 True로
        # criminal_spot[r][c] = 1      # 범죄자 가능 위치 True로
        return  # 끝

    else:  # 아직이면 계속 돌려
        ele = underground[r][c]
        delta_list = turnel[underground[r][c]]
        # delta_list =
        for dr, dc in delta_list:  # 델타를 돌며
            nr = r + dr  # 새 위치 계산
            nc = c + dc

            a = 1
            pass
            # 범위에 들고 0이 아니
            if (
                    0 <= nr < LEN_ROW and  # 범위에 들고
                    0 <= nc < LEN_COL and
                    underground[nr][nc] and  # 0이 아니며
                    (-dr, -dc) in turnel[underground[nr][nc]]  # 그 터널이랑 이어진 모양새라면
            ):
                track_criminal(nr, nc, spent_time + 1)  # 도둑 보내
            else:  # 벗어나면
                continue  # 다음으로


T = int(input())
turnel = {
    # 1: [(-1, 0), (1, 0), (0, -1), (0, 1)],  # 상하좌우
    1: [(0, 1), (1, 0), (0, -1), (-1, 0)],  # 우하좌상
    2: [(-1, 0), (1, 0)],  # 상하
    3: [(0, -1), (0, 1)],  # 좌우
    4: [(-1, 0), (0, 1)],  # 상우
    5: [(1, 0), (0, 1)],  # 하우
    6: [(1, 0), (0, -1)],  # 하좌
    7: [(-1, 0), (0, -1)],  # 상좌
}

for tc in range(1, T + 1):
    # 첫 줄에는 지하 터널 지도의 세로 크기 N, 가로 크기 M, 맨홀 뚜껑이 위치한장소의 세로 위치 R, 가로 위치 C, 그리고 탈출 후 소요된 시간 K 이 주어진다.
    LEN_ROW, LEN_COL, R, C, K = map(int, input().split())

    underground = [list(map(int, input().split())) for _ in range(LEN_ROW)]

    # 범죄자 스팟 저장할 array
    criminal_spot = []
    for _ in range(LEN_ROW):
        # criminal_spot.append([False] * LEN_COL)
        criminal_spot.append([0] * LEN_COL)

    # 범죄자 돌리기. 초기는 R C 1시간
    track_criminal(R, C, 1)

    # 범죄자 수 계산
    spot_count = 0
    for i in range(LEN_ROW):
        for j in range(LEN_COL):
            spot_count += 1 if criminal_spot[i][j] else 0

    print(f'#{tc} {spot_count}')
~~~
<br><br>

## 총평
- 강점
  - 터널 타입별 방향 테이블을 잘 정의했고, **양방향 연결 검증**을 `(-dr, -dc) in turnel[...]`로 정확히 처리했습니다.
  - 시간 제한 K를 기반으로 **확장 중단**을 하려는 의도가 있습니다.
- 개선 필요
  - **정확성/안정성**: 시작 칸이 0(터널 없음)인 경우를 처리하지 않아도 방문으로 카운트될 수 있습니다.
  - **불필요 코드**: `a = 1`, `pass`, 사용하지 않는 지역변수(`ele`) 등 디버그 잔재가 남아 가독성을 해칩니다.
  - **전략 비효율**: DFS 재귀 + “남은 루트 길이”를 `criminal_spot`에 저장해 프루닝하는 방식은 로직이 복잡하고, 동일 칸을 여러 번 방문할 여지가 남습니다(조건이 `>`라서 동등/열등 업데이트가 발생).
  - **전역 의존**: `criminal_spot`, `LEN_ROW` 등 외부 상태에 강하게 의존 → 테스트/재사용 어려움.
- 병목/리스크
  - 이 문제는 **최단 시간(최소 시간)** 도달 집합을 묻기 때문에, **BFS(층별 탐색)**가 자연스럽습니다.  
    현재 DFS는 같은 칸을 더 늦은 시간에 재방문할 수 있어 불필요한 분기/호출이 증가합니다.
  - 재귀 깊이는 최대 K(문제 제한상 작지만), 반복 BFS가 더 안전합니다.
<br><br>

## 복잡도 및 병목
- 현재 구현(DFS+프루닝):
  - 시간 복잡도: 최악 시 각 칸을 여러 시간대에 재방문 가능 → **O(N·M·분기수)**로 분석이 까다롭고, 비효율 가능.
  - 공간 복잡도: 재귀 스택 **O(K)** + 보조 배열 **O(N·M)**.
- 권장 구현(BFS):
  - 시간 복잡도: 각 칸 최대 한 번 방문(연결성 검증 포함) → **O(N·M)**.
  - 공간 복잡도: 방문 배열/큐 **O(N·M)**.
  - 병목 지점 제거: 동일 칸 중복 방문 제거, 층별 종료로 조기 커팅 명확.
<br><br>

## 보완점
### 1. BFS(층별 탐색)로 전환   [중요도: High] [효과: 성능/안정성/가독]
- **Reasoning:** 시간을 레벨로 보는 문제이므로 BFS가 정답 탐색에 일치합니다. 한 번 방문(최단 도달) 이후에는 재방문이 필요 없고, 큐 기반으로 구현이 간결합니다.
- **Conclusion:** `visited[r][c]`를 사용하고, `t == K`면 확장 중단. 카운트는 방문 시 1씩 증가.

~~~python
from collections import deque

def reachable_cells_bfs(grid, R, C, K, tunnel):
    if grid[R][C] == 0:   # 시작 칸이 막혀 있으면 0
        return 0
    N, M = len(grid), len(grid[0])
    visited = [[False]*M for _ in range(N)]
    q = deque([(R, C, 1)])
    visited[R][C] = True
    count = 1

    while q:
        r, c, t = q.popleft()
        if t == K:
            continue
        for dr, dc in tunnel[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < N and 0 <= nc < M):
                continue
            if grid[nr][nc] == 0:
                continue
            # 양방향 연결 확인
            if (-dr, -dc) not in tunnel[grid[nr][nc]]:
                continue
            if visited[nr][nc]:
                continue
            visited[nr][nc] = True
            count += 1
            q.append((nr, nc, t + 1))
    return count
~~~

<br><br>

### 2. 시작 칸 예외 처리   [중요도: High] [효과: 정확성]
- **Reasoning:** 맨홀 위치가 빈 칸(0)일 수 있음. 이 경우 결과는 0이어야 합니다.
- **Conclusion:** BFS 시작 전에 `grid[R][C] == 0` 체크로 즉시 반환.

<br><br>

### 3. 불필요/죽은 코드 제거   [중요도: Med] [효과: 가독]
- **Reasoning:** `a = 1`, `pass`, 주석 처리된 진리값 표기, 사용되지 않는 지역변수 등은 오해를 유발.
- **Conclusion:** 전부 제거.

<br><br>

### 4. 전역 의존 축소 + 함수화   [중요도: Med] [효과: 유지보수]
- **Reasoning:** 테스트/재사용 편의성을 위해 함수 인자로 모든 의존성 전달.
- **Conclusion:** `reachable_cells_bfs(grid, R, C, K, tunnel)` 형태로 구성.

<br><br>

### 5. 네이밍 및 오탈자   [중요도: Low] [효과: 가독]
- **Reasoning:** `turnel` → `tunnel`로 표기 통일.
- **Conclusion:** 딕셔너리 이름 수정.

<br><br>

## 최종 코드 예시
~~~python
from collections import deque
from typing import List, Tuple, Dict

# 터널 타입 → 이동 가능한 방향(상,하,좌,우)
TUNNEL: Dict[int, List[Tuple[int, int]]] = {
    1: [(0, 1), (1, 0), (0, -1), (-1, 0)],  # 우 하 좌 상
    2: [(-1, 0), (1, 0)],                  # 상 하
    3: [(0, -1), (0, 1)],                  # 좌 우
    4: [(-1, 0), (0, 1)],                  # 상 우
    5: [(1, 0), (0, 1)],                   # 하 우
    6: [(1, 0), (0, -1)],                  # 하 좌
    7: [(-1, 0), (0, -1)],                 # 상 좌
}

def reachable_cells_bfs(grid: List[List[int]], R: int, C: int, K: int) -> int:
    """맨홀 (R,C)에서 시작해 K시간 내 도달 가능한 칸의 수를 BFS로 계산."""
    N, M = len(grid), len(grid[0])
    if K <= 0:
        return 0
    if not (0 <= R < N and 0 <= C < M):
        return 0
    if grid[R][C] == 0:
        return 0

    visited = [[False] * M for _ in range(N)]
    q = deque([(R, C, 1)])
    visited[R][C] = True
    count = 1

    while q:
        r, c, t = q.popleft()
        if t == K:  # 더 이상 확장하지 않음
            continue

        for dr, dc in TUNNEL[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < N and 0 <= nc < M):
                continue
            if grid[nr][nc] == 0:
                continue
            # 양방향 연결 가능한지 확인
            if (-dr, -dc) not in TUNNEL[grid[nr][nc]]:
                continue
            if visited[nr][nc]:
                continue

            visited[nr][nc] = True
            count += 1
            q.append((nr, nc, t + 1))
    return count


# 입출력
T = int(input())
for tc in range(1, T + 1):
    N, M, R, C, K = map(int, input().split())
    underground = [list(map(int, input().split())) for _ in range(N)]
    ans = reachable_cells_bfs(underground, R, C, K)
    print(f"#{tc} {ans}")
~~~
