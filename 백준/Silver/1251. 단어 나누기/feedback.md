# 피드백
## 작성 코드
~~~python
# 1251 단어 나누기

import sys

input = sys.stdin.readline

"""
단어를 3개로 쪼갠다
3개의 단어를 reverse한다
다시 붙인다
이런 단어 중에서 사전순으로 가장 앞서는 단어를 출력하는 프로그램을 만드시오

1. 인덱스 N-3까지 ord가 제일 작은 문자를 찾는다
2. 그걸로 뒤집는다
3. 인덱스 N-2까지...반복
"""


def find_earlist_char_idx(sentence, start_idx, end_idx):
    """
    sentence[start_idx: end_idx]에서, 가장 사전적으로 먼저 오는 문자의 인덱스를 반환한다.

    Args:
        sentence (char): 인자로 받을 문자열
        start_idx (int): sentence에서 인덱스 따질 범위 시작점
        end_idx (int): sentence에서 인덱스 따질 범위 끝점

    Returns:
        int: 사전적으로 제일 빠른 문자 인덱스
    """
    min_ord = ord(sentence[start_idx])
    min_idxs = []

    for i, char in enumerate(sentence):
        if start_idx <= i < end_idx:  # 범위에 들어와야 계산

            if ord(char) < min_ord:  # 최소값 갱신 시 update
                min_ord = ord(char)
                min_idxs = [i]

            elif ord(char) == min_ord:  # 똑같다면 추가
                min_idxs.append(i)

    return min_idxs


def is_earlier(arr1, arr2):
    """
    ord값 리스트 2개를 받아다가, 각 자리수별로 비교한 후
    arr2값이 arr1보다 작다면 True, 아니라면 False 반환

    Example:
        arr1 = [2, 4, 13, 42, 1]
        arr2 = [2, 4, 12, 44, 1]
        -> 12가 13보다 작으므로 return True
    """

    for i in range(len(arr1)):
        if arr2[i] < arr1[i]:   # 2가 더 작으면
            return True
        elif arr2[i] > arr1[i]:   # 2가 더 크면
            return False

    else:   # 모두 같았다면
        return False



def cal_ord(sentence):
    """
    sentence문자열을 돌며 각 ord값을 list형태로 반환
    """
    result = []
    for s in sentence:
        result.append(ord(s))

    return result


# 단어 입력
word = input().rstrip()
N = len(word)  # 단어 길이

ords = []

earlist_idxs = find_earlist_char_idx(word, 0, N - 2)
worst_char = 'z' * len(word)
min_ord = cal_ord(worst_char)     # 초기값은 최악 단어로.
result = worst_char

for flag1 in earlist_idxs:  # 일단 첫번쨰 flag는 최저값에서 찾아야함
    for flag2 in range(flag1 + 1, N - 1):  # 맨 마지막값은 빼야 단어길이 1 이상이 보장됨
        word1 = word[:(flag1 + 1)][::-1]  # 뒤집
        word2 = word[(flag1 + 1): (flag2 + 1)][::-1]
        word3 = word[(flag2 + 1):][::-1]

        new_word = word1 + word2 + word3
        new_word_ord = cal_ord(new_word)      # ord 배열 계산

        if is_earlier(min_ord, new_word_ord):       # new_word가 기존보다 더 빠르면
            min_ord = new_word_ord
            result = new_word

print(result)
~~~
<br><br>

## 총평
- 강점
  - 첫 글자가 될 수 있는 후보를 “최소 문자 위치”로 제한하여 탐색 공간을 줄이려는 아이디어는 타당합니다(첫 구간을 뒤집은 후의 첫 글자가 `word[flag1]`이 되므로, 사전식 최소 해의 첫 글자는 전체 후보 중 최소 문자여야 함).
  - 인덱스 범위를 고려하여 세 구간이 모두 비어있지 않도록 분할 범위를 잘 잡았습니다.
- 개선 필요
  - 파이썬은 문자열의 사전식 비교가 내장되어 있어 `ord` 배열 생성과 수동 비교가 불필요합니다. 현재는 매 시도마다 `cal_ord`와 `is_earlier`로 O(N) 추가 비용이 발생합니다.
  - `find_earlist_char_idx`의 이름 철자(`earlist` → `earliest`) 및 반환 타입/도큐스트링 불일치(주석은 `int` 반환이라 쓰였지만 실제로는 `list` 반환).
  - 불필요한 전역/임시 변수(`ords`, `worst_char`, `min_ord`) 사용 등으로 가독성이 떨어집니다.
- 병목/리스크
  - 핵심 루프는 (분할 2중 루프) × (슬라이싱 뒤집기) × (ord 변환/비교)로 인해 총 O(N^3) 근사. 특히 매 후보마다 `cal_ord(new_word)`가 O(N)으로 추가되어 상수항이 큽니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도
  - 현재 구현: 분할 인덱스 쌍 (i, j)의 개수 O(N^2). 각 후보마다 세 구간 슬라이싱/뒤집기 O(N), 추가로 `cal_ord` 및 `is_earlier` 비교 O(N). ⇒ 총 O(N^3).
  - 문자열 직접 비교로 바꾸면 후보 생성 O(N) + 비교 O(N)이나, CPython 내장 비교는 C 레벨에서 빠르게 최적화되어 있고 평균 조기 중단이 많아 체감 비용이 작습니다.
