# 1989_초심자의회문검사
 

T = int(input())    # 테케 갯수 입력
for tc in range(1, T+1):
    sentence = input()  # 문자열 입력

    if sentence == sentence[::-1]:   # 뒤집은 것이 원본과 똑같다면
        is_palindrome = 1           # 회문임
    else:
        is_palindrome = 0           # 다르다면 회문 아님

    print(f"#{tc} {is_palindrome}")