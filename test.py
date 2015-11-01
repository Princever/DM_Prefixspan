def expand(maxSeqs):
    result = []
    for each in maxSeqs:
        tmp = []
        count = 0
        for one in each:
            count += 1
        time1 = 0
        
        if count == 2:   
            while time1 <= 1:
            	time2 = 0
                while time2 <= 4:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 3:
            while time1 <= 2:
            	time2 = 0
                while time2 <= 2:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 4:
            while time1 <= 3:
            	time2 = 0
                while time2 <= 1:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 5:
            while time1 <= 4:
            	time2 = 0
                while time2 <= 1:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count >= 6:
            tmp += each

    	if tmp != []:
        	result += [tmp]
    return result


test = [[[1]],[[1],[2]],[[1],[2],[3]],[[1],[2],[3],[4]],[[1],[2],[3],[4],[5]],[[1],[2],[3],[4],[5],[6]],[[1],[2],[3],[4],[5],[6],[7]],[[1],[2],[3],[4],[5],[6],[7],[8]],[[1],[2],[3],[4],[5],[6],[7],[8],[9]],[[1],[2],[3],[4],[5],[6],[7],[8],[9],[0]]]

ans = expand(test)
print ans