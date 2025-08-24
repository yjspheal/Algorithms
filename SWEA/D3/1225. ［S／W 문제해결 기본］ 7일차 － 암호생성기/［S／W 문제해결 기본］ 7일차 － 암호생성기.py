# 1225. [S/W 문제해결 기본] 7일차 - 암호생성기

from collections import deque

T = 10

for _ in range(1, T + 1):
    tc = int(input())
    arr = list(map(int, input().split()))
    dq = deque(arr)

    while True:
        # 1 ~ 5 감소가 한 사이클
        for i in range(1, 6):
            # 맨 앞 값을 ele변수로 뺌
            ele = dq.popleft()
            ele -= i    # i만큼 빼줘야 함
            if ele <= 0:    # 끝나는 시점
                dq.append(0)
                break
            else:
                dq.append(ele)
        else:   # break가 안 났다면 계속
            continue

        break   # break가 됐다면 아예 빠져나가도록


    print(f'#{tc}', *dq)
