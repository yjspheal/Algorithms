# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

N = int(input())
A= []

for i in range(N):
	A.append((int(input()),i)) # 정렬 기준을 고려하여 데이터, index 순서로 저장

Max = 0
sorted_A = sorted(A) 

for i in range(N):
	if Max < sorted_A[i][1] - i: # 정렬 전 index - 정렬 후 index 계산의 최댓값 저장 
		Max = sorted_A[i][1] - i

print(Max + 1)
~~~
<br><br>


## 총평
- 강점
  - 문제의 핵심 로직(정렬 후 원래 인덱스와 비교해 최대 이동 거리 계산)을 잘 구현함
  - 불필요한 라이브러리를 쓰지 않고, `sys.stdin.readline`으로 빠른 입력 처리
- 개선 필요
  - 변수 네이밍이 직관적이지 않음 (`A`, `Max` → 의미가 모호)
  - 주석이 간단하나 코드의 의도(버블 소트 지수 문제임)를 명확히 드러내지 않음
  - `max` 대신 `Max` 변수명을 사용하여 내장함수 이름과 혼동 유발
- 병목/리스크
  - `sorted()` 사용으로 시간복잡도는 O(N log N) → 문제 요구 성능에는 충분
  - 메모리도 O(N)으로 안정적이며 병목은 없음
<br><br>


## 복잡도 및 병목
- 시간 복잡도: O(N log N) (`sorted()` 정렬이 지배적)
- 공간 복잡도: O(N) (입력 배열과 정렬 배열 저장)
- 병목 지점: 정렬 연산 (`sorted(A)`)이 주된 연산이지만 일반 입력 크기(≤500,000 수준)에서는 충분히 효율적
<br><br>


## 보완점
### 1. 변수명 개선   [중요도: High] [효과: 가독성]
- `A`, `Max` 같은 모호한 이름 대신, `arr`, `max_shift` 등 의미가 명확한 이름을 사용하면 유지보수성이 향상됩니다.
~~~python
arr = []
for i in range(N):
    arr.append((int(input()), i))  # (값, 원래 인덱스)
~~~

<br><br>


### 2. max 함수 활용   [중요도: Med] [효과: 가독성]
- 수동으로 `if` 조건문으로 최대값 비교 대신 `max()` 내장함수를 활용하면 코드가 간결해집니다.
~~~python
max_shift = 0
for i in range(N):
    max_shift = max(max_shift, sorted_arr[i][1] - i)
~~~

<br><br>


### 3. 함수화 및 도큐스트링 추가   [중요도: Low] [효과: 유지보수성]
- 입력 처리와 로직을 함수로 분리하고 간단한 설명을 추가하면 코드 재사용과 이해도가 높아집니다.
~~~python
def bubble_sort_index(arr: list[tuple[int,int]]) -> int:
    """
    버블 소트 지수 계산:
    정렬 전후 인덱스 차이의 최댓값 + 1을 반환.
    """
    sorted_arr = sorted(arr)
    max_shift = 0
    for i in range(len(arr)):
        max_shift = max(max_shift, sorted_arr[i][1] - i)
    return max_shift + 1
~~~
<br><br>


## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline

def bubble_sort_index(arr: list[tuple[int,int]]) -> int:
    """
    버블 소트 지수 계산:
    정렬 전후 인덱스 차이의 최댓값 + 1을 반환.
    """
    sorted_arr = sorted(arr)
    max_shift = 0
    for i in range(len(arr)):
        max_shift = max(max_shift, sorted_arr[i][1] - i)
    return max_shift + 1

N = int(input())
arr = [(int(input()), i) for i in range(N)]  # (값, 원래 인덱스)

print(bubble_sort_index(arr))
~~~
