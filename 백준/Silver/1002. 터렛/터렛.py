from math import sqrt
result = []
N = int(input())

for i in range(N):
    x1,y1,r1,x2,y2,r2 = map(int,input().split())

    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    marine = r1 + r2
    
    if distance >= max(r1,r2):
        if distance == marine:
            result.append(1)
        elif distance < marine :
            result.append(2)
        else:
            result.append(0)
            
    else:
        if distance + min(r1,r2) == max(r1,r2):
            if distance == 0:
                result.append(-1)
            else:
                result.append(1)
        elif distance + min(r1,r2) > max(r1,r2):
            result.append(2)
        else:
            result.append(0)
            
for r in result:
    print(r)