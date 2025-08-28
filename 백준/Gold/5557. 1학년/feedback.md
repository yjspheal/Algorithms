# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

N = int(input())
nums = list(map(int,input().split()))

i = 0
result = {}
for idx in range(21):
  result[idx] = 0

result[nums[0]] = 1

while i < N - 2:
  i += 1
  res = {}
  for n in range(21):
    res[n] = 0
    try:
      res[n] += result[n + nums[i]]
    except:
      pass

    try:
      res[n] += result[n - nums[i]]
    except:
      pass

  result = res

print(result[nums[-1]])
~~~
<br><br>

## 총평
- 강점
  - DP 전개 아이디어가 정확합니다: 첫 수를 시작값으로 두고, 마지막 수를 목표로 두며 중간 수들을 ±로 더해 0..20 범위에 도달하는 경우의 수를 누적.
  - 목표 범위를 0..20로 제한하는 문제 특성을 반영.
- 개선 필요
  - `dict` + `try/except`로 경계(0..20)를 처리하여 **예외를 로직 흐름**으로 사용 → 불필요한 오버헤드.
  - 불변 크기(21)의 상태라면 **리스트(길이 21)** 가 더 간단하고 빠릅니다.
  - 모든 `n`에 대해 0 카운트까지 순회하고, 그 안에서 다시 예외를 시도 → **중복·불필요 연산** 증가.
  - 변수 네이밍(`result`, `res`, `nums`)과 루프 구조(while + 수동 인덱스 증가)가 가독성을 떨어뜨립니다.

<br><br>

## 복잡도 및 병목
- 시간 복잡도(현 코드): 각 단계마다 21개 상태 × 두 번의 `dict` 조회와 예외 처리 시도 → 대략 **O(21·(N-2)) = O(N)** 이지만 예외 처리 비용과 딕셔너리 오버헤드로 실제 느림.
- 공간 복잡도: **O(21)** 상태를 딕셔너리로 보관(리스트로 대체 가능).
- 병목 지점: `try/except` 남용, 딕셔너리 접근 비용, 0 카운트 상태까지 전부 순회.

<br><br>

## 보완점
### 1. 리스트 기반 DP로 전환 + 경계 체크로 예외 제거   [중요도: High] [효과: 성능/가독]
- **Reasoning:** 상태 공간이 21로 고정이므로 리스트가 가장 단순·빠릅니다. 예외 대신 `0 <= idx <= 20` 조건으로 경계를 명시하면 분기 비용이 작고 의도가 명확합니다.
- **Conclusion (핵심 스니펫):**
~~~python
dp = [0] * 21
dp[nums[0]] = 1
for i in range(1, N-1):
    a = nums[i]
    nxt = [0] * 21
    for v in range(21):
        cnt = dp[v]
        if cnt == 0:
            continue
        nv = v + a
        if 0 <= nv <= 20:
            nxt[nv] += cnt
        nv = v - a
        if 0 <= nv <= 20:
            nxt[nv] += cnt
    dp = nxt
print(dp[nums[-1]])
~~~

<br><br>

### 2. “활성 상태만” 전개하여 불필요 순회 감소   [중요도: Med] [효과: 성능]
- **Reasoning:** 많은 `v`에서 `dp[v]==0`이면 연산이 낭비됩니다. 위 스니펫의 `if cnt == 0: continue`가 바로 이 최적화입니다.
- **Conclusion:** 0 상태 스킵으로 실제 연산량 감소(최악은 동일 O(N), 평균 성능↑).

<br><br>

### 3. 네이밍/루프 구조 정리   [중요도: Low] [효과: 가독성]
- **Reasoning:** `for i in range(1, N-1)`가 `while i < N-2`보다 의도가 명확하고 안전. 변수명도 `dp`, `nxt`, `A` 등으로 의미를 드러내면 유지보수성↑.
- **Conclusion:** 최종 코드에 반영.

<br><br>

## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline

N = int(input())
A = list(map(int, input().split()))

# dp[v] = 현재까지 만들 수 있는 값 v(0..20)에 도달하는 방법 수
dp = [0] * 21
dp[A[0]] = 1  # 첫 숫자는 반드시 그대로 시작

for i in range(1, N - 1):  # 마지막 값은 목표값이므로 제외
    a = A[i]
    nxt = [0] * 21
    for v in range(21):
        cnt = dp[v]
        if cnt == 0:
            continue
        nv = v + a
        if 0 <= nv <= 20:
            nxt[nv] += cnt
        nv = v - a
        if 0 <= nv <= 20:
            nxt[nv] += cnt
    dp = nxt

print(dp[A[-1]])
~~~
