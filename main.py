import os

ROOT = 'courses'
courses = os.listdir(ROOT)

def users_BBA():
    Read = open(dir2 + "/classList.csv", 'r')
    userNames = Read.read().strip(',').split()
    Read.close()
    del userNames[0]
    BBAbsence = []
    csvFile = open(dir2 + "/attendance_BB.csv", 'r')
    attendanceBB = []
    for line in csvFile:
        row = line.split(',')
        attendanceBB.append(row)
    for row in attendanceBB:
        if row[1] in userNames:
            BBcount = 0
            for item in row:
                if item == 'Absent':
                    BBcount += 1
            BBAbsence.append(BBcount)
    return userNames, BBAbsence

def class_info():
    Read = open(dir2 +"/classInfo.csv", 'r')
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


def sheets(AD_Files):
    sheets=[]
    Count = 0
    for file in AD_Files:
        if file.startswith("Lecture"):
            sheets.append(file)
            Count += 1
    return sheets, Count

def CU(All_users,lectures,CD,lectures_count):
    CUList=[]
    CUAbsence =[]
    for name in All_users:
        CUList.append(0)
    for lecture in lectures:
        dir3 = os.path.join(dir2, lecture)
        csvFile =  open(dir3)
        CUData = []
        for line in csvFile:
            row = line.split(',')
            CUData.append(row)
        for row in CUData:
            i = 0
            for user in All_users:
                if user == row[1]:
                    entry = CUList[i]
                    entry += 1
                    attendedTime = row[6]
                    attendedH = attendedTime[0]
                    attendedM = attendedTime[2:4]
                    attendedM = int(attendedM) + (int(attendedH) * 60)
                    if int(attendedM) < (0.75 * int(CD[0])):
                        entry -= 1
                    CUList[i] = entry

                i += 1
    i = 0
    for user in CUList:
        entry = CUList[i]
        entry = lectures_count - entry
        CUAbsence.append(entry)
        i+=1
    list2 = []
    i=0
    for user in All_users:
        entry = (float(CUAbsence[i]) / float(lectures_count)) * 100
        entry = format(entry,'.2f')
        list2.append(entry)
        i += 1
    return CUAbsence, list2

def BB_percentage(All_users,Black_board,lectures_count):
    list = []
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(lectures_count))*100
        i+=1
        list.append(format(entry,'.2f'))
    return list

def CCU(All_users,collaborate_ultra,CD):
    list = []
    list2 = []
    i=0
    for user in All_users:
        entry = (int(collaborate_ultra[i])/float(CD[1]))*100
        list.append(round(entry,2))
        if float(list[i]) > 25:
            list2.append("Dismissed")
        elif float(list[i]) < 25 and float(list[i]) > 15:
            list2.append("Warning")
        else:
            list2.append("OK")
        i += 1
    return list, list2

def CBB(All_users,Black_board,CD):
    list=[]
    list2 = []
    i=0
    for user in All_users:
        entry = (int(Black_board[i])/float(CD[1]))*100
        list.append(round(entry,2))
        if float(list[i])>25:
            entry = "Dismissed"
            list2.append(entry)
        elif float(list[i])<25 and float(list[i])>15:
            entry = "Warning"
            list2.append(entry)
        else:
            entry = "OK"
            list2.append(entry)
        i += 1
    return list, list2

def sheet(All_users,Black_board,collaborate_ultra,C_percentage,B_pecentage,C_C_Ultra,C_Status,C_BB_Absence,general_status):
    WriteFile = open(ROOT + "/"+ directory+ "/CUvsBBReport_"+directory+"_"+file+".txt", 'w')

    WriteFile.write(
        "Username       |CU_Absance | BB_Absance | CU_Absance% | BB_Absance% | C_CU_Absance% | CU_Status | C_BB_Absance% | BB_Status|\n")
    i = 0
    WriteFile.write((str('-')*124) +  "\n")
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
            (str('-') * 124) + '\n')
    WriteFile.close()

def generate_file():
    AD_Files = os.listdir(dir2)
    All_users, Black_board = users_BBA()
    CD = class_info()
    lectures, lectures_count = sheets(AD_Files)
    collaborate_ultra,C_percentage = CU(All_users,lectures,CD,lectures_count)
    B_pecentage = BB_percentage(All_users,Black_board,lectures_count)
    C_C_Ultra, C_Status = CCU(All_users,collaborate_ultra,CD)
    C_BB_Absence,general_status = CBB(All_users,Black_board,CD)
    sheet(All_users,Black_board,collaborate_ultra,C_percentage,B_pecentage,C_C_Ultra,C_Status,C_BB_Absence,general_status)
    

for directory in courses:
    dir1 = os.path.join(ROOT,directory)
    if os.path.isdir(dir1):
        subDir = os.listdir(dir1)
        for file in subDir:
            dir2 = os.path.join(dir1, file)
            if os.path.isdir(dir2):
                generate_file()
