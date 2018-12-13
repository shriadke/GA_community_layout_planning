def surround(point,size,grid):
    x=point[0]
    y=point[1]
    if 0<x<24 and 0<y<24:
        count = 0
        for a in range((x-1),x+size+1): 
            for b in range(y-1,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        print("hi", a, b, grid[a][b])
                        count=count+1
        if (count==4*(size+1)):
            return 1
    elif x==0 and y==0:
        count = 0
        for a in range((x),x+size+1): 
            for b in range(y,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
        if (count==(2*(size+1)-1)):
            return 1
    elif x==0 and 0<y<24:
        count = 0
        for a in range((x),x+size+1): 
            for b in range(y-1,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
               
        if (count==(3*(size+1)-1)):
            return 1
    elif 0<x<24 and y==0:
        count = 0
        for a in range((x-1),x+size+1): 
            for b in range(y,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
        if (count==(3*(size+1)-1)):
            return 1
    return 0
X=np.load("populationGridsnew.npy")
print(X[0,:,:])
grid=X[0,:,:]
S=np.load("startsList.npy")
a=0
houses=[S[a].get('houses'),2,1]
coffice=[S[a].get('coffice'),2,4]
club=[S[a].get('club'),4,6]
play=[S[a].get('play'),4,5]
clinic=[S[a].get('clinic'),4,3]
school=[S[a].get('school'),5,9]
market=[S[a].get('market'),5,8]

A=[]
A.append(surround(coffice[0][0], coffice[1],grid1))
for i in range(2):
    b=surround(play[0][i], play[1], grid1)
    A.append(b)
A.append(surround(club[0][0],club[1],grid1))
A.append(surround(school[0][0],school[1],grid1))
for i in range(20):
    b=surround(houses[0][i],houses[1],grid1 )
    A.append(b)


print("hi",coffice[0][0])
A.append(surround(clinic[0][0],clinic[1],grid1))
A.append(surround(market[0][0],market[1],grid1))


print(A)
