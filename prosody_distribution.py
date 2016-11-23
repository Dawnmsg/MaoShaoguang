
import csv
import string
import sys
import math
import numpy as np


temp=str(sys.argv[1]).replace('.wav','')
print(temp)
filename=temp+'.prosody.csv'
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    dataSize=0;
    arr=[]
    loudness=[]
    eng=[]
    for row in reader:
        if dataSize>0:
          if float(row[3])>0.8:
              arr.append(1)
              loudness.append(float(row[4]))
              eng.append(float(row[2]))
          else:
              arr.append(0)
          dataSize += 1
        else:
          dataSize += 1


    sil=[]
    voi=[]
    sil.append(0)
    voi.append(0)
    silnum = 0
    voinum = 0

    #calculate distribution of silence and voice
    for i in range(0,dataSize-2):
        if arr[i]==0 and arr[i+1]==0:
            sil[silnum] +=1
        elif  arr[i+1] ==1 and arr[i] ==1:
            voi[voinum] +=1
        elif  arr[i]==0 and arr[i+1]==1:
            sil[silnum] +=1
            silnum +=1
            sil.append(0)
        else:
            voi[voinum] +=1
            voinum +=1
            voi.append(0)

    silunify = [0]*50
    voiunify = [0]*50
    for i in range(1,silnum-1):
        siluni= math.floor(sil[i]/2)
        if siluni < 50:
            silunify[siluni] +=1/(silnum-2)
    for i in range(0,voinum):
        voiuni= math.floor(voi[i]/2)
        if voiuni <50:
            voiunify[voiuni] +=1/voinum

    np.savetxt(temp + '.sil.csv', silunify, delimiter=',')
    np.savetxt(temp + '.voice.csv', voiunify, delimiter=',')

    # calculate distribution of loudness
    loudunify = [0]*50
    for i in range(0,len(loudness)-1):
        louduni = math.floor(loudness[i]/0.08)

        if louduni < 50:
            loudunify[louduni] +=1/len(loudness)
    np.savetxt(temp + '.loud.csv', loudunify, delimiter=',')

    # calculate distribution of fundamental frequency
    engavg=np.mean(eng)
    engunify =[0]*50
    for i in range(0,len(eng)-1):
        eng[i] -=engavg
        if eng[i]>=0:
            enguni = math.floor(eng[i]/4+25)
            if enguni <= 50:
                engunify[enguni-1] += 1/len(eng)
        else:
            enguni = math.floor(eng[i] / 4) + 25
            if enguni>=0:
                engunify[enguni-1] +=1/len(eng)
    np.savetxt(temp + '.f0.csv', engunify, delimiter=',')
csvfile.close()