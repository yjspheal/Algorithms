#

# import sys
# 
# sys.stdin = open('sample_input.txt')


def pre_order(node_num):
    """
    전위순회하며 노드 번호를 출력
    """
    global sub_nodes
    if node_num:  # 내가 0이 아닌 한

        sub_nodes += 1  # 서브트리 노드 수 + 1
        pre_order(left_child[node_num])  # 전위순회 왼
        pre_order(right_child[node_num])  # 전위순회 오


T = int(input())
for tc in range(1, T + 1):
    # 엣지 수, 서브트리 루트노드
    E, N = map(int, input().split())
    tree = list(map(int, input().split()))

    # 왼 오 자식들. 노드 번호는 1번부터 E+1번까지 존재한다.
    left_child = [0] * (E + 2)
    right_child = [0] * (E + 2)

    for i in range(E):
        p = tree[2 * i]
        c = tree[2 * i + 1]

        if left_child[p] == 0:   # p한테 자식이 없다면
            left_child[p] = c

        else:
            right_child[p] = c

    sub_nodes = 0
    pre_order(N)  # 루트부터 순회

    print(f'#{tc} {sub_nodes}')
