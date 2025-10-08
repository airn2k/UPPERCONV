from pickle import NONE
import pandas as pd
from datetime import datetime

data = pd.read_csv('upper_air_data.csv')


file_object = open('my_file.FSL', encoding='utf8',mode='w')

for i in range(0,len(data),17):
    original = data.iloc[i,0]
    # Parse data time which is in 022-07-01 00:00:00
    dt = datetime.strptime(original, "%Y-%m-%d %H:%M:%S")
    # Format as  0   1   JUL 2022; hour within 7 chars, day within 6 chars, month within 9 chars and year within 8 chars, month is capitalised
    formatted = f"{dt.hour:>7} {dt.day:>6} {dt.strftime('%b').upper():>8} {dt.year:>7}"
    file_object.writelines("    254"+formatted+"\n")
    # Next lines will be these
    #  1  99999 999999  52.47N  8.16W   106   1200
    #  2  32767  32767  32767     32  32767  32767
    #  3          NONE                32767     ms
    # but the 1200 will be the hour and minutes
    L1 = "      1  99999 999999  52.47N  8.16W   106   " + f"{dt.hour:02}" + "00\n"
    L2 = "      2  32767  32767  32767     17  32767  32767\n"
    L3 = "      3          NONE                32767     ms\n"
    file_object.writelines(L1)
    file_object.writelines(L2)
    file_object.writelines(L3)
    # Now loop through the next 17 rows to get the data
    for j in range(i, i+17):
        if j >= len(data):
            break
        pressure = int(data.iloc[j,1])
        pressure_str = f"{pressure:>7}"
        height = int(data.iloc[j,2])
        height_str = f"{height:>7}"
        dew_point = int(data.iloc[j,3])
        dew_point_str = f"{dew_point:>7}"
        temperature = int(data.iloc[j,4])
        temperature_str = f"{temperature:>7}"
        wind_direction = int(data.iloc[j,5])
        wind_direction_str = f"{wind_direction:>7}"
        wind_speed = int(data.iloc[j,6])
        wind_speed_str = f"{wind_speed:>7}"
        # if it's the first row first column is 9 else it's 5
        if j == i:
            first_col = "      9"
        else:
            first_col = "      5"
        line = f"{first_col}{pressure_str}{height_str}{dew_point_str}{temperature_str}{wind_direction_str}{wind_speed_str}\n"
        file_object.writelines(line)
    # print(formatted)

file_object.close()
