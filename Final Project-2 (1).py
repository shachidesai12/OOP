#Name: Shachi Desai
#Student ID: 100947068
#INFR2141 - Final Project 
#Aug 1, 2024
#Purpose: Develop a GUI that implements six different types of encryption methods 
##########################################################################################################################################################

from tkinter import *
import random
import math

#Class to store the message
class Message:
    #Variable to ensure rsa_key is only created once and then stored in a dictionary 
    called = False
    rsa_key = {}

    def __init__(self,message):
        self.message = message
        #Call method to find RSA Key
        if Message.called == False:
            self.find_rsa_key()
            

#Class to call and execute encryption and decryption methods based on user input
class plainTextMsg(Message):
    #Method to check user input and call correct method accordingly
    def encryption(self,method,type):
        if (method == "Substitution Cipher") and (type == "E"):
            return self.sub_cipher()
        elif (method == "Substitution Cipher") and (type == "D"):
            return self.de_sub_cipher(self.message)
        elif (method == "Playfair Cipher") and (type == "E"):
            return self.play_cipher()
        elif (method == "Playfair Cipher") and (type == "D"):
            return self.de_play_cipher()
        elif (method == "Caesar Cipher") and (type == "E"):
            return self.caesar_cipher()
        elif (method == "Caesar Cipher") and (type == "D"):
            return self.de_caesar_cipher()
        elif (method == "Transposition Cipher") and (type == "E"):
            return self.trans_cipher(self.message)
        elif (method == "Transposition Cipher") and (type == "D"):
            return self.de_trans_cipher(self.message)
        elif (method == "Product Cipher") and (type == "E"):
            return self.product_cipher()
        elif (method == "Product Cipher") and (type == "D"):
            return self.de_product_cipher()
        elif (method == "RSA") and (type == "E"):
            return self.rsa_cipher()
        elif (method == "RSA") and (type == "D"):
            return self.de_rsa_cipher()

    #Encryption method for substitution cipher    
    def sub_cipher(self):
        #Convert message to list 
            self.List = list(self.message)
        
            #Initialize original alphabet
            alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.','!']
    
            #Create a key 
            key = ['!','o','J','v','f','U','b','M','q','g','T','B','H','P','z','A','K','O','d','s','C','W','S','n','N','R','y','w','h','j','u','Q','p','m','.','l','I','E','k',' ','i','r','V','F','X','a','e','Y','Z','L','c','G','x','D','t']
        
            #Create an encrypted list, replacing the letter in the message with the key
            self.coded = [key[alpha.index(c)]for c in self.message]
            
            #Use join to turn encrypted list back into a string
            str1 = ''
            self.coded = str1.join(self.coded)
            
            return self.coded #Return the encrypted message
    
    #Encryption method for playfair cipher
    def play_cipher(self):
        #Create the key grid
        key = [['A','B','C','D','E'],
              ['F','G','H','I','K'],
              ['L','M','N','O','P'],
              ['Q','R','S','T','U'],
              ['V','W','X','Y','Z']]
        
        #Remove spaces from the message and create empty list
        self.sentence = self.message.upper() #Convert string to uppercase to match key
        self.sentence = self.sentence.replace(" ","")
        
        #Replace J with I as playfair doesn't use the letter J
        self.sentence = self.sentence.replace("J","I")
        
        #Create an empty list to store encrypted message
        encryptedList = []

        #Convert sentence to pairs 
        listofPairs = self.convertToPairs(self.sentence)

        #Find row and column of pair to determone which method to use 
        for pair in listofPairs: #For each pair in the list 
            #check key
            for i in range(5): #For each row in the key
                for j in range(5):
                    if key[i][j] == pair[0]:
                        firstValRow,firstValCol = i,j #If first letter in pair found in key matrix return i and j location values
                    if key [i][j] == pair[1]:
                        secondValRow,secondValCol = i,j #If second letter in pair found in key matrix return i and j location values
            #Check to see if in the same row
            if firstValRow == secondValRow:
                self.checkRows(firstValRow,firstValCol,secondValRow,secondValCol,key, encryptedList)
            #Check to see if in the same column
            elif firstValCol == secondValCol:
                self.checkCol(firstValRow,firstValCol,secondValRow,secondValCol,key, encryptedList)
            #If not same row or column, use box method
            else:
                self.corner(firstValRow,firstValCol,secondValRow,secondValCol,key, encryptedList)

        #Convert final List to string
        str1= ''
        encryptedSentence = str1.join(encryptedList)
        
        return encryptedSentence #Return encrypted message

    #Method to convert string to pairs (Aid in playfair cipher)
    def convertToPairs(self,sentence):
        #initialize list to store the pairs 
        pairs = []
        tempPair = []

        #Go from 0 to end of sentence, increase by 2 (We want pairs) each time
        for i in range(0,len(self.sentence),2):
            pairs.append(self.sentence[i:i+2]) #Sentence separated into pairs is now in pairs[]
    
        #Replace duplicate letter with X 
        for i in range (0,len(pairs)):
            pair = pairs[i] #Look at each pair individually
            #if a letter is single pair it up with x 
            if len(pair) == 1:
                a = pair[0]
                b = 'x'
            else: 
                #Set each letter in pair to a and b 
                a = pair[0]
                b = pair[1]
                #If there is a double letter replace the second one with x 
                if a == b:
                    b = 'x'

            #Append the a and b into temporary list
            tempPair.append(a)
            tempPair.append(b)

        #Convert temporary list to string
        str1 = ''
        tempPair = str1.join(tempPair)
        tempPair = tempPair.upper()

        #Separate temporaryList into pairs again, empty the pairs list first  
        pairs.clear()

        for i in range(0,len(tempPair),2):
            pairs.append(tempPair[i:i+2]) 
        return pairs #Return the new list of pairs 

    #Method to deal with letters in same row (Aid in playfair cipher)
    def checkRows(self,oneRow,oneCol,twoRow,twoCol,key, encryptedList):
    
         #Take care of wrap around if letter in last spot
         if oneCol == 4:
             oneCol = -1 #By setting it to -1, when 1 will be added it will be wrapped around to position 0
         if twoCol == 4:
             twoCol = -1

         #Move each letter one to the right, keeping the rows the same
         encrypt = key[oneRow][oneCol+1] + key[twoRow][twoCol+1]

         #Add the encrypted pair to the encrypyted list
         encryptedList.append(encrypt)
         
         return encryptedList #Return the encrypted message

    #Method to deal with letters in same column (Aid in playfair cipher)
    def checkCol(self,oneRow,oneCol,twoRow,twoCol,key, encryptedList):

        #Take care of wrap around if letter in last 
        if oneRow == 4:
            oneRow = -1 #By setting it to -1, when 1 will be added it will be wrapped around to position 0
        if twoRow == 4:
            twoRow = -1  

        #Move each letter one down, keeping the columns the same
        encrypt = key[oneRow+1][oneCol] + key[twoRow+1][twoCol]

        #Add the encrypted pair to the encrypyted list
        encryptedList.append(encrypt)
        
        return encryptedList #Return encrypted message

    #Method to deal with letters not in same row or column(Aid in playfair cipher)
    def corner(self,oneRow,oneCol,twoRow,twoCol,key, encryptedList):
        
        #Rows stay the same only switching the column value
        encrypt = key[oneRow][twoCol] + key[twoRow][oneCol]
        
        #Add the encrypted pair to the encrypyted list
        encryptedList.append(encrypt)
        
        return encryptedList #Return encrypted message
        
    #Encryption method for caesar cipher
    def caesar_cipher(self):
        #Change sentence to lowercase 
        sentence = self.message.lower()

        #Initialize alphabet
        self.alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        #Initialize key 
        self.key = 3
        #Initialize empty list for encryption
        self.encrypted = []

        #Iterate through the message
        for char in sentence:
            isLetter = char.isalpha() #Check if character is a letter
            if isLetter == True:
                index = self.alpha.index(char)   #Find index of characted in alpha list
                #Account for wrap around
                if index == 23:
                    index = -3
                elif index == 24: 
                    index = -2
                elif index == 25:
                    index = -1
                self.encrypted.append(self.alpha[index+self.key])  #Append letter at index + key to encryption
            else:
                self.encrypted.append(char) #If character not letter, append as is 
        
        #Use join to turn encrypted list back into a string
            str1 = ''
            self.cipherText = str1.join(self.encrypted)

        return self.cipherText #Return encrypted message

    #Encryption method for transposition cipher   
    def trans_cipher(self,message):
        #Initialize message and empty list for encrypted message
        self.sentence = message
        self.encrypted = []

        #Determine key to determine number of columns
        self.key = 4

        #Start reading at column 1 then move to the next
        for i in range(self.key):
            j = i
            while j < len(self.sentence):
                self.encrypted.append(self.sentence[j])
                j +=self.key #Since key represents # of columns and we are reading down the column 
        
         #Use join to turn encrypted list back into a string
        str1 = ''
        self.cipherText = str1.join(self.encrypted)

        return self.cipherText #Return encrypted message
         
    #Encryption method for product cipher (Consists of substitution and transposition)
    def product_cipher(self):
        #Call method for substitution cipher 
        subCipher = self.sub_cipher()

        #Call method for transposition using output of substitution cipher
        return self.trans_cipher(subCipher)

    #Method to find RSA public and private key
    def find_rsa_key(self):
        #Find 2 prime numbers p and q 
        p = self.getPrimeNumber()
        q = self.getPrimeNumber()

        #Make sure they are 2 different prime numbers 
        if p == q:
            q = self.getPrimeNumber() #If came call method again

        #Find n
        self.n = p*q

        #Find phi(n)
        self.phi = (p-1)*(q-1)

        #Account for possible value error when finding public key
        try:
            #Find public key: e 
            self.e = random.randint(2,self.phi)

            #Need to make sure e is not coprime to phi
            #co-prime numbers have their gcd as 1 
            #We need to make sure they don't have 1 as gcd
            while math.gcd(self.e, self.phi) != 1:
                self.e = random.randint(2,self.phi)
        except ValueError:
            self.find_rsa_key()

        #Get private key: e*d = 1 mod phi(n)
        self.d = pow(self.e,-1,self.phi)
        
        #Put key values in dictionary to access when needed 
        Message.rsa_key = {'e':self.e,'n':self.n,'d':self.d}
        #Change called to True so that key is not created again 
        Message.called = True

    #Encryption method for RSA Cipher
    def rsa_cipher(self):
        #Get the key values from dictionary
        n = Message.rsa_key['n']
        e = Message.rsa_key['e']

        #To encrypt: message**e mod n - do this for each letter, convert message to ASCII using ord 
        self.r_encrypted = [pow(ord(char),e,n) for char in self.message]

        return self.r_encrypted #Return encrypted message

    #Method to check for prime number (Aid in RSA cipher) 
    def check_prime(self,x):
        #A number is prime if it is ONLY divisible by 1 and itself
        for i in range(2,x):
            #from 2 to x-1 if it is divisible it has a factor other than 1 and itself
            if x%i == 0: #Check to see if divisible
                return False
                break
        return True
    
    #Method to get prime number (Aid in RSA cipher) 
    def getPrimeNumber(self):
        check = False
        while check == False:
            #Generate random numbers and check if they are prime
            prime = random.randint(30,200)
            if self.check_prime(prime) == True:
                check = True
                return prime #Return the prime number

    #Decryption method for substitution cipher
    def de_sub_cipher(self,message):
        #Convert message to a list 
        self.List = list(message)
        
        #flip key and alpha from encryption method
        key = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.','!']
        alpha = ['!','o','J','v','f','U','b','M','q','g','T','B','H','P','z','A','K','O','d','s','C','W','S','n','N','R','y','w','h','j','u','Q','p','m','.','l','I','E','k',' ','i','r','V','F','X','a','e','Y','Z','L','c','G','x','D','t']
    
        #Create a decrypted list, replacing the letter in the message with the key
        self.coded = [key[alpha.index(c)]for c in message]
        
        #Use join to turn decrypted list back into a string
        str1 = ''
        self.coded = str1.join(self.coded)
        
        return self.coded #Return decrypted message
    
    #Decryption method for playfair cipher
    def de_play_cipher(self):
        #Create the grid key
        key = [['A','B','C','D','E'],
              ['F','G','H','I','K'],
              ['L','M','N','O','P'],
              ['Q','R','S','T','U'],
              ['V','W','X','Y','Z']]
        
        #Remove spaces from the message and create empty list
        self.sentence = self.message.replace(" ","")
        decryptedList = []

        #Convert sentence to pairs 
        pairList = self.convertToPairs(self.sentence)

        #Find row and column of pair 
        for pair in pairList: #For each pair in the list 
            #check key
            for i in range(5): #For each row in the key
                for j in range(5):
                    if key[i][j] == pair[0]:
                        firstValRow,firstValCol = i,j #If letter found in matrix return its location
                    if key [i][j] == pair[1]:
                        secondValRow,secondValCol = i,j
            #Check to see if in the same row
            if firstValRow == secondValRow:
                self.de_checkRows(firstValRow,firstValCol,secondValRow,secondValCol,key, decryptedList)
            elif firstValCol == secondValCol:
                self.de_checkCol(firstValRow,firstValCol,secondValRow,secondValCol,key, decryptedList)
            else:
                self.de_corner(firstValRow,firstValCol,secondValRow,secondValCol,key, decryptedList)

        #Convert Final List to string
        str1= ''
        decryptedSentence = str1.join(decryptedList)
        
        return decryptedSentence #Return decrypted message
    
    #Method to deal with letters in same row (Aid in decrypting playfair cipher)
    def de_checkRows(self,oneRow,oneCol,twoRow,twoCol,key, decryptedList):
    
         #Take care of wrap around if letter in last 
         if oneCol == 0:
             oneCol = 5 #By setting it to 5, when 1 will be subtracted it will be wrapped around to position 4
         if twoCol == 0:
             twoCol = 5

         #Move each letter one to the left (opposite of encrypting) 
         decrypt = key[oneRow][oneCol-1] + key[twoRow][twoCol-1]

         #Add the decrypted pair to the decrypyted list
         decryptedList.append(decrypt)
         
         return decryptedList #Return decrypted message
    
    #Method to deal with letters in same column (Aid in decrypting playfair cipher)
    def de_checkCol(self,oneRow,oneCol,twoRow,twoCol,key, decryptedList):

        #Take care of wrap around if letter in last 
        if oneRow == 0:
            oneRow = 5 #By setting it to 5, when 1 will be subtracted it will be wrapped around to position 4
        if twoRow == 0:
            twoRow = 5  

        #Move each letter one up (Opposite of encryption) 
        decrypt = key[oneRow-1][oneCol] + key[twoRow-1][twoCol]

        #Add the decrypted pair to the decrypyted list
        decryptedList.append(decrypt)

        return decryptedList #Return decrypted message
    
    #Method to deal with letters not in same row or column(Aid in decrypting playfair cipher)
    def de_corner(self,oneRow,oneCol,twoRow,twoCol,key, decryptedList):
        
        #Rows stay the same only changing column
        decrypt = key[oneRow][twoCol] + key[twoRow][oneCol]
        
        #Add the decrypted pair to the encrypyted list
        decryptedList.append(decrypt)
        return decryptedList #Return decrypted message
    
    #Decryption method for caesar cipher
    def de_caesar_cipher(self):
        #Change sentence to lowercase 
        sentence = self.message.lower()

        #Initialize alphabet
        self.alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        #Initialize key 
        self.key = 3
        #Initialize empty list for encryption
        self.encrypted = []

        #Iterate through the message
        for char in sentence:
            isLetter = char.isalpha() #Check if character is a letter
            if isLetter == True:
                index = self.alpha.index(char)   #Find index of characted in alpha list
                #Account for wrap around
                if index == 2:
                    index = 28
                elif index == 1: 
                    index = 27
                elif index == 0:
                    index = 26
                self.encrypted.append(self.alpha[index-self.key])  #Append letter at index - key to edecrypt (Opposite of encryption)
            else:
                self.encrypted.append(char) #If character not letter, append as is 
        
        #Use join to turn encrypted list back into a string
            str1 = ''
            self.cipherText = str1.join(self.encrypted)

        return self.cipherText #Return decrypted message
    
    #Decryption method for transposition cipher
    def de_trans_cipher(self,message):
        self.key = 4
        # Find the number of rows that were created when encrypting
        numRow = len(message) / self.key
        numRow = math.ceil(numRow) #Round up to account for missing letters 
        
        # Assign the number of columns to the key
        numCol = self.key
        
        # Find the blank boxes in the last row
        totalBox = numRow*numCol
        blankBox = totalBox - len(message)
  
        #Initialize the empty decrypted list
        decrypted = [''] * numRow
   
        # The column and row variables point to where in the grid the next
        # character in the encrypted message will go:
        column = 0
        row = 0
   
        #Fill in each col one at a time (Reverse from when we encrypt)
        for char in message:
            decrypted[row] += char
            row += 1 #Fill in the column downwards
   
            #If reached end of column go back to top and fill next column
            if (row == numRow):
                row = 0 #Back to top
                column += 1 #Move onto the next column
            #If reached a blank box go back to top and fill next column
            elif (row == numRow - 1 and column >= numCol - blankBox):
                row = 0 #Back to top
                column += 1 #Move onto the next column

        #Use join to turn encrypted list back into a string
        str1 = ''
        self.cipherText = str1.join(decrypted)
                
        return self.cipherText #return decrypted message
    
    #Decryption method for transposition cipher
    def de_product_cipher(self):
        message = self.message
        transDecrypt = ""
        #Call decryption in opposite order, so transposition cipher decryption first
        transDecrypt = self.de_trans_cipher(message)

        #Call method for substitution decryption using output of transDecryption cipher
        sub = self.de_sub_cipher(transDecrypt)
        
        return sub #Return decrypted message

    #Decryption method for RSA cipher
    def de_rsa_cipher(self):
        #get private keys 
        n = Message.rsa_key['n']
        d = Message.rsa_key['d']

        #Want to split the string up into a list
        if isinstance(self.message, str):
            self.splitMessage = self.message.split()
            self.message = [int(x) for x in self.splitMessage]

        #To decrypt do the same thing as encryption but using the private key: 
        decrypted = [pow(char,d,n) for char in self.message]

        #Convert decrypted message from ASCII back to letters
        decrypted_message = "".join(chr(char) for char in decrypted)
        return decrypted_message #Return decrypted message

