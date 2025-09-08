# 5201. [파이썬 S/W 문제해결 구현] 3일차 - 컨테이너 운반

# import sys
# 
# sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    c_cnt, t_cnt = map(int, input().split())

    containers = [0]*51 # 용량 최대 50

    for c in map(int, input().split()):
        containers[c] += 1  # 해당 중량을 가진 컨테이너 갯수 +1

    max_weight = 0
    for t in map(int, input().split()): # 트럭을 돌며
        for i in range(t, 0, -1):   # 자기 용량에서 하나씩 줄여가며
            if containers[i]:   # 해당하는 무게의 컨테이너를 발견하면
                containers[i] -= 1  # 하나 적재
                max_weight += i     # 용량 계산산
                break


    print(f'#{tc} {max_weight}')
