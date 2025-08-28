# 피드백
## 작성 코드
~~~python
# 1860. 진기의 최고급 붕어빵

# import sys
# sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M, K = map(int, input().split())     # N명의 손님, M초마다 K개의 붕어빵 생성
    visitor_list = [0] * 11112      # 각 초에 손님이 몇명 오는지 저장할 리스트. 초는 11111 이하이다.
    latest_time = 0     # 젤 늦게 오는 손님 초 저장할 변수

    for visit_time in map(int, input().split()):    # 인풋받은 걸 하나씩 순회하며
        visitor_list[visit_time] += 1       # 해당 시간에 손님이 한명 왔다

        if visit_time > latest_time:        # 젤 늦은 시간 update
            latest_time = visit_time

    current_boong = 0   # 현재 붕어빵 재고

    result = 'Possible' # 붕어빵 제공 가능 여부
    # 각 초별로 붕어빵 재고 파악
    for i in range(latest_time + 1):    # 제일 늦게오는 사람 초까지만 보면 됨
        if i > 0 and i % M == 0:      # M초마다 붕어빵 K개 생성
            current_boong += K

        current_boong -= visitor_list[i]    # 지금 온 손님에게 하나씩 주기
        if current_boong < 0:       # 붕어빵 재고보다 더 줘야되는 상황이었으면
            result = 'Impossible'       # 불가능

    print(f'#{tc} {result}')
~~~
<br><br>

## 총평
- 강점
    - 문제 요구사항을 정확히 반영한 시뮬레이션(0초에는 생산 없음, M의 배수 시점에만 생산).
    - 최대 도착 시각까지만 순회하는 등 불필요한 반복을 제한.
    - 코드가 단순하고 직관적이며, 구현 의도가 주석으로 잘 설명되어 있음.
- 개선 필요
    - 방문자 카운트를 위해 고정 길이 배열(11112) 사용: 입력과 무관하게 항상 동일한 메모리를 할당.
    - 매 초 단위 시뮬레이션은 N이 작고 최대 시각이 큰 경우 비효율적.
    - 조기 종료(break) 미적용으로 불가능 판정 이후에도 불필요한 반복 수행.
    - 함수화/타입힌트/입출력 분리 등 구조화 부족으로 테스트성·재사용성 낮음.
- 병목/리스크
    - 시간: 초 단위 루프가 핵심 병목. N 대비 latest_time가 큰 테스트에서 비효율적.
    - 안정성: M이 0인 비정상 입력 시 모듈로/정수나눗셈 사용에서 예외 가능(문제 조건상 발생하지 않더라도 방어적 처리 여지).
<br><br>

## 복잡도 및 병목
- 시간 복잡도
    - 현재 구현: O(latest_time + N). 방문자 입력 처리 O(N), 초 단위 시뮬레이션 O(latest_time).
    - 병목 지점: 초 단위 for 루프 전체.
- 공간 복잡도
    - 현재 구현: O(1) 상수처럼 보이지만, 실제로는 고정 크기 배열 O(11112) 할당. 입력 특성과 무관.
- 현실적 입력에서의 비효율
    - 일반적으로 N은 수십~수백이며, 최대 시각 상한(11111)은 상대적으로 큼. 이 경우 방문자 정렬 기반 O(N log N) 검증이 더 유리함.
<br><br>

## 보완점
### 1. 정렬 기반 누적검증으로 전환   [중요도: High] [효과: 성능, 가독, 단순성]
Reasoning:
- 각 손님 도착 시각 t에서 생산 가능한 붕어빵 수는 floor(t / M) * K. 손님을 도착 시각 오름차순으로 순회하며, i번째 손님(1-indexed)에 대해 i <= produced를 만족하는지 확인하면 충분함.
- 초 단위 시뮬레이션 제거로 시간 복잡도는 O(N log N)(정렬)로 감소, 루프 본체는 O(N)로 단순해짐.
- 배열 11112 같은 매직 넘버와 불필요한 메모리 사용을 제거.

Conclusion (리팩터 코드):
~~~python
from typing import List

