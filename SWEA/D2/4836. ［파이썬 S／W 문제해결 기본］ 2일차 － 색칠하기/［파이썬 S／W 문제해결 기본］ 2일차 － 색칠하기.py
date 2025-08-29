# 4836. [파이썬 S/W 문제해결 기본] 2일차 - 색칠하기

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    coloring_area = [[0]*10 for _ in range(10)]      # 색칠 구역
    purple_count = 0     # 보라영역 갯수 초기화


    for _ in range(int(input())):   # 2번쨰 input값 = 색칠 횟수

        # 왼쪽 위 모서리 인덱스 r1, c1, 오른쪽 아래 모서리 r2, c2와 색상 정보 color
        r1, c1, r2, c2, color = map(int, input().split())       

        # 모든 좌표를 돌며 coloring_area에 색을 칠함 
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1):
                # color = 1 -> 빨강, 2 -> 파랑
                if coloring_area[i][j] == color:    # 이미 동일한 색이 칠해져있었다면
                    pass
                else:
                    coloring_area[i][j] += color    # 아니면 + color

                    if coloring_area[i][j] == 3:    # 이 순간 더해서 3이 됐다면
                        purple_count += 1           # 보라 영역 갯수 + 1
                    
    print(f'#{test_case} {purple_count}')