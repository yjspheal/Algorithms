# 1231 중위순회


def in_order(node_info):
    """
    중위순회하며 노드 값을 출력
    """
    len_node_info = len(node_info)
    if len_node_info == 2:  # 노드 길이가 2면. 즉 리프라면
        print(node_info[-1], end='')  # 값을 출력

    else:
        in_order(tree[int(node_info[2])])  # 중위순회 왼
        print(node_info[1], end='')  # 값을 출력
        if len_node_info > 3:
            in_order(tree[int(node_info[3])])  # 중위순회 왼


T = 10
for tc in range(1, T + 1):
    N = int(input())  # 노드 수

    # tree 초기화. 인덱스 맞추기 위해 앞에 빈 리스트 추가
    tree = [[]] + [list(input().split()) for _ in range(N)]

    # 프린트 시작
    print(f'#{tc} ', end='')

    # 순회하며 프린트. 루트노드의 번호는 항상 1이다
    in_order(tree[1])

    print()  # 엔터용
