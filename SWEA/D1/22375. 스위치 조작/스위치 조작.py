# 22375_스위치조작. 스위치 조작 

T = int(input())

for tc in range(1, T + 1):
    N = int(input())  # 스위치 갯수

    start_lights = list(map(int, input().split()))  # 시작 전구 배열
    target_lights = list(map(int, input().split()))  # 목표 전구 배열

    switch_time = 0  # 지금까지 바뀐 횟수

    # 인덱스를 돌며
    for i in range(N):
        # 지금 전구 상태 = 시작 전구 상태 + 바꾼 횟수 를 2로 나눈 나머지(0 or 1이므로)
        c_light = (start_lights[i] + switch_time) % 2

        t_light = target_lights[i]  # 타겟 전구

        if c_light != t_light:  # 서로 다르면
            switch_time += 1  # 바꾼 횟수 + 1

    print(f'#{tc} {switch_time}')
