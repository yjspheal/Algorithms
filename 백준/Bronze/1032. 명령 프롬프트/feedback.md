# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

T = int(input())
# 단어를 리스트로 받아옴
words = [input().rstrip() for tc in range(T)]

# 단어의 길이
N = len(words[0])

result = ''
for i in range(N):
    # 첫번째 단어와 같은지를 기준으로
    char = words[0][i]
    for word in words[1:]:
        if word[i] != char:
            result += '?'
            break
    else:
        result += char

print(result)
~~~
<br><br>

## 총평
- 핵심 로직이 간단하며, 문제 의도(파일명 공통 패턴 찾기)를 충실히 구현함.
- `break`/`else` 구문 활용으로 흐름 제어를 깔끔하게 처리한 점이 좋음.
- 변수명(`T`, `N`, `words`, `char`)이 직관성이 조금 떨어짐. `T`는 파일 개수인데 입력 개수로만 보일 수 있음.
- 문자열 연결(`result += ...`)은 반복문에서 O(n²) 시간이 될 수 있음 → 리스트에 append 후 `''.join` 하는 방식이 더 효율적임.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: O(N·T)  
  (단어 길이 `N`, 단어 개수 `T` → 각 자리마다 모든 단어 비교)
- 공간 복잡도: O(N·T) (입력 문자열 저장)
- 병목 지점: `result += char` 부분. Python 문자열은 불변(immutable)이라 매번 새 문자열을 생성하므로 길이가 길 때 비효율 발생 가능.
<br><br>

## 보완점
### 1. 문자열 연결 최적화  [중요도: High] [효과: 성능]
현재 `result += ...`는 반복문마다 새 문자열 객체를 생성해 O(N²) 가능성이 있음. 리스트에 모았다가 마지막에 join으로 합치면 O(N)으로 줄일 수 있음.
~~~python
result_chars = []
for i in range(N):
    char = words[0][i]
    for word in words[1:]:
        if word[i] != char:
            result_chars.append('?')
            break
    else:
        result_chars.append(char)

print(''.join(result_chars))
~~~
<br><br><br>

### 2. 변수명 개선  [중요도: Med] [효과: 가독]
- `T` → `num_words`  
- `N` → `word_length`  
- 루프 변수도 `i` 대신 `pos` 같은 의미 있는 이름 추천
~~~python
num_words = int(input())
words = [input().rstrip() for _ in range(num_words)]
word_length = len(words[0])
~~~
<br><br><br>

### 3. 함수화 및 도큐스트링 추가  [중요도: Low] [효과: 가독/유지보수]
메인 로직을 함수로 빼면 테스트 및 재사용 용이.
~~~python
def find_pattern(words: list[str]) -> str:
    """
    여러 단어에서 공통 패턴을 찾아 반환.
    서로 다른 문자가 존재하면 '?'로 대체.

    Args:
        words (list[str]): 입력된 단어 리스트
    Returns:
        str: 공통 패턴 문자열
    """
    word_length = len(words[0])
    result_chars = []
    for pos in range(word_length):
        char = words[0][pos]
        for word in words[1:]:
            if word[pos] != char:
                result_chars.append('?')
                break
        else:
            result_chars.append(char)
    return ''.join(result_chars)
~~~
<br><br><br>

## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline


def find_pattern(words: list[str]) -> str:
    """
    여러 단어에서 공통 패턴을 찾아 반환.
    서로 다른 문자가 존재하면 '?'로 대체.
    """
    word_length = len(words[0])
    result_chars = []
    for pos in range(word_length):
        char = words[0][pos]
        for word in words[1:]:
            if word[pos] != char:
                result_chars.append('?')
                break
        else:
            result_chars.append(char)
    return ''.join(result_chars)


num_words = int(input())
words = [input().rstrip() for _ in range(num_words)]
print(find_pattern(words))
~~~
