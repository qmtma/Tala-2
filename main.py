import os

ROOT = 'courses'
courses = os.listdir(ROOT)

def users():
    Read = open(f"{ROOT}/{directory}/{file}/classList.csv", 'r')
    userNames = Read.read().strip(',').split()
    Read.close()
    del userNames[0]
    return userNames

def class_Details():
    Read = open(f"{ROOT}/{directory}/{file}/classInfo.csv", 'r')
    contents = []
    for line in Read:
        read = Read.read().rstrip("\n")
        read = read.split(',')
        contents.append(read)
    for line in contents:
        if line[0].isdigit():
            duration = line[0]
        if line[1].isdigit():
            classes_num = line[1]
    CD = [duration,classes_num]
    Read.close()
    return CD

def blackBoard_Absence():
    BBAbsence=[]
    csvFile =  open(f"{ROOT}/{directory}/{file}/attendance_BB.csv", 'r')
    attendanceBB = []
    for line in csvFile:
        row = line.split(',')
        attendanceBB.append(row)
    for row in attendanceBB:
        if row[1] in All_users:
            BBcount = 0
            for item in row:
                if item == 'Absent':
                    BBcount += 1
            BBAbsence.append(BBcount)
    return BBAbsence

def sheets():
    sheets=[]
    Count = 0
    for file in AD_Files:
        if file.startswith("Lecture"):
            sheets.append(file)
            Count += 1
    return sheets, Count

def collab_ultra():
    CUList={}
    CUAbsence =[]
    for name in All_users:
        CUList.update({name:0})
    for lecture in lectures:
        csvFile =  open(f"{ROOT}/{directory}/{file}/{lecture}")
        CUData = []
        for line in csvFile:
            row = line.split(',')
            CUData.append(row)
        for row in CUData:
            for user in CUList:
                if user == row[1]:
                    entry = CUList.get(user)
                    entry += 1
                    attendedTime = row[6]
                    attendedH = attendedTime[0]
                    attendedM = attendedTime[2:4]
                    attendedM = int(attendedM) + (int(attendedH) * 60)
                    if int(attendedM) < (0.75 * int(CD[0])):
                        entry -= 1
                    CUList.update({user: entry})
    for user in CUList:
        entry = CUList.get(user)
        entry = lectures_count - entry
        CUAbsence.append(entry)
    return CUAbsence

def collaborate_percentage():
    i=0
    list = []
    for user in All_users:
        entry = (float(collaborate_ultra[i])/float(lectures_count))*100
        entry = round(entry,2)
        list.append(entry)
        i+=1
    return list

def black_board_percentage():
    list = []
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(lectures_count))*100
        i+=1
        list.append(round(entry,2))
    return list

def cumulative_colab_ultra():
    list = []
    i=0
    for user in All_users:
        entry = (int(collaborate_ultra[i])/float(CD[1]))*100
        i+=1
        list.append(round(entry,2))
    return list

def collab_status():
    list=[]
    i=0
    for user in All_users:
        if float(C_C_Ultra[i])>25:
            list.append("Dismissed")
        elif float(C_C_Ultra[i])<25 and float(C_C_Ultra[i])>15:
            list.append("Warning")
        else: list.append("OK")
        i+=1
    return list

def cumulative_BB_absence():
    list=[]
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(CD[1]))*100
        i+=1
        list.append(round(entry,2))
    return list

def Black_Status():
    list = []
    i = 0
    for user in All_users:
        if float(C_BB_Absence[i])>25:
            entry = "Dismissed"
            list.append(entry)
        elif float(C_BB_Absence[i])<25 and float(C_BB_Absence[i])>15:
            entry = "Warning"
            list.append(entry)
        else:
            entry = "OK"
            list.append(entry)
        i+=1
    return list

def extract_sheet():
    WriteFile = open(f"{ROOT}/{directory}/CUvsBBReport_{directory}_{file}.txt", 'w')

    WriteFile.write(
        "Username       CU_Absance  BB_Absance  CU_Absance%  BB_Absance%  C_CU_Absance%  CU_Status  C_BB_Absance%  BB_Status\n")
    i = 0
    for user in All_users:
        len0 = len("Username       ") - len(user)
        len1 = len("CU_Absance No ") - len(str(collaborate_ultra[i]))
        len2 = len(" BB_Absance No ") - len(str(Black_board[i]))
        len3 = len(" CU_Absance% ") - len(str(C_percentage[i]))
        len4 = len(" BB_Absance% ") - len(str(B_pecentage[i]))
        len5 = len(" C_CU_Absance% ") - len(str(C_C_Ultra[i]))
        len6 = len(" CU_Status ") - len(C_Status[i])
        len7 = len(" C_BB_Absance% ") - len(str(C_BB_Absence[i]))
        len8 = len(" BB_Status") - len(general_status[i])
        WriteFile.writelines(
            f"{user}{(len0 * ' ')}{collaborate_ultra[i]}{(len1 * ' ')}{Black_board[i]}{(len2 * ' ')}{C_percentage[i]}{(len3 * ' ')}{B_pecentage[i]}{(len4 * ' ')}{C_C_Ultra[i]}{(len5 * ' ')}{C_Status[i]}{(len6 * ' ')}{C_BB_Absence[i]}{(len7 * ' ')}{general_status[i]}\n")
        i += 1
    WriteFile.close()

for directory in courses:
    if os.path.isdir(f"{ROOT}/{directory}"):
        subDir = os.listdir(f"{ROOT}/{directory}")
        for file in subDir:
            if os.path.isdir(f"{ROOT}/{directory}/{file}"):
                AD_Files = os.listdir(f"{ROOT}/{directory}/{file}")
                All_users = users()
                CD = class_Details()
                lectures , lectures_count = sheets()
                Black_board = blackBoard_Absence()
                collaborate_ultra = collab_ultra()
                C_percentage = collaborate_percentage()
                B_pecentage = black_board_percentage()
                C_C_Ultra = cumulative_colab_ultra()
                C_Status = collab_status()
                C_BB_Absence = cumulative_BB_absence()
                general_status = Black_Status()
                extract_sheet()
