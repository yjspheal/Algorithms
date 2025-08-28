# 피드백
## 작성 코드
~~~python
import sys

input = sys.stdin.readline 

import math

# 시험장의 수
N = int(input())

# 각 시험장에 있는 응시자 수
arr = list(map(int, input().rstrip().split()))

# 주감독관 시야ㅂ 부감독관 시야
B, C = map(int, input().rstrip().split())

tester = 0

for students in arr:
    students -= B  # 총시험관 1명
    tester += 1

    if students > 0:
        if students % C == 0:
            tester += students // C
        else:
            tester += students // C + 1

print(tester)
~~~
<br><br>

## 총평
- 강점
  - 한 시험장당 **주감독관 1명 무조건 배치** 후, 남은 인원에 대해 **부감독관 수를 올림 나눗셈**으로 계산하는 핵심 로직이 정확합니다.
  - 입력 규모(최대 N)만큼 한 번 순회하는 **O(N)** 시간, **O(1)** 추가 공간으로 효율적입니다.
- 개선 필요
  - `math` 모듈을 임포트했지만 사용하지 않음(불필요 임포트).
  - 변수/주석 네이밍이 불명확함(예: “시야ㅂ” → “감독 가능 인원(수용인원)”).  
  - 올림 나눗셈을 분기(`if/else`)로 처리 → **분기 없이 정수 올림 나눗셈**으로 단순화 가능.
  - 루프 안에서 `tester += 1`로 주감독관을 더하는 것보다, **초기값을 `N`으로 두는 편이 의도가 명확**합니다.
- 병목/리스크
  - Python에서는 합계가 매우 커져도 `int`가 임의정밀도라 안전하지만, **타 언어로 이식 시 64-bit 정수(예: `long long`) 필요**하다는 점을 주석으로 남기면 좋습니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: **O(N)** (시험장 수만큼 한 번의 순회)
- 공간 복잡도: **O(1)** (상수 크기 변수만 사용)
- 병목 지점: 없음 (입력 파싱이 지배적이며, 계산은 상수 연산)
<br><br>

## 보완점
### 1. 분기 없는 올림 나눗셈으로 단순화  [중요도: High] [효과: 가독/성능]
- **Reasoning:** `ceil(x / C)`는 정수 연산으로 `(x + C - 1) // C`로 계산 가능. 분기 제거로 간결하며 빠름.
- **Conclusion (리팩터):** 남은 인원 `rem = students - B`가 양수일 때 `tester += (rem + C - 1) // C`.

~~~python
rem = students - B
if rem > 0:
    tester += (rem + C - 1) // C
~~~

<br><br>

### 2. 초기값에 주감독관 수 반영  [중요도: Med] [효과: 가독]
- **Reasoning:** 모든 시험장에 주감독관 1명 배치 → `tester = N`으로 시작하면 의도가 명확.
- **Conclusion:** 루프 내부의 `tester += 1` 제거 가능.

~~~python
tester = N
for students in arr:
    rem = students - B
    if rem > 0:
        tester += (rem + C - 1) // C
~~~

<br><br>

### 3. 불필요 임포트/주석/네이밍 정리  [중요도: Low] [효과: 가독/유지보수]
- **Reasoning:** 사용하지 않는 `math` 제거, 주석의 오타 및 의미 수정(“시야” → “감독 가능 인원(수용인원)”).
- **Conclusion:** 명확한 도메인 용어 사용(주감독/부감독 “수용 인원”).

<br><br>

## 최종 코드 예시
~~~python
import sys

input = sys.stdin.readline

# 시험장의 수
N = int(input())

# 각 시험장에 있는 응시자 수
arr = list(map(int, input().split()))

# 주감독관/부감독관이 한 시험장에서 감독할 수 있는 최대 응시자 수(수용 인원)
B, C = map(int, input().split())

# 모든 시험장에 주감독관 1명씩 배치
tester = N

for students in arr:
    rem = students - B  # 주감독관이 담당하고 남은 인원
    if rem > 0:
        # 부감독관 수: rem을 C로 올림 나눗셈
        tester += (rem + C - 1) // C

print(tester)
~~~
