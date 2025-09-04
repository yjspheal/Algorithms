# 1244. [S/W 문제해결 응용] 2일차 - 최대 상금

# import sys
#
# sys.stdin = open('input.txt')

def trans(num_list):
    """
    리스트가 들어오면, 한번 바꿔서 될 수 있는 최대치로 바꾸어 return한다.
    *최대치: 앞에서부터 붙였을 때 가장 큰 수가 되도록

    Args:
        arr: 1~9 정수로 이루어진 일차원 리스트

    Returns:
        list: 바뀐 일차원 리스트
    """

    global transed_idxs
    is_same = False

    for i in range(len(num_list)-1): # 마지막에서 두번째자리까지
        max_after_char = '0'  # 아래 j(num_str[j] 중 max값)
        max_j = 0  # 아래 j(num_str[j] 중 max값)

        for j in range(i+1, len(num_list)):
            # max값 업데이트
            if num_list[j] >= max_after_char:
                max_j = j
                max_after_char = num_list[j]

        if num_list[i] < num_list[max_j]:     # 지금 제일 앞자리 애가 다음에있는 수보다 작으면
            if i in transed_idxs:    # i가 이미 바뀐 리스트에 있었다면
                del transed_idxs[transed_idxs.index(i)]   # i라는 값을 지운다..

            num_list[i], num_list[max_j] = num_list[max_j], num_list[i] # 자리 바꾸기
            transed_idxs.append(max_j)   # 바꼈다는 체크

            return num_list

        if num_list[i] == num_list[max_j]:     # 지금 제일 앞자리 애가 다음에있는 수와 같다면
            is_same = True



    # 다 돌아도 return이 안 됐으면 제일 영향 없도록 바꾸기
    if is_same: # 만약 똑같은 게 있었다
        return num_list

    else:   # 똑같은 것도 없으면 걍 마지막 2개 바꾸기
        num_list[-1], num_list[-2] = num_list[-2], num_list[-1]
        return num_list

T = int(input())
for tc in range(1, T + 1):
    num, trans_count = input().split()  # 문자형으로 받기
    trans_count= int(trans_count)
    nums = list(num)
    nums_copy = nums[:]


    transed_idxs = []        # 바뀐 인덱스 담을 리스트

    for _ in range(trans_count):
        nums_copy = trans(nums_copy)


    # 만약 바뀐 애들 중에 기존 위치에 값 똑같은 애들 있다면
    for n in range(1, 10):
        same_nums = []  # 현재 값
        same_tis = []   # 현재 인덱스

        for ti in transed_idxs:
            a = nums[ti]
            if nums[ti] == str(n):
                same_nums.append(nums_copy[ti])    # 리스트에 인덱스 추가
                same_tis.append(ti)

        same_nums.sort(reverse= True)   # 값은 내림차순 정렬
        same_tis.sort()     # 인덱스는 오름차순

        for idx, ti in enumerate(same_tis):
            nums_copy[ti] = same_nums[idx]



    result = ''.join(nums_copy)
    print(f'#{tc} {result}')
