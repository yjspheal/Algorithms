# 피드백
## 작성 코드
~~~python
# 배열 돌리기 4

import sys
input = sys.stdin.readline
# sys.stdin = open('input.txt')

import itertools
from copy import deepcopy


def rotate_clockwise_arr(arr, mid_r, mid_c, s):
    """
    arr[mid_r][mid_c]를 중심으로, s길이만큼 시계방향으로 1만큼 rotate하는 함수

    Args:
        arr (list): 숫자로 이루어진 이중리스트
        mid_r (int): 중심이 될 행의 인덱스
        mid_r (int): 중심이 될 열의 인덱스
        s (int): rotate시킬 범위

    Notes:
        arr 원본을 변환합니다.
    """
    for i in range(1, s + 1):
        # 좌 상 우 하 인덱스
        left = mid_c - i
        top = mid_r - i
        right = mid_c + i
        bottom = mid_r + i

        # 일단 빼서 저장. 하나씩 돌리며 덮어씌우므로 첫번째 값은 따로 저장해준다.
        left_top = arr[top][left]

        # 왼쪽줄 끌어올리기
        for r in range(top + 1, bottom + 1):
            arr[r - 1][left] = arr[r][left]

        # 아랫줄 왼쪽으로 당기기
        for c in range(left + 1, right + 1):
            arr[bottom][c - 1] = arr[bottom][c]

        # 오른쪽 끌어내리기
        for r in range(bottom - 1, top - 1, -1):
            arr[r + 1][right] = arr[r][right]

        # 윗줄 오른쪽으로 당기기
        for c in range(right - 1, left - 1, -1):
            arr[top][c + 1] = arr[top][c]

        arr[top][left + 1] = left_top  # 빠진값 채워주기


# NxM, 회전연산 수 K
N, M, K = map(int, input().rstrip().split())

# 배열 받기
nums = [list(map(int, input().rstrip().split())) for _ in range(N)]
nums_copy = deepcopy(nums)      # 원본 저장용

rotates = []    # 연산들. permutation 용
# K번의 연산
for _ in range(K):
    temp_row, temp_col, temp_step = map(int, input().split())

    rotates.append((temp_row, temp_col, temp_step))

# 최소합 할당
min_sum = float('inf')


for perm in itertools.permutations(rotates):
    for row, col, step in perm:
        # 인덱스 맞춰주기
        rotate_clockwise_arr(nums, row - 1, col - 1, step)

    # 업데이트
    for i in range(len(nums)):
        if sum(nums[i]) < min_sum:
            min_sum = sum(nums[i])

    nums = deepcopy(nums_copy)        # 다시 원본으로 변경

print(min_sum)
~~~
<br><br>

## 총평
- 강점
  - 레이어(테두리) 단위로 한 칸씩 **시계 방향 회전**을 정확히 구현했고, 연산 순열 전부를 적용해 **최소 행 합**을 탐색하는 접근이 문제 의도와 일치합니다.
  - 인덱스 계산(좌/상/우/하 경계 및 저장-이동-복원 순서)이 올바르며, K≤6인 특성상 전수(permutation) 탐색이 현실적입니다.
- 개선 필요
  - `deepcopy`를 매 순열마다 사용 → 리스트의 리스트 구조에서는 **얕은 복사(list comprehension)**로 충분하며 더 가볍습니다.
  - 행 합 업데이트에서 `sum(nums[i])`를 두 번 호출(비교·대입) → **한 번만 계산**하거나 `min(map(sum, ...))`으로 일괄 처리하면 깔끔합니다.
  - 회전 함수의 도큐스트링에서 인자 설명이 **mid_c 설명 누락/복제**(오탈자).
  - 전역에서 1-index → 0-index 보정을 **매 호출마다** 수행 중. 미리 0-index로 변환해두면 호출부가 단순해집니다.
