# 피드백
## 작성 코드
~~~python
# 2105. [모의 SW 역량테스트] 디저트 카페 

T = int(input())


def cal_unique_desserts(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    네 좌표를 돌며 디저트 종류 수를 return
    겹치는 게 있다면 -1을 반환한다
    """

    ate_desserts = set()  # 이미 먹은 디저트 종류 저장

    # 네 방향에 대해서 계산
    # 우하
    for x, y in zip(range(x1, x2), range(y1, y2)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  #이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 좌하
    for x, y in zip(range(x2, x3), range(y2, y3, -1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 좌상
    for x, y in zip(range(x3, x4, -1), range(y3, y4, -1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장

    # 우상
    for x, y in zip(range(x4, x1, -1), range(y4, y1)):
        dessert = cafes[x][y]
        if dessert in ate_desserts:
            return -1  # 이미 먹었으면 불가능으로 끝

        ate_desserts.add(dessert)  # 아니면 디저트 저장


    return len(ate_desserts)  # 종류 return


def find_cafe_route(r, c):
    """
    해당 지점에서 시계방향으로 돌 수 있는 모든 영역을 찾아내어 리스트로 반환하는 함수
    """

    available_routes = []

    for i in range(1, N - max(r, c) + 1):  # 하우로 얼마나 이동가능?
        nr = r + i
        nc = c + i
        # 원랜 델타 썼었는데 생각해보니까 필요없음

        if 0 <= nr < N and 0 <= nc < N:  # 범위에 든다면

            for j in range(1, N - min(nr, nc) + 1):  # 하좌로 더 가자
                nr2 = nr + j
                nc2 = nc - j

                if 0 <= nr2 < N and 0 <= nc2 < N:  # 범위에 든다면
                    nr3 = nr2 - i  # nr2에서 좌상으로 i만큼 이동한 게 셋째 꼭지점
                    nc3 = nc2 - i

                    if 0 <= nr3 < N and 0 <= nc3 < N:  # 범위에 든다면

                        available_routes.append((r, c, nr, nc, nr2, nc2, nr3, nc3))

    return available_routes


# 하우, 하좌, 상좌, 상우 시계방향 회전 델타 생성
cross_delta = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

for tc in range(1, T + 1):
    N = int(input())  # 행렬 길이

    cafes = [list(map(int, input().split())) for _ in range(N)]  # 카페 정보 담은 이차원배열

    max_desserts = -1  # 디저트를 가장 많이 먹을 떄의 디저트 수

    for row in range(N - 2):  # 아래에서 2줄은 시계 루트 불가능
        for col in range(1, N - 1):  # 좌우 1줄씩 불가능
            routes = find_cafe_route(row, col)  # 가능한 루트 계산

            for rout in routes:
                current_desserts = cal_unique_desserts(*rout)

                if current_desserts > max_desserts:  # 크다면 업데이트
                    max_desserts = current_desserts

    print(f'#{tc} {max_desserts}')
~~~
<br><br>

## 총평
- 강점
  - 정사각 격자에서 대각선 4방향(↘↙↖↗)으로 닫힌 루프를 구성하고, **디저트 종류의 중복 여부를 `set`으로 판정**하는 핵심 아이디어가 문제 의도와 잘 맞습니다.
  - 모서리를 중복 포함하지 않도록 `range(..., ...)`의 **끝점 배제**를 사용한 점이 좋습니다.
- 개선 필요
  - `find_cafe_route`의 **범위 상한이 느슨**해 많은 불필요 후보를 만들고 내부에서 다시 범위를 검사합니다(성능↓, 가독성↓).
  - 후보 루트 목록을 전부 **리스트에 적재**한 뒤 재순회 → 메모리/시간 낭비. 즉시 평가 가능.
  - `zip(range, range)` 기반의 4변 순회는 깔끔하지만, **각 변 길이를 직접 다루는 편이 더 빠르고 명확**합니다(불필요한 range/zip 생성 제거).
  - 전역(`cafes`, `N`) 의존, 타입힌트/도큐스트링 미흡.
- 병목/리스크
  - 최악 복잡도 대략 **O(N² · 후보 수 · 경로 길이)**. N≤20이라 통과 가능하나, 불필요 후보가 많아 **시간 여유가 줄 수 있음**.
<br><br>

## 복잡도 및 병목
- 시간 복잡도(현 코드 추정):  
  - 시작점 O(N²) × (i, j) 두 변 길이 조합(상수에 가까운 O(N²) 수준) × 경로 길이 O(i+j) ≲ **O(N⁵)** 근사.
- 공간 복잡도: 후보 루트 리스트 저장으로 **O(후보 수)** 추가 사용.
- 병목 지점:  
  1) 느슨한 상한으로 생성되는 **불필요 후보 루트**  
  2) **후보 리스트 누적** 후 재순회  
  3) 매 변마다 `zip(range, range)` 객체 생성
<br><br>

## 보완점
### 1. 후보 상한을 수학적으로 타이트하게 설정   [중요도: High] [효과: 성능]
- **Reasoning**: (r,c)에서 첫 변 길이를 `a≥1`로 두고 ↘ 이동 후 좌표 `(r+a, c+a)`.  
  두 번째 변 길이 `b≥1`에서 ↙ 이동 후 좌표 `(r+a+b, c+a-b)`.  
  경계 조건은:
  - `a ≤ min(N-1-r, N-1-c)`
  - `b ≤ min(N-1-(r+a), c+a)`
  이렇게 두면 내부 `if` 경계검사 대부분이 **사전에 제거**됩니다.
- **Conclusion**: `for a in range(1, a_max+1)` / `for b in range(1, b_max+1)`로 직접 생성.

<br><br>

### 2. 루트 즉시 평가(리스트 축적 제거)   [중요도: High] [효과: 성능/가독]
- **Reasoning**: 후보를 모아두지 말고, **그 자리에서 바로 `cal`** 하여 최대값 갱신.
- **Conclusion**: `find_cafe_route` 자체를 제거하고, 메인 루프에서 (a,b) 이중루프로 즉시 평가.

<br><br>

### 3. 경로 순회 최적화(직접 인덱싱)   [중요도: Med] [효과: 성능/가독]
- **Reasoning**: `zip(range, range)` 대신 **정수 증가/감소로 직접 좌표 이동**하면 오브젝트 생성 비용과 인덱싱 분기가 줄어듭니다.  
- **Conclusion**: 네 변을 `for k in range(1, a+1)`/`for k in range(1, b+1)` 형태로 전개.

<br><br>

### 4. 함수화/전역의존 제거 + 타입힌트   [중요도: Med] [효과: 유지보수]
- **Reasoning**: 테스트가 쉬워지고 사이드이펙트 감소.
- **Conclusion**: `count_loop(cafes, r, c, a, b)` 등으로 분리, `N`은 `len(cafes)`로 유도.

<br><br>

### 5. 미세 개선: 조기 종료 및 스킵   [중요도: Low] [효과: 성능]
- **Reasoning**: 현재까지 먹은 개수 + 남은 변 최대 길이로 **상한 추정** 후 `max_desserts`를 넘기기 어려우면 스킵 가능(복잡해질 수 있어 선택 사항).
- **Conclusion**: 기본 구조 최적화로도 충분히 통과되므로 선택 적용.

<br><br>

## 최종 코드 예시
~~~python
from typing import List, Set

def count_unique_on_loop(cafes: List[List[int]], r: int, c: int, a: int, b: int) -> int:
    """
    시작점 (r,c)에서 변 길이 a,b로 만드는 마름모(↘ a, ↙ b, ↖ a, ↗ b)를
    시계방향으로 한 바퀴 돌며 먹은 디저트 종류 수를 반환.
    중복 디저트가 나오면 -1 반환.
    """
    N = len(cafes)
    seen: Set[int] = set()

    # 1) ↘ a
    x, y = r, c
    for k in range(1, a + 1):
        nx, ny = x + 1, y + 1
        d = cafes[nx][ny]
        if d in seen:
            return -1
        seen.add(d)
        x, y = nx, ny

    # 2) ↙ b
    for k in range(1, b + 1):
        nx, ny = x + 1, y - 1
        d = cafes[nx][ny]
        if d in seen:
            return -1
        seen.add(d)
        x, y = nx, ny

    # 3) ↖ a
    for k in range(1, a + 1):
        nx, ny = x - 1, y - 1
        d = cafes[nx][ny]
        if d in seen:
            return -1
        seen.add(d)
        x, y = nx, ny

    # 4) ↗ b (끝나면 (r,c) 바로 위칸이 아니라 정확히 (r,c)로 돌아와야 함)
    for k in range(1, b + 1):
        nx, ny = x - 1, y + 1
        # 마지막 스텝에서 (nx, ny)가 (r, c)가 되는 것이 정상 루프
        if k == b:
            # (nx, ny) == (r, c)여야 정상 종료. (문제 조건상 항상 성립하는 a,b를 보장해 루프 생성)
            # 시작칸의 디저트는 첫 변에서 이미 포함되므로 여기서는 중복 체크만.
            return len(seen)  # 모든 칸은 seen에 한 번씩 들어갔음.
        d = cafes[nx][ny]
        if d in seen:
            return -1
        seen.add(d)
        x, y = nx, ny

    return -1  # 도달 불가(논리상 오지 않음)


def solve():
    T = int(input())
    for tc in range(1, T + 1):
        N = int(input())
        cafes = [list(map(int, input().split())) for _ in range(N)]

        ans = -1
        # 시작점은 가장자리에서는 마름모가 불가능하므로 1..N-2 사이가 안전 범위
        for r in range(0, N - 2):
            for c in range(1, N - 1):
                # 첫 변 길이 a의 상한: (r+a, c+a)가 격자 안
                a_max = min((N - 1) - r, (N - 1) - c)
                for a in range(1, a_max + 1):
                    # 두 번째 변 길이 b 상한: (r+a+b, c+a-b)가 격자 안
                    b_max = min((N - 1) - (r + a), c + a)
                    for b in range(1, b_max + 1):
                        res = count_unique_on_loop(cafes, r, c, a, b)
                        if res > ans:
                            ans = total

        print(f"#{tc} {ans}")


if __name__ == "__main__":
    solve()
~~~
