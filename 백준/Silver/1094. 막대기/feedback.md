# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline

X = int(input().rstrip())

count = 0
# 어차피 2의 지수, 1 2 4 8 .. 이중에 필요한거 하나씩 골라서 만들게된다
for k in [64, 32, 16, 8 , 4, 2, 1]:
    if X >= k:
        X -= k
        count += 1

print(count)
~~~
<br><br>

## 총평
- 강점
  - 64→1로 내려가며 필요한 막대만 선택하는 그리디가 **이진표현의 1비트 개수와 동일**하다는 성질을 잘 이용했습니다.
  - 반복 횟수가 7번 고정 → 충분히 빠르고 안정적입니다.
- 개선 필요
  - `int(input())`는 개행/공백을 무시하므로 `.rstrip()`은 불필요.
  - 하드코딩한 리스트 대신, **비트 개수(popcount)**를 직접 세면 더 간단·명확합니다.
- 병목/리스크
  - 현재도 O(1)이지만, 목적이 “세트 비트 수”이므로 그에 맞는 구현이 **표현력과 가독성**을 높입니다.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 현재 구현 O(1) (항상 7회 비교).  
- 공간 복잡도: O(1).  
- 병목 지점: 없음. 다만 표현을 간결화하면 유지보수성이 좋아집니다.
<br><br>

## 보완점
### 1. 비트 개수로 직접 계산   [중요도: High] [효과: 가독/간결]
- **Reasoning:** 막대 수 = X의 이진수에서 1의 개수. Python 3.8+에선 `bin(x).count('1')`, 3.10+에선 `int.bit_count()` 사용 가능.
- **Conclusion:** 분기 없이 한 줄로 해결하거나, 커널리핸(브라이언 커니핸) 알고리즘으로도 O(세트비트수)로 계산 가능.

~~~python
# (가장 단순한 형태)
X = int(input())
print(bin(X).count('1'))
~~~

<br><br>

### 2. 입력 처리 단순화   [중요도: Low] [효과: 가독]
- **Reasoning:** `int(input())` 자체가 개행을 무시.
- **Conclusion:** `.rstrip()` 제거.

<br><br>

## 최종 코드 예시
~~~python
import sys
input = sys.stdin.readline

X = int(input())
# 막대기의 개수 = X의 이진 표현에서 1의 개수
# Python 3.10+라면: print(X.bit_count())
print(bin(X).count('1'))
~~~
