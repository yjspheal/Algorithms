# 1954_달팽이숫자 

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# # sys.stdin = open("input.txt", "r")
# sys.stdin = open("input.txt", "r")

"""
중꺾마.. 하지만 여기선 꺾어야한다
1. 오른쪽 끝점을 구한다
2. 아래 끝점을 구한다
3. 왼 끝점을 구한다
4. 위 끝점을 구한다.
5. for 로 열심히 돈다. 1부터 N^2 까지 해당 지점을 돌아가면서 채운다
"""

def snail_number_maker(N):
    """
    N이 들어오면, NxN 크기의 반시계방향 달팽이 숫자를 만들어 return 한다.

    Args:
        N(int): NxN의 사이즈

    Returns:
        List: 달팽이화된 NxN 리스트

    Examples:
        N = 3 -> List = [['1', '2', '3'], ['8', '9', '4'], ['7', '6', '5']]
    """
    if N == 1:
        return [['1']]
    current_x = -1
    current_y = 0

    # 목표 좌표 초기화
    right = N - 1
    lower = N - 1
    left = 0
    upper = 1

    snail_arr = [['-'] * N for _ in range(N)]        # 달팽이 만들 NxN 행렬 초기화

    X = []      # 그 시점에 있어야하는 X좌표 (크기 = N^2)
    Y = []      # 그 시점에 있어야하는 y봐표 (크기 = N^2)

    count = 0   # 지금 몇개째 만들고 있는지 count
    is_making = True
    while is_making:        # count가 N제곱이 될때까지, 즉 X와  Y 리스트 길이가 N제곱이 될 때까지
        # 아래를 먼가 줄일 수 있을 것 같은데...머르겟음

        # 오른쪽갔다가
        for x in range(current_x + 1, right + 1):
            count += 1
            X.append(x)
            Y.append(current_y)
            current_x = x       # 현재 x 업데이트
            if count == N ** 2:
                is_making = False
                break

        right -= 1

        # 아래 갔다가
        for y in range(current_y + 1, lower + 1):
            count += 1
            X.append(current_x)
            Y.append(y)
            current_y = y       # 현재 y 업데이트

        lower -= 1

        # 왼쪽 갔다가
        for x in range(current_x - 1, left - 1, -1):
            count += 1
            X.append(x)
            Y.append(current_y)
            current_x = x       # 현재 x 업데이트
            if count == N ** 2:
                is_making = False
                break

        left += 1

        # 위로 갔다가
        for y in range(current_y - 1, upper - 1, -1):
            count += 1
            X.append(current_x)
            Y.append(y)
            current_y = y       # 현재 y 업데이트

        upper += 1


    # 1 ~ N 제곱 까지의 수에 대해서 x, y 좌표에 넣는다.
    for num, x, y in zip(range(1, N**2 + 1), X, Y):
        # snail_arr의 해당 위치에 값을 넣는다.
        snail_arr[y][x] = str(num)
        # y가 행값임을 유의

    return snail_arr

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):

    N = int(input())

    snail = snail_number_maker(N)

    print(f'#{tc}')

    for row in snail:
        print(*row)