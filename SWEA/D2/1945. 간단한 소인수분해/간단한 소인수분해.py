# 1945. 간단한 소인수분해 

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N = int(input())

    # 2 3 5 7 11의 지수가 몇인지 저장할 리스트
    prime_counts = [0] * 5
    primes = [2, 3, 5, 7, 11]
    for i, prime in enumerate(primes):
        while N % prime == 0:        # N이 prime으로 나눠진다면
            N //= prime              # N 업데이트
            prime_counts[i] += 1    # 해당 prime이 나눠진 횟수 +1


    print(f'#{tc}', *prime_counts)