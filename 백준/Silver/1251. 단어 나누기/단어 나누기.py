# 1251 단어 나누기

import sys

input = sys.stdin.readline

"""
단어를 3개로 쪼갠다
3개의 단어를 reverse한다
다시 붙인다
이런 단어 중에서 사전순으로 가장 앞서는 단어를 출력하는 프로그램을 만드시오

1. 인덱스 N-3까지 ord가 제일 작은 문자를 찾는다
2. 그걸로 뒤집는다
3. 인덱스 N-2까지...반복
"""


def find_earlist_char_idx(sentence, start_idx, end_idx):
    """
    sentence[start_idx: end_idx]에서, 가장 사전적으로 먼저 오는 문자의 인덱스를 반환한다.

    Args:
        sentence (char): 인자로 받을 문자열
        start_idx (int): sentence에서 인덱스 따질 범위 시작점
        end_idx (int): sentence에서 인덱스 따질 범위 끝점

    Returns:
        int: 사전적으로 제일 빠른 문자 인덱스
    """
    min_ord = ord(sentence[start_idx])
    min_idxs = []

    for i, char in enumerate(sentence):
        if start_idx <= i < end_idx:  # 범위에 들어와야 계산

            if ord(char) < min_ord:  # 최소값 갱신 시 update
                min_ord = ord(char)
                min_idxs = [i]

            elif ord(char) == min_ord:  # 똑같다면 추가
                min_idxs.append(i)

    return min_idxs


def is_earlier(arr1, arr2):
    """
    ord값 리스트 2개를 받아다가, 각 자리수별로 비교한 후
    arr2값이 arr1보다 작다면 True, 아니라면 False 반환

    Example:
        arr1 = [2, 4, 13, 42, 1]
        arr2 = [2, 4, 12, 44, 1]
        -> 12가 13보다 작으므로 return True
    """

    for i in range(len(arr1)):
        if arr2[i] < arr1[i]:   # 2가 더 작으면
            return True
        elif arr2[i] > arr1[i]:   # 2가 더 크면
            return False

    else:   # 모두 같았다면
        return False



def cal_ord(sentence):
    """
    sentence문자열을 돌며 각 ord값을 list형태로 반환
    """
    result = []
    for s in sentence:
        result.append(ord(s))

    return result


# 단어 입력
word = input().rstrip()
N = len(word)  # 단어 길이

ords = []

earlist_idxs = find_earlist_char_idx(word, 0, N - 2)
worst_char = 'z' * len(word)
min_ord = cal_ord(worst_char)     # 초기값은 최악 단어로.
result = worst_char

for flag1 in earlist_idxs:  # 일단 첫번쨰 flag는 최저값에서 찾아야함
    for flag2 in range(flag1 + 1, N - 1):  # 맨 마지막값은 빼야 단어길이 1 이상이 보장됨
        word1 = word[:(flag1 + 1)][::-1]  # 뒤집
        word2 = word[(flag1 + 1): (flag2 + 1)][::-1]
        word3 = word[(flag2 + 1):][::-1]

        new_word = word1 + word2 + word3
        new_word_ord = cal_ord(new_word)      # ord 배열 계산

        if is_earlier(min_ord, new_word_ord):       # new_word가 기존보다 더 빠르면
            min_ord = new_word_ord
            result = new_word

print(result)
