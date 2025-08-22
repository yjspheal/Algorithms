# [D4] [S/W 문제해결 기본] 9일차 - 중위순회 - 1231 

[문제 링크](https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV140YnqAIECFAYD) 

### 성능 요약

메모리: 53,888 KB, 시간: 69 ms, 코드길이: 776 Bytes

### 제출 일자

2025-08-22 15:19

> 출처: SW Expert Academy, https://swexpertacademy.com/main/code/problem/problemList.do

<br>
<br>

# 피드백
# 기존 코드
~~~python
# 1231 중위순회

import sys

sys.stdin = open('input.txt')


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

# 총평
- (강점) 재귀적 후위순회로 식 트리 평가를 간결히 구현.
- (개선 필요) 함수가 전역 변수 `tree`에 의존하고, 입력 포맷을 `len(node_info)==2`에 하드코딩하여 취약.
- (명명/문제 불일치) 파일 헤더는 **1231 중위순회**인데, 실제 풀이는 **사칙연산 트리 평가(보통 SWEA 1232)** 입니다. 헷갈림 유발.
- (타입 혼용) `return`에서 문자열/정수 타입이 섞이고, 매 스텝 `int()` 캐스팅이 중복.
- (I/O 의존) `sys.stdin = open('input.txt')`로 외부 파일에 의존 — 온라인 저지에서 실패 위험.
<br><br>

# 복잡도 및 병목
- 시간 복잡도: 각 노드를 정확히 한 번 방문하므로 **O(N)**.
- 공간 복잡도: 재귀 호출 스택이 트리 높이 H에 비례 → **O(H)** (최악 O(N)).
- 병목 지점:
  - `post_order()` 내부의 잦은 `int()` 변환 및 리스트 인덱싱(문자열 형태 유지) → 불필요한 변환 비용.
  - 전역 `tree` 접근(함수 외부 상태 의존) → 테스트/재사용 어려움, 버그 유발.
<br><br>

# 보완점
## 1. 전역 제거 & 명확한 자료구조로 파싱  [중요도: High] [효과: 안정성/가독]
- 트리를 `dict[int, tuple(value|op, left, right)]`로 보관하고, `eval_node(tree, idx)`처럼 인자로 주입.
- 리프는 `(value, None, None)`로 통일해 `len==2` 같은 취약한 체크 제거.

~~~python
def eval_node(tree: dict[int, tuple[str, int|None, int|None]], idx: int) -> int:
    val, left, right = tree[idx]
    if left is None and right is None:
        return int(val)
    a = eval_node(tree, left)
    b = eval_node(tree, right)
    # 연산 적용 ...
~~~

<br><br><br>

## 2. 타입 일관성 확보(항상 int 반환)  [중요도: High] [효과: 안정성]
- 리프에서 문자열을 그대로 반환했다가 상위에서 `int()`로 강제 캐스팅하는 패턴 제거.
- 연산 결과는 항상 `int`로 유지.

~~~python
# 리프에서 바로 int로 변환
if left is None and right is None:
    return int(val)
~~~

<br><br><br>

## 3. 입력 파싱을 견고하게(가변 길이 라인)  [중요도: Med] [효과: 안정성/가독]
- 한 줄이 `idx, token[, l, r]` 형태이므로 길이에 따라 분기하여 안전 파싱.
- 불필요한 앞의 빈 리스트(`tree=[[]]+...`) 제거하고 1-based 인덱스를 그대로 dict 키로 사용.

~~~python
parts = input().split()
i = int(parts[0])
if len(parts) == 2:              # 리프
    tree[i] = (parts[1], None, None)
else:                            # 내부 노드
    tree[i] = (parts[1], int(parts[2]), int(parts[3]))
~~~

<br><br><br>

## 4. 예외 처리 & 0-나눗셈 방지  [중요도: Low] [효과: 안정성]
- 문제에서 0으로 나누는 입력이 없다고 가정하더라도, 방어적으로 체크하면 디버깅 편의 증가.

~~~python
if op == '/':
    if b == 0:
        raise ZeroDivisionError("division by zero in input tree")
    return a // b
~~~

<br><br><br>

## 5. 명명 및 문서화 정리  [중요도: Low] [효과: 가독]
- 파일/주석의 문제 번호를 실제 로직(사칙연산 평가)과 일치시키기.
- 함수/변수 이름을 역할 중심으로: `post_order` → `eval_node`.
<br><br><br>

# 최종 코드 예시
~~~python
"""
사칙연산 이진트리 평가 (SWEA 1232 스타일 입력 가정)
- 각 라인: idx value [left right]
- 리프: "idx number"
- 내부노드: "idx op left right" (op in + - * /), 나눗셈은 정수 나눗셈(//)

입출력 예시는 온라인 저지 형식에 맞춰 표준입력을 사용합니다.
"""

from typing import Dict, Tuple, Optional

Node = Tuple[str, Optional[int], Optional[int]]  # (token, left, right)


def eval_node(tree: Dict[int, Node], idx: int) -> int:
    """
    주어진 트리에서 idx를 루트로 하는 서브트리를 후위순회로 평가하여 정수값을 반환.
    항상 int를 반환하며, 리프는 (정수문자열, None, None) 형태라고 가정.
    """
    token, left, right = tree[idx]
    if left is None and right is None:  # 리프
        return int(token)

    # 내부 노드: 연산자
    a = eval_node(tree, left)   # type: ignore[arg-type]
    b = eval_node(tree, right)  # type: ignore[arg-type]

    if token == '+':
        return a + b
    if token == '-':
        return a - b
    if token == '*':
        return a * b
    # 정수 나눗셈
    if b == 0:
        raise ZeroDivisionError("division by zero in input tree")
    return a // b


def solve() -> None:
    import sys

    T = 10  # SWEA 관례
    input = sys.stdin.readline

    for tc in range(1, T + 1):
        N_line = input().strip()
        # 빈 줄이 섞일 수 있으면 스킵
        while N_line == '':
            N_line = input().strip()
        N = int(N_line)

        tree: Dict[int, Node] = {}
        for _ in range(N):
            parts = input().split()
            i = int(parts[0])
            if len(parts) == 2:
                # 리프: idx, value
                tree[i] = (parts[1], None, None)
            else:
                # 내부노드: idx, op, left, right
                tree[i] = (parts[1], int(parts[2]), int(parts[3]))

        ans = eval_node(tree, 1)  # 루트는 1
        print(f"#{tc} {ans}")


if __name__ == "__main__":
    # 표준 입력을 사용합니다. 로컬 테스트 시 아래 주석을 해제하고 예시를 넣을 수 있습니다.
    # import sys, io
    # sys.stdin = io.StringIO("""\
    # 1
    # 7
    # 1 - 2 3
    # 2 - 4 5
    # 3 / 6 7
    # 4 2147483647
    # 5 2147483646
    # 6 3
    # 7 3
    # """)
    solve()
~~~


