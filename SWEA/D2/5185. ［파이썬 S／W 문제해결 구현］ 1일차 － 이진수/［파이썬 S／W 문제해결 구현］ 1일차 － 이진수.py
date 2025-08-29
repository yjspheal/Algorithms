# 5185. [파이썬 S/W 문제해결 구현] 1일차 - 이진수
 
# import sys
# sys.stdin = open("input.txt", "r")
 
T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
def hexa_to_bi(hexa_digit):
    hexa_dict = {'A': 10,
                 'B': 11,
                 'C': 12,
                 'D': 13,
                 'E': 14,
                 'F': 15,
                 }


    try:        # 0 ~ 9면
        hexa_num = int(hexa_digit)
    except:     # 알파벳이면
        hexa_num = hexa_dict[hexa_digit]

    # 16진수는 2진수 4개로 바뀌므로 16 -> 2 다이렉트로 변환
    first_digit = hexa_num // 8
    hexa_num -= first_digit * 8


    second_digit = hexa_num // 4
    hexa_num -= second_digit * 4

    third_digit = hexa_num // 2
    hexa_num -= third_digit * 2

    fourth_digit = hexa_num // 1

    return str(first_digit) + str(second_digit) + str(third_digit) + str(fourth_digit)


for test_case in range(1, T + 1):
    digit_count, hexa_str = input().split()

    bi_str = ''
    for hx in hexa_str:
        bi_str += hexa_to_bi(hx)
    
    print(f'#{test_case} {bi_str}')


