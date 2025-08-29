# 4875. [파이썬 S/W 문제해결 기본] 5일차 - 미로

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")


 
def where_to_go(now_point):
    """
    현재 point를 기준으로, 이동할 수 있는 point를 계산하여 return하는 함수

    Args:
        now_point (tuple): 현재 위치의 좌표

    Returns:
        List: 이동할 수 있는 좌표들의 list
        ex)
        [(0, 1), (1, 2)]
    """
     
    x, y = now_point
 
    # 이론상 갈 수 있는 점은 위 아래 왼쪽 오른쪽 4개
    # 그 중 arr를 벗어나지 않는 점만 추가
    can_go = []
 
    if x >= 1:
        can_go.append((x-1, y))
    if x < N-1:
        can_go.append((x+1, y))
    if y >= 1:
        can_go.append((x, y-1))
    if y < N-1:
        can_go.append((x, y+1))


    # # 거기서 직전에 머물던 점이거나, 벽이거나 하면 안 돼
    # for tu in can_go:
    #     if tu in went_points or tu in walls:        # can_go에서 지우기
    #         can_go.remove(tu)
                    
 
    # return can_go

    # 방문했거나, 벽인 곳은 제외한 새로운 리스트 반환
    return [pt for pt in can_go if pt not in went_points and pt not in walls]
     
 

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N = int(input())   #n*n 행렬에서 n값 확인
    arr = []                 # n*n행렬 담을 리스트
    for a in range(N):  # 각 줄마다 받아와서 array_list에 추가할거야
        i = list(map(int, input()))   
        arr.append(i)
    #print(array_list)
    # [[1, 3, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 2, 1]]


    ########### 행렬 input 받아서,
    ############ 시작점, 도착점, 길, ~길 구분하는 코드입니다.

    walls = set()           #벽
    went_points = set()     #다녀간 길
    
    for row in range(N):
        for col in range(N):
            if arr[row][col] == 2:    # 출발
                start_point = (row,col)
            elif arr[row][col] == 3:  # 도착
                end_point = (row, col)
            elif arr[row][col] == 1:   # 벽
                walls.add((row, col))
                
 
    #출발점에서 시작해볼까...
    now_point = start_point
    went_points.add(now_point)      # 방문
    
    # where_to_go(now_point)는 갈 수 있는 좌표들을 list로 반환
    # where_to_go(now_point)가 빈 list가 아닐 때까지 반복
    # 갈림길 list가 필요!
    forks = []

    # 도착했는지 여부
    is_arrived = 0

    """
    모든 now_point를 돌며, len(where_to_go(now_point)) > 1이면 forks에 추가한다.
    더이상 갈 곳이 없다면 직전 fork로 돌아간다.
    돌아갈 때 방금 지나온 곳은 벽(0)으로 만든다.
    만약 돌아온 갈림길이 더이상 갈림길이 아니게 됐다면 forks 에서 pop한다.
    만약 도중에 3을 만나면 1을 반환한다.
    더이상 돌아갈 갈림길이 없다면 0을 반환한다.
    """
    # fork때 되돌아가rl & 지나온 길 wall화 위한 route 기록
    route = [start_point]

    # 갈 곳이 있거나, 되돌아갈 forks가 남아있는 동안
    while True:   
        # 3이면 끝
        if now_point == end_point:
            is_arrived = 1
            break

        # 아니면 갈 수 있는 곳들 순회
        nxts = where_to_go(now_point)

        # 갈 데가 있으면
        if nxts:    
            # 2개 이상이면 갈림길로 추가
            if len(nxts) >= 2:
                forks.append(now_point)
            
            # 첫번쨰로 이동한다
            now_point = nxts[0]

            # 첫번쨰가 답이 아니라도 상관없다
            # fork로 되돌아올것이기때문이다..
            went_points.add(now_point)
            route.append(now_point)     # 경로 기록
            # print(nxts)


        # 갈 곳이 없다면
        else:
            # 만약 되돌아갈 fork도 없다면 실패로 끝
            if not forks:
                break
            
            # 직전에 들렀던 fork의 좌표
            last_fork = forks.pop()
            
            
            # 루트에서 last_fork가 나올 때까지 pop 하며 wall화
            while route and route[-1] != last_fork:
                dead = route.pop()
                walls.add(dead)            # 막다른 길 전체를 벽으로
            
            now_point = last_fork         # fork 지점으로 복귀

    print(f'#{tc} {is_arrived}')