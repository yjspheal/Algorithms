# 📑 목차
- [기존 코드](#기존-코드)
- [총평](#총평)
- [복잡도 및 병목](#복잡도-및-병목)
- [보완점](#보완점)
  - [1. 3×3 검사 인덱스 버그 수정 (`j`의 시작값)  [중요도: High] [효과: 안정성]](#1-3×3-검사-인덱스-버그-수정-j의-시작값--중요도-high-효과-안정성)
  - [2. `sudoku += zip(*sudoku)`로 원본을 변형하지 않기  [중요도: High] [효과: 안정성/가독]](#2-sudoku--zipsudo쿠로-원본을-변형하지-않기--중요도-high-효과-안정성가독)
  - [3. 중복 카운팅 로직 단순화(비트마스크/셋)  [중요도: Med] [효과: 성능/가독]](#3-중복-카운팅-로직-단순화비트마스크셋--중요도-med-효과-성능가독)
  - [4. 조기 종료(early return)와 함수 분리  [중요도: Med] [효과: 성능/유지보수]](#4-조기-종료early-return와-함수-분리--중요도-med-효과-성능유지보수)
  - [5. 타입힌트/PEP8/입출력 주석 정리  [중요도: Low] [효과: 가독/유지보수]](#5-타입힌트pep8입출력-주석-정리--중요도-low-효과-가독유지보수)
- [최종 코드 예시](#최종-코드-예시)

<br><br>

# 기존 코드
~~~python
# 1974. 스도쿠 검증

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    # 9x9 스도쿠 이차원배열
    sudoku = [list(map(int, input().split())) for _ in range(9)]
    sudoku += list(zip(*sudoku))        # 열을 행으로 바꿔서 밑에 추가

    is_valid = 1       # 스도쿠 맞는지 여부

    for line in sudoku:     # 각 줄을 돌며
        status = [0] * 10       # 1 ~ 9까지 값이 각 몇개인지 담을 리스트

        for num in line:
            status[num] += 1    # 해당 숫자 갯수 1 증가

            if status[num] > 1:     # 근데 그 값이 1 초과라면
                is_valid = 0
                break               # 스도쿠 아님 + break

        else:       # break가 안 됐다면 continue
            continue

        # break가 됐었다는 뜻이므로 해당 스도쿠를 완전히 벗어난다.
        break


    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            status = [0] * 10  # 1 ~ 9까지 값이 각 몇개인지 담을 리스트
            for i in range(row, row+3):
                for j in range(row, row+3):
                    num = sudoku[i][j]

                    status[num] += 1  # 해당 숫자 갯수 1 증가

                    if status[num] > 1:     # 근데 그 값이 1 초과라면
                        is_valid = 0
                        break               # 스도쿠 아님 + break

                # for문이 많으므로 그냥 break없이 다 돌자.

    print(f'#{tc} {is_valid}')
~~~
<br><br>

# 총평
- 전반 아이디어(행/열/박스 중복 검사)는 적절합니다. 다만 **원본 그리드를 변형**하고(**행 아래 열을 덧붙임**), **3×3 박스 루프의 인덱스 버그** 때문에 오동작 가능성이 큽니다.
- 행/열 검증을 같은 배열에서 처리하려고 `sudoku += zip(*sudoku)`를 쓰면 이후 인덱싱이 18행 기준이 되어 **박스 검사에서 엉뚱한 영역**을 볼 수 있습니다.
- 중복 카운트용 리스트는 동작하지만, **비트마스크(또는 set)** 가 더 간결하고 빠릅니다.
- 루프 내 `break` 처리 흐름이 복잡합니다. **검증 함수를 분리**하고 조기 종료(early return)로 단순화하는 편이 좋습니다.

# 복잡도 및 병목
- N=9 고정 문제라 빅오 차이는 체감상 미미합니다. 그래도 현재 구조는
  - 행 9개 + 열 9개 + 박스 9개 × 각 9칸 검사 → **O(81)**.
- 병목보다 **버그/가독성/유지보수**가 핵심 이슈입니다.

# 보완점
## 1. 3×3 검사 인덱스 버그 수정 (`j`의 시작값)  [중요도: High] [효과: 안정성]
- 현재:
  ```python
  for i in range(row, row+3):
      for j in range(row, row+3):  # ← BUG: j는 col부터 시작해야 함
  ```
- 올바른 범위:
  ```python
  for i in range(row, row+3):
      for j in range(col, col+3):  # col 사용
  ```

## 2. `sudoku += zip(*sudoku)`로 원본을 변형하지 않기  [중요도: High] [효과: 안정성/가독]
- 열 검증을 위해 원본 배열에 열을 **덧붙이면** 이후 인덱싱이 복잡해지고 박스 검사 범위와 **충돌**합니다.
- 대신, **행은 그대로**, **열은 `zip(*sudoku)`로 별도 순회**, **박스는 좌표 기반으로 별도 검사**하세요.

## 3. 중복 카운팅 로직 단순화(비트마스크/셋)  [중요도: Med] [효과: 성능/가독]
- 리스트 카운팅 대신 비트마스크:
  - 각 숫자 `x(1..9)`에 대해 `bit = 1 << (x-1)`를 OR 하며, 이미 켜진 비트가 나오면 중복.
  - 분기/메모리 접근이 줄어들어 깔끔하고 빠릅니다.
- 또는 `len(set(line)) == 9`를 쓰되 **모든 값이 1..9**인지도 확인하세요.

## 4. 조기 종료(early return)와 함수 분리  [중요도: Med] [효과: 성능/유지보수]
- `is_valid_row/col/box`를 함수로 쪼개고, 하나라도 실패 시 즉시 `0` 반환.
- 테스트 케이스 루프는 결과만 출력.

## 5. 타입힌트/PEP8/입출력 주석 정리  [중요도: Low] [효과: 가독/유지보수]
- `List[List[int]]` 타입힌트, 의미 있는 함수명/변수명 사용.
- 외부 파일 의존(`sys.stdin = open('input.txt')`)은 주석 처리하고, 주석으로 **샘플 입력**을 안내.

# 최종 코드 예시
~~~python
from typing import List
import sys

input = sys.stdin.readline


def valid_group_1to9(nums: List[int]) -> bool:
    """
    길이 9의 숫자 배열이 1..9를 중복 없이 정확히 1개씩 포함하는지 검사.
    비트마스크로 중복을 탐지한다.
    """
    mask = 0
    for x in nums:
        if x < 1 or x > 9:
            return False
        bit = 1 << (x - 1)
        if mask & bit:
            return False
        mask |= bit
    # 1..9가 모두 한 번씩 등장했는지 (필요 시 아래 한 줄로도 검증 가능: mask == (1<<9)-1)
    return True


def is_valid_sudoku(board: List[List[int]]) -> bool:
    # 행 검사
    for r in range(9):
        if not valid_group_1to9(board[r]):
            return False

    # 열 검사
    for c in range(9):
        col = [board[r][c] for r in range(9)]
        if not valid_group_1to9(col):
            return False

    # 3x3 박스 검사
    for sr in (0, 3, 6):        # start row
        for sc in (0, 3, 6):    # start col
            box = [board[r][c] for r in range(sr, sr + 3) for c in range(sc, sc + 3)]
            if not valid_group_1to9(box):
                return False

    return True


def main() -> None:
    T = int(input())
    for tc in range(1, T + 1):
        board = [list(map(int, input().split())) for _ in range(9)]
        print(f"#{tc} {1 if is_valid_sudoku(board) else 0}")


if __name__ == "__main__":
    # 표준 입력 예시
    # 1
    # 7 3 5 6 1 4 8 9 2
    # 8 4 2 9 7 3 5 6 1
    # 9 6 1 5 8 2 4 3 7
    # 1 9 7 8 5 6 3 2 4
    # 2 5 3 1 4 7 6 8 9
    # 4 8 6 3 2 9 1 7 5
    # 3 7 8 4 9 1 2 5 6
    # 5 1 9 2 6 8 7 4 3
    # 6 2 4 7 3 5 9 1 8
    main()
~~~
