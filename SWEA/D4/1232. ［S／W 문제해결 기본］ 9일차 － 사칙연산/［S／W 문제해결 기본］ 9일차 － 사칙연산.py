# 1232 사칙연산

def post_order(node_info):
    """
    후위순회하며 노드 값을 계산
    """
    len_node_info = len(node_info)

    if len_node_info == 2:  # 노드 길이가 2면. 즉 리프라면
        return node_info[1]  # 값을 리턴

    else:
        num1 = int(post_order(tree[int(node_info[2])]))  # 후위순회 왼
        num2 = int(post_order(tree[int(node_info[3])]))  # 후위순회 오

        operator = node_info[1]  # 리프가 아니면 모두 연산자이다

        # 값을 업데이트한다.
        if operator == '+':
            node_info[1] = num1 + num2
        elif operator == '-':
            node_info[1] = num1 - num2
        elif operator == '*':
            node_info[1] = num1 * num2
        else:  # 사칙연산만 들어있다. 소수점 아래는 버린다.
            node_info[1] = num1 // num2

    return node_info[1]  # 업데이트된 값을 리턴한다.


T = 10
for tc in range(1, T + 1):
    N = int(input())  # 노드 수

    # tree 초기화. 인덱스 맞추기 위해 앞에 빈 리스트 추가
    tree = [[]] + [list(input().split()) for _ in range(N)]

    # 루트노드의 번호는 항상 1이다
    print(f'#{tc} {post_order(tree[1])}')
