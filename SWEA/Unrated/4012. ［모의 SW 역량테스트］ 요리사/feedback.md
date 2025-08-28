# 피드백
## 작성 코드
~~~python
import itertools


def cal_ingredients_synergy(arr, comb):
    """
    식재료 시너지 정보가 들은 arr에 대해, comb에 들은 인덱스 번호(재료번호)에 따른 시너지 합을 계산하여 리턴하는 함수
    Args:
        arr (list): 숫자를 인자로 갖는 이차원 배열
        comb (list): 사용할 재료의 번호들
    Returns:
        int: 시너지합
    """

    synergy = 0
    # comb가 123이었다면 각 재료 두개씩 시너지를 확인해야하므로 12, 23, 13을 체크
    for i1, i2 in itertools.combinations(comb, 2):
        synergy += arr[i1][i2]
        synergy += arr[i2][i1]  # i1i2와 i2i1은 다르다

    return synergy


T = int(input())
for tc in range(1, T + 1):
    N = int(input())  # NxN행렬의 길이
    ingredients = [list(map(int, input().split())) for _ in range(N)]  # 재료 정보가 담긴 이차원 배열

    # 최초 최소합 초기화
    min_sub = abs(
        cal_ingredients_synergy(ingredients, list(range(N // 2))) - cal_ingredients_synergy(ingredients,
                                                                                            list(range(N // 2, N))))

    already_checked_combs = set()       # 이미 체크한 comb 확인용

    # 나머지 반절 조합을 계산하기 위한 리스트
    base_comb = list(range(N))

    # 절반을 조합하여 만들기
    for half_comb in itertools.combinations(range(N), N // 2):
        comb1 = half_comb
        if comb1 in already_checked_combs:      # 이미 봤던거라면, 즉 정반대 조합을 통해 체크했더라면
            continue

        comb2 = tuple([num for num in range(N) if num not in comb1])       # 0 ~ N-1 중 comb1에 안 들은 조합 계산

        synergy1 = cal_ingredients_synergy(ingredients, comb1)
        synergy2 = cal_ingredients_synergy(ingredients, comb2)

        # abs 안 쓰고 하려고 이렇게씀
        current_sub = synergy1 - synergy2 if synergy1 > synergy2 else synergy2 - synergy1

        # min_sub 업데이트
        if current_sub < min_sub:
            min_sub = current_sub

        # 이미 봤다는 확인용 set에 추가. comb1는 어차피 다시 돌아오지 않으므로 넣을 필요 없다
        already_checked_combs.add(tuple(comb2))

    print(f'#{tc} {min_sub}')
~~~
<br><br>

## 총평
- 강점
  - 팀 분할을 `C(N, N/2)`로 생성하고, 팀 내 모든 2쌍에 대해 시너지 합을 계산하는 직관적 풀이.
  - 함수 분리(`cal_ingredients_synergy`)로 문제 의도를 명확히 드러냄.
- 개선 필요
  - **중복 탐색**: `A`와 `B`가 서로 보완(complement)인데 둘 다 탐색(또는 Set으로 회피) → 생성·체크 비용이 큼.
  - **내부 비용**: 매 팀마다 `num not in comb1`로 보완 팀을 만들 때 O(N²) 비용(조합 길이×탐색).
  - **시너지 합 계산**: 매번 `arr[i][j] + arr[j][i]`를 더함 → 같은 쌍에 대해 2회 인덱싱 반복.
  - **가독성**: 미사용 변수(`base_comb`) 존재, 타입힌트/도큐스트링이 더해지면 유지보수 용이.
<br><br>

## 복잡도 및 병목
- 시간 복잡도(현재):
  - 조합 수 `C(N, N/2)`에 대해 팀당 시너지 계산 `O((N/2)^2)` × 2팀
  - 보완 팀 생성 시 `not in` 탐색으로 추가 `O(N^2)`까지 가중
  - 대략 `O(C(N, N/2) · N^2)` 수준
- 공간 복잡도: `O(N^2)`(입력), 기타 `O(1)` 보조 구조
- 병목 지점:
  1) 보완 팀 계산 시 선형 포함 검사
  2) 보완 조합까지 전부 생성/검사(대칭 중복)
  3) 시너지 합에서 2회 인덱싱 반복
<br><br>

## 보완점
### 1. 대칭 제거: “0번은 항상 A팀” 규약   [중요도: High] [효과: 성능/가독]
- **Reasoning:** A/B가 보완 관계이므로, **한쪽만** 탐색하면 됨.
- **방법:** 0번 재료를 A팀에 고정하고, 나머지 `N-1` 중에서 `N/2-1`개만 선택 → 조합 수가 **절반**으로 감소.
- **결론 코드:** `for team_a_rest in combinations(range(1,N), N//2-1)`.
<br><br>

### 2. 보완 팀 생성 O(N)로 단순화   [중요도: High] [효과: 성능]
- **Reasoning:** `if num not in comb1`은 튜플에 대한 선형 탐색(반복 시 O(N²)).
- **방법:** 불린 배열로 선택 표시 후 한 번의 선형 스캔으로 보완 팀 구성.
- **결론:** 팀 생성 비용을 `O(N)`으로 축소.
<br><br>

### 3. 시너지 합 사전 계산(대칭 합 S)   [중요도: Med] [효과: 성능]
- **Reasoning:** 모든 쌍에 대해 `S[i][j] = arr[i][j] + arr[j][i]`를 한 번만 계산해두면, 팀 시너지 합은 **`sum(S[i][j])`**(i<j)로 끝.
- **효과:** 인덱싱 절반/연산량 감소, 코드 명확성↑.
<br><br>

### 4. 함수화/타입힌트 및 불필요 코드 제거   [중요도: Low] [효과: 가독/유지보수]
- **Reasoning:** 테스트 용이성 및 의미 전달력 향상, 미사용 변수 제거.
- **결론:** 시너지 계산/보완팀 생성을 함수로 분리, 타입힌트·도큐스트링 추가.
<br><br>

## 최종 코드 예시
~~~python
import itertools
from typing import List, Iterable

def build_pair_synergy(a: List[List[int]]) -> List[List[int]]:
    """S[i][j] = a[i][j] + a[j][i] (i!=j), 대칭 합 테이블 생성."""
    n = len(a)
    S = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            s = a[i][j] + a[j][i]
            S[i][j] = S[j][i] = s
    return S

def team_synergy(team: Iterable[int], S: List[List[int]]) -> int:
    """팀 내 모든 2쌍에 대한 시너지 합(대칭 합 테이블 사용)."""
    total = 0
    # team을 튜플로 변환(조합에서 넘어올 때는 이미 튜플)
    t = tuple(team)
    for i in range(len(t)):
        ti = t[i]
        for j in range(i+1, len(t)):
            total += S[ti][t[j]]
    return total

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = [list(map(int, input().split())) for _ in range(N)]

    S = build_pair_synergy(A)

    # 0번을 A팀에 고정 → 나머지에서 N//2 - 1개 선택
    ans = float('inf')
    indices = list(range(N))

    for rest in itertools.combinations(range(1, N), N//2 - 1):
        teamA = (0,) + rest

        # 보완 팀(B) 구성: 불린 선택표로 O(N) 생성
        picked = [False]*N
        for x in teamA:
            picked[x] = True
        teamB = tuple(i for i in indices if not picked[i])

        sA = team_synergy(teamA, S)
        sB = team_synergy(teamB, S)

        diff = sA - sB if sA > sB else sB - sA
        if diff < ans:
            ans = diff

        # 최적 가능 하한 0 → 조기 종료
        if ans == 0:
            break

    print(f"#{tc} {ans}")
~~~
