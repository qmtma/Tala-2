import os

ROOT = 'courses'
courses = os.listdir(ROOT)

def users():
    Read = open(f"{ROOT}/{directory}/{file}/classList.csv", 'r')
    userNames = Read.read().strip(',').split()
    Read.close()
    del userNames[0]
    return userNames

def class_info():
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

def BBA(All_users):
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

def sheets(AD_Files):
    sheets=[]
    Count = 0
    for file in AD_Files:
        if file.startswith("Lecture"):
            sheets.append(file)
            Count += 1
    return sheets, Count

def CU(All_users,lectures,CD,lectures_count):
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

def CU_percentage(All_users,collaborate_ultra,lectures_count):
    i=0
    list = []
    for user in All_users:
        entry = (float(collaborate_ultra[i])/float(lectures_count))*100
        entry = round(entry,2)
        list.append(entry)
        i+=1
    return list

def BB_percentage(All_users,Black_board,lectures_count):
    list = []
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(lectures_count))*100
        i+=1
        list.append(round(entry,2))
    return list

def CCU(All_users,collaborate_ultra,CD):
    list = []
    i=0
    for user in All_users:
        entry = (int(collaborate_ultra[i])/float(CD[1]))*100
        i+=1
        list.append(round(entry,2))
    return list

def CS(All_users,C_C_Ultra):
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

def CBB(All_users,Black_board,CD):
    list=[]
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(CD[1]))*100
        i+=1
        list.append(round(entry,2))
    return list

def BS(All_users,C_BB_Absence):
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

def sheet(All_users,Black_board,collaborate_ultra,C_percentage,B_pecentage,C_C_Ultra,C_Status,C_BB_Absence,general_status):
    WriteFile = open(f"{ROOT}/{directory}/CUvsBBReport_{directory}_{file}.txt", 'w')

    WriteFile.write(
        "Username       |CU_Absance | BB_Absance | CU_Absance% | BB_Absance% | C_CU_Absance% | CU_Status | C_BB_Absance% | BB_Status|\n")
    i = 0
    WriteFile.write(f"{str('-')*len('Username       |CU_Absance | BB_Absance | CU_Absance% | BB_Absance% | C_CU_Absance% | CU_Status | C_BB_Absance% | BB_Status|')}\n")
    for user in All_users:
        len0 = len(" BB_Absance ") - len(str(Black_board[i]))
        len1 = len(" CU_Absance% ") - len(str(C_percentage[i]))
        len2 = len(" BB_Absance% ") - len(str(B_pecentage[i]))
        len3 = len(" C_CU_Absance% ") - len(str(C_C_Ultra[i]))
        len4 = len(" CU_Status ") - len(C_Status[i])
        len5 = len(" C_BB_Absance% ") - len(str(C_BB_Absence[i]))
        len6 = len("BB_Status ") - len(general_status[i])
        WriteFile.writelines(
            user + (6 * ' ') + "|" + str(collaborate_ultra[i]) + (10 * ' ') + "|" + str(Black_board[i]) + (len0 * ' ') + "|" + str(C_percentage[i]) + (len1 * ' ') + "|" + str(B_pecentage[i]) + (len2 * ' ') + "|" + str(C_C_Ultra[i]) + (len3 * ' ') + "|" + str(C_Status[i]) + (len4 * ' ') + "|" + str(C_BB_Absence[i]) + (len5 * ' ') + "|" + str(general_status[i]) + (len6 * ' ') + "\n")
        i += 1
        WriteFile.write(
            f"{str('-') * len('Username       |CU_Absance | BB_Absance | CU_Absance% | BB_Absance% | C_CU_Absance% | CU_Status | C_BB_Absance% | BB_Status|')}\n")
    WriteFile.close()

def generate_file():
    AD_Files = os.listdir(f"{ROOT}/{directory}/{file}")
    All_users = users()
    CD = class_info()
    lectures, lectures_count = sheets(AD_Files)
    Black_board = BBA(All_users)
    collaborate_ultra = CU(All_users,lectures,CD,lectures_count)
    C_percentage = CU_percentage(All_users,collaborate_ultra,lectures_count)
    B_pecentage = BB_percentage(All_users,Black_board,lectures_count)
    C_C_Ultra = CCU(All_users,collaborate_ultra,CD)
    C_Status = CS(All_users,C_C_Ultra)
    C_BB_Absence = CBB(All_users,Black_board,CD)
    general_status = BS(All_users,C_BB_Absence)
    sheet(All_users,Black_board,collaborate_ultra,C_percentage,B_pecentage,C_C_Ultra,C_Status,C_BB_Absence,general_status)
    pass

for directory in courses:
    if os.path.isdir(f"{ROOT}/{directory}"):
        subDir = os.listdir(f"{ROOT}/{directory}")
        for file in subDir:
            if os.path.isdir(f"{ROOT}/{directory}/{file}"):
                generate_file()
