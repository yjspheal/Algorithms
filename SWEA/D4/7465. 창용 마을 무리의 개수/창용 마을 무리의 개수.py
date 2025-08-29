# 7465. 창용 마을 무리의 개수

# import sys
#
# sys.stdin = open('input.txt')

def dfs(start_p, adj_list, check_group):
    """
    시작 사람 번호와 전체 방문 여부(group_list)를 인자로 받아
    시작 사람이 속하는 무리의 사람들을 모두 group_list True로 만들어 return하는 함수

    Args:
        start_p(int) : 시작 사람 번호
        adj_list (list) : 인접리스트
        check_group (list) : 무리 생성 여부가 담긴 boolean 리스트
    """
    stack = [start_p]  # 시작 사람을 스택에 넣고 시작
    check_group[start_p] = True  # 무리에도 넣어준다

    while stack:
        curr_p = stack.pop()  # 사람 하나 꺼내서
        for next_p in adj_list[curr_p]:  # 연결된 사람들도
            if not check_group[next_p]:
                check_group[next_p] = True  # 무리에 넣고 스택에도 넣는다
                stack.append(next_p)

    return check_group  # 현재 무리여부 체크 상태를 보여준다


T = int(input())
for tc in range(1, T + 1):
    # 사람 수, 관계 수
    people, relationship = map(int, input().split())

    cy_adj = [[] for _ in range(people + 1)]  # 창용관계도 인접리스트
    for _ in range(relationship):  # 관계 수만큼
        p1, p2 = map(int, input().split())  # 사람 페어

        cy_adj[p1].append(p2)  # 서로를 추가해준다
        cy_adj[p2].append(p1)

    cy_group = [False] * (people + 1)  # 사람 체크 여부, 즉 무리가 있는 사람들

    # 1번부터 people번까지의 사람을 돌며
    count_group = 0  # 무리 수=0
    for person in range(1, people + 1):
        if not cy_group[person]:  # person이 아직 무리가 없다면
            count_group += 1  # 무리 수 + 1
            cy_group = dfs(person, cy_adj, cy_group)  # dfs돌려서 무리 체크 상태를 업데이트

    print(f'#{tc} {count_group}')
