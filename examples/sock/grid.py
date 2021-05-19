grid=5
dist=3
first=2
for i in range(grid):
    for j in range(grid):
        line=str(i*grid+j+first)+" 0 " + str(i*dist)+ " " + str(j*dist)
        print(line)

print("1 0 -3 6") #slip radio