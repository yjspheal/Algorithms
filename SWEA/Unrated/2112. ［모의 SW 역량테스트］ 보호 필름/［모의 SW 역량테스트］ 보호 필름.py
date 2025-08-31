# 2112. [모의 SW 역량테스트] 보호 필름

# import sys
# sys.stdin = open('input.txt')

def is_pass(arr):
    """
    t개의 row를 갖는 이차원배열 arr에 대해, 모든 열이 조건을 만족하는지 여부를 return
    조건: 각 열에 대해, 동일하게 연속되는 값이 pass_value개 이상

    Args:
        arr (list): 0 또는 1 값을 갖는 이차원배열

    Return:
        bool: 만족 여부
    """
    global pass_value, thickness

    for column in zip(*arr):  # 열을 돌며
        column = [0] + list(column)  # 맨 앞 값 추가
        res = False  # 일단 아니라고 가정
        for i in range(1, thickness + 1):  # 2번째 값부터 끝까지
            column[i] += column[i - 1]  # 이전까지의 합

            if i >= pass_value:  # 처음부터 합이 pv개가 될 수 있는 범위부터

                # check = [i, i-pv, column[i], column[i-pv]]
                if (
                        column[i - pass_value] == column[i]  # 값이 유지가 되고있다, 즉 모두 0이었다
                        or column[i - pass_value] + pass_value == column[i]  # 모두 1이었다
                ):
                    res = True  # 이번 열은 True
                    break  # 다음 열을 보자

        if res is False:  # 열을 다 돌았는데 False면
            return False  # 바로 False 리턴하고 끝

    return True  # False인 행이 없었던 것이므로 True리턴


def count_trans_film(row_idx, switch_count):
    """
    arr의 일부 행(최대 pv-1개)를 골라 해당 행을 모두 0 또는 1로 바꾸어 조건 충족 여부를 체크 후 바꾼 횟수를 반환하는 함수
    Args:
        row_idx (int): 이번에 바꿀 행 인덱스
        switch_count (int): 현재까지 바꾼 행 수
    Returns:
        int: 바꾼 행 수
    """
    global films, thickness, width, pass_value, result
    arr = films

    if switch_count >= result:      # 지금까지의 최소변경횟수를 넘었다면 끝
        return

    if row_idx == thickness:     # 마지막행까지 체크 완
        if is_pass(arr):    #  통과했다면
            result = min(result, switch_count)  # 조건 만족 시 바꾼 행 수 return
        return result


    origin_row = arr[row_idx][:]  # 원본 유지를 위해 이번 행 복사해둠

    count_trans_film(row_idx + 1, switch_count)    # 일단 약 없이 다음 행 돌리기

    arr[row_idx] = [0] * width      # 실패했다면 다 A로 채우기
    count_trans_film(row_idx + 1, switch_count + 1)    # 약 횟수 + 1


    arr[row_idx] = [1] * width  # 그래도 실패했다면 다 B로 채우기
    count_trans_film(row_idx + 1, switch_count + 1)  # 약 횟수 + 1

    arr[row_idx] = origin_row   # 그래도 실패했다면 다시 원본으로 둘려두기
 
T = int(input())
for tc in range(1, T + 1):
    # 필름의 두께, 가로크기, 합격점
    thickness, width, pass_value = map(int, input().split())
    films = [list(map(int, input().split())) for _ in range(thickness)]  # 필름 정보 담는 이차원배열

    result = pass_value     # 커봐야 pass_value임.
    count_trans_film(0 , 0)

    print(f'#{tc} {result}')
