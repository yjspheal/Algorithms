# 피드백
## 작성 코드
~~~python
import sys
input = sys.stdin.readline
import itertools

def cal_players_synergy(arr, comb):
    """
    선수간 시너지 정보가 들은 arr에 대해, comb에 들은 인덱스 번호(재료번호)에 따른 시너지 합을 계산하여 리턴하는 함수
    Args:
        arr (list): 숫자를 인자로 갖는 이차원 배열
        comb (tuple): 사용할 재료의 번호들
    Returns:
        int: 시너지합
    """

    synergy = 0
    # comb가 123이었다면 각 재료 두개씩 시너지를 확인해야하므로 12, 23, 13을 체크
    for i1, i2 in itertools.combinations(comb, 2):
        synergy += arr[i1][i2]
        synergy += arr[i2][i1]  # i1i2와 i2i1은 다르다

    return synergy



N = int(input())  # NxN행렬의 길이
players = [list(map(int, input().rstrip().split())) for _ in range(N)]  # 선수 정보가 담긴 이차원 배열

# 최초 최소합 초기화
min_sub = float('inf')
already_checked_combs = set()       # 이미 체크한 comb 확인용

# 나머지 반절 조합을 계산하기 위한 리스트
base_comb = list(range(N))

# 절반을 조합하여 만들기
for half_comb in itertools.combinations(range(N), N // 2):
    comb1 = half_comb
    if comb1 in already_checked_combs:      # 이미 봤던거라면, 즉 정반대 조합을 통해 체크했더라면
        continue

    comb2 = tuple([num for num in range(N) if num not in comb1])       # 0 ~ N-1 중 comb1에 안 들은 조합 계산

    synergy1 = cal_players_synergy(players, comb1)
    synergy2 = cal_players_synergy(players, comb2)

    # abs 안 쓰고 하려고 이렇게씀
    current_sub = synergy1 - synergy2 if synergy1 > synergy2 else synergy2 - synergy1

    # min_sub 업데이트
    if current_sub < min_sub:
        min_sub = current_sub

    # 이미 봤다는 확인용 set에 추가. comb1는 어차피 다시 돌아오지 않으므로 넣을 필요 없다
    already_checked_combs.add(tuple(comb2))

print(min_sub)
~~~
<br><br>

## 총평
- 강점
  - 양 팀으로 N을 절반 분할하고, 팀 내 모든 2쌍의 시너지를 합산해 차이의 최솟값을 찾는 접근이 문제 의도에 부합합니다.
  - 팀 시너지 계산을 별도 함수로 분리해 구조가 명확합니다.
- 개선 필요
  - **대칭 중복 탐색**: (팀 A, 팀 B)와 (팀 B, 팀 A)를 모두 보게 되어 불필요한 조합/검사가 발생합니다(집합으로 일부 회피하지만 조합 생성·보완팀 계산 비용은 여전).
  - **보완 팀 생성 비용**: `tuple([num for num in range(N) if num not in comb1])`는 매번 `not in` 선형 탐색 → **O(N^2)** 추가 오버헤드.
  - **시너지 합 중복 인덱싱**: `arr[i][j] + arr[j][i]`를 항상 두 번 조회 → **대칭 합 테이블**로 일회 전처리하면 계산량과 코드가 줄어듭니다.
  - 도큐스트링에 ‘재료’ 표현 등 도메인 용어 불일치, 타입힌트/주석 보강 여지.
- 병목/리스크
  - 시간 복잡도는 대략 `O(C(N, N/2) · N^2)` 수준(팀 합산 두 번). N ≤ 20에서 파이썬도 통과 가능하지만, 상수 비용을 줄이면 여유가 커집니다.

<br><br>

## 복잡도 및 병목
- 현재 구현:
  - 시간: 조합 수 `C(N, N/2)` × 팀 시너지 합산 `O((N/2)^2)` × 2팀 + 보완팀 생성(최대 O(N^2)) ≈ **O(C(N, N/2) · N^2)**.
  - 공간: 입력 `O(N^2)` + 보조 구조 소량.
- 병목 지점:
  1) 보완팀 생성의 선형 탐색 반복
  2) 대칭 중복 조합 탐색
  3) 시너지 인덱싱 2회 반복

<br><br>

## 보완점
### 1. 대칭 제거: 0번 선수를 항상 A팀에 고정   [중요도: High] [효과: 성능/가독]
- **Reasoning:** (A,B)와 (B,A)는 동일. 0번을 A팀에 고정하면 조합 수를 절반으로 줄입니다.
- **Conclusion:** `for teamA_rest in combinations(range(1, N), N//2 - 1)`로 순회.

### 2. 대칭 합 테이블 S 전처리   [중요도: Med] [효과: 성능/가독]
- **Reasoning:** `S[i][j] = A[i][j] + A[j][i]`를 미리 만들면 팀 시너지는 `sum(S[i][j]) (i<j)` 한 번으로 끝납니다.
- **Conclusion:** 인덱싱 절반, 코드 단순화.

### 3. 보완 팀 생성 O(N)으로 단순화   [중요도: Med] [효과: 성능]
- **Reasoning:** 불린 배열로 선택표를 만들면 한 번의 선형 스캔으로 보완 팀을 만들 수 있습니다(또는 간단히 리스트 내포로도 O(N) 보장).
- **Conclusion:** `picked = [False]*N; for x in teamA: picked[x]=True; teamB = [i for i in range(N) if not picked[i]]`.

### 4. 조기 종료(최적 하한 = 0)   [중요도: Low] [효과: 성능]
- **Reasoning:** 차이가 0이면 더 나은 답이 없으므로 즉시 종료 가능.
- **Conclusion:** `if ans == 0: break`.

### 5. 도큐스트링/타입힌트 정정   [중요도: Low] [효과: 가독/유지보수]
- **Reasoning:** ‘재료’ → ‘선수’로 용어 통일, 타입 명시.

<br><br>

## 최종 코드 예시
~~~python
import sys
import itertools
from typing import List, Iterable

input = sys.stdin.readline

def build_pair_synergy(a: List[List[int]]) -> List[List[int]]:
    """S[i][j] = a[i][j] + a[j][i] (i != j) 대칭 합 테이블."""
    n = len(a)
    S = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            s = a[i][j] + a[j][i]
            S[i][j] = S[j][i] = s
    return S

def team_synergy(team: Iterable[int], S: List[List[int]]) -> int:
    """팀 내 모든 2쌍(i<j)의 대칭 시너지 합."""
    t = tuple(team)
    total = 0
    for i in range(len(t)):
        ti = t[i]
        row = S[ti]
        for j in range(i+1, len(t)):
            total += row[t[j]]
    return total

N = int(input())
A = [list(map(int, input().split())) for _ in range(N)]
S = build_pair_synergy(A)

ans = float('inf')
indices = list(range(N))

# 0번을 A팀에 고정 → 나머지에서 N//2 - 1개 선택
for rest in itertools.combinations(range(1, N), N//2 - 1):
    teamA = (0,) + rest

    # 보완 팀(B)을 O(N)으로 생성
    picked = [False] * N
    for x in teamA:
        picked[x] = True
    teamB = tuple(i for i in indices if not picked[i])

    sA = team_synergy(teamA, S)
    sB = team_synergy(teamB, S)

    diff = sA - sB if sA >= sB else sB - sA
    if diff < ans:
        ans = diff
        if ans == 0:  # 조기 종료 (최적 하한)
            break

print(ans)
~~~
