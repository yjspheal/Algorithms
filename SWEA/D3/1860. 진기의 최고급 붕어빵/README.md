# [D3] 진기의 최고급 붕어빵 - 1860 

[문제 링크](https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5LsaaqDzYDFAXc) 

### 성능 요약

메모리: 66,432 KB, 시간: 274 ms, 코드길이: 1,158 Bytes

### 제출 일자

2025-08-19 21:54



> 출처: SW Expert Academy, https://swexpertacademy.com/main/code/problem/problemList.do


<br><br>

# 피드백
## 기존 코드
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
        if i > 0 and i % M == 0:        # M초마다 붕어빵 K개 생성
            current_boong += K

        current_boong -= visitor_list[i]    # 지금 온 손님에게 하나씩 주기
        if current_boong < 0:               # 붕어빵 재고보다 더 줘야되는 상황이었으면
            result = 'Impossible'           # 불가능

    print(f'#{tc} {result}')
~~~
<br><br>

## 총평
- 문제 의도(시뮬레이션) 그대로 구현했고, “0초에는 생산 없음”을 `i > 0 and i % M == 0`으로 정확히 처리한 점이 좋습니다.
- 다만 `11112`라는 매직 넘버 사용과 전초(0..latest_time) 순회로 불필요한 시간·공간 낭비가 있습니다.
- 불가능이 확정된 시점에서도 루프가 계속 도는 점, 테스트 케이스 루프 내부가 함수화되어 있지 않은 점이 아쉽습니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 현재 구현은 `O(latest_time + N)`  
  (손님 입력 집계 `O(N)` + 0~latest_time 전초 스캔 `O(latest_time)`)
- 공간 복잡도: `O(latest_time)` (길이 11112의 배열 사용)
- 병목 지점:
  - 전초 스캔 루프(파일: 본문 for 루프) — 손님이 적고 `latest_time`이 상대적으로 클 때 비효율.
  - 결과가 이미 `Impossible`이어도 루프를 끝까지 도는 부분.
  - 고정 크기 배열 `11112`(매직 넘버) — 입력 제약에 묶여 있고 가독성 저하.
<br><br>

## 보완점
### 1. “이벤트 기반(정렬)”으로 전환해 전초 스캔 제거  [중요도: High] [효과: 성능/가독]
각 손님 도착 시간 `t`에 대해, 그 시점까지 생산된 붕어빵 수는 `floor(t / M) * K` 입니다.  
손님을 도착 시간으로 정렬한 뒤 `i`번째(1-based) 손님 방문 때 `produced < i`이면 바로 `Impossible`입니다.  
- 시간: `O(N log N)` (정렬) — 기존 `O(latest_time + N)` 대비, `latest_time`가 크고 `N`이 작은 케이스에서 유리
- 공간: `O(1)` 추가(정렬 인플레이스 가정)

~~~python
# 핵심 로직 예시
arrivals.sort()
for i, t in enumerate(arrivals, start=1):
    produced = (t // M) * K
    if produced < i:
        return "Impossible"
return "Possible"
~~~

<br><br><br>

### 2. 조기 종료(Early break)로 불필요한 연산 차단  [중요도: High] [효과: 성능]
현재 코드는 `current_boong < 0`이어도 끝까지 순회합니다. 즉시 `break` 또는 즉시 결과 리턴으로 낭비 제거.
~~~python
for i in range(latest_time + 1):
    ...
    if current_boong < 0:
        result = "Impossible"
        break
~~~

<br><br><br>

### 3. 매직 넘버(11112) 제거 및 입력 기반 크기 사용  [중요도: Med] [효과: 안정성/가독]
제약이 바뀌면 오류 위험이 있습니다. `max(arrivals)`를 사용하거나, 아예 이벤트 기반으로 전환해 배열 자체를 제거하세요.
~~~python
latest_time = max(arrivals)
visitor = [0] * (latest_time + 1)
~~~

<br><br><br>

### 4. 함수화 + 타입힌트 + 도큐스트링  [중요도: Med] [효과: 가독/유지보수]
입출력 분리, 테스트 용이. 예외·엣지(손님이 0명, `M==0` 불가 등 문제 제약)도 주석으로 명시.
~~~python
from typing import List

def can_serve_all(arrivals: List[int], M: int, K: int) -> str:
    """
    M초마다 K개 생산. arrivals[i]는 i번째 손님 도착 초.
    반환: "Possible" | "Impossible"
    """
    arrivals.sort()
    for i, t in enumerate(arrivals, 1):
        if (t // M) * K < i:
            return "Impossible"
    return "Possible"
~~~

<br><br><br>

### 5. 변수명 일관성과 주석 정제  [중요도: Low] [효과: 가독]
`visitor_list`→`arrivals_per_sec`처럼 의도를 드러내고, 중복/자명한 주석은 줄여 핵심 문맥만 남기세요.
<br><br><br>

## 최종 코드 예시
~~~python
# 1860. 진기의 최고급 붕어빵 - 이벤트(정렬) 기반 풀이
# - 시간: O(N log N)
# - 공간: O(1) (정렬 인플레이스 가정)
from typing import List

def can_serve_all(arrivals: List[int], M: int, K: int) -> str:
    """
    arrivals: 손님 도착 시각(초) 리스트
    M: M초마다
    K: K개 붕어빵 생산
    규칙: 0초에는 생산 없음. t초 도착 손님까지 누적 생산 = (t // M) * K
    """
    arrivals.sort()
    for i, t in enumerate(arrivals, start=1):  # i = 지금까지 도착한 손님 수
        produced = (t // M) * K
        if produced < i:
            return "Impossible"
    return "Possible"

if __name__ == "__main__":
    import sys
    input = sys.stdin.readline

    T = int(input().strip())
    for tc in range(1, T + 1):
        N, M, K = map(int, input().split())
        arrivals = list(map(int, input().split()))
        # 가드: 입력 신뢰 (문제 제약 상 M>=1, K>=1, len(arrivals)==N 가정)
        result = can_serve_all(arrivals, M, K)
        print(f"#{tc} {result}")
~~~
