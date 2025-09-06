sum, k = map(int,input().split())

num = sum // k
rmd = sum % k

print(num ** (k - rmd) * (num + 1) ** rmd)