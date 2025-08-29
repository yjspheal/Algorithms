# 4871. [파이썬 S/W 문제해결 기본] 4일차 - 그래프 경로

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")

T = int(input())       # 테스트 케이스 개수 입력
for tc in range(1, T + 1):
    V, E = map(int, input().split())        # 노드 개수, 간선 개수
    
    # 빈 리스트 V+1개를 원소로 가짐
    # 각 노드가 어던 노드와 이어져있는지 표현
    link = [[] for _ in range(V+1)]        

    # 간선 정보 입력
    for _ in range(E):
        start, end = map(int, input().split())
        link[start].append(end)            # start에서 end가 

    S, G = map(int, input().split())        # 출발, 도착 노드

    # 노드 방문 여부 체크
    visited = [False] * (V+1)     

    global answer # 함수 안에서도 쓸 수 있도록 전역변수 선언
    answer = 0    # 경로 존재 여부(1: 있음, 0: 없음), 기본값 0

    # DFS 함수 정의
    def dfs(node):
        global answer
        
        # 만약 현재 노드가 도착노드 G라면, 경로 찾은것
        if node == G:
            answer = 1                      
            return
        visited[node] = True                # 현재 노드 방문 처리

        # 인접한 노드들에 대해
        for nxt in link[node]:
            if not visited[nxt]:            # 아직 방문 안 했다면
                dfs(nxt)                    # 그 노드로 재귀 탐색

    dfs(S)                                  # 출발 노드 S에서 탐색 시작

    print(f'#{tc} {answer}')                # 테스트케이스 번호와 경로 존재 여부 출력