- 병목/리스크
  - 시간 복잡도: 대략 `O(K! * K * L)` (L은 모든 레이어 둘레 합). N, M ≤ 50, K ≤ 6이므로 충분.  
  - 병목은 주로 **불필요한 복사와 합계 재계산**(가독성·미세 성능).

<br><br>

## 복잡도 및 병목
- 시간 복잡도: `O(K! * K * (∑레이어둘레))` ≈ `O(K! * K * (N+M)*S)` (S: 최대 s).  
- 공간 복잡도: `O(N*M)` (원본 보드 + 작업 보드), 추가는 상수.
- 병목 지점: `deepcopy` 반복, 행 합 반복 계산.

<br><br>

## 보완점
### 1. 얕은 복사로 작업 보드 생성  [중요도: High] [효과: 성능/가독]
- **Reasoning:** 보드는 숫자만 담은 2차원 리스트 → `board = [row[:] for row in base]`면 충분.  
- **Conclusion:** 순열마다 `deepcopy` 대신 얕은 복사를 사용.

~~~python
board = [row[:] for row in base]
~~~

<br><br>

### 2. 행 합 계산 단순화  [중요도: Med] [효과: 가독]
- **Reasoning:** 루프 내 `sum` 중복 호출 대신 한 번에 최소를 계산.
- **Conclusion:** `min_sum = min(min_sum, min(map(sum, board)))`.

<br><br>

### 3. 연산을 미리 0-index로 변환  [중요도: Low] [효과: 가독]
- **Reasoning:** 매 호출의 `-1` 제거로 호출부 간결.
- **Conclusion:** 입력 시 `rotates0.append((r-1, c-1, s))`.

<br><br>

### 4. 도큐스트링 오탈자 수정 및 타입힌트  [중요도: Low] [효과: 유지보수]
- **Reasoning:** 파라미터 설명 일치, 타입 명시로 의도 명확화.
- **Conclusion:** 함수 시그니처/주석 정리.

<br><br>

## 최종 코드 예시
~~~python
import sys
import itertools
from typing import List, Tuple

input = sys.stdin.readline

def rotate_clockwise_arr(arr: List[List[int]], mid_r: int, mid_c: int, s: int) -> None:
    """
    중심 (mid_r, mid_c)를 기준으로, 거리 1..s의 모든 레이어를 '시계 방향'으로 한 칸씩 회전한다.
    arr는 제자리(in-place)에서 수정된다.
    """
    for i in range(1, s + 1):
        left, top  = mid_c - i, mid_r - i
        right, bottom = mid_c + i, mid_r + i

        saved = arr[top][left]  # 왼쪽 위 모서리 값 저장

        # 왼쪽 열 위로 끌어올리기
        for r in range(top + 1, bottom + 1):
            arr[r - 1][left] = arr[r][left]
        # 아래 행 왼쪽으로 밀기
        for c in range(left + 1, right + 1):
            arr[bottom][c - 1] = arr[bottom][c]
        # 오른쪽 열 아래로 내리기
        for r in range(bottom - 1, top - 1, -1):
            arr[r + 1][right] = arr[r][right]
        # 위 행 오른쪽으로 밀기
        for c in range(right - 1, left - 1, -1):
            arr[top][c + 1] = arr[top][c]

        # 비운 자리 채우기
        arr[top][left + 1] = saved


# 입력
N, M, K = map(int, input().split())
base = [list(map(int, input().split())) for _ in range(N)]

ops: List[Tuple[int, int, int]] = []
for _ in range(K):
    r, c, s = map(int, input().split())
    ops.append((r - 1, c - 1, s))  # 0-index로 변환

min_sum = float('inf')

for perm in itertools.permutations(ops):
    board = [row[:] for row in base]  # 얕은 복사로 작업 보드 생성
    for r, c, s in perm:
        rotate_clockwise_arr(board, r, c, s)
    # 행 합의 최소 갱신
    min_sum = min(min_sum, min(map(sum, board)))

print(min_sum)
~~~
