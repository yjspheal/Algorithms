# 4874. [파이썬 S/W 문제해결 기본] 5일차 - Forth

def calculate_forth(numerics):
    """
    후위표기법 식을 계산하여 값을 return하는 함수
    """
    # Forth 계산을 위한 stack 초기화
    stack = []
    # results = []    # 값이 여러개라면
    for element in numerics:
        if element.isdecimal():  # element가 숫자라면 stack에 추가
            stack.append(int(element))

        elif element in operators:  # element가 연산자라면
            try:
                num2 = stack.pop()  # 마지막서 두개를 변수로 할당
                num1 = stack.pop()  # 마지막서 두개를 변수로 할당

                # result = eval(f'{num1} {element} {num2}')        # 문자열 계산식을 계산해주는 함수
                # 온라인 저지에서 eval 사용 불가능하므로 직접 사칙연산으로 대체

                if element == '+':
                    _ = num1 + num2

                elif element == '-':
                    _ = num1 - num2

                elif element == '*':
                    _ = num1 * num2

                else:
                    _ = num1 // num2  # 문제 조건: 나눗셈은 항상 나누어떨어진다.

                stack.append(_)

            # 에러 나는 경우 ex) operator가 들어왔는데 stack에 숫자 2개가 없다 등
            except:
                return 'error'

        elif element == '.':  # ‘.’은 스택에서 숫자를 꺼내 출력한다.
            if len(stack) != 1:
                return 'error'
            else:
                return stack[0]

            # try:
            #     results.append(str(stack.pop()))
            #     # .이 여러번 나올 수 있으므로 바로 return하지 않음
            # except:
            #     return 'error'

        else:  # 위 경우가 아닌 값이 들어왔다면 에러 return
            return 'error'

    return 'error'  # 다 끝났는데 result가 없으면 error


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.


for test_case in range(1, T + 1):
    # 숫자나 연산자들이 들어옴.
    numbers = list(input().split())

    # 사칙연산자들
    operators = '+-*/'

    print(f'#{test_case} {calculate_forth(numbers)}')
