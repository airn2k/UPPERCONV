import pandas as pd
from datetime import datetime

data = pd.read_csv('clara_bog_upper_air_2023_2025.csv')
data['t'] = data['t']-273.15

L1 = "1  54775  72518  53.32N  7.62W   55"
L2 = "2                      \n"
L3 = "3           ALY                \n"

file_object = open('my_file.FSL', encoding='utf8',mode='w')

for i in range(0,len(data),13):
    original = data.iloc[i,0]
    # Parse the datetime
    dt = datetime.strptime(original, "%d/%m/%Y %H:%M")
    formatted = f"{dt.hour}\t{dt.day}\t{dt.strftime('%b')}\t{dt.year}"
    file_object.writelines("254    "+formatted+"\n")
    file_object.writelines(L1+"\t" + str(2355 - 100*dt.hour) +"\n")
    file_object.writelines(L2)
    file_object.writelines(L3)
    for j in range(0,12):
        if (j==0):
            file_object.writelines("9  "+str(round(data.iloc[i+j,1]*10))+"  "+str(round(data.iloc[i+j,4]))+"  "+str(round(data.iloc[i+j,3]*10))+"\n")
        else:
            file_object.writelines("4  "+str(round(data.iloc[i+j,1]*10))+"  "+str(round(data.iloc[i+j,4]))+"  "+str(round(data.iloc[i+j,3]*10))+"\n")

    print(formatted)

file_object.close()
