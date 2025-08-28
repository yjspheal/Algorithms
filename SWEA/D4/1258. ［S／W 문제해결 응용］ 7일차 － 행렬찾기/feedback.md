# 피드백
## 작성 코드
~~~python
T = int(input())
for tc in range(1, T + 1):
    N = int(input())  # NxN
    chemicals = [list(map(int, input().split())) for _ in range(N)]

    sizes = []  # 서브 matrix 크기 담을 리스트

    # 화학물질 통이 겹칠 수 없다
    dr = [0, 1]  # 우 좌
    dc = [1, 0]

    for r in range(N):
        for c in range(N):
            if chemicals[r][c] > 0:  # 화학 칸이면
                nr, nc = r, c
                while 0 <= nr + 1 < N and chemicals[nr + 1][c] > 0:  # 화학칸일 때까지 아래로
                    nr += 1

                while 0 <= nc + 1 < N and chemicals[r][nc + 1] > 0:  # 화학칸일 때까지 오른
                    nc += 1

                # 사각형을 모두 0화
                for i in range(r, nr + 1):
                    for j in range(c, nc + 1):
                        chemicals[i][j] = 0

                row = nr - r + 1  # 사이즈 계산
                col = nc - c + 1

                sizes.append((row * col, row, col))

    sizes.sort()  # 맨 앞 값 기준으로 sort

    print(f'#{tc} {len(sizes)}', end=' ')
    for size in sizes:
        print(size[1], size[2], end=' ')

    print()
~~~
<br><br>

## 총평
- 강점
  - (r,c)에서 **아래로 높이, 오른쪽으로 너비**를 측정하고 해당 직사각형을 0으로 지우는 방식은 각 칸을 최대 한 번만 처리하므로 효율적입니다.
  - 결과를 `(면적, 행, 열)`로 저장 후 정렬해 요구 정렬(면적 우선, 다음 행)도 자연스럽게 충족합니다.
- 개선 필요
  - `dr/dc`는 사용되지 않습니다(제거 권장).
  - 경계값에서 `99` 같은 매직 넘버는 없지만, 내부 while의 조건식이 길어 가독성이 떨어집니다(변수로 빼서 명확히).
  - 정렬 키를 명시적으로 두어 “면적 → 행 → 열”을 분명히 표현하는 편이 유지보수에 안전합니다.
- 병목/리스크
  - 시간복잡도는 각 칸을 한 번만 0으로 만들므로 **O(N²)**, 정렬은 **O(R log R)**(R=서브행렬 수). 병목은 없음.
  - 스캔 순서가 행우선이므로 **항상 직사각형의 좌상단에서만 측정**하게 되어 정확합니다(지운 뒤 재방문하지 않음).

<br><br>

## 복잡도 및 병목
- 시간 복잡도: 격자 스캔 O(N²) + 결과 정렬 O(R log R) (R ≤ N²)  
- 공간 복잡도: 입력 O(N²) + 결과 리스트 O(R)
- 병목 지점: 없음(상수 인자 개선만 여지)

<br><br>

## 보완점
### 1) 불필요 변수 제거 및 조건식 정리   [중요도: Low] [효과: 가독성]
- **Reasoning**: 사용하지 않는 `dr/dc` 제거, while 조건을 의미 있는 변수(`down_ok`, `right_ok`)로 분해하면 읽기 쉬움.
- **Conclusion**: 코드를 간결화하고 의도를 명확히 표현.

### 2) 정렬 키 명시   [중요도: Low] [효과: 가독성/안정성]
- **Reasoning**: 현재도 `(면적, 행, 열)`로 정렬되지만, 키를 명시하면 요구사항 변경 시 대응이 쉬움.
- **Conclusion**: `sizes.sort(key=lambda x: (x[0], x[1], x[2]))`.

### 3) 함수화/타입힌트로 구조화   [중요도: Low] [효과: 유지보수]
- **Reasoning**: 핵심 로직을 함수로 분리해 테스트/재사용이 쉬워짐.
- **Conclusion**: `find_submatrices()`로 분리.

<br><br>

## 최종 코드 예시
~~~python
import sys
from typing import List, Tuple

input = sys.stdin.readline

def find_submatrices(grid: List[List[int]]) -> List[Tuple[int, int, int]]:
    """
    0/양수로 이루어진 격자에서 '연속 양수'로 채워진 직사각형 블록들을 찾아
    (면적, 행수, 열수) 튜플로 반환한다. 방문한 블록은 0으로 지워 재방문을 방지한다.
    """
    n = len(grid)
    res: List[Tuple[int, int, int]] = []

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                continue

            # 높이 측정(아래로 연속 양수)
            rr = r
            while rr + 1 < n and grid[rr + 1][c] > 0:
                rr += 1
            height = rr - r + 1

            # 너비 측정(오른쪽으로 연속 양수)
            cc = c
            while cc + 1 < n and grid[r][cc + 1] > 0:
                cc += 1
            width = cc - c + 1

            # 블록 지우기(0으로 설정)
            for i in range(r, r + height):
                for j in range(c, c + width):
                    grid[i][j] = 0

            res.append((height * width, height, width))

    # 면적 → 행 → 열 기준 오름차순
    res.sort(key=lambda x: (x[0], x[1], x[2]))
    return res


T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    chemicals = [list(map(int, input().split())) for _ in range(N)]

    sizes = find_submatrices(chemicals)

    print(f"#{tc} {len(sizes)}", end=" ")
    for _, r, c in sizes:
        print(r, c, end=" ")
    print()
~~~
