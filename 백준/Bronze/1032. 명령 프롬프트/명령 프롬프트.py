import sys
input = sys.stdin.readline

T = int(input())
# 단어를 리스트로 받아옴
words = [input().rstrip() for tc in range(T)]

# 단어의 길이
N = len(words[0])

result = ''
for i in range(N):
    # 첫번째 단어와 같은지를 기준으로
    char = words[0][i]
    for word in words[1:]:
        if word[i] != char:
            result += '?'
            break
    else:
        result += char

print(result)