#Class to create the GUI
class GUI:
    def __init__(self):

        #Create lists to store for final output
        self.inputMessage = []
        self.outputMessage = []

        #Create window and title for window
        self.window = Tk()
        self.window.title("Encryption Application")

        title = Label(self.window, text="Encrypting Application", font=('Arial',18))
        title.pack()

        #Create frame for user inputs
        inputFrame = Frame(self.window)
        inputFrame.pack()

        #Entry box for user input
        Label(inputFrame, text="Enter message: ").grid(row=1,column=0)
        self.sentence = StringVar()
        self.messageEntry = Entry(inputFrame, textvariable= self.sentence, width = 30,bg="white")
        self.messageEntry.grid(row=1,column=1, columnspan=1)

        #Frame 2 to choose cipher method and to encrypt or decrypt
        Frame2 = Frame(self.window)
        Frame2.pack()

        #Dropdown menu for encryption method
        self.clicked = StringVar()
        self.clicked.set("Substitution Cipher")

        Label(Frame2,text="Choose Method:").grid(row=2,column=0)
        method_dropdown = OptionMenu(Frame2, self.clicked,  "Substitution Cipher","Playfair Cipher","Caesar Cipher","Transposition Cipher","Product Cipher", "RSA")
        method_dropdown.grid(row=2,column=1)

        #Button to encrypt and decrypt
        encrypt = Button(Frame2,text=" Encrypt ", fg = "black", bg = "lightgrey", command = self.encryption).grid(row=2,column=2)
        decrypt = Button(Frame2,text=" Decrypt ", fg = "black", bg = "lightgrey",command = self.decryption).grid(row=2,column=3)

        #Frame 3 for Stop button 
        Frame3 = Frame(self.window)
        Frame3.pack()

        Label(Frame3,text = "Press stop to get all your outputs:").grid(row=3,column=0)
        Label(Frame3,text = "Reset everything:",).grid(row=3,column=2)
        
        #Create text window for output
        self.output = Text(self.window)
        self.output.pack()

        #Buttons for stop and reset
        Button(Frame3,text=" STOP ", fg = "RED", command = self.finalOutput).grid(row=3,column=1)
        Button(Frame3,text=" RESET ", fg = "BLACK", command = self.reset).grid(row=3,column=3)
        
        #Additional label 
        Frame4 = Frame(self.window)
        Frame4.pack()
        Label(Frame4,text="****For RSA Decryption, enter message integers separated by a space(Ex. 123 1234 123)****").grid(row=4,column=0)
        
        self.window.mainloop()
    
    #Method for if encryption button called
    def encryption(self):
        method = self.clicked.get()

        #Create message object
        message = plainTextMsg(self.sentence.get())
        EorD = "Encrypted"

        #Call encryption method to return encrypted text
        encryptedText = message.encryption(method, "E")

        #Add input and output message to lists 
        self.inputMessage.append((self.sentence.get(),method,EorD))
        self.outputMessage.append((encryptedText,method,EorD))

    #Method for if decryption button called
    def decryption(self):
        method = self.clicked.get()
        #Create message object
        message = plainTextMsg(self.sentence.get())
        EorD = "Decrypted"

        #Call decryption method to return decrypted text
        encryptedText = message.encryption(method,"D")

        #Add input and output message to lists 
        self.inputMessage.append((self.sentence.get(),method,EorD))
        self.outputMessage.append((encryptedText,method,EorD))
        
    #Method to display final output
    def finalOutput(self):
        
        #Erase current display so contents aren't repeated
        self.output.delete("1.0",END)
        
        #Get valeus from input and output list to display
        for i, (plain_text, method, EorD) in enumerate(self.inputMessage):
            encrypted_text, method, EorD = self.outputMessage[i]
            #Display list contents in this formate
            display = f"Method: {method}\nInput: {plain_text}\n{EorD}: {encrypted_text}\n\n"
            self.output.insert(END, display)

    #Method to reset everything
    def reset(self):
        #Empty lists to store for final output
        self.inputMessage.clear()
        self.outputMessage.clear()

        #Erase current display
        self.output.delete("1.0",END)



def main():
    #Call GUI class 
    GUI()

if __name__ == '__main__':
    main()