# 피드백
## 작성 코드
~~~python
# 17281. 야구공

import sys
import itertools

input = sys.stdin.readline

N = int(input())
baseballs = [list(map(int, input().split())) for _ in range(N)]
GAME_PLAYER = 9


def play_baseball(arr, s_player):
    """
    이번 이닝의 각 선수별 점수를 인자로 받아, start_player 부터 시작했을 때 점수와 다음 시작 player 를 return
    """
    global score

    base_status = 0
    out_count = 0
    c_player = s_player

    while out_count < 3:
        hit = arr[c_player]
        if hit == 0:
            out_count += 1
        else:
            score += 1
            base_status = (base_status << 1) | 1
            base_status <<= (hit - 1)
            base_status &= 0b111
        c_player = (c_player + 1) % GAME_PLAYER

    non_home = bin(base_status).count('1')
    score -= non_home
    return c_player % GAME_PLAYER


max_score = 0
perms = itertools.permutations(range(2, 10))
for perm in perms:
    player_perm = list(perm[:3]) + [1] + list(perm[3:])
    current_player = 0
    score = 0
    for inning in baseballs:
        current_inning_hits = [inning[p - 1] for p in player_perm]
        current_player = play_baseball(current_inning_hits, current_player)
    max_score = score if score > max_score else max_score

print(max_score)
~~~
<br><br>

## 총평
- 순열(8!) × 시뮬레이션 구조가 문제 의도에 부합합니다.
- 주자 관리를 비트마스크로 표현한 점은 좋으나, **득점 로직이 “가산 후 정산”** 방식이라 오류 위험과 불필요 연산이 있습니다.
- `global score`와 `bin(...).count('1')`(문자열 변환)는 각각 **안정성/성능** 측면에서 개선 필요.
<br><br>

## 복잡도 및 병목
- 시간 복잡도: 전체 대략 O(8! · N · 9) (N≤50). 파이썬에서도 충분히 가능.
- 공간 복잡도: O(N·9) 입력 저장, 이외 O(1).
- 병목 지점:
  - `bin(...).count('1')`: 매 타석 문자열 생성 → 불필요한 할당 비용.
  - 전역 변수 갱신: 함수 재사용/테스트가 어려워짐.
<br><br>

## 보완점
### 1. 전역 제거 + 즉시 득점(popcount, PyPy 호환)  [중요도: High] [효과: 정확성/안정성/성능]
- 타구 처리 시 `(base_status << hit) | (1 << (hit-1))`로 **주자 이동 + 타자 배치**를 한 번에.
- 넘어간 비트 수(=득점자 수)를 **popcount**로 즉시 더하고, `&= 0b111`로 1~3루만 보존.
- **주의:** PyPy3이므로 `int.bit_count()` 사용 금지 → **커니핸 루프**로 구현.

~~~python
def popcount(x: int) -> int:
    cnt = 0
    while x:
        x &= x - 1
        cnt += 1
    return cnt
~~~

<br><br><br>

### 2. 함수 분리로 가독성 향상  [중요도: Med] [효과: 가독/유지보수]
- `play_inning`(이닝 시뮬레이션)과 `simulate_game`(전체 경기)을 분리하면 테스트와 디버깅이 쉬워집니다.
- 메인 루프에서는 `max_score = max(max_score, score)`로 간단화.
<br><br><br>

## 최종 코드 예시
~~~python
import sys
import itertools

input = sys.stdin.readline

N = int(input())
baseballs = [list(map(int, input().split())) for _ in range(N)]
GAME_PLAYER = 9


def popcount(x: int) -> int:
    """PyPy3 호환 popcount (문자열 변환/bit_count 사용 안 함)."""
    cnt = 0
    while x:
        x &= x - 1
        cnt += 1
    return cnt


def play_inning(hits, start_player):
    """
    base_status 비트 정의(하위 3비트만 유지):
      - bit0: 1루, bit1: 2루, bit2: 3루
    타구 처리:
      - 이동+타자 배치: base_status = (base_status << hit) | (1 << (hit - 1))
      - 득점: popcount(base_status >> 3)
      - 1~3루 보존: base_status &= 0b111
    """
    base_status = 0
    out_count = 0
    c_player = start_player
    inning_score = 0

    while out_count < 3:
        hit = hits[c_player]
        if hit == 0:
            out_count += 1
        else:
            base_status = (base_status << hit) | (1 << (hit - 1))
            inning_score += popcount(base_status >> 3)
            base_status &= 0b111
        c_player = (c_player + 1) % GAME_PLAYER

    return c_player, inning_score


def simulate_game(order):
    score = 0
    current_player = 0
    for inning in baseballs:
        # 타순에 맞춘 이번 이닝 타격 결과
        hits = [inning[p - 1] for p in order]
        current_player, inning_score = play_inning(hits, current_player)
        score += inning_score
    return score


max_score = 0
for perm in itertools.permutations(range(2, 10)):  # 2~9
    order = list(perm[:3]) + [1] + list(perm[3:])  # 1번은 4번 타자 고정
    max_score = max(max_score, simulate_game(order))

print(max_score)
~~~
