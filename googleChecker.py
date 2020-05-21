from datetime import date

fileAddress = ""
email = []
password = []
gmailmail = []
gmailpassword = []
yahoomail = []
yahoopassword = []
othermail = []
otherpassword = []


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
    f.close()


def getcreds(add):
    print("Opening File...")
    data = open(add, "r")
    print("File Opened Successfully. Reading data... All errors will be stored in a file Named ErrorLog.txt, "
          "find it in the folder where the script file is")
    data = data.read()
    print("Data Read successfully, Parsing.... please wait.")
    bulk = data.split('\n')
    print("Parsed Successfully. Detecting emails and password seperated by unique identifier ':' , '|' , '::' . .")

    failure = 0
    success = 0
    for i in range(0, len(bulk)):
        tempData = bulk[i]
        if '::' in tempData:
            if '|' in tempData:
                errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                failure = failure + 1
            else:
                tempDataCred = tempData.split('::')
                if '@' not in tempDataCred[0]:
                    errorregister(4, "Email does not have an @. bro is your combolist drunk? at index {line}".format(
                        line=i), tempDataCred[0])
                    failure = failure + 1
                elif len(tempDataCred) > 2:
                    errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1
        elif ':' in tempData:
            if '|' in tempData:
                errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                failure = failure + 1
            else:
                tempDataCred = tempData.split(':')
                if '@' not in tempDataCred[0]:
                    errorregister(4, "Email does not have an @. bro is your combolist drunk? at index {line}".format(
                        line=i), tempDataCred[0])
                    failure = failure + 1
                elif len(tempDataCred) > 2:
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
                if '@' not in tempDataCred[0]:
                    errorregister(4, "Email does not have an @. bro is your combolist drunk? at index {line}".format(
                        line=i), tempDataCred[0])
                    failure = failure + 1
                elif len(tempDataCred) > 2:
                    errorregister(1, "Faliure at line {line}. 2 unique identifier detected.".format(line=i), tempData)
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1
        else:
            errorregister(2, "Faliure at line {line}. no unique identifier detected.".format(line=i), tempData)
            failure = failure + 1

    print("\nFailure - ", failure)
    print("Success - ", success)
    print("\nDetection Successful with the stats mentioned above. Validating the integrity of all email and "
          "password...")
    if len(email) != len(password):
        print("Length of email and password arrays don't match, sum ting wong with yo file or something man.")
        errorregister(3, "Fatal Error - Length of email and password arrays don't match, sum ting wong with yo file "
                         "or something man.", " ")
        setfileadress()
    else:
        print("File Validated, Total credentials is ", len(email))
        print("Starting Credential Segregation....")
        credssegregator()


def credssegregator():
    for i in range(0, len(email)):
        tempDataEmail = email[i]
        if '@gmail.com' in tempDataEmail:
            gmailmail.append(email[i])
            gmailpassword.append(password[i])
        elif '@yahoo.' in tempDataEmail:
            yahoomail.append(email[i])
            yahoopassword.append(password[i])
        else:
            othermail.append(email[i])
            otherpassword.append(password[i])

    print("\n\nTotal Gmail Accounts - ", len(gmailmail))
    print("Total Yahoo Accounts - ", len(yahoopassword))
    print("Others - ", len(otherpassword))


setfileadress()
