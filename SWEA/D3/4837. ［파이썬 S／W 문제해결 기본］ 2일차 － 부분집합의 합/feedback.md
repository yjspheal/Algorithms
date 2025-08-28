# 피드백
## 작성 코드
~~~python
import itertools

T = int(input().rstrip())
A = list(range(1, 13))
for tc in range(1, T+1):
    # N = 부분집합 원소의 수, 부분집합의 합 K
    N, K = map(int, input().split())
    count_K_sets = 0

    for subset in itertools.combinations(A, N):
        if sum(subset) == K:
            count_K_sets += 1

    print(f'#{tc} {count_K_sets}')
~~~
<br><br>

## 총평
- 강점
  - `itertools.combinations`를 사용해 부분집합 생성을 간결하게 처리 → 가독성 높음
  - 문제 의도(부분집합 합 판별)를 직관적으로 충족
- 개선 필요
  - `sum(subset)`을 매번 호출 → 시간 복잡도에 불리 (조합의 수 * 부분집합 크기만큼 합 연산 반복)
  - 입력/출력 구조는 간단하지만, 대회 코드 스타일에서 불필요한 `.rstrip()` 사용
  - 변수 네이밍이 직관적이지만 더 명확한 주석/도큐스트링이 있으면 유지보수성 개선
- 병목/리스크
  - 최대 12개 원소 중 조합을 전부 탐색하므로 최악의 경우 2^12 ≈ 4096 수준 → 본 문제에서는 큰 문제 없음.
  - 하지만 매번 `sum()`을 호출하는 구조는 N이 커지면 불리할 수 있음.

<br><br>

## 복잡도 및 병목
- 시간 복잡도: O(C(12, N) * N)  
  (`combinations` 생성 O(C(12, N)), 각 부분집합에 대해 `sum` 수행 O(N))
- 공간 복잡도: O(N) (조합 단위로 부분집합 저장)
- 병목 지점: `sum(subset)` 반복 호출

<br><br>

## 보완점
### 1. 누적합 방식으로 합 검증 최적화   [중요도: High] [효과: 성능]
- `sum(subset)` 대신 조합 생성 시 동시에 합을 계산하거나, filter 구조로 합만 계산 → 불필요한 반복 합산 제거
~~~python
for subset in itertools.combinations(A, N):
    total = 0
    for x in subset:
        total += x
    if total == K:
        count_K_sets += 1
~~~

<br><br>

### 2. 불필요한 `.rstrip()` 제거   [중요도: Low] [효과: 가독성]
- `int(input())`만으로 충분. `.rstrip()`은 불필요.

~~~python
T = int(input())
~~~

<br><br>

### 3. 함수화 및 도큐스트링 추가   [중요도: Med] [효과: 가독성, 유지보수]
- 반복적인 코드를 함수로 분리하고 설명을 추가하면 구조가 명확해짐.

~~~python
def count_subsets_with_sum(n: int, k: int) -> int:
    """크기 n인 부분집합 중 합이 k인 부분집합 개수 반환"""
    A = range(1, 13)
    count = 0
    for subset in itertools.combinations(A, n):
        if sum(subset) == k:
            count += 1
    return count
~~~

<br><br>

## 최종 코드 예시
~~~python
import itertools

def count_subsets_with_sum(n: int, k: int) -> int:
    """크기 n인 부분집합 중 합이 k인 부분집합 개수 반환"""
    A = range(1, 13)
    count = 0
    for subset in itertools.combinations(A, n):
        total = 0
        for x in subset:
            total += x
        if total == k:
            count += 1
    return count

T = int(input())
for tc in range(1, T + 1):
    N, K = map(int, input().split())
    result = count_subsets_with_sum(N, K)
    print(f'#{tc} {result}')
~~~
