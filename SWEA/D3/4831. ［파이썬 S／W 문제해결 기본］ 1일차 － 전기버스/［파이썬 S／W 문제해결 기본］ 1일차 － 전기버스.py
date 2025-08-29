# 4831. [파이썬 S/W 문제해결 기본] 1일차 - 전기버스

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")


def count_charging_station(stations):
    """
    충전정류장 번호 list를 인자로 받아, 최소로 들를 충전정류장 수를 찾아 return하는 함수

    Args:
        stations (list): 각 충전정류장 번호를 원소로 가진 리스트

    Returns:
		    int: 최소 방문 충전정류장 수
    """

    # 충전정류장 간의 거리를 계산하여 리스트화
    distances = []
    for i in range(1, len(stations)):
        # 현재 거리
        distance = stations[i] - stations[i-1]
        if distance > k:    # k보다 큰 구간이 있다면 바로 0 return
            return 0
        # 아니라면 리스트에 추가
        distances.append(stations[i] - stations[i-1])

    # 들러야 할 정류장 수 초기화
    count_go_stations = 0

    # distance가 남아있는동안 순회
    while distances:
        # 이번 턴에 가고 있는 정류장 길이를 계산
        current_sum = 0
        # 앞에서 몇개까지 갈 수 있는지를 계산
        for j in range(len(distances)):
            current_sum += distances[j]

            if current_sum > k:             # 이번 턴 간 길이가 k 초과면 직전까지 방문
                count_go_stations += 1
                del distances[:j]           # j-1까지 방문하였으니 지워버림
                break

            elif j == len(distances) - 1 or current_sum == k:  # k 이하인데 끝까지 온거거나, 아니면 딱 k와 동일하다면
                count_go_stations += 1
                del distances[:j+1]           # j까지 방문하였으니 지워버림
                break

            else:   # 위에 모두 해당하지 않다면 다음 정류장으로
                continue

    # 첫 정류장은 충전횟수에 포함하지 않으므로 -1
    return count_go_stations - 1

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    # k: 한번 충전으로 이동 가능한 거리(=정류장 수), N: 종점 번호, M: 충전정류장 수
    k, N, M = map(int, input().split())
    # M개의 충전정류장, 출발지, 종점 추가
    station_list = [0] + list(map(int, input().split())) + [N]
    # station_list = [0, 1, 3, 6, 7, 9, 10]

    # 들를 정류장 갯수
    select_station_count = count_charging_station(station_list)

    print(f'#{tc} {select_station_count}')
