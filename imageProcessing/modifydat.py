def sort_coor(lis):
    #sort coordinate left-top
    #sort by bubble sort // must change to better sort
    bound = 5
    for i in range(len(lis)):
        for j in range(len(lis)-1):
            if abs(lis[j][1]-lis[j+1][1]) >= bound  and lis[j][1] > lis[j+1][1]:
                lis[j],lis[j+1] = lis[j+1],lis[j]
            elif  abs(lis[j][1]-lis[j+1][1]) < bound  and lis[j][0] > lis[j+1][0]:
                lis[j],lis[j+1] = lis[j+1],lis[j]
    return lis