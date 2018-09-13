zero2 = ["INDI","FAM"]
zero1 = ["HEAD","TRLR","NOTE"]
one = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV"]
two = ["DATE"]

gedFile = open("/Users/Ksekh/Downloads/proj02test.ged","r")
with gedFile:
    for line in gedFile:
        gedSet = line.strip().split()
        print("--> " + line, end=''),

        if gedSet[0] == "0":
            if len(gedSet) == 3 and gedSet[2] in zero2:
                print("<-- " + gedSet[0] + "|" + gedSet[2] + "|" + "Y" + "|" + gedSet[1])
            elif len(gedSet) >= 2 and gedSet[1] in zero1:
                print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "Y" + "|" + " ".join(gedSet[2:]))
            else:
                print ("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "N" + "|" + " ".join(gedSet[2:]))
        elif gedSet [0] == "1":
            if len(gedSet) >= 2 and gedSet[1] in one:
                print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "Y" + "|" + " ".join(gedSet[2:]))
            else:
                print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "N" + "|" + " ".join(gedSet[2:]))
        elif gedSet[0] == "2":
            if len(gedSet) >= 2 and gedSet[1] in two:
                print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "Y" + "|" + " ".join(gedSet[2:]))
            else:
                print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "N" + "|" + " ".join(gedSet[2:]))
        else:
            print("<-- " + gedSet[0] + "|" + gedSet[1] + "|" + "N" + "|" + " ".join(gedSet[2:]))
