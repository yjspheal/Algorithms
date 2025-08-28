# 피드백
## 작성 코드
~~~python
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

## 총평
- 강점
  - 중복 여부를 카운팅 배열로 즉시 판별 → 구현이 직관적임.
  - 조기 종료(`break`)로 불필요한 순회를 줄이려는 의도 좋음.
- 개선 필요
  - **정확성 이슈(버그)**: 3×3 검사에서 내부 루프가 `for j in range(row, row+3)`로 되어 있어 열 인덱스를 잘못 사용함(→ `range(col, col+3)`이어야 함).
  - **자료 구조 변조 리스크**: 열 검증을 위해 `sudoku += list(zip(*sudoku))`로 원본 그리드를 변형. 이후 3×3 블록 인덱싱이 **18×9** 구조에 적용되어 의도와 다르게 작동할 수 있음(행/열 혼합, `tuple` 혼입).
  - 카운팅 배열은 간단하지만, 1~9를 정확히 한 번씩 포함하는지의 “완전성” 검증을 일관되게 보장하기 위해 모듈화가 필요.
- 병목/리스크
  - 입력 크기(9×9)는 작아 시간·공간 모두 상수 수준. 주요 리스크는 **정확성**과 **가독성/유지보수성**.
<br><br>

## 복잡도 및 병목
- 시간 복잡도:  
  - 행 9개 + 열 9개 + 블록 9개 각각 9원소 검사 ⇒ 총 81×3 = 243 원소 처리 → **O(1)** (상수).
- 공간 복잡도:  
  - 카운팅 배열/비트마스크 등 보조 메모리 **O(1)**.
- 병목 지점:  
  - 병목은 없음. 이 문제는 **정확성(인덱싱/구조 변조)**이 핵심 리스크.
<br><br>

## 보완점
### 1. 3×3 블록 인덱싱 버그 수정   [중요도: High] [효과: 정확성]
- 현재 `for j in range(row, row+3)`로 열 인덱스를 행 기준 변수로 사용. **정확히는 `range(col, col+3)`**이어야 하며, 이 오류로 잘못된 셀을 검사함.  
- 또한 열 검증을 위해 그리드를 변형하면 블록 인덱싱이 어긋날 수 있으므로, **원본 그리드는 그대로 두고** 열/블록은 별도 순회로 검사하는 것이 안전.

~~~python
for r0 in (0, 3, 6):
    for c0 in (0, 3, 6):
        # for i in range(r0, r0+3):
        #     for j in range(r0, r0+3):  # ❌
        for i in range(r0, r0+3):
            for j in range(c0, c0+3):    # ✅
                ...
~~~

<br><br>

### 2. 열 검증 시 원본 그리드 변조 금지 (`zip(*grid)`는 순회에만 사용)   [중요도: High] [효과: 안정성/가독성]
- `sudoku += list(zip(*sudoku))`는 행 리스트에 열 튜플을 이어붙여 **형태를 바꾸는** 동작. 이후 인덱싱이 꼬일 수 있음.
- 권장: 원본 `grid`를 유지하고, **행/열/블록**을 각각 별도의 루프로 검사.

~~~python
grid = [list(map(int, input().split())) for _ in range(9)]
# 행 검사: for row in grid
# 열 검사: for col in zip(*grid)   # append 금지, '그냥 순회'만
# 블록 검사: 3중 루프 (0,3,6)
~~~

<br><br>

### 3. 중복 검증 유틸 함수화(비트마스크/셋)   [중요도: Med] [효과: 가독성/성능]
- 매번 카운팅 배열을 초기화하는 대신 **비트마스크** 또는 **집합**을 쓰면 코드가 짧고 오류가 줄어듭니다.  
- 비트마스크는 1~9 각각을 1비트로 대응, 이미 본 수면 `mask & (1<<v)`로 검출.

~~~python
def valid_unit(nums) -> bool:
    mask = 0
    for v in nums:
        if not (1 <= v <= 9): 
            return False
        bit = 1 << v
        if mask & bit:        # 중복
            return False
        mask |= bit
    # 1~9가 정확히 한 번씩이면 mask == 0b1111111110 (값 2~512 합)
    return mask == 0b1111111110
~~~

*간단히 하려면* `return set(nums) == set(range(1,10))`도 가능(조금 더 파이써닉).  

<br><br>

### 4. 조기 종료 로직 정리   [중요도: Med] [효과: 가독성]
- 현재 `for-else-continue-break` 패턴은 읽기 난이도↑.  
- `if not valid_unit(...): is_valid = 0;` 후 **즉시 루프 탈출**하는 구조로 단순화.

~~~python
ok = True
for row in grid:
    if not valid_unit(row):
        ok = False
        break
if ok:
    for col in zip(*grid):
        if not valid_unit(col):
            ok = False
            break
...
~~~

<br><br>

### 5. 함수화/타입힌트/도큐스트링   [중요도: Low] [효과: 유지보수]
- 채점 환경에서도 문제없고, 테스트/재사용이 쉬워짐.

~~~python
from typing import List

def is_valid_sudoku(grid: List[List[int]]) -> int:
    """유효한 스도쿠면 1, 아니면 0 반환"""
    ...
~~~

<br><br>

## 최종 코드 예시
~~~python
from typing import List, Iterable

def valid_unit(nums: Iterable[int]) -> bool:
    """1~9가 정확히 1번씩 등장하면 True"""
    mask = 0
    for v in nums:
        if not (1 <= v <= 9):
            return False
        bit = 1 << v
        if mask & bit:            # 이미 본 숫자
            return False
        mask |= bit
    # 1~9가 모두 포함되었는지 확인: 비트 1~9가 1이어야 함 (0b1111111110)
    return mask == 0b1111111110


def is_valid_sudoku(grid: List[List[int]]) -> int:
    """9x9 스도쿠 유효성 검사. 유효하면 1, 아니면 0."""
    # 행 검사
    for row in grid:
        if not valid_unit(row):
            return 0

    # 열 검사 (원본 변조 없이 순회만)
    for col in zip(*grid):
        if not valid_unit(col):
            return 0

    # 3x3 블록 검사
    for r0 in (0, 3, 6):
        for c0 in (0, 3, 6):
            block = []
            for i in range(r0, r0 + 3):
                for j in range(c0, c0 + 3):   # ✅ 열 인덱스는 c0 기준
                    block.append(grid[i][j])
            if not valid_unit(block):
                return 0

    return 1


T = int(input())
for tc in range(1, T + 1):
    grid = [list(map(int, input().split())) for _ in range(9)]
    print(f"#{tc} {is_valid_sudoku(grid)}")
~~~
