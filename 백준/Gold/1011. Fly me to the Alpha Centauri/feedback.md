# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

Test = int(input())
distance = [0]*Test

for t in range(Test):
  start, end = map(int,input().split())
  distance[t] = end - start

def count_run(D):
  if D < 4:
    return D

  for k in range(2,D):
    if D <= k ** 2:           # = (k*(k+1)) // 2 + ((k-1)*k) // 2
      return k + (k-1)          

    elif D <= k ** 2 + k:
      return k + (k-1) + 1

for d in distance:
  print(count_run(d))
~~~
<br><br>

## 총평
- 강점
  - 이동 규칙의 패턴을 잘 포착해 `k^2`와 `k^2+k` 경계로 분기하는 핵심 아이디어가 맞습니다.
  - 작은 거리 `D<4`에 대한 빠른 처리로 예외 케이스를 정리했습니다.
- 개선 필요
  - `count_run`이 `k`를 2부터 증가시키며 검사 → **O(√D)** 반복. `math.isqrt`로 **O(1)**에 바로 계산 가능합니다.
  - 입출력: 굳이 모든 거리를 리스트에 저장하지 않아도 **바로 처리**가 가독성과 메모리 측면에서 유리합니다.
  - 네이밍/주석: `Test`, `distance`보다 `T`, `dists` 혹은 스트리밍 처리로 명확히 하고, 수학적 근거를 도큐스트링으로 남기면 유지보수성이 좋아집니다.
- 병목/리스크
  - 현재도 시간 제한 내 통과 가능하나, 큰 입력에서 **반복 루프가 불필요**합니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도(현재): 각 테스트마다 `k`가 √D 근처에서 반환되므로 **O(√D)**.
- 공간 복잡도(현재): 거리 배열 저장으로 **O(T)**.
- 병목 지점: `for k in range(2, D)` 루프의 증가 탐색.
<br><br>

## 보완점
### 1. 정수 제곱근으로 O(1) 계산   [중요도: High] [효과: 성능/가독]
- **이유(Reasoning)**: 거리 `D`에 대해 `n = ⌊√D⌋`라 두면
  - `D == n^2` → 이동 횟수 `2n - 1`
  - `n^2 < D ≤ n^2 + n` → `2n`
  - `n^2 + n < D` → `2n + 1`
  이 공식을 사용하면 반복 없이 즉시 계산 가능합니다.
- **결론(리팩터)**:
~~~python
import math

def count_run(D: int) -> int:
    if D <= 3:
        return D
    n = math.isqrt(D)
    if D == n * n:
        return 2 * n - 1
    elif D <= n * n + n:
        return 2 * n
    else:
        return 2 * n + 1
~~~

<br><br>

### 2. 입력을 즉시 처리(배열 저장 제거)   [중요도: Med] [효과: 가독/메모리]
- **이유**: 거리를 리스트에 모을 필요가 없습니다. 읽자마자 계산·출력하면 간단합니다.
- **결론**:
~~~python
import sys, math
input = sys.stdin.readline

def count_run(D: int) -> int:
    if D <= 3:
        return D
    n = math.isqrt(D)
    if D == n * n:
        return 2 * n - 1
    return 2 * n if D <= n * n + n else 2 * n + 1

T = int(input())
for _ in range(T):
    a, b = map(int, input().split())
    print(count_run(b - a))
~~~

<br><br>

### 3. 도큐스트링으로 수학적 근거 명시   [중요도: Low] [효과: 가독/유지보수]
- **이유**: 왜 저 공식이 맞는지 한 줄 남기면 이후 유지보수/리뷰에 유리합니다.
- **결론**: 함수 주석에 계단식 증가 규칙(`1,2,3, …, k, …, 3,2,1`)과 구간 경계(`n^2`, `n^2+n`)를 기재.
<br><br>

## 최종 코드 예시
~~~python
import sys
import math

input = sys.stdin.readline

def count_run(D: int) -> int:
    """
    거리 D를 최소 이동 횟수로 가는 규칙:
      n = floor(sqrt(D))
      - D == n^2       -> 2n - 1
      - n^2 < D <= n^2 + n -> 2n
      - D > n^2 + n    -> 2n + 1
    (증가/감소 속도 패턴: 1,2,3,...,n,...,3,2,1)
    """
    if D <= 3:
        return D
    n = math.isqrt(D)
    if D == n * n:
        return 2 * n - 1
    return 2 * n if D <= n * n + n else 2 * n + 1

T = int(input())
for _ in range(T):
    a, b = map(int, input().split())
    print(count_run(b - a))
~~~
