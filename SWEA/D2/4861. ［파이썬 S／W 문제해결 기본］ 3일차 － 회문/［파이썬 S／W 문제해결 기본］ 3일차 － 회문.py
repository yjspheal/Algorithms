# 4861. [파이썬 S/W 문제해결 기본] 3일차 - 회문

def is_palindrome(s):
    """
    주어진 s 문자열이 회문인지 판단하는 함수
    Args:
        s (str): 문자열
    Returns:
        boolean: 회문 여부를 나타내는 불리언값(회문 = True)
    """
    s_len = len(s)  # 문자열 길이
    check_idx = s_len // 2  # 앞뒤가 똑같은지 체크가 필요

    # s의 앞부분 == 역방향 s의 앞부분인지 확인
    if s[:check_idx] == s[::-1][:check_idx]:
        return True
    else:
        return False


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    # NxN개의 문자열 matrix에서 길이 M의 회문 찾기
    # 회문은 무조건 존재함을 전제로 함
    size, target_length = map(int, input().split())  # matrix 행열 길이와 회문 대상 문자열 길이 input

    # 문자열을 담아둘 리스트 생성
    chars_list = []
    for time in range(size):
        # 문자열은 iterable이므로 그대로 append
        chars_list.append(input())

    # 세로로 있는 경우도 체크 필요하므로 transpose하여 list에 담아둠
    reversed_chars = zip(*chars_list)
    # join하지 않으면 한 자씩 떨어져있으므로 join해야함
    reversed_chars = list(map(''.join, reversed_chars))

    # 기존 list에 transpose한 문자열 추가
    chars_list += reversed_chars

    palindrome_string = ''  # 결과물 return을 위한 빈 문자열 생성
    has_palindrome = False  # 이중반복문을 돌아야하므로 계산 효울을 위해 boolean값 할당

    # 첫번째 행부터 회문 존재하는지 체크
    for chars in chars_list:
        if has_palindrome:  # 회문을 이미 찾았다면 break
            break
        # 연속된 target개의 문자열에 대해서 체크가 필요
        for i in range(len(chars) - target_length + 1):
            # 해당 부분의 문자열이 회문이라면
            current_chars = chars[i:(i + target_length)]
            if is_palindrome(current_chars):
                palindrome_string = current_chars  # 회문 업데이트
                has_palindrome = True  # 찾았다는 표시
                break

    print(f'#{test_case} {palindrome_string}')