- 공간 복잡도
  - 슬라이스 문자열 생성으로 후보당 O(N) 임시 메모리. 보장된 상한은 동일하나, 불필요한 `ord` 리스트를 제거하면 임시 객체 수를 줄여 GC 부담을 낮출 수 있습니다.
- 병목 지점
  - `cal_ord`와 `is_earlier` 호출(후보마다 O(N) 2회).
  - 불필요한 초기값 구성(`'z' * N` → `ord` 배열 변환)도 초기 상수 비용 증가 요인.
<br><br>

## 보완점
### 1. 문자열 내장 사전식 비교 활용으로 비교 비용 제거  [중요도: High] [효과: 성능, 가독]
- **근거(Reasoning)**: 파이썬은 문자열 간 `<` 비교가 사전식으로 정의되어 있으며 C 레벨에서 최적화되어 있습니다. `cal_ord`/`is_earlier`를 없애고, 후보 문자열을 직접 최소값과 비교하면 동일한 의미를 더 빠르고 간결하게 달성합니다.
- **결론/리팩터**
~~~python
best = None
for i in range(1, N-1):
    for j in range(i+1, N):
        cand = word[:i][::-1] + word[i:j][::-1] + word[j:][::-1]
        if best is None or cand < best:
            best = cand
print(best)
~~~

<br><br>

### 2. 불일치 도큐스트링/네이밍 정정 및 타입힌트 추가  [중요도: Med] [효과: 가독, 유지보수]
- **근거**: 함수가 **리스트**를 반환하는데 도큐스트링은 **정수**라고 되어 있습니다. 네이밍 오타(`earlist`)도 오해를 유발합니다. 타입힌트 추가로 의도를 명확히 합니다.
- **결론/리팩터**
~~~python
from typing import List

def find_earliest_char_indices(s: str, start: int, end: int) -> List[int]:
    """s[start:end]에서 최소 문자에 해당하는 모든 인덱스를 반환한다."""
    if start >= end:
        return []
    min_ch = min(s[start:end])
    return [i for i in range(start, end) if s[i] == min_ch]
~~~

<br><br>

### 3. “최소 첫 문자” 가지치기는 유지하되, 비교만 단순화  [중요도: Med] [효과: 성능(상수 감소), 가독]
- **근거**: 처음 아이디어(첫 글자가 될 수 있는 인덱스를 최소 문자로 한정)는 탐색 공간을 줄입니다. 이 가지치기를 유지하면서도 비교를 문자열 직접 비교로 바꾸면 상수 시간이 줄어듭니다.
- **결론/리팩터**
~~~python
N = len(word)
first_cut_candidates = []
if N >= 3:
    first_cut_candidates = find_earliest_char_indices(word, 0, N-2)  # i <= N-3

best = None
for i in first_cut_candidates:
    for j in range(i+1, N):
        cand = word[:i+1][::-1] + word[i+1:j+1][::-1] + word[j+1:][::-1]
        if best is None or cand < best:
            best = cand
print(best)
~~~

<br><br>

### 4. 불필요한 전역/임시 변수 제거 및 입력 검증  [중요도: Low] [효과: 가독, 안정성]
- **근거**: `ords`, `worst_char`, `min_ord` 등은 리팩터 후 불필요합니다. 또한 길이가 3 미만인 입력에 대한 안전 처리(문제 조건상 보통 최소 3이지만 방어적 코드는 유익).
- **결론/리팩터**
~~~python
word = input().strip()
if len(word) < 3:
    print(word)  # 또는 예외/조기 종료
    raise SystemExit
# 이후 핵심 로직만 유지
~~~
<br><br>

## 최종 코드 예시
~~~python
import sys
from typing import List

input = sys.stdin.readline

def find_earliest_char_indices(s: str, start: int, end: int) -> List[int]:
    """s[start:end]에서 최소 문자에 해당하는 모든 인덱스를 반환한다."""
    if start >= end:
        return []
    min_ch = min(s[start:end])
    return [i for i in range(start, end) if s[i] == min_ch]

def main() -> None:
    word = input().strip()
    N = len(word)
    if N < 3:
        print(word)
        return

    # 첫 글자가 될 수 있는 위치는 첫 구간의 마지막 인덱스 i(0 <= i <= N-3)
    # 뒤집힌 결과의 첫 글자는 word[i]이므로, s[0:N-2) 내 최소 문자 위치만 고려
    first_cut_candidates = find_earliest_char_indices(word, 0, N - 2)

    best = None
    for i in first_cut_candidates:
        # 두 번째 컷 j는 i+1 <= j <= N-2 (세 구간 모두 비어있지 않게)
        for j in range(i + 1, N - 1):
            cand = word[: i + 1][::-1] + word[i + 1 : j + 1][::-1] + word[j + 1 :][::-1]
            if best is None or cand < best:  # 문자열 사전식 비교(내장)
                best = cand

    # first_cut_candidates가 비었을 가능성은 없음(N>=3이면 최소 한 자리 존재)
    print(best)

if __name__ == "__main__":
    main()
~~~
