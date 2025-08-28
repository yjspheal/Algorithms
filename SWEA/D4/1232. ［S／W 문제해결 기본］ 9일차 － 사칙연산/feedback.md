
# 피드백
## 기존 코드
~~~python
# 1232 사칙연산

def post_order(node_info):
    """
    후위순회하며 노드 값을 계산
    """
    len_node_info = len(node_info)

    if len_node_info == 2:  # 노드 길이가 2면. 즉 리프라면
        return node_info[1]  # 값을 리턴

    else:
        num1 = int(post_order(tree[int(node_info[2])]))  # 후위순회 왼
        num2 = int(post_order(tree[int(node_info[3])]))  # 후위순회 오

        operator = node_info[1]  # 리프가 아니면 모두 연산자이다

        # 값을 업데이트한다.
        if operator == '+':
            node_info[1] = num1 + num2
        elif operator == '-':
            node_info[1] = num1 - num2
        elif operator == '*':
            node_info[1] = num1 * num2
        else:  # 사칙연산만 들어있다. 소수점 아래는 버린다.
            node_info[1] = num1 // num2

    return node_info[1]  # 업데이트된 값을 리턴한다.


T = 10
for tc in range(1, T + 1):
    N = int(input())  # 노드 수

    # tree 초기화. 인덱스 맞추기 위해 앞에 빈 리스트 추가
    tree = [[]] + [list(input().split()) for _ in range(N)]

    # 루트노드의 번호는 항상 1이다
    print(f'#{tc} {post_order(tree[1])}')
~~~
<br><br>

## 총평
- (강점) 입력 포맷을 그대로 담아 재귀로 후위평가를 수행하며 전체 시간 복잡도는 O(N)로 적절합니다.
- (개선 필요) 전역 변수 `tree`에 의존하고, `node_info`를 **제자리 갱신(mutation)** 하는 설계는 가독성과 안정성을 떨어뜨립니다. 타입이 섞인 리스트(문자/정수)도 유지보수가 어렵습니다.
- (리스크) `int()`를 중복 호출하고, 잘못된 입력(자식 인덱스 범위, 0으로 나눗셈)에 대한 예외 처리가 없습니다. `return node_info[1]`이 항상 정수임을 보장하지 않는 구조입니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 각 노드를 한 번씩 방문하므로 **O(N)**.
- 공간 복잡도: 트리 저장 **O(N)**, 재귀 콜스택 **O(H)** (H는 트리 높이).
- 병목 지점:
  - `post_order()` 내부에서 `int(post_order(...))`로 **불필요한 형 변환**(라인: 왼/오 평가) → 결과가 이미 정수라면 중복 연산.
  - `node_info[1]`에 연산 결과를 **덮어쓰기** → 동일 노드 재평가 시 의도치 않은 값/타입 혼합 가능성.
  - **전역 의존** `tree` → 테스트/재사용 어려움.
<br><br>

## 보완점
### 1. 전역 제거: (tree, idx) 인터페이스로 변경  [중요도: High] [효과: 가독/안정성/테스트 용이]
- `post_order(tree, idx)` 형태로 바꾸고, 함수 외 상태에 의존하지 않도록 합니다.
~~~python
def evaluate(tree, idx: int) -> int:
    token = tree[idx]
    # ...
~~~
<br><br><br>

### 2. 불변 평가: 입력 변경 금지  [중요도: High] [효과: 안정성/가독]
- `node_info[1]`에 결과를 덮어쓰지 말고 **로컬 변수**에서 계산 후 반환합니다. 입력은 파싱된 **토큰/자식 인덱스**만 보관합니다.
~~~python
# before: node_info[1] = num1 + num2
# after:
return num1 + num2
~~~
<br><br><br>

### 3. 명시적 파싱 + 타입힌트  [중요도: Med] [효과: 가독/유지보수]
- 노드 레코드를 `(op_or_val, left, right)` 형태로 통일하고, 리프/연산자 판단을 명시적으로 합니다.
- 타입힌트를 부여하고 도큐스트링에 입력 포맷을 정의합니다.
~~~python
from typing import List, Tuple, Optional

Node = Tuple[str, Optional[int], Optional[int]]  # (token, left, right)
~~~
<br><br><br>

