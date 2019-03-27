#!/usr/bin/env python
# coding: utf-8

# In[1]:


jobs = list(range(21))
processTime = [0, 10, 10, 13, 4, 9, 4, 8, 15, 7, 1, 9, 3, 15, 9, 11, 6, 5, 14, 18, 3]
dueDate = [0, 50, 38, 49, 12, 20, 105, 73, 45, 6, 64, 15, 6, 92, 43, 78, 21, 15, 50, 150, 99]
weights = [0, 10, 5, 1, 5, 10, 1, 5, 10, 5, 1, 5, 10, 10, 5, 1, 10, 5, 5, 1, 5]


# In[2]:


initialSol = jobs #0~20
length = len(jobs) - 1 #20

def Tardiness(sol):
    totalTime = 0
    tardiness = 0
    for i in sol:
        totalTime = totalTime + processTime[i]
        lateTime = totalTime - dueDate[i]
        if(lateTime < 0):
            lateTime = 0
        tardiness = tardiness + weights[i] * lateTime
    return tardiness


tabuList = []
MAXNUM = 9999
bestTardiness = MAXNUM

def CheckTabu(newTabu):
    for tabu in tabuList:
        if(tabu == newTabu):
            return True
    return False

def TabuFunc(sol, tabuListMaxSize):
#     joblist = []
#     newTabu = []
    newAns = MAXNUM
    for i in range(1,length):
        tmpSol = sol.copy()
        tmpSol[i],tmpSol[i+1] = tmpSol[i+1],tmpSol[i]
        tmpAns = Tardiness(tmpSol)
        if(tmpAns < newAns):
            tmpTabu = [tmpSol[i],tmpSol[i+1]]
            tmpTabu.sort()
            if( CheckTabu(tmpTabu)==False ):
                newtardiness = tmpAns
                joblist = tmpSol.copy()
                newAns = tmpAns
                newTabu = tmpTabu
    if(len(tabuList) < tabuListMaxSize):
        tabuList.append( newTabu )
    else:
        tabuList.pop(0)
        tabuList.append(newTabu)
    return newtardiness, joblist.copy()


# In[3]:


print('Find best parameters:')
print('test tabu list size from 1~20 and run time from 1~500')
for testTabusize in range(1,20):
    testTardiness, testjoblist = TabuFunc(initialSol,testTabusize)
    if(testTardiness<bestTardiness):
            bestTardiness = testTardiness
            bestTabuListSize = testTabusize
            bestjoblist = testjoblist.copy()
    for testtime in range(500):
        testTardiness, testjoblist = TabuFunc(testjoblist,testTabusize)
        if(testTardiness<bestTardiness):
            bestTardiness = testTardiness
            bestTabuListSize = testTabusize
            besttime = testtime
            bestjoblist = testjoblist.copy()
#             print(bestTardiness,bestjoblist)
            
print('Tabu list size of',bestTabuListSize,'and run',besttime+2,'times will get besttardiness of', bestTardiness, '.\nAnd the job sequence is:', bestjoblist[1:])


print('\n\nDetail of best-parameter solution:\n')
tabuList = []
print('Initial solution =',initialSol[1:])
finalTardiness, finaljoblist = TabuFunc(initialSol,bestTabuListSize)
print('runtime =',1,'\ntabu list =', tabuList, '\ntardiness =',finalTardiness,'\njob sequence =',finaljoblist[1:])
for i in range(besttime+1):
    finalTardiness, finaljoblist= TabuFunc(finaljoblist,bestTabuListSize)
    print('\nruntime =',i+2,'\ntabu list =', tabuList, '\ntardiness =',finalTardiness,'\njob sequence =',finaljoblist[1:])

print('\n\nAgain show best result:')
print('tabu size =', bestTabuListSize)
print('run', i+2,'times')
print('job sequence =', finaljoblist[1:])
print('total weighted tardiness =', finalTardiness)
print('tabulist =',tabuList)
print('ps. trial-and-error adjustment of parameters is in the beginning')

