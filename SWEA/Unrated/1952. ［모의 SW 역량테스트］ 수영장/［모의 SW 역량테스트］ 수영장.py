# 1952. [모의 SW 역량테스트] 수영장

# import sys
# 
# sys.stdin = open('sample_input.txt')

T = int(input())
for tc in range(1, T + 1):
    # 일 월 3개월 1년권 가격
    price_d, price_m, price_3m, price_y = map(int, input().split())

    next_year = [0] + list(map(int, input().split()))  # 인덱스 맞추기용

    for i in range(len(next_year)):  # 내년 계획을 돌며

        if next_year[i] * price_d > price_m:  # 다 일일권으로 다니는거보다 월간권이 싸면
            next_year[i] = price_m  # 월간권으로 바꿔둔다
        else:
            next_year[i] *= price_d  # 아니면 일일권으로 계산한 가격을 둔다

    min_cost = sum(next_year)  # 최소값으로 저장

    # 3개월권 쓰는 월 구해보기
    tri_plans = []
    for month in range(1, 13):  # 12월까지 1번 산다면
        tri_plans.append([month])

        for month2 in range(month + 3, 13):  # 2번 산다면
            tri_plans.append([month, month2])

            for month3 in range(month2 + 3, 13):  # 3번 산다면
                tri_plans.append([month, month2, month3])

                for month4 in range(month3 + 3, 13):  # 4번 산다면
                    tri_plans.append([month, month2, month3, month4])



    # 다시 내년 계획을 돌며
    for tri_plan in tri_plans:
        cost = 0  # 현재 비용 0

        m = 1  # 이번 달
        while m <= 12:
            if m in tri_plan:  # 3개월권 구매달이면
                cost += price_3m  # 구매하고 3개월 흐름
                m += 3
            else:
                cost += next_year[m]  # 구매 안하면 걍 기존값
                m += 1  # 다음달로

            if cost > min_cost:  # 이미 최소값을 넘어섰다면
                break  # 끝

        if cost < min_cost:  # 최소값보다싸다면 update
            min_cost = cost

    # 3개월권 구매값보다 연간권이 싸다면 update
    if min_cost > price_y:
        min_cost = price_y

    print(f'#{tc} {min_cost}')
