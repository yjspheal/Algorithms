# 1970. 쉬운 거스름돈

# 온라인 저지에서는 stdin 사용 불가하므로 주석처리
# import sys
# sys.stdin = open("input.txt", "r")

def calculate_bills(price):
    """
    주어진 price가 어떤 지폐 조합(최소갯수)로 만들어질 수 있는지 계산하여 반환하는 함수
        ex) 6만 7천원 -> 50000 1장, 10000 1장, 5000 1장, 1000 2장

    Args:
        price(int): 주어진 돈 가격

    Returns:
        List: 각 지폐가 몇 장씩 필요한지를 담은 리스트, 길이는 8(5만, 만, 5천, 천, 5백, 백, 5십, 십)
            ex) 위 예시의 경우 [1, 1, 1, 2, 0, 0, 0, 0]
    """

    # idea
    # price를 50000으로 나누고 남은 나머지를 10000으로 나누고 남은 나머지를 5000으로 나누고 나머지를 ...

    # 지폐와 동전 종류를 담은 리스트
    bills = [50000, 10000, 5000, 1000, 500, 100, 50, 10]

    # 각 필요 장수를 담을 리스트
    bill_counts = []

    # bills를 순회하며
    for bill in bills:
        # price를 나눈 몫 계산(= 필요 장수)
        bill_count = price // bill
        bill_counts.append(bill_count)

        # price를 bill로 나누고 남은 나머지로 업데이트
        price %= bill

    return bill_counts


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    # 거스름돈 input
    charge = int(input())

    # charge의 지폐 조합 리스트로 받음
    charge_bills = calculate_bills(charge)
    
    # 형식 맞게 print
    print(f'#{tc}')

    for bill in charge_bills:
        print(bill, end = ' ')
    
    print()