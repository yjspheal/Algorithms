# 5186. [파이썬 S/W 문제해결 구현] 1일차 - 이진수2
 

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = float(input())
    bi_num = ''
    for exponent in range(-1, -13, -1):
        if N >= 2 ** exponent:
            N -= 2 ** exponent
            bi_num += '1'
        elif N == 0:
            break
        else:
            bi_num += '0'
    # bi_num = int(bi_num)

    if N > 0:
        bi_num = 'overflow'
    
    print(f'#{test_case} {bi_num}')