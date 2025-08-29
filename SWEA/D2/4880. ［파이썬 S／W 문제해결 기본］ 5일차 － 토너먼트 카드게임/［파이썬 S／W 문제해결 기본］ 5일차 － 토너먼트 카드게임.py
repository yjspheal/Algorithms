# 4880. [파이썬 S/W 문제해결 기본] 5일차 - 토너먼트 카드게임
 
# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")


T = int(input())
for tc in range(1, T+1):
    N = int(input())
    # 가위바위보카드
    cards = list(map(int, input().split()))
    
    # dp[l][r]에 단순 승자가 아니라, [l, r] 구간에서 진행된 모든 매치의 승리 로그를 리스트로 저장
    dp = [[None]*(N+1) for _ in range(N+1)]
    
    # 길이 1 구간 -> 자기 자신이 ㅛㅡㅇ자
    for i in range(1, N+1):
        dp[i][i] = [i]   # 리스트에 학생 번호 하나만 저장

    # 길이 2부터 N까지 모든 구간 처리
    for length in range(2, N+1):
        for l in range(1, N-length+2):
            r = l + length - 1
            mid = (l + r)//2
            
            # 각 구간 계산
            left_log  = dp[l][mid]
            right_log = dp[mid+1][r]
            
            left_winner  = left_log[-1]   # 구간 [l, mid]의 마지막 승자
            right_winner = right_log[-1]  # 구간 [mid+1, r]의 마지막 승자
            
            lc = cards[left_winner-1]
            rc = cards[right_winner-1]
            
            # 가위바위보
            # 비겼다면
            if lc == rc:
                winner = left_winner if left_winner < right_winner else right_winner
            # 왼쪽이 이겼다면
            elif (lc == 1 and rc == 3) or (lc == 2 and rc == 1) or (lc == 3 and rc == 2):
                winner = left_winner
            else:
                winner = right_winner
            
            # 로그를 전부 이어 붙이고 마지막에 새 승자 추가
            dp[l][r] = left_log + right_log + [winner]
    
    # 최종 구간의 승자 로그
    final_log = dp[1][N]
    # 마지막에 기록된 값이 최종 우승자
    champion = final_log[-1]

    print(f"#{tc} {champion}")
