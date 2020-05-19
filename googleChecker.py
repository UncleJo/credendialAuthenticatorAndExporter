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


def getcreds(add):
    print("Opening File...")
    data = open(add, "r")
    print("File Opened Successfully. Reading data...")
    data = data.read()
    print("Data Read successfully, Parsing.... please wait.")
    bulk = data.split('\n')
    print("Parsed Successfully. Detecting emails and password seperated by unique identifier ':' and '|' . . .\n")

    failure = 0
    success = 0
    for i in range(0, len(bulk)):
        tempData = bulk[i]
        if ':' in tempData:
            if '|' in tempData:
                print("Faliure at line ", i, ". 2 unique identifier detected.")
                print("Contents - ", tempData, "\n")
                failure = failure + 1
            else:
                tempDataCred = tempData.split(':')
                if len(tempDataCred) > 2:
                    print("Faliure at line ", i, ", 2 unique identifier detected.")
                    print("Contents - ", tempData, "\n")
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1

        elif '|' in tempData:
            if ':' in tempData:
                print("Faliure at line ", i, ". 2 unique identifier detected.")
                print("Contents - ", tempData, "\n")
                failure = failure + 1
            else:
                tempDataCred = tempData.split('|')
                if len(tempDataCred) > 2:
                    print("Faliure at line ", i, ", 2 unique identifier detected.")
                    print("Contents - %s \n", tempData)
                    failure = failure + 1
                else:
                    email.append(tempDataCred[0])
                    password.append(tempDataCred[1])
                    success = success + 1
        else:
            print("Failure at line ", i,",no unique identifier found.")
            print("Contents - ", tempData,"\n")
            failure = failure + 1

    print("Failure - ", failure)
    print("Success - ", success)
    print("\n\nDetection Successful with the stats mentioned above. Validating the integrity of all email and "
          "password...")
    validateemailpassword()


def validateemailpassword():
    if len(email) != len(password):
        print("Length of email and password arrays don't match, sum ting wong with yo file or something man.")
        setfileadress()
    for i in range(0, len(password)):
        tempDataEmail = email[i]
        if '@' not in tempDataEmail:
            print(i)
            email.pop(i)
            password.pop(i)
    print("File Validated, Total credentials is ", len(email))


setfileadress()
