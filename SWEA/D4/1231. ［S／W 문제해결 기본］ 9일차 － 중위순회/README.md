# [D4] [S/W 문제해결 기본] 9일차 - 중위순회 - 1231 

[문제 링크](https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV140YnqAIECFAYD) 

### 성능 요약

메모리: 53,888 KB, 시간: 69 ms, 코드길이: 776 Bytes

### 제출 일자

2025-08-22 15:19

> 출처: SW Expert Academy, https://swexpertacademy.com/main/code/problem/problemList.do

<br><br>
# 피드백
## 기존 코드
~~~python
# 1231 중위순회

def in_order(node_info):
    """
    중위순회하며 노드 값을 출력
    """
    len_node_info = len(node_info)
    if len_node_info == 2:  # 노드 길이가 2면. 즉 리프라면
        print(node_info[-1], end='')  # 값을 출력

    else:
        in_order(tree[int(node_info[2])])  # 중위순회 왼
        print(node_info[1], end='')  # 값을 출력
        if len_node_info > 3:
            in_order(tree[int(node_info[3])])  # 중위순회 왼


T = 10
for tc in range(1, T + 1):
    N = int(input())  # 노드 수

    # tree 초기화. 인덱스 맞추기 위해 앞에 빈 리스트 추가
    tree = [[]] + [list(input().split()) for _ in range(N)]

    # 프린트 시작
    print(f'#{tc} ', end='')

    # 순회하며 프린트. 루트노드의 번호는 항상 1이다
    in_order(tree[1])

    print()  # 엔터용
~~~
<br><br>

## 총평
- (강점) 문제 정의에 맞게 중위 순회(in-order traversal)를 올바르게 구현했고, 전체 시간 복잡도는 O(N)으로 효율적입니다.
- (개선 필요) 
  - 전역 변수 `tree`에 의존 → 함수 독립성 저하, 테스트 어려움.
  - `len(node_info)`로 리프/내부 노드 판별은 가독성이 떨어지고 입력 포맷 의존적.
  - 출력 로직이 함수 내부에 고정되어 있어 **재사용 불가** (예: 문자열로 반환하고 싶을 때).
- (리스크) else 블록에서 오른쪽 자식 호출 부분 주석이 `# 중위순회 왼`으로 잘못 달려 있어 혼동 유발.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: O(N) (모든 노드를 정확히 한 번 방문).
- 공간 복잡도: O(N) (트리 저장) + O(H) (재귀 깊이).
- 병목 지점 없음 (단순 재귀 구조).
<br><br>

## 보완점
### 1. 전역 제거 및 (tree, idx) 인터페이스로 변경  [중요도: High] [효과: 가독/재사용]
- 전역 `tree` 제거 후, `in_order(tree, idx)` 형태로 전달.
~~~python
def in_order(tree, idx, result):
    if idx >= len(tree) or not tree[idx]:
        return
    node = tree[idx]
    # 왼쪽
    if len(node) >= 3:
        in_order(tree, int(node[2]), result)
    # 현재
    result.append(node[1])
    # 오른쪽
    if len(node) >= 4:
        in_order(tree, int(node[3]), result)
~~~
<br><br>

### 2. 출력 분리 (리턴값 활용)  [중요도: High] [효과: 재사용/유지보수]
- 함수에서 직접 `print`하지 않고 문자열을 반환하게 하면, 다른 용도(검증, 문자열 조작)에 활용 가능.
~~~python
expression = "".join(result)
print(f"#{tc} {expression}")
~~~
<br><br>

### 3. 입력 파싱 구조 개선  [중요도: Med] [효과: 안정성]
- `len(node_info)` 대신 노드 구조를 `(값, left?, right?)`로 통일하여 가독성 향상.
- 잘못된 입력 처리(예: 자식 인덱스 없음/범위 벗어남) 시 에러 메시지 제공.
<br><br>

### 4. 주석 및 도큐스트링 보강  [중요도: Low] [효과: 가독]
- `# 중위순회 왼` 오타 수정 → `# 중위순회 오른쪽`.
- 함수 도큐스트링에 반환 타입과 동작 설명을 명확히 기술.
<br><br>

## 최종 코드 예시
~~~python
from typing import List

def in_order(tree: List[List[str]], idx: int, result: List[str]) -> None:
    """
    중위순회(In-order traversal)를 수행하며 노드 값을 result 리스트에 추가한다.
    
    Args:
        tree (List[List[str]]): 1-based 인덱스 트리 구조.
        idx (int): 현재 방문할 노드 인덱스.
        result (List[str]): 방문한 노드 값을 누적할 리스트.
    """
    if idx >= len(tree) or not tree[idx]:
        return

    node_info = tree[idx]

    # 왼쪽 자식 방문
    if len(node_info) >= 3:
        in_order(tree, int(node_info[2]), result)

    # 현재 노드 값
    result.append(node_info[1])

    # 오른쪽 자식 방문
    if len(node_info) >= 4:
        in_order(tree, int(node_info[3]), result)


def solve() -> None:
    """
    SWEA 1231: 중위순회 문제 풀이.
    10개의 테스트케이스에 대해 중위순회 문자열을 출력한다.
    """
    import sys
    input = sys.stdin.readline

    T = 10
    for tc in range(1, T + 1):
        N = int(input().strip())
        tree = [[]] + [input().split() for _ in range(N)]

        result: List[str] = []
        in_order(tree, 1, result)  # 루트는 1번 노드

        expression = "".join(result)
        print(f"#{tc} {expression}")


if __name__ == "__main__":
    # 로컬 테스트 예시
    """
    sample = """\
1
7
1 W 2 3
2 F 4 5
3 R 6 7
4 O
5 L
6 D
7 !
"""
    import sys, io
    sys.stdin = io.StringIO(sample)
    """
    solve()
~~~
