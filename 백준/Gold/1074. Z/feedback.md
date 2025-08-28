# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

N, row, col = map(int,input().split())

num = 0

while N > 0:
  num += (row // 2 **(N-1) * 2 **(N-1) * 2 ** N) + (col // 2 **(N-1) * 2 **(N-1)* 2 **(N-1))
  row %= 2 **(N-1)
  col %= 2 **(N-1)
  N -= 1

print(num)
~~~
<br><br>

## 총평
- 강점
  - 각 단계에서 사분면을 판정(행/열을 `2^(N-1)`로 나눈 몫)하고, 해당 사분면 면적(`(2^(N-1))^2`)만큼 인덱스에 더하는 **Z-순회(모튼 코드) 규칙을 정확히 구현**했습니다.
  - 반복으로 `row, col`을 하위 사분면 좌표로 축소해가는 방식이 직관적이며, **시간·공간 모두 O(N), O(1)**로 충분히 효율적입니다.
- 개선 필요
  - 매 반복마다 `2 ** (N-1)`를 여러 번 계산하고, `//`, `%`도 중복 호출되어 **불필요한 연산**이 많습니다.
  - 수식이 길어 가독성이 떨어집니다(동일 항의 반복, 괄호/지수 연산 남발).
  - 변수 네이밍과 미세 포맷팅(공백) 개선 여지.
- 병목/리스크
  - 입력 범위에서 성능 이슈는 없지만, **지수 연산과 나눗셈**을 줄이면 더 깔끔하고 빠릅니다.
  - 논리 오류는 없음(현재 공식을 전개하면 `(2*(row_div)+col_div)*half*half`와 동치).

<br><br>

## 복잡도 및 병목
- 시간 복잡도: 각 레벨당 상수 연산 → **O(N)**  
- 공간 복잡도: 보조 변수만 사용 → **O(1)**
- 병목 지점: 반복되는 `2 ** (N-1)` 계산, 몫/나머지 연산의 중복 사용(미세 비효율)

<br><br>

## 보완점
### 1. `half` 캐싱 + 사분면 공식으로 단순화   [중요도: High] [효과: 성능/가독]
- **Reasoning:** 각 단계의 한 변 길이를 `half = 1 << (N-1)`로 캐싱하면 지수/나눗셈 호출을 줄일 수 있습니다.  
  사분면 번호는 `quad = (row >= half) * 2 + (col >= half)`로 계산, 누적치는 `num += quad * half * half`.
- **Conclusion (핵심 루프만 발췌):**
~~~python
half = 1 << (N-1)
while half:
    quad = (row >= half) * 2 + (col >= half)
    num += quad * half * half
    if row >= half: row -= half
    if col >= half: col -= half
    half >>= 1
~~~

<br><br>

### 2. 비트연산으로 더욱 간결하게(선택)   [중요도: Med] [효과: 성능/가독]
- **Reasoning:** 모튼 코드는 사실상 `row`와 `col`의 비트를 상위비트부터 **인터리브**하는 과정입니다.  
  각 단계에서 `num = (num << 2) | ((row>>k & 1) << 1) | (col>>k & 1)`로 만들 수 있습니다.
- **Conclusion (핵심 루프만 발췌):**
~~~python
ans = 0
for k in range(N-1, -1, -1):
    ans <<= 2
    ans |= ((row >> k) & 1) << 1 | ((col >> k) & 1)
~~~

<br><br>

### 3. 네이밍 및 포맷 정리   [중요도: Low] [효과: 가독]
- **Reasoning:** `row, col` 유지하되, 누적값은 `num` 또는 `ans`로 통일, 공백/괄호 정리.
- **Conclusion:** 최종 코드에서 반영.

<br><br>

## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline

N, row, col = map(int, input().split())

num = 0
half = 1 << (N - 1)  # 현재 단계의 한 변 길이

while half:
    # 현재 사분면: 상(0)/하(1) → 행, 좌(0)/우(1) → 열
    quad = (row >= half) * 2 + (col >= half)  # 0..3
    num += quad * half * half                 # 해당 사분면 면적만큼 오프셋 추가

    # 하위 사분면 좌표로 축소
    if row >= half:
        row -= half
    if col >= half:
        col -= half

    half >>= 1  # 다음 단계(크기 절반)

print(num)
~~~
