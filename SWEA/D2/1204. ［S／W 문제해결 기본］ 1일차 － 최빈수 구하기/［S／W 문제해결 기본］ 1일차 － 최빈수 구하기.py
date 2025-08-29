# 1204. [S/W 문제해결 기본] 1일차 - 최빈수 구하기

# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    _ = int(input())

    arr = map(int, input().split())

    scores = [0] * 101  # 학생의 점수는 0점 이상 100점 이하의 값이다

    for num in arr:         # num점을 받은 학생 수를 scores에 업데이트
        scores[num] += 1

    mode_score_counts = max(scores) # 같은 점수를 받은 최대 학생수

    # 최대 학생수를 가진 점수 리스트를 저장
    mode_score_list = list(filter(lambda x: scores[x] == mode_score_counts, range(101)))
    
    # 그중 최대값을 결과값으로 print
    print(f'#{test_case} {max(mode_score_list)}')