# 피드백
## 작성 코드
~~~python
# import sys
# 
# sys.stdin = open('sample_input.txt')

T = int(input())
for tc in range(1, T + 1):
    # 일 월 3개월 1년권 가격
    price_d, price_m, price_3m, price_y = map(int, input().split())

    next_year = [0] + list(map(int, input().split()))  # 인덱스 맞추기용

    for i in range(len(next_year)):  # 내년 계획을 돌며

        if next_year[i] * price_d > price_m:  # 다 일일권으로 다니는거보다 월간권이 싸면
            next_year[i] = price_m  # 월간권으로 바꿔둔다
        else:
            next_year[i] *= price_d  # 아니면 일일권으로 계산한 가격을 둔다

    min_cost = sum(next_year)  # 최소값으로 저장

    # 3개월권 쓰는 월 구해보기
    tri_plans = []
    for month in range(1, 13):  # 12월까지 1번 산다면
        tri_plans.append([month])

        for month2 in range(month + 3, 13):  # 2번 산다면
            tri_plans.append([month, month2])

            for month3 in range(month2 + 3, 13):  # 3번 산다면
                tri_plans.append([month, month2, month3])

                for month4 in range(month3 + 3, 13):  # 4번 산다면
                    tri_plans.append([month, month2, month3, month4])



    # 다시 내년 계획을 돌며
    for tri_plan in tri_plans:
        cost = 0  # 현재 비용 0

        m = 1  # 이번 달
        while m <= 12:
            if m in tri_plan:  # 3개월권 구매달이면
                cost += price_3m  # 구매하고 3개월 흐름
                m += 3
            else:
                cost += next_year[m]  # 구매 안하면 걍 기존값
                m += 1  # 다음달로

            if cost > min_cost:  # 이미 최소값을 넘어섰다면
                break  # 끝

        if cost < min_cost:  # 최소값보다싸다면 update
            min_cost = cost

    # 3개월권 구매값보다 연간권이 싸다면 update
    if min_cost > price_y:
        min_cost = price_y

    print(f'#{tc} {min_cost}')
~~~
<br><br>

## 총평
- 강점
  - 일/월 단가를 먼저 최소화하고, 3개월권 조합을 따로 탐색하는 흐름이 논리적으로 타당합니다.
  - 3개월권이 겹치지 않도록 (month, month+3, …)만 고려하여 불필요한 경우의 수를 많이 줄였습니다.
- 개선 필요
  - 3개월권 조합을 전부 만들어 시뮬레이션하는 방식은 여전히 **브랜치 수가 많고 코드가 장황**합니다.
  - `m in tri_plan` 검사가 매 달 O(길이) 선형 탐색이며, 조기 종료 로직이 있어도 **구현 복잡도**가 높습니다.
  - 인덱스 0도 순회/합산에 포함시키는 구조가 맞긴 하지만(0이라 영향 없음), **명시성이 떨어져** 오해의 여지가 있습니다.
- 병목/리스크
  - 시간복잡도는 최악 시 3개월권 조합 수 × 12달 시뮬레이션으로 **상수 범위**이긴 하나, 문제 크기에 비해 **불필요하게 복잡**합니다.
  - 로직 분기가 많아 유지보수/오류 추적이 어렵습니다.
<br><br>

## 복잡도 및 병목
- 현재 방식
  - 시간 복잡도: 3개월권 조합 개수를 `C`라 할 때 O(C·12). 여기서 `C`는 비겹침 조건으로 제한되지만 여전히 여러 중첩 루프에 의존.
  - 공간 복잡도: O(C·최대선택수) (모든 tri_plans 저장).
  - 병목 지점: tri_plans 생성/순회 + 매달 `in` 탐색.
- 권장 방식(DP)
  - 시간 복잡도: O(12) — 각 달마다 상수 가지(min(일/월, 3개월, 1년))만 고려.
  - 공간 복잡도: O(12) 혹은 O(1) 롤링.
<br><br>

