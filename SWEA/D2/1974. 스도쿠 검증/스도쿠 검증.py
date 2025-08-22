
T = int(input())
for tc in range(1, T + 1):
    # 9x9 스도쿠 이차원배열
    sudoku = [list(map(int, input().split())) for _ in range(9)]
    sudoku += list(zip(*sudoku))        # 열을 행으로 바꿔서 밑에 추가

    is_valid = 1       # 스도쿠 맞는지 여부

    for line in sudoku:     # 각 줄을 돌며
        status = [0] * 10       # 1 ~ 9까지 값이 각 몇개인지 담을 리스트

        for num in line:
            status[num] += 1    # 해당 숫자 갯수 1 증가

            if status[num] > 1:     # 근데 그 값이 1 초과라면
                is_valid = 0
                break               # 스도쿠 아님 + break

        else:       # break가 안 됐다면 continue
            continue

        # break가 됐었다는 뜻이므로 해당 스도쿠를 완전히 벗어난다.
        break


    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            status = [0] * 10  # 1 ~ 9까지 값이 각 몇개인지 담을 리스트
            for i in range(row, row+3):
                for j in range(row, row+3):
                    num = sudoku[i][j]

                    status[num] += 1  # 해당 숫자 갯수 1 증가

                    if status[num] > 1:     # 근데 그 값이 1 초과라면
                        is_valid = 0
                        break               # 스도쿠 아님 + break

                # for문이 많으므로 그냥 break없이 다 돌자.

    print(f'#{tc} {is_valid}')