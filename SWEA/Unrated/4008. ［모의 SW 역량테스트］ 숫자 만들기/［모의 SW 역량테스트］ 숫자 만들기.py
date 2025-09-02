# 4008. [모의 SW 역량테스트] 숫자 만들기

# import sys
import math

# sys.stdin = open('input.txt')

def dfs(cal_num, curr_num_idx, operator_list, num_list):
    """
    cal_num과, curr_num_idx번째 숫자 사이에 op_idx에 해당하는 연산자를 넣어 계산을 반복
    """
    global max_num, min_num

    if curr_num_idx == N:    # 마지막 숫자까지 했다면
        max_num = max(max_num, cal_num)     # 업데이트 후 리턴
        min_num = min(min_num, cal_num)
        return

    for i in range(4):
        if operator_list[i] >= 1:   # 해당 연산자가 한개 이상 있다면
            operator_list[i] -= 1   # 갯수 -1

            # 계산
            if i == 0:
                new_cal_num = cal_num + num_list[curr_num_idx]
            elif i == 1:
                new_cal_num = cal_num - num_list[curr_num_idx]
            elif i == 2:
                new_cal_num = cal_num * num_list[curr_num_idx]
            else:
                # if num_list[curr_num_idx] == 0: # zero division error 방지
                #     return
                new_cal_num = math.trunc(cal_num / num_list[curr_num_idx])

            dfs(new_cal_num, curr_num_idx + 1, operator_list, num_list)

            operator_list[i] += 1   # 안쓸거면 다시 돌리기



T = int(input())
for tc in range(1, T + 1):
    N = int(input())    # 숫자의 갯수
    operators = list(map(int, input().split()))     # 연산자 수. + - * / 순
    nums = list(map(int, input().split()))      # 수식에 사용되는 숫자들

    max_num = -float('inf')     # 최대, 최소값 정의
    min_num = float('inf')

    dfs(nums[0], 1, operators, nums)

    print(f'#{tc} {max_num - min_num}')