## 보완점
### 1. DP로 월별 최솟값 누적   [중요도: High] [효과: 성능/가독]
- **Reasoning:** 각 달 `i`까지의 최소 비용 `dp[i]`만 알면, 다음을 통해 상수 시간에 전이 가능합니다.
  - `dp[i] = min(dp[i-1] + min(일×이용횟수, 월권), dp[i-3] + 3개월권, dp[i-12] + 연간권)`
  - 경계는 음수 인덱스 대신 0으로 캡핑하여 처리.
- **Conclusion (리팩터):** 조합 열거가 필요 없어지고, 코드 길이가 줄며 실수 가능성을 줄입니다.
~~~python
def min_cost_swim(days, price_d, price_m, price_3m, price_y):
    # days: 1..12 월별 이용 일수
    monthly_min = [0] * 13
    for i in range(1, 13):
        monthly_min[i] = min(days[i] * price_d, price_m)

    dp = [0] * 13
    for i in range(1, 13):
        # 1달 더하기
        cand1 = dp[i-1] + monthly_min[i]
        # 3달권
        cand2 = dp[i-3] + price_3m if i >= 3 else price_3m
        # 1년권
        cand3 = price_y
        dp[i] = min(cand1, cand2, cand3)
    return dp[12]
~~~

<br><br>

### 2. 불필요한 조합 저장/순회를 제거   [중요도: Med] [효과: 성능/메모리]
- **Reasoning:** `tri_plans` 전체를 미리 구성할 필요 없이, DP가 모든 선택지를 내포합니다.
- **Conclusion:** tri_plans 관련 코드(생성/순회/`in` 검사)를 전부 제거합니다. 메모리와 브랜치가 감소합니다.

<br><br>

### 3. 인덱스 명시성 개선(1-based 입력 유지)   [중요도: Low] [효과: 가독]
- **Reasoning:** `[0] + ...` 패턴은 SWEA에서 흔하지만, 처리 루프에서 `range(13)` 등의 상수와 함께 의도를 분명히 하면 혼동이 줄어듭니다.
- **Conclusion:** `days = [0] + list(map(int, input().split()))` 후, 처리 루프는 **1..12**만 명시적으로 접근.

<br><br>

### 4. 함수화/타입힌트/도큐스트링   [중요도: Low] [효과: 유지보수]
- **Reasoning:** 테스트/재사용 편의·의미 전달력이 증가.
- **Conclusion:** 메인 루프에서 함수를 호출하는 구조.

<br><br>

## 최종 코드 예시
~~~python
from typing import List

def min_cost_swim(days: List[int], price_d: int, price_m: int, price_3m: int, price_y: int) -> int:
    """
    1~12월 월별 이용일(days[1..12])과 이용권 가격으로 1년 최소 비용을 계산한다.
    전이식:
      dp[i] = min(
        dp[i-1] + min(days[i]*일권, 월권),
        dp[i-3] + 3개월권,
        1년권
      )
    경계: i<3  구간은 dp[음수] 대신 0으로 간주.
    """
    # 월별 '일권 vs 월권' 최소 비용
    monthly_min = [0] * 13
    for i in range(1, 13):
        monthly_min[i] = min(days[i] * price_d, price_m)

    dp = [0] * 13
    for i in range(1, 13):
        # 1달 추가
        cand1 = dp[i - 1] + monthly_min[i]
        # 3개월권: i<3이면 이전 비용 0으로 처리
        cand2 = (dp[i - 3] if i >= 3 else 0) + price_3m
        # 1년권
        cand3 = price_y
        dp[i] = min(cand1, cand2, cand3)

    return dp[12]


T = int(input())
for tc in range(1, T + 1):
    price_d, price_m, price_3m, price_y = map(int, input().split())
    # days[1..12]로 맞추기 위해 앞에 0을 둔다.
    days = [0] + list(map(int, input().split()))
    result = min_cost_swim(days, price_d, price_m, price_3m, price_y)
    print(f"#{tc} {result}")
~~~
