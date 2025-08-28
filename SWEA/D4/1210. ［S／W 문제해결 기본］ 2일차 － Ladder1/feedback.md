# 피드백
## 작성 코드
~~~python
# 1210. [S/W 문제해결 기본] 2일차 - Ladder1

"""
idea
1. 도착지에서 시작해서 거슬러 올라간다.
2. 좌 or 우를 만난다면 막힐 때까지, 즉 1인동안 해당 방향으로 계속 이동
3. 막히면, 좌우를 만날 때까지 올라간다.
4. 행이 0이되면 해당 col값을 출력

[제약 사항]
한 막대에서 출발한 가로선이 다른 막대를 가로질러서 연속하여 이어지는 경우는 없다.
"""

def climb_ladder(arr, end_c):
    """
    0(벽), 1(길), 2(도착점)로 이루어진 이차원 리스트 arr에 대해서, 1만을 이어서 2에 도달하게 되는 루트의 시작점의 col값을 반환
    단, 경로는 위에서 아래로만 진행되어야 함

    Args:
        arr (list): 0, 1, 2로 이루어진 이차원 리스트
        end_c (int): 도착점의 열 값

    Returns:
        int: 시작점의 col 값
    """
    N = 100     # 총 행 수

    r = N - 1      # 현재는 마지막줄이므로 99에 위치
    c = end_c   # 현재 col 위치

    # 방금까지 왼쪽으로 왔으면 오른쪽에 길이 있는 것이 당연
    # 그렇게 가면 무한으로 도므로 방지용 변수 제작
    going_right = False
    going_left = False

    while r > 0:    # 행이 0이 되면 끝
        # 왼쪽에 길이 있다면
        if 0 <= c - 1 < N and arr[r][c - 1] == 1 and not going_right:
            # 끝까지 간다
            while True:
                going_left = True
                c -= 1
                if c == 0 or arr[r][c-1] == 0:      # 열이 0, 즉 왼쪽 끝에 도달했거나 벽에 막히게되면 break
                    r -= 1 if r > 0 else 0     # 첫줄이 아니라면 1 올라간다
                    break

        # 오른쪽에 길이 있다면
        # print(r, c)
        if 0 <= c + 1 < N and arr[r][c + 1] == 1 and not going_left:
            # 끝까지 간다
            while True:
                going_right = True
                c += 1
                if c == 99 or arr[r][c+1] == 0:      # 열이 99, 즉 오른쪽 끝에 도달했거나 벽에 막히게되면 break
                    r -= 1 if r > 0 else 0     # 첫줄이 아니라면 1 올라간다
                    break

        # 좌우가 막혔다면 위로 올라감. 다만 이번엔 막힐 때까지가 아닌, 다음 좌우가 나올 때까지.
        while (r > 0) and (c == 0 and arr[r][c+1] == 0) or (c == 99 and arr[r][c-1] == 0) or (1 <= c < N and arr[r][c-1] == 0 and arr[r][c+1] == 0):
        # 너무 긴데...?
            going_left = going_right = False    # 로 초기화
            r -= 1
            if r == 0:  # 첫 행에 도달했다면 break
                break

    # 현재 c가 출발 c가 된다.
    return c

T = 10  # 테케 10으로 고정
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    _ = int(input())  # 테케 번호와 동일
    ladder = [list(map(int, input().split())) for _ in range(100)]  # 사다리 정보 담긴 이차원 배열

    # 도착점 찾기
    end_col = 0
    for c in range(100):
        if ladder[-1][c] == 2:      # 2는 항상 마지막줄에있으므로
            end_col = c

    # 첫 col값 찾기
    start_col = climb_ladder(ladder, end_col)

    print(f'#{tc} {start_col}')
~~~
<br><br>

## 총평
- 강점
  - “좌/우는 끝까지 진행, 그 외에는 위로”라는 **사다리 역추적 규칙**을 잘 포착했습니다.
  - 경계 체크(0/99)와 진행 방향 플래그를 두어 **왕복(좌→우→좌…)을 방지**하려는 의도가 드러납니다.
