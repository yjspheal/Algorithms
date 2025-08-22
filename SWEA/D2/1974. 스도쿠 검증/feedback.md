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
