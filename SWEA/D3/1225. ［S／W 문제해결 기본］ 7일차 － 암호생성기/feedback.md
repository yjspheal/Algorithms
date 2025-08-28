# 피드백
## 작성 코드
~~~python
from collections import deque

T = 10

for _ in range(1, T + 1):
    tc = int(input())
    arr = list(map(int, input().split()))
    dq = deque(arr)

    while True:
        # 1 ~ 5 감소가 한 사이클
        for i in range(1, 6):
            # 맨 앞 값을 ele변수로 뺌
            ele = dq.popleft()
            ele -= i    # i만큼 빼줘야 함
            if ele <= 0:    # 끝나는 시점
                dq.append(0)
                break
            else:
                dq.append(ele)
        else:   # break가 안 났다면 계속
            continue

        break   # break가 됐다면 아예 빠져나가도록


    print(f'#{tc}', *dq)
~~~
<br><br>

## 총평
- 강점
  - `deque`를 사용해 O(1)로 양끝 삽입/삭제를 수행하여 자료구조 선택이 적절합니다.
  - 문제 규칙(1~5 감소의 반복, 0 이하에서 종료)을 정확히 구현했습니다.
- 개선 필요
  - 종료 전까지 “완전 시뮬레이션”만 수행하여 입력 값이 큰 경우 불필요한 사이클을 많이 돕니다.
  - 중첩 `for-else + while True + 이중 break`는 흐름 파악이 어려워 가독성이 떨어집니다.
  - 상수/의미 있는 네이밍, 함수화/도큐스트링/타입힌트 부재로 유지보수성이 낮습니다.
- 병목/리스크
  - **병목**은 사이클 수 자체입니다. 한 사이클은 최대 5번의 pop/append로 O(1)이지만, 종료까지의 **사이클 수가 값의 크기에 비례**해 커질 수 있습니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 한 사이클(1~5 감소)은 O(1). 전체는 **O(C)** (C=종료까지의 사이클 수). 현재 구현은 C가 입력 최소값/감소량(평균적으로 3) 정도에 비례하여 증가.
- 공간 복잡도: O(1) 추가 공간(고정 크기 8, `deque` 재사용).
- 병목 지점: 종료까지 “불필요한 완전 시뮬레이션” 반복. 특히 값이 큰 테스트 케이스에서 사이클 수가 불필요하게 큼.
<br><br>

## 보완점
### 1. 선행 정규화(모듈러)로 사이클 수 급감  [중요도: High] [효과: 성능]
**Reasoning**  
- 1~5의 합은 15이므로, “완전한 1~5 사이클 1회”는 전체 합으로 보면 각 원소에 대해 **값을 15씩 줄이는 효과**와 동치입니다.  
- 따라서 모든 원소에서 동일한 **15의 배수**를 미리 빼면, 실제 시뮬레이션 사이클 수를 크게 줄일 수 있습니다.  
- 다만 최소값이 정확히 15의 배수일 때 전부에서 그 배수를 통째로 빼버리면 시작 전에 0이 생겨 즉시 종료되는 **원래 흐름과의 미세한 차이**가 생깁니다.  
- 이를 방지하려고 관례적으로 `k = max(min(arr)//15 - 1, 0)`을 사용해 **한 사이클은 남겨둔 상태**로 정규화합니다(즉, 모두가 양수 상태로 시뮬 시작).

**Conclusion (코드)**
~~~python
# 최소값 기반 선행 정규화: 15의 배수만큼 미리 감산
min_v = min(dq)
k = min_v // 15
if k > 0:
    k -= 1  # 한 사이클은 남겨 정확한 흐름 보장
    if k > 0:
        dec = 15 * k
        dq = deque(x - dec for x in dq)
~~~
<br><br><br>

### 2. 루프 구조 단순화 및 상태 변수 도입  [중요도: Med] [효과: 가독/성능]
**Reasoning**  
- 현재는 `while True` + `for-else` + 이중 `break/continue`로 흐름이 복잡합니다.  
- 감소 값은 1→5→1→… 순환하므로, **감소 값 상태 변수(`dec`)**를 두고 한 번에 한 원소만 처리하는 **단일 루프**가 더 읽기 쉽고 분기 수도 줄어듭니다.