- 개선 필요
  - **불리언 우선순위 버그 가능성**:  
    아래 긴 while 조건은 `and`가 `or`보다 먼저 평가됩니다.  
    ```python
    while (r > 0) and (cond1) or (cond2) or (cond3):
    ```  
    실제로는 `((r>0) and cond1) or cond2 or cond3`가 되어, `r==0`이어도 `cond2`/`cond3`가 참이면 루프에 들어갈 수 있는 형태입니다(내부에서 다시 `r==0` 처리로 탈출하더라도 **의도와 다름**). 또한 이 조건식은 **가독성/검증 난이도**가 매우 높습니다.
  - **방향 플래그 복잡도**: `going_left/going_right` 조합과 중첩 while-True 구조는 **분기 상태 폭발**과 실수 유발 여지가 큽니다.
  - **매직 넘버**: `99` 같은 상수 대신 `N-1`를 사용하면 안전합니다.
  - **도큐스트링 문구**: “경로는 위에서 아래로만 진행”은 본 코드(아래→위 역추적)와 불일치.

<br><br>

## 복잡도 및 병목
- 시간 복잡도: 한 칸을 좌/우/상으로만 이동하며 되돌아가지 않도록 구현하면 **O(R·C)** 이하(100×100 고정).  
- 공간 복잡도: **O(1)** (상수 변수만 사용).
- 병목/리스크: 로직 복잡성으로 인한 **경계/우선순위 실수**가 가장 큰 리스크입니다.

<br><br>

## 보완점
### 1) 좌/우는 “끝까지”, 그 후 한 칸 “위로” 단순화   [중요도: High] [효과: 가독/안정성]
- **Reasoning**: 사다리 규칙상 가로선을 만나면 **해당 방향으로 연속된 1을 끝까지 이동** 후 위로 한 칸 올라가면 됩니다. 방향 플래그/복잡한 조건 없이 세 구문으로 충분합니다:  
  (1) 왼쪽에 1 → 왼쪽으로 쭉, 그 다음 위로 1  
  (2) 아니고 오른쪽에 1 → 오른쪽으로 쭉, 그 다음 위로 1  
  (3) 좌/우 모두 0 → 위로 1
- **Conclusion (핵심 루프):**
~~~python
while r > 0:
    # 왼쪽으로 갈 수 있으면 끝까지
    if c > 0 and grid[r][c-1] == 1:
        while c > 0 and grid[r][c-1] == 1:
            c -= 1
        r -= 1
    # 오른쪽으로 갈 수 있으면 끝까지
    elif c + 1 < M and grid[r][c+1] == 1:
        while c + 1 < M and grid[r][c+1] == 1:
            c += 1
        r -= 1
    # 좌우 모두 막힘 → 위로
    else:
        r -= 1
~~~

### 2) 매직 넘버 제거 및 경계 안전화   [중요도: Med] [효과: 안정성]
- `N=100, M=100`을 사용하고, 인덱스 비교는 `0 <= c-1`, `c+1 < M` 형태로 표준화.

### 3) 도착점 탐색/함수 문구 정리   [중요도: Low] [효과: 가독성]
- `end_col = ladder[-1].index(2)`로 간결화(항상 존재 가정).  
- 도큐스트링은 실제 동작(아래→위 역추적)을 반영.

<br><br>

## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline

def climb_ladder(grid, end_c):
    """
    사다리 격자(grid)에서 마지막 행의 도착 열 end_c에서 시작해
    좌/우 가로선을 만나면 그 방향으로 '연속된 1'을 끝까지 이동한 뒤 위로 1칸,
    좌우가 모두 0이면 위로 1칸 올라가며,
    최상단(행 0)에 도달했을 때의 열 인덱스를 반환한다.
    """
    N, M = len(grid), len(grid[0])
    r, c = N - 1, end_c

    while r > 0:
        # 왼쪽으로 계속
        if c > 0 and grid[r][c - 1] == 1:
            while c > 0 and grid[r][c - 1] == 1:
                c -= 1
            r -= 1
        # 오른쪽으로 계속
        elif c + 1 < M and grid[r][c + 1] == 1:
            while c + 1 < M and grid[r][c + 1] == 1:
                c += 1
            r -= 1
        # 좌우 모두 막힘 → 위로
        else:
            r -= 1
    return c

T = 10
for tc in range(1, T + 1):
    _ = int(input().strip())  # 테스트 케이스 번호(사용 안 함)
    ladder = [list(map(int, input().split())) for _ in range(100)]
    end_col = ladder[-1].index(2)  # 마지막 행에서 2의 열 찾기
    print(f"#{tc} {climb_ladder(ladder, end_col)}")
~~~
