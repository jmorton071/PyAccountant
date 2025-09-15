"""
Author: 
This code was created by Joe Morton

Description:
This code goes through General Journal Excel files to find any errors in the debits/credits
It informs users what the error is (the difference in amounts) and in which transaction

Credits:
ChatGPT was used for assistance with debugging
W3Schools, StackOverflow, and Python websites were used for help with syntax

Future Plans:
I plan to extend this program to make use of Linked Lists rather than enormous lists to store data. 
I'd also like the system to suggest fixes to the user when it encounters errors in the journals.
"""

#Import needed classes
import csv
import os

#Main method
def main():
    #Initialize needed local variables
    file = ""
    journalType = ""
    ask = True
    transDebitTotal = 0.0
    transCreditTotal = 0.0
    lineNum = 1
    #Greeting message for user
    #Prompt user for an input
    print("Welcome to PyAccountant! Where prompted, please enter a file name. Please ONLY input a .csv file.")
    print("Type HELP for help.")
    print("")
    #Loop to continue asking user for file name until a valid file name is inputted.
    while(ask):
        #Gets file name
        file = input("What is your file's name? ")
        #Checks if file has a csv type ending
        #Skips this step if the user has asked for help
        if(not(file.endswith(".csv")) and file != "HELP"):
            #Adds a csv ending if there is no csv ending found
            file += ".csv"
        #Checks if file exists
        if(os.path.exists(file)):
            #Ends asking user
            ask = False
            #Gets type of journal, edits response for easier use later on
            journalType = input("What type of journal is your file? ").lower()
            journalType.removesuffix(" journal")
            #Checks journal type, uses proper method
            if(journalType == "general"):
                #Informs user
                print(f"Opening {file} as General Journal.")
                print("")
                #Calls method
                generalJournal(file, transDebitTotal, transCreditTotal, lineNum)
            elif(journalType == "cash receipts" or journalType == "purchases" or journalType == "cash disbursements" or journalType == "sales"):
                print(f"Opening {file} as {journalType.upper()} Journal.")
                print("")
                specialJournal(file, transDebitTotal, transCreditTotal, lineNum, journalType)
            #Informs user there is an error with their input
            else:
                print("PyAccountant does not support this journal type.")
        #Assists user
        elif(file == "HELP"):
            #Assists the user with any challenges they may be facing in the use of the program. 
            #Open to expansion if new difficulties are found
            print("PyAccountant's file name recognition is case sensitive. Please ensure your file name is properly capitalized before submitting. ")
            print("PyAccountant only accepts .csv type files, please ensure your file is a .csv file.")
            print("PyAccountant requires your file to be in the same folder as the PyAccountant code, please ensure it is.")
            print("If none of this helps, kill the terminal and restart the program or close and re-open the code.")
        #Informs user their response is invalid
        else:
            print("Invalid file name! Please try again! Type HELP for assitance. ")        

#Method for general journals
def generalJournal(fileName, transDebitTotal, transCreditTotal, lineNum):
    #Opens file in read mode, allows use with the name "file"
    with open(fileName, "r") as file:
        #Initialize needed local variables
        lineReader = csv.reader(file)
        location = 0
        transactionNum = 0
        debitList = []
        creditList = []
        #Reads through all lines in the reader
        for line in lineReader:
            #This is the usual line for the heading PyAccountant will need: the first two lines are usually used for company name, date, etc. 
            if(lineNum == 3):
                #Assigns the line as a list to lineList for parsing                 
                lineList = line
                #Reads through all elements in line list until it finds debit to save location
                for i in range(len(lineList)):
                    #When debit has been found, saves the location for use in the calculations
                    if("Debit" in lineList[i]):
                        location = i  
                #Backup in case location is not able to be found by PyAccountant
                if(location == 0):
                    #Informs user nothing could be found
                    print("PyAccountant couldn't find a header.")
                    #Asks user for input of debit column
                    location = -1 + int(input("Which column of your file is the DEBIT column? "))
                    #Informs user if input is invalid
                    while(location < 0 or location > len(lineList[0])):
                        print(f"Error {location} is an invalid number.")
                        location = int(input("Please input a valid column. "))
            #Runs through the rest of the lines saves debit locations
            elif(lineNum > 3):
                #Debits are saved with debit location
                debitList.append(line[location])
                #Credits saved with debit location plus one, one column to the right
                creditList.append(line[location+1])
            #Line num increases
            lineNum += 1
        #Runs through all values in debit list
        for i in range(len(debitList)):
            #Checks if value is blank, if it is not continues code.
            if(debitList[i] != " "):
                #Tries to add value to debit total, adds nothing if there is no applicable number
                try:
                    transDebitTotal += float(debitList[i].replace(",", ""))
                except:
                    debitList[i] = ""
            #Does same for credits
            if(creditList[i] != " "):
                try:
                    transCreditTotal += float(creditList[i].replace(",", ""))
                except:
                    creditList[i] = ""
            #Checks for blank debit and credit (end of transaction)
            if(creditList[i] == "" and debitList[i] == ""):
                #Adds one to transaction number
                transactionNum += 1
                #Checks if debits = credits
                if(transCreditTotal != transDebitTotal):
                    #Takes absolute value of difference
                    diff = abs(float(transDebitTotal - transCreditTotal))
                    #Informs user of difference and in which transaction
                    print(f"Error in transaction {transactionNum}. Debit total {transDebitTotal} is not equal to credit total {transCreditTotal}.") 
                    print(f"There is a difference of ${diff}.")
                    print("")
                #Resets totals
                transDebitTotal = 0.0 
                transCreditTotal = 0.0
        #Informs user program is done reading file
        print("PyAccountant has finished reading your file.")

