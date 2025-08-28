# 피드백
## 작성 코드
~~~python
# 1211. [S/W 문제해결 기본] 2일차 - Ladder2

def down_ladder(arr, c):
    """
    arr[0][c] 지점에서 사다리를 내려가는 루트에 드는 길이를 구하여 return
    Args:
        arr (list): 1, 0으로 이루어진 100x100 행렬
        c (int): 시작점의 x값
    Returns:
        int: 루트 길이
    """
    r = 0  # 시작점의 행
    route_length = 0  # 루트의 길이 계산

    while r < 100:  # 바닥에 닿기 전까지
        if arr[r][c - 1] == 1:  # 왼쪽에 길이 있다면
            while arr[r][c - 1] == 1:  # 왼쪽 끝까지 간다
                c -= 1
                route_length += 1  # 루트 길이에 1 추가

        elif arr[r][c + 1] == 1:  # 오른쪽에 길이 있다면
            while arr[r][c + 1] == 1:  # 오른쪽 끝까지 간다
                c += 1
                route_length += 1  # 루트 길이에 1 추가

        r += 1  # 아래로 한칸 간다
        route_length += 1  # 루트 길이에 1 추가

        while r < 100 and arr[r][c - 1] == 0 and arr[r][c + 1] == 0:  # 바닥이 아니고 양쪽이 벽이라면
            r += 1
            route_length += 1  # 사다리가 나오거나 받가이 나올 때까지 밑으로 간다

    return route_length


T = 10
for _ in range(1, T + 1):
    tc = input()
    ladder = []  # 사다리 정보를 담은 이차원 배열

    for __ in range(100):  # 사다리는 100x100
        # 양쪽에 벽을 하나씩 둔다(셀렉션)
        ladder.append([0] + list(map(int, input().split())) + [0])

    start_points = []  # 시작점 인덱스들을 모을 리스트
    for i in range(101):
        if ladder[0][i] == 1:  # 시작점이라면 인덱스 추가
            start_points.append(i)

    # 초기값 설정
    shortest_length = down_ladder(ladder, start_points[0])
    shortest_x = start_points[0]

    for start_point in start_points[1:]:  # 첫번째 건 위에서 했으므로
        current_length = down_ladder(ladder, start_point)  # 이번 start point의 루트 길이

        if current_length < shortest_length:  # 더 짧다면 루트 길이와 x를 업데이트
            shortest_length = current_length
            shortest_x = start_point

    print(f'#{tc} {shortest_x - 1}')  # 앞에 셀렉션 제외
~~~
<br><br>

## 총평
- 강점
  - 좌/우가 열려 있으면 수평으로 끝까지 이동 후 한 칸 하강, 좌·우 모두 닫히면 아래로 계속 이동하는 전형적인 사다리 탐색 로직을 잘 반영했습니다.
  - 경계 문제를 피하려고 양쪽에 0 패딩을 두는 방식이 안전하며, 내부 인덱스 연산이 단순해집니다.
- 개선 필요
  - **출력 포맷 버그 가능성**: `tc = input()`은 줄바꿈 문자를 포함할 수 있어 `print(f'#{tc} ...')`에서 줄바꿈이 끼어들 위험이 있습니다. `strip()` 또는 `int()`로 읽는 편이 안전합니다.
  - **매 테스트에서의 불필요한 연산**: 각 시작점에 대해 전체 경로를 끝까지 계산합니다. 이미 찾은 최단 경로보다 길어지면 **중간에 가지치기(early stop)** 할 수 있습니다.
  - **매직 넘버(100, 101)**: 크기를 상수/변수로 통일하면 재사용성과 가독성이 좋아집니다.
  - **중복 조건 평가**: `arr[r][c-1]` / `arr[r][c+1]` 접근이 반복되므로, 한 번 읽어 캐시하거나 흐름을 함수로 분리하면 의도가 더 명확합니다.
  - **주석·오탈자**: “받가이(=바닥이)” 등 오탈자 수정, 도큐스트링의 입력/출력 설명을 더 명확히 하면 좋습니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 시작점의 개수를 `S`(최대 약 100), 경로 길이를 `L`이라고 하면 전체는 대략 **O(S·L)**. 최악치에서 `L`은 격자 한 변 크기·수평 이동을 포함하므로 O(10^4) 수준 가능.
- 공간 복잡도: 입력 격자 O(N^2). 탐색은 상수 보조 공간 O(1).
- 병목 지점: “이미 최단보다 길어진 경로를 끝까지 시뮬레이션”하는 부분이 불필요한 연산을 유발합니다(가지치기 부재).
<br><br>

