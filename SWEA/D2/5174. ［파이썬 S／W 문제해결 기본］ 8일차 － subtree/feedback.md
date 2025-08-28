# 피드백
## 작성 코드
~~~python 
def pre_order(node_num):
    """
    전위순회하며 노드 번호를 출력
    """
    global sub_nodes
    if node_num:  # 내가 0이 아닌 한

        sub_nodes += 1  # 서브트리 노드 수 + 1
        pre_order(left_child[node_num])  # 전위순회 왼
        pre_order(right_child[node_num])  # 전위순회 오


T = int(input())
for tc in range(1, T + 1):
    # 엣지 수, 서브트리 루트노드
    E, N = map(int, input().split())
    tree = list(map(int, input().split()))

    # 왼 오 자식들. 노드 번호는 1번부터 E+1번까지 존재한다.
    left_child = [0] * (E + 2)
    right_child = [0] * (E + 2)

    for i in range(E):
        p = tree[2 * i]
        c = tree[2 * i + 1]

        if left_child[p] == 0:   # p한테 자식이 없다면
            left_child[p] = c

        else:
            right_child[p] = c

    sub_nodes = 0
    pre_order(N)  # 루트부터 순회

    print(f'#{tc} {sub_nodes}')
~~~
<br><br>

## 총평
- 강점
  - 간단한 전위 순회로 **서브트리 노드 수를 정확히 카운트**하는 접근이 직관적입니다.
  - 입력 특성(E 간선 ⇒ 노드 수 E+1)에 맞춰 배열 크기를 산정해 **인덱싱 안전성**을 확보했습니다.
- 개선 필요
  - `global sub_nodes`에 의존하는 구조는 테스트/재사용성이 낮고 사이드이펙트 위험이 있습니다.
  - `pre_order`의 도큐스트링은 “출력”이라고 되어 있으나 실제론 **카운트만 수행**합니다(불일치).
  - 재귀는 트리 높이에 비례한 콜스택을 사용하므로, 입력 범위가 커질 경우 **재귀 한도** 리스크가 있습니다(이 문제에선 보통 안전하나, 습관적으로 반복/스택이 더 견고).
  - 입력 파싱 루프는 동작상 문제 없으나, **의미가 드러나도록** 리팩터링하면 가독성이 좋아집니다.
- 병목/리스크
  - 시간 복잡도는 서브트리 크기 `k`에 대해 **O(k)**, 공간은 재귀 높이 `h`에 대해 **O(h)**. 성능 병목은 없습니다.
  - 실제 리스크는 **글로벌 상태/재귀 의존**으로 인한 유지보수성/안정성입니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: `O(k)` (N을 루트로 하는 서브트리의 노드 수 `k`만 방문)
- 공간 복잡도: 재귀 `O(h)` (트리 높이 `h`), 반복 스택으로 바꾸면 `O(h)`이지만 **명시적 제어**가 쉬워짐
- 병목 지점: 없음(상수 시간 연산의 반복). 품질 측면의 병목은 **글로벌 상태와 재귀 사용**.
<br><br>

## 보완점
### 1. 전역 변수 제거 + 반복(스택) DFS로 변환   [중요도: High] [효과: 안정성/가독]
- **이유(Reasoning)**: 전역 상태는 함수 호출 순서/범위에 따라 오작동 위험이 있고, 테스트가 어렵습니다. 반복 DFS는 재귀 한도 이슈가 없고, 함수가 **입력→출력**으로 명확해집니다.
- **결론(리팩터)**: `count_subtree(N, left, right)`가 정수를 반환하도록 변경하고, 내부에서 스택으로 순회합니다.

~~~python
def count_subtree(root: int, left: list[int], right: list[int]) -> int:
    if root == 0:
        return 0
    cnt = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if node == 0:
            continue
        cnt += 1
        lc, rc = left[node], right[node]
        if lc: stack.append(lc)
        if rc: stack.append(rc)
    return cnt
~~~

<br><br>

### 2. 도큐스트링/네이밍 정정   [중요도: Med] [효과: 가독/유지보수]
- **이유**: 현재 `pre_order`의 설명은 “출력”이라 되어 있어 실제 동작과 불일치.
- **결론**: 함수명을 `count_subtree`로 바꾸고 도큐스트링을 “서브트리 노드 수 반환”으로 명확화.

~~~python
def count_subtree(root: int, left: list[int], right: list[int]) -> int:
    """root를 루트로 하는 서브트리의 노드 수를 반환한다."""
    ...
~~~

<br><br>

### 3. 입력 파싱 루프 가독성 개선   [중요도: Low] [효과: 가독]
- **이유**: `tree[2*i]`, `tree[2*i+1]`는 익숙하지 않으면 읽기 불편.
- **결론**: `for p, c in zip(tree[::2], tree[1::2]):`로 의도를 드러냅니다. 또한 `V = E + 1`을 명시해 배열 크기 근거를 남깁니다.

~~~python
V = E + 1
left_child  = [0] * (V + 1)
right_child = [0] * (V + 1)

for p, c in zip(tree[::2], tree[1::2]):
    if left_child[p] == 0:
        left_child[p] = c
    else:
        right_child[p] = c
~~~

<br><br>

### 4. 경계값(N==0) 및 타입힌트   [중요도: Low] [효과: 안정성/가독]
- **이유**: 문제에서 거의 없지만, `N==0`일 때 즉시 0을 반환하면 안전합니다. 타입힌트는 오탈자/사용 방법을 분명히 합니다.
- **결론**: 이미 1번 리팩터 코드에 반영(초기 가드 및 타입힌트).
<br><br>

## 최종 코드 예시
~~~python
from typing import List

def count_subtree(root: int, left: List[int], right: List[int]) -> int:
    """root를 루트로 하는 서브트리의 노드 수를 반환한다."""
    if root == 0:
        return 0
    cnt = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if node == 0:
            continue
        cnt += 1
        lc, rc = left[node], right[node]
        if lc: stack.append(lc)
        if rc: stack.append(rc)
    return cnt


T = int(input())
for tc in range(1, T + 1):
    E, N = map(int, input().split())
    pairs = list(map(int, input().split()))

    V = E + 1  # 노드 번호는 1..V (문제 특성)
    left_child  = [0] * (V + 1)
    right_child = [0] * (V + 1)

    # 간선 (parent, child) 채우기
    for p, c in zip(pairs[::2], pairs[1::2]):
        if left_child[p] == 0:
            left_child[p] = c
        else:
            right_child[p] = c

    result = count_subtree(N, left_child, right_child)
    print(f"#{tc} {result}")
~~~
