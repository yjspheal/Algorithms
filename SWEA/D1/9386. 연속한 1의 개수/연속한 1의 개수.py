# 9386. 연속한 1의 개수
 
T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    """
    연속한 1의 갯수 중 최대값을 출력하는 프로그램
    """

    # 수열의 길이 N
    N = int(input())

    # binary로 이루어진 수열
    str_bin = input()

    max_ones = 0
    current_ones = 0
    # str_bin을 순회하며
    for i in range(N):
        num = int(str_bin[i])   # 현재 숫자

        # num이 1이면 current_ones에 1 더함
        if num:
            current_ones += 1
            if current_ones > max_ones:     # 만약 current_ones가 max를 넘기면 업데이트
                max_ones = current_ones
        else:   # num이 0이면 연속이 끊긴 것이므로 current_ones를 0으로 초기화
            current_ones = 0

    print(f'#{tc} {max_ones}')