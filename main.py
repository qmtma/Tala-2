import os
import csv

ROOT = 'courses'
courses = os.listdir(ROOT)


def getUsernames():
    with open(f"{ROOT}/{course}/{level}/classList.csv", 'r') as csvFile:
        userNames = csvFile.read().strip(',').split()
    csvFile.close()
    del userNames[0]
    return userNames
    pass


def getClassInfo():
    with open(f"{ROOT}/{course}/{level}/classInfo.csv", 'r') as csvFile:
        classData = csv.reader(csvFile, delimiter=',')
        for row in classData:
            if row[0].isdigit():
                classDuration = row[0]
            if row[1].isdigit():
                classPerSem = row[1]
        CI = [classDuration,classPerSem]
        csvFile.close()
        return CI
    pass


def getBBabsence():
    BBAbsence=[]
    with open(f"{ROOT}/{course}/{level}/attendance_BB.csv", 'r') as csvFile:
        attendanceBB = csv.reader(csvFile, delimiter=',')
        for row in attendanceBB:
            if row[1] in userList:
                BBcount =0
                for item in row:
                    if item == 'Absent':
                        BBcount+=1
                BBAbsence.append(BBcount)
        return BBAbsence
    pass


def getAttendanceLists():
    AttendanceLists=[]
    FileCount = 0
    for file in AD_Files:
        if file.startswith("Lecture"):
            AttendanceLists.append(file)
            FileCount += 1
    return AttendanceLists, FileCount
    pass


def getCUabsence():
    CUList={}
    CUAbsence =[]
    for name in userList:
        CUList.update({name:0})
    for lecture in lectures:
        with open(f"{ROOT}/{course}/{level}/{lecture}") as csvFile:
            CUData = csv.reader(csvFile, delimiter=",")
            for row in CUData:
                for user in CUList:
                    if user == row[1]:
                        entry = CUList.get(user)
                        entry +=1
                        attendedTime = row[6]
                        attendedH = attendedTime[0]
                        attendedM = attendedTime[2:4]
                        attendedM = int(attendedM) + (int(attendedH) * 60)
                        if int(attendedM) < (0.75 * int(CI[0])):
                            entry -= 1
                        CUList.update({user:entry})
    for user in CUList:
        entry = CUList.get(user)
        entry = AttendanceTaken - entry
        CUAbsence.append(entry)
    return CUAbsence


    pass


def getCUAPer():
    i=0
    list = []
    for user in userList:
        entry = (float(CUAbsence[i])/float(AttendanceTaken))*100
        entry = round(entry,2)
        list.append(entry)
        i+=1
    return list
    pass


def getBBA_per():
    list = []
    i=0
    for user in userList:
        entry = (int(BBAbsence[i])/float(AttendanceTaken))*100
        i+=1
        list.append(round(entry,2))
    return list
    pass


def getCCUAbsence():
    list = []
    i=0
    for user in userList:
        entry = (int(CUAbsence[i])/float(CI[1]))*100
        i+=1
        list.append(round(entry,2))
    return list
    pass


def getCUStatus():
    list=[]
    i=0
    for user in userList:
        if float(C_CU_Absence[i])>25:
            list.append("Dismissed")
        elif float(C_CU_Absence[i])<25 and float(C_CU_Absence[i])>15:
            list.append("Warning")
        else: list.append("OK")
        i+=1
    return list
    pass


def getCBBAbsence():
    list=[]
    i=0
    for user in userList:
        entry = (int(BBAbsence[i])/float(CI[1]))*100
        i+=1
        list.append(round(entry,2))
    return list
    pass


def getBBStatus():
    list = []
    i = 0
    for user in userList:
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
    pass


for course in courses:
    if os.path.isdir(f"{ROOT}/{course}"):
        AttendanceData = os.listdir(f"{ROOT}/{course}")
        for level in AttendanceData:
            if os.path.isdir(f"{ROOT}/{course}/{level}"):
                AD_Files = os.listdir(f"{ROOT}/{course}/{level}")
                userList = getUsernames()
                CI = getClassInfo()
                lectures , AttendanceTaken = getAttendanceLists()
                BBAbsence = getBBabsence()
                CUAbsence = getCUabsence()
                CUA_Per = getCUAPer()
                BBA_per = getBBA_per()
                C_CU_Absence = getCCUAbsence()
                CU_Status = getCUStatus()
                C_BB_Absence = getCBBAbsence()
                BB_Status = getBBStatus()
                with open(f"{ROOT}/{course}/CUvsBBReport_{course}_{level}.txt",'w') as WriteFile:

                    WriteFile.write("Username       |CU_Absance No | BB_Absance No | CU_Absance% | BB_Absance% | C_CU_Absance% | CU_Status | C_BB_Absance% | BB_Status\n")
                    i=0
                    for user in userList:
                        len0 = len("Username       ")-len(user)
                        len1 = len("CU_Absance No ")-len(str(CUAbsence[i]))
                        len2 = len(" BB_Absance No ")-len(str(BBAbsence[i]))
                        len3 = len(" CU_Absance% ")-len(str(CUA_Per[i]))
                        len4 = len(" BB_Absance% ")- len(str(BBA_per[i]))
                        len5 = len(" C_CU_Absance% ")- len(str(C_CU_Absence[i]))
                        len6 = len(" CU_Status ") - len(CU_Status[i])
                        len7 = len(" C_BB_Absance% ") - len(str(C_BB_Absence[i]))
                        len8 = len(" BB_Status") - len(BB_Status[i])
                        WriteFile.writelines(f"{user}{(len0*' ')}|{CUAbsence[i]}{(len1*' ')}|{BBAbsence[i]}{(len2*' ')}|{CUA_Per[i]}{(len3*' ')}|{BBA_per[i]}{(len4*' ')}|{C_CU_Absence[i]}{(len5*' ')}|{CU_Status[i]}{(len6*' ')}|{C_BB_Absence[i]}{(len7*' ')}|{BB_Status[i]}\n")
                        i+=1
