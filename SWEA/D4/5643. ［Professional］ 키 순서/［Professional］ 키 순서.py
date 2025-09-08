# 5643. [Professional] 키 순서

# import sys
# 
# sys.stdin = open('input.txt')


def find_small_location(curr_num):
    """
    학생 번호를 인자로 받아, 해당 학생보다 작은 학생 수를 찾아감
    """
    ### 1. 나보다 작은 애들
    if height_info[curr_num][0]:  # 이미 계산해둔 게 있으면 그거 ㄱㄱ
        return height_info[curr_num][0]

    else:  # 이미 계산해둔 게 없을 땐 계싼
        if not small_adj_list[curr_num]:  # 나보다 더 큰 애가 없다면
            return set()

        # 나보다 크다고 주어졌던 애들을 돌며, 나보다 큰 모든 애들을 찾아간다.
        small_stds = set()  # 나보다 큰 애들 수 저장
        for small_std in small_adj_list[curr_num]:
            small_stds.add(small_std)     # 해당 학생 집어넣고
            small_stds  = small_stds.union(find_small_location(small_std))  # 나보다 큰 애들 '보다 큰 애들 보다 ...'을 계산하여 더함
        height_info[curr_num][0] = small_stds
        return small_stds


def find_tall_location(curr_num):
    """
    학생 번호를 인자로 받아, 해당 학생보다 큰 학생 수를 찾아감
    """
    ### 2. 나보다 큰애들

    if height_info[curr_num][1]:  # 이미 계산해둔 게 있으면 그거 ㄱㄱ
        return height_info[curr_num][1]

    else:  # 이미 계산해둔 게 없을 땐 계싼
        if not tall_adj_list[curr_num]:  # 나보다 더 큰 애가 없다면
            return set()

        # 나보다 크다고 주어졌던 애들을 돌며, 나보다 큰 모든 애들을 찾아간다.
        tall_stds = set()  # 나보다 큰 애들 수 저장
        for tall_std in tall_adj_list[curr_num]:
            tall_stds.add(tall_std)     # 해당 학생 집어넣고
            tall_stds  = tall_stds.union(find_tall_location(tall_std))  # 나보다 큰 애들 '보다 큰 애들 보다 ...'을 계산하여 더함
        height_info[curr_num][1] = tall_stds
        return tall_stds



T = int(input())
for tc in range(1, T + 1):
    s_cnt = int(input())  # 학생 수
    M = int(input())  # 키 비교 횟수

    small_adj_list = [[] for _ in range(M + 1)]  # 나보다 작다고 한 애들 저장
    tall_adj_list = [[] for _ in range(M + 1)]  # 나보다 크다고 한 애들 저장

    for _ in range(M):
        s1, s2 = map(int, input().split())  # s1 < s2

        small_adj_list[s2].append(s1)  # s1이 s2보다 작으므로
        tall_adj_list[s1].append(s2)  # s2가 s1보다 크므로

    height_info = [[set(), set()] for _ in range(M + 1)]  # height_info[i] = [i보다 작은 학생 수, i보다 큰 학생 수]

    for s in range(1, s_cnt + 1):   # 모든 학생들을 돌며
        find_small_location(s)
        find_tall_location(s)

    located_cnt = 0  # 제 자리 찾은 애들 수
    for sm, tl in height_info[1:]:
        sm_cnt = len(sm)
        tl_cnt = len(tl)
        # if sm is None or tl is None:  # None이 남아있다면, 동떨어진 학생이 있다는 것 -> 아무도 자기 순서 모름
        #     break
        if sm_cnt + 1 + tl_cnt == s_cnt:  # 작은 애들 + 나 +  큰 애들 == 전체 학생 수라면 자리 찾은 것
            located_cnt += 1

    print(f'#{tc} {located_cnt}')