## 보완점
### 1. 가지치기(Early Stop) 추가  [중요도: High] [효과: 성능]
- **근거(Reasoning)**: 현재 최단 거리 `best`가 있을 때, 새로운 시작점에서 내려가며 누적 `route_length`가 `best` 이상이 되는 순간 탐색을 중단하면 그 시작점에 대한 나머지 시뮬레이션을 건너뛸 수 있습니다.
- **결론/리팩터**
~~~python
def down_ladder(arr, c, size, cutoff=None):
    r = 0
    length = 0
    while r < size:
        # 좌 이동
        while arr[r][c - 1] == 1:
            c -= 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
        # 우 이동
        while arr[r][c + 1] == 1:
            c += 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
        # 아래 한 칸
        r += 1
        length += 1
        if cutoff is not None and length >= cutoff:
            return length
        # 좌우 막혔으면 아래로 계속
        while r < size and arr[r][c - 1] == 0 and arr[r][c + 1] == 0:
            r += 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
    return length
~~~

<br><br>

### 2. 크기 상수화 및 포맷 안정화  [중요도: Med] [효과: 가독, 안정성]
- **근거**: `100`, `101`을 상수로 두고, `tc` 입력은 `strip()`/`int()`로 명확히 처리합니다.
- **결론/리팩터**
~~~python
SIZE = 100
PAD = 1   # 좌우 패딩
tc = int(input().strip())
row = [0] + list(map(int, input().split())) + [0]
# ...
for i in range(1, SIZE + 1):  # 패딩 제외한 유효 영역
    if ladder[0][i] == 1:
        start_points.append(i)
print(f'#{tc} {shortest_x - PAD}')
~~~

<br><br>

### 3. 함수 시그니처/주석 정제 및 타입힌트  [중요도: Low] [효과: 가독, 유지보수]
- **근거**: 입력 격자 크기와 패딩 전제를 명시하고, 타입힌트로 의도를 드러내면 디버깅이 쉽습니다.
- **결론/리팩터**
~~~python
from typing import List

def down_ladder(arr: List[List[int]], c: int, size: int, cutoff: int | None = None) -> int:
    """패딩(좌우 0)된 사다리 arr에서 (r=0, c)부터 바닥까지의 경로 길이를 반환한다.
    cutoff 이상 길어지면 즉시 중단하고 현재 길이를 반환한다."""
    # 구현은 보완점 1 참조
~~~
<br><br>

## 최종 코드 예시
~~~python
import sys
from typing import List

input = sys.stdin.readline

SIZE = 100     # 유효 격자 한 변 길이
PAD = 1        # 좌우 패딩(0) 개수

def down_ladder(arr: List[List[int]], c: int, size: int, cutoff: int | None = None) -> int:
    """패딩(좌우 0)된 사다리 arr에서 (r=0, c)부터 바닥까지 경로 길이를 반환.
    cutoff(최단 후보) 이상 길어지면 즉시 중단."""
    r = 0
    length = 0
    while r < size:
        # 왼쪽으로 가능한 만큼
        while arr[r][c - 1] == 1:
            c -= 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
        # 오른쪽으로 가능한 만큼
        while arr[r][c + 1] == 1:
            c += 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
        # 아래로 한 칸
        r += 1
        length += 1
        if cutoff is not None and length >= cutoff:
            return length
        # 좌우가 닫혀 있으면 아래로 계속
        while r < size and arr[r][c - 1] == 0 and arr[r][c + 1] == 0:
            r += 1
            length += 1
            if cutoff is not None and length >= cutoff:
                return length
    return length

def main() -> None:
    T = 10
    for _ in range(1, T + 1):
        tc = int(input().strip())  # 포맷 안정화
        ladder: List[List[int]] = []
        for _ in range(SIZE):
            # 좌우 패딩 0 추가
            ladder.append([0] + list(map(int, input().split())) + [0])

        # 시작점(맨 윗줄의 1) 수집: 유효 영역만(패딩 제외)
        start_points = [i for i in range(PAD, SIZE + PAD) if ladder[0][i] == 1]

        # 초기값: 첫 시작점으로 경로 계산
        shortest_x = start_points[0]
        shortest_len = down_ladder(ladder, shortest_x, SIZE, cutoff=None)

        # 나머지 시작점 탐색(가지치기 사용)
        for s in start_points[1:]:
            cur_len = down_ladder(ladder, s, SIZE, cutoff=shortest_len)
            if cur_len < shortest_len:
                shortest_len = cur_len
                shortest_x = s

        # 문제 포맷: 패딩 좌표를 실제 좌표로 환산
        print(f'#{tc} {shortest_x - PAD}')

if __name__ == "__main__":
    main()
~~~
