- [기존 코드](#기존-코드)
- [총평](#총평)
- [복잡도 및 병목](#복잡도-및-병목)
- [보완점](#보완점)
  - [1. 순열별 작업 배열 분리로 `deepcopy` 최소화  \[중요도: High\] \[효과: 성능/가독\]](#1-순열별-작업-배열-분리로-deepcopy-최소화--중요도-high-효과-성능가독)
  - [2. 회전 로직을 "레이어 단위" 유틸로 분리  \[중요도: Med\] \[효과: 가독/안정성\]](#2-회전-로직을-레이어-단위-유틸로-분리--중요도-med-효과-가독안정성)
  - [3. 합 계산 단순화 및 중복 연산 제거  \[중요도: Med\] \[효과: 성능/가독\]](#3-합-계산-단순화-및-중복-연산-제거--중요도-med-효과-성능가독)
  - [4. PEP8/타입힌트/도큐스트링 정리  \[중요도: Low\] \[효과: 가독/유지보수\]](#4-pep8타입힌트도큐스트링-정리--중요도-low-효과-가독유지보수)
- [최종 코드 예시](#최종-코드-예시)


# 기존 코드
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

# 총평
- 핵심 로직(테두리 레이어를 시계 방향으로 1칸 회전)은 정공법으로 잘 구현되어 있습니다.
- `itertools.permutations`로 연산 순서를 전부 시도하는 접근은 (K ≤ 6) 문제 제약에 부합합니다.
- 다만, 매 순열 처리 후 `deepcopy`로 원본 복구를 하는 구조는 불필요한 전체 복사를 유발합니다(가독/성능 모두 손해).
- 함수/변수 네이밍과 도큐스트링에 오타가 있어 유지보수성이 떨어집니다(매개변수 설명에서 `mid_c`가 `mid_r`로 중복 표기).
- 입력/출력, 회전 함수, 순열 적용을 명확히 분리하면 테스트가 용이하고 버그 가능성이 줄어듭니다.
<br><br>

# 복잡도 및 병목
- 시간 복잡도:
  - 한 번의 "회전 연산"(`r,c,s`) 처리: 바깥에서 안쪽으로 `s`개의 레이어, 각 레이어는 둘레 길이 O(N+M)에 선형. ⇒ **O(s·(N+M))**.
  - 연산 순서 전부 탐색: 순열 수 K! (K ≤ 6). ⇒ 전체 **O(K! · K · s · (N+M))** 수준(연산 K개를 순서대로 적용하므로 K 배수 포함).
- 공간 복잡도:
  - 현재 구현: `nums_copy`에 대한 **O(N·M)** 추가 메모리 + 매 순열마다 `deepcopy` 재할당.
- 병목 지점:
  - **메모리/복사 병목**: 순열 루프 끝에서 `nums = deepcopy(nums_copy)` (파일 말미). K! 번 전체 배열을 깊은 복사.
  - **합 계산 중복**: 같은 행 합을 두 번 이상 계산할 수 있음(`sum(nums[i])`를 if와 min 업데이트에서 각각 호출).  
<br><br>

# 보완점
## 1. 순열별 작업 배열 분리로 `deepcopy` 최소화  [중요도: High] [효과: 성능/가독]
- 원본 `nums`를 보존하고, **순열마다 작업용 배열을 얕은 복사로 한 번만 생성**(각 행 슬라이싱)하여 그 위에 회전을 적용하세요.
- 순열 끝날 때마다 deep copy로 원복하지 않고, 다음 순열에서 다시 원본으로부터 복사하면 됩니다.
~~~python
work = [row[:] for row in nums]   # 순열 시작 시 1회
# ... 회전 적용 ...
# 다음 순열에서 다시 원본으로부터 복사
~~~

<br><br>

## 2. 회전 로직을 "레이어 단위" 유틸로 분리  [중요도: Med] [효과: 가독/안정성]
- 현재 함수는 중심좌표/반경을 입력받아 내부에서 레이어 인덱스를 산출합니다.  
  레이어 회전을 담당하는 헬퍼(`rotate_layer_clockwise`)를 두고, 외부에서 top/left/bottom/right를 넘기면 **경계 계산이 명확**해집니다.
- 또한 도큐스트링의 매개변수 오타(`mid_c`)를 바로잡고 타입힌트를 추가하세요.
~~~python
def rotate_layer_clockwise(a, top, left, bottom, right): ...
def apply_op(a, r, c, s):  # 1-indexed 입력을 0-index로 변환 후 레이어 돌리기
    r -= 1; c -= 1
    for d in range(1, s+1):
        rotate_layer_clockwise(a, r-d, c-d, r+d, c+d)
~~~

<br><br>

## 3. 합 계산 단순화 및 중복 연산 제거  [중요도: Med] [효과: 성능/가독]
- `min_sum = min(min_sum, min(map(sum, work)))` 형태로 한 번에 처리하면 **코드가 짧고 `sum` 호출 중복**이 없습니다.
~~~python
min_sum = min(min_sum, min(map(sum, work)))
~~~

<br><br>

## 4. PEP8/타입힌트/도큐스트링 정리  [중요도: Low] [효과: 가독/유지보수]
- 매개변수 설명 오타 수정(`mid_c`) 및 함수 분리로 도메인 의도가 명확해집니다.
- 표준 라이브러리만 사용해 타입힌트를 추가하세요.
~~~python
from typing import List, Tuple
def apply_op(a: List[List[int]], r: int, c: int, s: int) -> None: ...
~~~

<br><br>

# 최종 코드 예시
~~~python
"""
Baekjoon 17406 - 배열 돌리기 4

- K (≤ 6) 회전 연산의 순서를 전부 시도하여, 적용 후 각 행 합의 최솟값의 최소를 구한다.
- 순열(최대 720개)마다 작업 배열을 생성하여 원본 복원을 위한 deepcopy를 제거.
- 회전은 레이어(사각 테두리)를 오른쪽(시계)으로 1칸 회전.
"""

from typing import List, Tuple
import sys
import itertools

input = sys.stdin.readline


def rotate_layer_clockwise(a: List[List[int]], top: int, left: int, bottom: int, right: int) -> None:
    """
    사각 경계 [top..bottom] x [left..right]의 테두리를 시계 방향으로 1칸 회전한다.
    a를 제자리에서 수정한다.
    """
    if top >= bottom or left >= right:
        return

    saved = a[top][left]  # 맨 좌상단을 보관

    # 왼쪽 열: 위로 끌어올림 (top+1..bottom) -> (top..bottom-1)
    for r in range(top + 1, bottom + 1):
        a[r - 1][left] = a[r][left]

    # 아래 행: 왼쪽으로 당김 (left+1..right) -> (left..right-1)
    for c in range(left + 1, right + 1):
        a[bottom][c - 1] = a[bottom][c]

    # 오른쪽 열: 아래로 내림 (bottom-1..top) -> (bottom..top+1)
    for r in range(bottom - 1, top - 1, -1):
        a[r + 1][right] = a[r][right]

    # 위 행: 오른쪽으로 당김 (right-1..left) -> (right..left+1)
    for c in range(right - 1, left - 1, -1):
        a[top][c + 1] = a[top][c]

    # 비워진 (top, left+1)에 saved 채우기
    a[top][left + 1] = saved


def apply_op(a: List[List[int]], r: int, c: int, s: int) -> None:
    """
    단일 연산 (r, c, s)을 a에 적용한다.
    문제 입력의 (r, c)는 1-indexed 중심. 내부에서는 0-index로 변환해 사용.
    각 d=1..s 레이어를 시계 방향으로 1칸 회전.
    """
    r -= 1
    c -= 1
    for d in range(1, s + 1):
        top, left = r - d, c - d
        bottom, right = r + d, c + d
        rotate_layer_clockwise(a, top, left, bottom, right)


def main() -> None:
    N, M, K = map(int, input().split())
    base: List[List[int]] = [list(map(int, input().split())) for _ in range(N)]
    ops: List[Tuple[int, int, int]] = [tuple(map(int, input().split())) for _ in range(K)]

    ans = float("inf")

    for order in itertools.permutations(ops):
        # 순열마다 작업용 배열 1회 생성 (얕은 복사)
        work = [row[:] for row in base]

        # 연산 순서대로 적용
        for r, c, s in order:
            apply_op(work, r, c, s)

        # 각 행의 합 중 최솟값으로 갱신
        row_min = min(map(sum, work))
        if row_min < ans:
            ans = row_min

    print(ans)


if __name__ == "__main__":
    # 예시 입력이 없으면 주석으로 사용 예를 참고하세요.
    # 아래는 간단한 테스트 예시입니다.
    # 입력 예시:
    # 5 6 2
    # 1 2 3 2 5 6
    # 3 8 7 2 1 3
    # 8 2 3 1 4 5
    # 3 4 5 1 1 1
    # 9 3 2 1 4 3
    # 3 4 2
    # 4 2 1
    #
    # 기대 출력: 12
    #
    # 실제 제출 시에는 온라인 저지의 입력을 사용합니다.
    main()
~~~
