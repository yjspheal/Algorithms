# 피드백
## 작성 코드
~~~python
def is_palindrome(char_list):
    """
    char_list 문자열 리스트에 대해, 회문인지 판단하여 맞다면 True 아니면 False를 반환하는 함수
    """
    return char_list == char_list[::-1]


T = 10
for tc in range(1, T + 1):
    M = int(input())  # 찾아야하는 회문의 길이
    sentences = [list(input()) for _ in range(8)]  # 8x8의 글자판이 주어진다
    sentences += list(zip(*sentences))  # 세로줄을 추가한다

    len_sentences = len(sentences)  # 16으로 고정이지만 그냥 계산
    len_row = len(sentences[0])  # 8로 고정이지만 그냥 계산

    count = 0  # 회문 갯수 계산
    for row in sentences:
        for i in range(len_row - M + 1):  # + M-1까지 회문인지 체크
            if is_palindrome(row[i: i + M]):        # 회문이라면 count + 1
                palindrome = row[i: i + M]
                count += 1

    print(f'#{tc} {count}')
~~~
<br><br>

## 총평
- 강점
  - `is_palindrome`을 별도 함수로 분리해 코드 가독성 확보
  - `zip(*sentences)`로 세로줄을 쉽게 구해 반복을 절약한 점은 매우 효율적
  - 문제 크기가 작아 전체 탐색(Brute force)로도 충분히 동작
- 개선 필요
  - `len_sentences`, `len_row`는 문제 조건상 고정값(16, 8)이므로 변수로 둘 필요가 없음
  - `palindrome = row[i:i+M]`은 디버깅 용도로 보이며 불필요
  - `is_palindrome`이 단순 비교만 수행하므로 inline으로 처리하거나, slicing 대신 양쪽 비교로 최적화 가능
- 병목/리스크
  - 시간복잡도는 O(16 * (8-M+1) * M) = O(128M), 충분히 작아 성능 문제는 없음
  - 다만 `[::-1]` 슬라이싱은 매번 새로운 리스트를 생성하므로, M이 커질 경우 상대적으로 비효율적일 수 있음

<br><br>

## 복잡도 및 병목
- 시간 복잡도: O(16 * (8-M+1) * M) → 최대 O(1024) 수준
- 공간 복잡도: O(8*8) 입력 저장, 추가로 슬라이싱 시 O(M)
- 병목 지점: `char_list[::-1]`로 매번 새로운 리스트를 만들어 비교하는 부분

<br><br>

## 보완점
### 1. 슬라이싱 대신 투포인터 비교   [중요도: High] [효과: 성능/안정성]
- `[::-1]` 대신 양쪽 끝에서 투포인터 방식으로 비교하면 불필요한 리스트 생성 비용이 줄어듦
~~~python
def is_palindrome(char_list) -> bool:
    left, right = 0, len(char_list) - 1
    while left < right:
        if char_list[left] != char_list[right]:
            return False
        left += 1
        right -= 1
    return True
~~~

<br><br>

### 2. 불필요한 변수 제거   [중요도: Med] [효과: 가독성]
- `len_sentences`, `len_row`, `palindrome` 변수는 사실상 필요 없음. 직접 16, 8 또는 `len()`을 바로 쓰는 편이 명확.

~~~python
for row in sentences:
    for i in range(9 - M):   # 8 - M + 1
        if is_palindrome(row[i:i+M]):
            count += 1
~~~

<br><br>

### 3. 함수화 및 도큐스트링 보강   [중요도: Low] [효과: 유지보수/재사용성]
- 메인 로직을 함수로 분리해 테스트 용이성 강화
~~~python
def count_palindromes(sentences, m: int) -> int:
    """8x8 보드에서 길이 m 회문 개수 세기"""
    sentences += list(zip(*sentences))  # 세로줄 추가
    count = 0
    for row in sentences:
        for i in range(9 - m):  # 8 - m + 1
            if is_palindrome(row[i:i+m]):
                count += 1
    return count
~~~

<br><br>

## 최종 코드 예시
~~~python
def is_palindrome(char_list) -> bool:
    """리스트가 회문인지 여부 반환"""
    left, right = 0, len(char_list) - 1
    while left < right:
        if char_list[left] != char_list[right]:
            return False
        left += 1
        right -= 1
    return True


def count_palindromes(sentences, m: int) -> int:
    """8x8 보드에서 길이 m 회문 개수 세기"""
    sentences += list(zip(*sentences))  # 세로줄 추가
    count = 0
    for row in sentences:
        for i in range(9 - m):  # 8 - m + 1
            if is_palindrome(row[i:i+m]):
                count += 1
    return count


T = 10
for tc in range(1, T + 1):
    M = int(input())
    sentences = [list(input()) for _ in range(8)]
    result = count_palindromes(sentences, M)
    print(f'#{tc} {result}')
~~~
