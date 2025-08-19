# 1860. 진기의 최고급 붕어빵

# import sys
# sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M, K = map(int, input().split())     # N명의 손님, M초마다 K개의 붕어빵 생성
    visitor_list = [0] * 11112      # 각 초에 손님이 몇명 오는지 저장할 리스트. 초는 11111 이하이다.
    latest_time = 0     # 젤 늦게 오는 손님 초 저장할 변수

    for visit_time in map(int, input().split()):    # 인풋받은 걸 하나씩 순회하며
        visitor_list[visit_time] += 1       # 해당 시간에 손님이 한명 왔다

        if visit_time > latest_time:        # 젤 늦은 시간 update
            latest_time = visit_time

    current_boong = 0   # 현재 붕어빵 재고

    result = 'Possible' # 붕어빵 제공 가능 여부
    # 각 초별로 붕어빵 재고 파악
    for i in range(latest_time + 1):    # 제일 늦게오는 사람 초까지만 보면 됨
        if i > 0 and i % M == 0:      # M초마다 붕어빵 K개 생성
            current_boong += K

        current_boong -= visitor_list[i]    # 지금 온 손님에게 하나씩 주기
        if current_boong < 0:       # 붕어빵 재고보다 더 줘야되는 상황이었으면
            result = 'Impossible'       # 불가능

    print(f'#{tc} {result}')