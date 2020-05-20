from datetime import date

fileAddress = ""
email = []
password = []


def setfileadress():
    print("Enter file Address")
    fileAddress = str(input())
    fileExistence = checkfileexist(fileAddress)

    if fileExistence is True:
        print("File address Verified! Starting DataMining ")
        getcreds(fileAddress)
    else:
        print("File not found, please try again\n\n")
        setfileadress()


def checkfileexist(address):
    try:
        open(address, 'r')
        return True
    except IOError:
        return False


def errorregister(errorcode, errormessage, contents):
    f = open("ErrorLog.txt", "a+")
    today = date.today()
    timestamp = today.strftime("%b-%d-%Y")
    data = "<{datetime}> - Error Code - {errcode}\nMessage - {msg}\nContents - {contents}\n\n".format(
        datetime=timestamp, errcode=errorcode, msg=errormessage, contents=contents)
    f.write(data)


def getcreds(add):
    print("Opening File...")
    data = open(add, "r")
    print("File Opened Successfully. Reading data... All errors will be stored in a file Named ErrorLog.txt, "
          "find it in the folder where the script file is")
    data = data.read()
    print("Data Read successfully, Parsing.... please wait.")
    bulk = data.split('\n')
    print("Parsed Successfully. Detecting emails and password seperated by unique identifier ':' and '|' . . .")

    failure = 0
    success = 0
    for i in range(0, len(bulk)):
        tempData = bulk[i]
        if ':' in tempData:
            if '|' in tempData:
                errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                failure = failure + 1
            else:
                tempDataCred = tempData.split(':')
                if len(tempDataCred) > 2:
                    errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1

        elif '|' in tempData:
            if ':' in tempData:
                errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                failure = failure + 1
            else:
                tempDataCred = tempData.split('|')
                if len(tempDataCred) > 2:
                    errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1
        else:
            errorregister(2, "Faliure at line {line}. no unique identifier detected.".format(line=i), tempData)
            failure = failure + 1

    print("Failure - ", failure)
    print("Success - ", success)
    print("\n\nDetection Successful with the stats mentioned above. Validating the integrity of all email and "
          "password...")
    validateemailpassword()


def validateemailpassword():
    if len(email) != len(password):
        print("Length of email and password arrays don't match, sum ting wong with yo file or something man.")
        errorregister(3, "Fatal Error - Length of email and password arrays don't match, sum ting wong with yo file "
                         "or something man.", " ")
        setfileadress()
    for i in range(0, len(password)):
        tempDataEmail = email[i]
        if '@' not in tempDataEmail:
            errorregister(4, "Email does not have an @. bro is your combolist drunk? at index {line}".format(line=i),
                          email[i])
            email.pop(i)
            password.pop(i)
    print("File Validated, Total credentials is ", len(email))


setfileadress()