**Conclusion (코드)**
~~~python
dec = 1
while True:
    v = dq.popleft() - dec
    if v <= 0:
        dq.append(0)
        break
    dq.append(v)
    dec += 1
    if dec == 6:
        dec = 1
~~~
<br><br><br>

### 3. 함수화/상수/타입힌트/도큐스트링 추가  [중요도: Med] [효과: 가독/유지보수]
**Reasoning**  
- 테스트 가능성, 재사용성, 의미 전달을 위해 핵심 로직을 함수로 분리합니다.
- `CYCLE_SUM=15`, `MAX_DEC=5` 등 의미 있는 상수를 도입하면 매직넘버 제거로 가독성이 좋아집니다.
- 타입힌트/도큐스트링은 문제 풀이 코드라도 유지보수와 협업에 유리합니다.

**Conclusion (코드)**
~~~python
from collections import deque
from typing import Deque, Iterable

CYCLE_SUM = 15
MAX_DEC = 5

def generate_password(seq: Iterable[int]) -> Deque[int]:
    """
    SWEA 1225 암호생성기 로직을 수행해 최종 큐를 반환한다.
    - 1~5 감소를 순환하며, 감소 결과가 0 이하인 값을 0으로 넣고 종료한다.
    - 시작 전, 최소값 기반으로 15의 배수를 선감산(1사이클은 남김)하여 사이클 수를 줄인다.
    """
    dq = deque(seq)
    # 선행 정규화
    min_v = min(dq)
    k = min_v // CYCLE_SUM
    if k > 0:
        k -= 1
        if k > 0:
            dec_all = CYCLE_SUM * k
            dq = deque(x - dec_all for x in dq)

    # 단일 루프로 시뮬레이션
    dec = 1
    while True:
        v = dq.popleft() - dec
        if v <= 0:
            dq.append(0)
            break
        dq.append(v)
        dec += 1
        if dec > MAX_DEC:
            dec = 1
    return dq
~~~
<br><br><br>

### 4. 입출력 최소화 및 표준 입력 가속(선택)  [중요도: Low] [효과: 성능/안정성]
**Reasoning**  
- 여러 테스트케이스에서 표준입력을 많이 읽으면 `sys.stdin.readline`이 미세하게 유리할 수 있습니다(특히 대용량 입출력 상황). 출력은 문제 형식상 한 줄이므로 현재도 충분하지만, 일관성 있게 관리 가능합니다.

**Conclusion (코드)**
~~~python
import sys
input = sys.stdin.readline
~~~
<br><br><br>

## 최종 코드 예시
~~~python
from collections import deque
from typing import Deque, Iterable
import sys

input = sys.stdin.readline

CYCLE_SUM = 15
MAX_DEC = 5
T = 10


def generate_password(seq: Iterable[int]) -> Deque[int]:
    """
    SWEA 1225 암호생성기
    - 1~5 감소를 순환 적용
    - 감소 결과가 0 이하가 되는 순간 해당 값을 0으로 넣고 종료
    - 시작 전 최소값 기반으로 15의 배수를 선감산하되, 한 사이클은 남겨 정확한 흐름 유지
    """
    dq = deque(seq)

    # 선행 정규화(모듈러): 한 사이클(1~5) 합은 15
    min_v = min(dq)
    k = min_v // CYCLE_SUM
    if k > 0:
        k -= 1  # 한 사이클은 남긴다
        if k > 0:
            dec_all = CYCLE_SUM * k
            dq = deque(x - dec_all for x in dq)

    # 단일 루프 시뮬레이션
    dec = 1
    while True:
        v = dq.popleft() - dec
        if v <= 0:
            dq.append(0)
            break
        dq.append(v)
        dec += 1
        if dec > MAX_DEC:
            dec = 1

    return dq


def main() -> None:
    for _ in range(1, T + 1):
        tc = int(input().strip())
        arr = list(map(int, input().split()))
        result = generate_password(arr)
        print(f'#{tc}', *result)


if __name__ == "__main__":
    main()
~~~
