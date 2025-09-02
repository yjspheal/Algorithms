# 5102. [파이썬 S/W 문제해결 기본] 6일차 - 노드의 거리

# import sys
#
# sys.stdin = open('input.txt')

from collections import deque

def bfs(start_node, node_count, target_node, adj_l):
    """

    """
    visited = [False] * (node_count+1)   # 노드 수만큼 길이.
    q = deque()

    q.append(start_node)    # 첫 노드 넣기
    visited[start_node] = 0  # 노드 방문 완료

    while q:
        current_node = q.popleft()

        for next_node in adj_l[current_node]:   # 현재 노드의 인접 노드들을 돌며
            if not visited[next_node]:  # 아직 방문 안 했다면
                q.append(next_node) # 큐에 넣고
                visited[next_node] = visited[current_node] + 1  # 노드 방문 처리 겸 거리 기록록
                if next_node == target_node:
                    return visited[next_node]


T = int(input())
for tc in range(1, T + 1):
    V, E = map(int, input().split())

    adj_list = [[] for _ in range(V+1)] # 인접리스트 생성

    for _ in range(E):
        n1, n2 = map(int, input().split())

        adj_list[n1].append(n2)     # 인접 리스트에 추가
        adj_list[n2].append(n1)

    S, G = map(int, input().split())

    path_length = bfs(S, V, G, adj_list)
    
    if path_length is None:
        path_length = 0

    print(f'#{tc} {path_length}')