#Method for special journals
def specialJournal(fileName, transDebit, transCredit, lineNum, journalType):
    #Opens file as file in read mode
    with open(fileName, "r") as file:
        #Initializes needed variables
        lineReader = csv.reader(file)
        drLocations = []
        crLocations = []
        transactionNum = 0
        #Goes through lines in the file
        for line in lineReader:
            #Checks if it is header line
            if(lineNum == 3):
                #Assigns line to lineList
                lineList = line
                #Iterates through all values in the list
                for i in range(len(lineList)):
                    #i assigned to location
                    location = i
                    #Takes value at index of i in line list
                    index = lineList[i].lower()
                    #Checks journal type
                    if(journalType == "cash receipts"):
                        #Checks for keywords of debits
                        if index == "cash" or index == "sales discount" or "debit" in index:
                            #Adds debit location to debit list
                            drLocations.append(location)
                        #Checks for keywords for credits
                        elif index == "accounts recievable" or index == "sales revenue" or "credit" in index:
                            crLocations.append(location)
                    elif(journalType == "sales"):
                        if index == "accounts recievable" or index == "cost of goods sold" or "debit" in index:
                            drLocations.append(location)
                        elif index == "sales" or index == "sales tax payable" or index == "inventory" or "credit" in index:
                            crLocations.append(location)
                    elif(journalType == "cash disbursements"):
                        if index == "accounts payable" or index == "supplies" or "debit" in index:
                            drLocations.append(location)
                        elif index == "cash" or index == "inventory" or index == "purchases discount" or "credit" in index:
                            crLocations.append(location)
                    elif(journalType == "purchases"):
                        if(index == "inventory" or "supplies" in index or "debit" in index):
                            drLocations.append(location)
                        elif(index == "accounts payable" or "credit" in index):
                            crLocations.append(location)
                #Sends message if there is no header that can be found 
                if(len(crLocations) == 0 or len(drLocations) == 0):
                    print("PyAccountant couldn't find a header.")
                    askForDebit = True
                    askForCredit = True
                    #Asks for debit values until user no longer wants to provide them
                    while(askForDebit):
                        #Asks for values one at a time
                        location = -1 + int(input("Enter ONE column of your file that is a DEBIT column. "))
                        while(location < 0 or location > len(lineList[0])):
                            print(f"Error {location} is an invalid number.")
                            location = int(input("Please input a valid column. "))
                        drLocations.append(location)
                        #Asks if they would like the continue
                        uContinue = input("Y or N, are there more debit columns you would like to input? ").upper()
                        if(uContinue == "N"):
                            askForDebit = False
                    while(askForCredit):
                        location = -1 + int(input("Enter ONE column of your file that is a CREDIT column. "))
                        while(location < 0 or location > len(lineList[0])):
                            print(f"Error {location} is an invalid number.")
                            location = int(input("Please input a valid column. "))
                        crLocations.append(location)
                        uContinue = input("Y or N, are there more credit columns you would like to input? ").upper()
                        if(uContinue == "N"):
                            ask = False
            #Runs through all lines in line list to find 
            elif(lineNum > 3):
                #Adds one to transaction number
                transactionNum += 1
                #Goes through all debit locations
                for location in drLocations:
                    #Checks if there is a number at each location
                    try:
                        #If there is, parses the float from the string, removing the "," character.
                        #Adds this parsed float to the debit total for the transaction.
                        transDebit += float(line[location].replace(",", ""))
                    #If not, moves on
                    except:
                        line[location] = ""
                for location in crLocations:
                    try:
                        transCredit += float(line[location].replace(",", ""))
                    except:
                        line[location] = ""
                #Checks that the two totals are equal
                if(transCredit != transDebit):
                    #Finds the difference
                    diff = abs(transDebit - transCredit)
                    #Informs user that there is an error in the transaction
                    print(f"Error in transaction {transactionNum}. Debit total {transDebit} is not equal to credit total {transCredit}.")
                    print(f"There is a difference of ${diff}.")
                    print("")
                #Resets totals
                transCredit = 0.0
                transDebit = 0.0
            #Adds one to line number
            lineNum += 1 
        #Informs user program is done reading the file.
        print("PyAccountant has finished reading your file.")

#Call main to start the program
main()