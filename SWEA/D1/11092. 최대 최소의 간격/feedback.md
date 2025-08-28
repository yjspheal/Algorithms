# 피드백
## 작성 코드
~~~python
T = int(input())
for tc in range(1, T + 1):
    N = int(input())

    arr = list(map(int, input().split()))

    min_idx = max_idx = 0
    # arr를 순회하며
    for i in range(N):
        # 작은 수가 여러개이면 먼저 나오는 위치
        if arr[i] < arr[min_idx]:
            min_idx = i

        # 큰 수가 여러 개이면 마지막으로 나오는 위치
        if arr[i] >= arr[max_idx]:
            max_idx = i

    print(f'#{tc} {abs(min_idx - max_idx)}')
~~~
<br><br>

## 총평
- 강점
  - **O(N)** 한 번의 순회로 최소/최대 위치를 동시에 탐색해 효율적임.
  - 조건(`min → 최초`, `max → 최후`)을 `if <`와 `if >=`로 정확히 처리한 점이 깔끔함.
  - 불필요한 내장함수 호출(`min`, `max`, `index`) 없이 직접 인덱스를 추적해 성능상 이점.
- 개선 필요
  - 함수화/도큐스트링이 없고, 변수 네이밍이 단순(`arr`, `N` 등)하여 의미가 불분명함.
  - `N`이 0인 경우(이 문제에선 입력 보장으로 없겠지만) 안전장치가 전혀 없음.
  - 전체 코드 구조가 반복되므로 함수로 묶으면 재사용성과 가독성이 향상됨.
- 병목/리스크
  - 입력 크기 `N`에 비례하는 O(N), 최악의 경우도 빠름. 리스크는 거의 없음.
  - 다만 “마지막 최대값”을 찾는 로직은 `>=`로 잘 처리했으나, 이 조건을 주석으로 분명히 남겨야 유지보수시 혼동이 줄어듦.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: O(N) (단일 순회)
- 공간 복잡도: O(1) (상수 변수만 사용)
- 병목 지점: 없음. 입력이 커도 문제 없음.
<br><br>

## 보완점
### 1. 함수화 및 도큐스트링 추가   [중요도: High] [효과: 가독성/유지보수]
- **이유**: 로직을 함수로 묶어 의미를 드러내면 코드 재사용과 테스트가 쉬워짐.
- **결론**: `def min_max_distance(arr: list[int]) -> int` 형태로 구현.

~~~python
def min_max_distance(arr: list[int]) -> int:
    """리스트에서 최소값의 첫 위치와 최대값의 마지막 위치 간 거리 반환"""
    min_idx = max_idx = 0
    for i, val in enumerate(arr):
        if val < arr[min_idx]:
            min_idx = i
        if val >= arr[max_idx]:  # 마지막 최대값
            max_idx = i
    return abs(min_idx - max_idx)
~~~

<br><br>

### 2. 변수 네이밍 개선   [중요도: Med] [효과: 가독성]
- `arr` → `numbers`, `N` → `size` 등으로 의미를 드러내면 읽기 쉬워짐.

~~~python
size = int(input())
numbers = list(map(int, input().split()))
~~~

<br><br>

### 3. 예외 처리(방어적 프로그래밍)   [중요도: Low] [효과: 안정성]
- 비어있는 리스트가 들어온 경우 즉시 0 반환하도록 방어 코드 추가 가능.
- 문제 조건상 필요는 없지만 습관적으로 좋음.

~~~python
if not arr:
    return 0
~~~

<br><br>

## 최종 코드 예시
~~~python
from typing import List

def min_max_distance(numbers: List[int]) -> int:
    """리스트에서 최소값의 첫 위치와 최대값의 마지막 위치 간 거리 반환"""
    if not numbers:
        return 0
    min_idx = max_idx = 0
    for i, val in enumerate(numbers):
        if val < numbers[min_idx]:
            min_idx = i
        if val >= numbers[max_idx]:  # 마지막 최대값
            max_idx = i
    return abs(min_idx - max_idx)


T = int(input())
for tc in range(1, T + 1):
    size = int(input())
    numbers = list(map(int, input().split()))
    result = min_max_distance(numbers)
    print(f"#{tc} {result}")
~~~
