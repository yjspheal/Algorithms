# 피드백
## 작성 코드
~~~python
s_number = list(range(1,31))

for time in range(28):
  student = int(input())
  del s_number[s_number.index(student)]

for s in s_number:
  print(s)
~~~
<br><br>

## 총평
- 강점
  - 아이디어가 직관적: 1~30 생성 후 제출자 번호를 삭제 ⇒ 남은 2명을 출력.
  - 입력 규모가 작아(30) 정답을 문제없이 도출.
- 개선 필요
  - `list.index()`가 매번 선형 탐색이고, `del` 또한 리스트 시프트가 발생 → 총 시간복잡도 **O(N²)** 패턴.
  - `time` 변수명은 관습적으로 쓰는 모듈명과 겹쳐 의미가 모호함(여기선 루프 카운터 → `_` 권장).
  - `del s_number[s_number.index(student)]`는 한 줄로는 간결하지만, 로직 의도가 불분명해질 수 있음.
- 병목/리스크
  - **병목**: `list.index(student) = O(N)` + `del`에 따른 시프트 `O(N)` → 28회 반복으로 **O(N²)**.
  - 입력이 커지면 비효율. (현재 문제는 작아도 습관적으로 개선해두는 게 좋음.)
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 현재 구현은 `28 * (index O(N) + del O(N))` ≈ **O(N²)**.
- 공간 복잡도: **O(N)** (리스트 30개 원소).
- 병목 지점: `list.index`와 `del`에 의한 선형 연산 반복.
<br><br>

## 보완점
### 1. `set` 차집합으로 단순화  [중요도: High] [효과: 성능/가독]
- **Reasoning:** 제출자 집합을 만들어 `전체 집합 - 제출자 집합`으로 두 명을 바로 구하면, 삭제/탐색 반복이 사라져 간결하고 빠릅니다.
- **Conclusion (코드):**
~~~python
all_stu = set(range(1, 31))
submitted = {int(input()) for _ in range(28)}
missing = sorted(all_stu - submitted)
for x in missing:
    print(x)
~~~

<br><br>

### 2. 불린 마킹 배열 사용  [중요도: High] [효과: 성능/가독]
- **Reasoning:** 인덱스로 바로 마킹하므로 모든 연산이 상수시간. 정수 범위가 작을 때 특히 깔끔.
- **Conclusion (코드):**
~~~python
seen = [False] * 31
for _ in range(28):
    seen[int(input())] = True

for i in range(1, 30 + 1):
    if not seen[i]:
        print(i)
~~~

<br><br>

### 3. 변수명/루프 개선  [중요도: Low] [효과: 가독]
- **Reasoning:** 의미 없는 카운터는 `_` 사용, 모듈명과 겹치는 `time` 지양.
- **Conclusion (코드 스니펫):**
~~~python
for _ in range(28):
    ...
~~~
<br><br>

## 최종 코드 예시
~~~python
# 세트 차집합으로 간결하고 빠르게 해결
all_stu = set(range(1, 31))
submitted = {int(input()) for _ in range(28)}
for x in sorted(all_stu - submitted):
    print(x)
~~~