def is_possible(arrivals: List[int], M: int, K: int) -> bool:
    """도착 시각 정렬 기반으로 붕어빵 제공 가능 여부 판단."""
    # 문제 전제상 M >= 1. 방어적으로 체크해도 됨.
    if M <= 0:
        # 생산 불가이므로 손님이 있다면 불가능
        return len(arrivals) == 0

    arrivals.sort()
    produced = 0
    served = 0
    for t in arrivals:
        produced = (t // M) * K
        served += 1
        if served > produced:
            return False
    return True
~~~
<br><br><br>

### 2. 조기 종료와 동적 크기 카운트로 기존 시뮬레이션 개선   [중요도: Med] [효과: 성능, 메모리]
Reasoning:
- 기존 방식 유지 시에도 latest_time 이후는 볼 필요 없음. 불가능 판정 즉시 break로 조기 종료하면 불필요 연산 감소.
- 방문자 카운트를 위해 입력 최대 시각을 먼저 구해 그 길이만큼 동적 배열을 할당하면, 매번 11112 길이를 만들지 않아도 됨.

Conclusion (리팩터 코드):
~~~python
def possible_by_seconds(arrivals, M, K) -> bool:
    if M <= 0:
        return len(arrivals) == 0

    latest_time = max(arrivals) if arrivals else 0
    counts = [0] * (latest_time + 1)
    for t in arrivals:
        counts[t] += 1

    stock = 0
    for sec in range(latest_time + 1):
        if sec > 0 and sec % M == 0:
            stock += K
        stock -= counts[sec]
        if stock < 0:
            return False  # 조기 종료
    return True
~~~
<br><br><br>

### 3. 입출력 분리, 함수화 및 타입힌트/도큐스트링 추가   [중요도: Med] [효과: 가독, 유지보수, 테스트 용이]
Reasoning:
- 문제 풀이 코어 로직을 함수로 분리하면 단위 테스트, 재사용, 검증이 쉬워짐.
- 타입힌트와 간단한 도큐스트링은 의도를 명확하게 하며 협업/유지보수에 유리.
- 입력은 solve()에 한정하고, 핵심 검증은 순수 함수로 유지.

Conclusion (리팩터 코드):
~~~python
from typing import List

def is_possible(arrivals: List[int], M: int, K: int) -> bool:
    """도착 시각 정렬 기반 검증."""
    if M <= 0:
        return len(arrivals) == 0
    arrivals.sort()
    for i, t in enumerate(arrivals, start=1):
        if i > (t // M) * K:
            return False
    return True

def solve() -> None:
    import sys
    input = sys.stdin.readline
    T = int(input().strip())
    for tc in range(1, T + 1):
        N, M, K = map(int, input().split())
        arrivals = list(map(int, input().split()))
        result = "Possible" if is_possible(arrivals, M, K) else "Impossible"
        print(f"#{tc} {result}")

if __name__ == "__main__":
    solve()
~~~
<br><br><br>

### 4. 네이밍/주석 정리 및 매직 넘버 제거   [중요도: Low] [효과: 가독]
Reasoning:
- visitor_list, current_boong 등은 의미가 통하지만 더 일반적인 naming과 불필요한 매직 넘버 제거로 가독성 향상.
- “11112” 같은 상수는 문제 설명에 의존하므로, 동적 크기 할당 또는 상수로 명시(예: MAX_TIME = 11111)하는 편이 명확.

Conclusion (권장 사항):
- visitor_list -> counts, current_boong -> stock, latest_time -> max_time 등 일반적 명명 사용.
- 11112 고정 배열 제거(2번 개선안 적용) 또는 상수 선언 후 근거 주석 명시.
<br><br><br>

### 5. 예외/엣지 처리 명시   [중요도: Low] [효과: 안정성]
Reasoning:
- 문제 조건상 M >= 1이나, 함수 수준에서 방어 코드를 두면 재사용 시 안전.
- N=0(손님 없음)도 자연스럽게 True를 반환함을 명시.

Conclusion (권장 사항):
- is_possible 내 M <= 0 처리 유지(또는 assert M > 0).
- 도큐스트링에 전제 조건 기재.
<br><br>

## 최종 코드 예시
~~~python
from typing import List

def is_possible(arrivals: List[int], M: int, K: int) -> bool:
    """진기의 최고급 붕어빵 가능 여부 판단.
    - 도착 시각 오름차순으로 순회하며, 각 시각 t에서 생산량 floor(t/M)*K와 누적 손님 수 비교.
    - 전제: M >= 1 (문제 조건). 방어적으로 M <= 0이면 손님 존재 시 불가 처리.
    """
    if M <= 0:
        return len(arrivals) == 0

    arrivals.sort()
    for i, t in enumerate(arrivals, start=1):
        if i > (t // M) * K:
            return False
    return True

def solve() -> None:
    import sys
    input = sys.stdin.readline
    T = int(input().strip())
    for tc in range(1, T + 1):
        N, M, K = map(int, input().split())
        arrivals = list(map(int, input().split()))
        result = "Possible" if is_possible(arrivals, M, K) else "Impossible"
        print(f"#{tc} {result}")

if __name__ == "__main__":
    solve()
~~~