### 4. 불필요한 형변환/분기 정리  [중요도: Med] [효과: 성능/가독]
- `post_order()`가 이미 정수를 반환하면 `int()` 제거.
- 연산자 분기는 dict 디스패치로 간결화 가능합니다(표준 라이브러리 `operator` 사용도 가능).
~~~python
ops = {'+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b, '/': lambda a,b: a//b}
return ops[token](evaluate(tree, L), evaluate(tree, R))
~~~
*주의: 문제의 정의가 **정수 나눗셈**임을 전제로 `//` 사용.
<br><br><br>

### 5. 입력 검증 및 예외 메시지  [중요도: Low] [효과: 안정성]
- 자식 인덱스 범위, 0으로 나누기 방지, 알 수 없는 토큰에 대한 명확한 에러 메시지.
~~~python
if token == '/' and right_val == 0:
    raise ZeroDivisionError("division by zero at node ...")
~~~
<br><br><br>

## 최종 코드 예시
~~~python
from typing import List, Tuple, Optional, Dict, Callable

# SWEA 1232 포맷 가정:
# - 리프: "i value"
# - 내부: "i op left right"
#  i는 1-based 인덱스, 루트는 1

Node = Tuple[str, Optional[int], Optional[int]]  # (token, left, right)

def parse_tree(n: int, lines: List[str]) -> List[Node]:
    """
    입력 라인들을 파싱하여 1-based 인덱스 트리 배열을 생성한다.
    각 원소는 (token, left, right) 형태:
      - 리프: (정수문자열, None, None)
      - 내부: (연산자문자열, left_idx, right_idx)
    """
    tree: List[Node] = [("", None, None)] * (n + 1)  # 0번은 더미
    for line in lines:
        parts = line.split()
        idx = int(parts[0])
        if len(parts) == 2:
            # leaf
            token = parts[1]  # 숫자 문자열로 보관 (평가 시 int 변환)
            tree[idx] = (token, None, None)
        elif len(parts) == 4:
            token, l, r = parts[1], int(parts[2]), int(parts[3])
            tree[idx] = (token, l, r)
        else:
            raise ValueError(f"Invalid line format: {line}")
    return tree

def evaluate(tree: List[Node], idx: int) -> int:
    """
    주어진 트리에서 idx를 루트로 하는 서브트리를 후위 순회로 평가하여 정수를 반환한다.
    입력 트리는 변경하지 않는다.
    """
    token, left, right = tree[idx]

    # 리프 노드
    if left is None and right is None:
        try:
            return int(token)
        except ValueError as e:
            raise ValueError(f"Invalid leaf value at node {idx}: {token}") from e

    # 내부 노드: 연산자
    if left is None or right is None:
        raise ValueError(f"Malformed internal node {idx}: missing children")

    if not (0 < left < len(tree)) or not (0 < right < len(tree)):
        raise IndexError(f"Child index out of range at node {idx}: ({left}, {right})")

    a = evaluate(tree, left)
    b = evaluate(tree, right)

    if token == '+':
        return a + b
    elif token == '-':
        return a - b
    elif token == '*':
        return a * b
    elif token == '/':
        if b == 0:
            raise ZeroDivisionError(f"Division by zero at node {idx}")
        return a // b  # 문제 정의: 정수 나눗셈(내림)
    else:
        raise ValueError(f"Unknown operator at node {idx}: {token}")

def solve() -> None:
    """
    SWEA 1232 사칙연산 풀이 드라이버.
    표준 입력에서 T, 각 테스트케이스의 N과 N개의 노드 라인을 읽어 결과를 출력한다.
    """
    import sys
    input = sys.stdin.readline

    T = 10
    for tc in range(1, T + 1):
        N = int(input().strip())
        lines = [input().strip() for _ in range(N)]
        tree = parse_tree(N, lines)
        ans = evaluate(tree, 1)  # 루트는 1
        print(f"#{tc} {ans}")

if __name__ == "__main__":
    # 실제 온라인저지에서는 표준입력을 사용.
    # 아래는 로컬 테스트용 예시입니다. 사용 시 주석 해제하여 확인하세요.
    """
    import io, sys
    sample = """\
1
7
1 - 2 3
2 - 4 5
3 / 6 7
4 8
5 7
6 20
7 5
"""
    sys.stdin = io.StringIO(sample)
    """
    solve()
~~~
