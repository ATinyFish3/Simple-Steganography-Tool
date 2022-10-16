#PLCS Project, Matthew Bream
#Image steganography tool

#For VIVA:

#cd to folder
#cd C:\Users\matth\OneDrive\Laptop Docs\Cyber Security\WM245 Programming Languages for Cyber Security\Cyber Project Folder
#python "Cyber Project.py"

#properties -> details -> bit depth 32 = 4 bands, bit depth 24 = 3 bands

#colour picker in paint -> colour wheel shows different hex values

#uncomment print(message) in getMessage() to show that text is/isn't encrypted + what is being found

#For testing (printable ASCII chars):
#0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c


#use from so not importing entire libraries when only parts of libraries are needed, efficiency

#tkinter for getting/saving images with some GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

#clear function to clear terminal screen
import os
clear = lambda: os.system('cls')
#(Is there a python 3 command to clear the output console?, 2019)

#time for sleep() function
import time
#Use sleep() so when clearing the console any outputs can be seen first

#numpy and PIL (pillow) for image/image manipulation
import numpy as np
from PIL import Image, ImageFile

#re for regex
import re



#Global variables, to reduce chance of mistakes as can be changed in one place
#Declared outside functions
cShift = 4#ceaser shift
uShift = 128#unicode shift (good if 128+)
endStatement = "!STOP!"#Flag to put at end of message so the end of the message can be found



def main():
    clear()
    print("Options:\n")
    print("[E]ncode\nor\n[D]ecode\nor\n[C]heck LSBs\nor\n[Q]uit\n")

    choice = input()#User's input choice for menu, main() in loop so will loop until valid choice entered

    if len(choice) == 1:#checks message is correct length for valid choice before checking its value so only one check performed rather than 2 when the subsequent checks are not needed

    
        if choice == 'E':
            print("Encoding...\n")
            stegEncode()#Go to encoding function

        if choice == 'D':
            print("Decoding...\n")
            stegDecode()#Go to decoding function

        if choice == 'C':
            print("Checking...\n")
            stegCheck()

        if choice == 'Q':
            print("Exiting...\n")
            time.sleep(1)
            return True#Sets exitVar to True so program will stop

        return False#While loop outside main() will call main again (until choice is valid)


def stegEncode():#Main function for encoding text in image
    messageContainsEndStatement = ''
    while messageContainsEndStatement != None:
        message = getText()#message will be the text to hide in the image
        messageContainsEndStatement = re.search(endStatement, message)#regex to search for endStatement in any part of the entered text
        if messageContainsEndStatement != None:
            print("Message cannot contain", endStatement)
            time.sleep(.5)
    message = message + endStatement
    
    choice = ''
    while choice != 'E' or choice != 'C' or choice != 'U':#Only accept valid inputs
        clear()
        print("Do you want to [E]ncrypt your text? Or leave it [U]nencrypted?\nor [C]ancel\n")
        choice = input()
        
        if choice == 'E':
            time.sleep(.5)
            clear()
            print("Encrypting...\n")
            message = messageEncrypt(message)#Will encrypt message (Caeser cypher)

            choice = 'U'#Then carry on to rest of encoding
            
        if choice == 'U':
            encodedMessage = textToBinary(message)#converts message to binary representation
            image = getImage()#image will be the file path to the image to hide the message in
            if image == False:#image returns as False if user cancels
                return

            imgArray, width, height, numBands = openImageBytes(image)#Get bytes of image

            newImgArray = changeImageBytes(encodedMessage, imgArray)#Change the LS Bytes of the image bytes using the message binary

            binaryToImage(newImgArray, width, height, numBands)#Convert the new bytes back to an image and save it
            #numBands used for reshaping array,
            
            print("Returning to menu\n")
            return
        
        if choice == 'C':#Option to cancel so user doesn't get "trapped"
            print("Returning to menu\n")
            return

        
def stegDecode():#Function for decoding an encoded image
    image = getImage()#image will be the file path to the image to hide the message in
    if image == False:#image returns as False if user cancels
        return

    imgArray, width, height, numBands = openImageBytes(image)#Get bytes of image

    message, isEncrypted = getMessage(imgArray)#Will get message out of the image bytes, isEncrypted used to determine if text needs to be decrypted 

    if isEncrypted == True:
        message = messageDecrypt(message)#Decrypts message if message was encrypted

    if message != None:#getMessage() will return None if there is no message found in the image, make sure message was found
        print("Here is the hidden message:\n" + message + "\n")#Print the message

    while True:
        print("Press enter to continue")
        a = input()
        break
    
    print("Returning to menu\n")


#Code adapted from stegDecode() and getMessage() functions
def stegCheck():#Function to print LSBs of an image (/file)
    image = getImage()#image will be the file path to the image to hide the message in
    if image == False:#image returns as False if user cancels
        return

    imgArray, width, height, numBands = openImageBytes(image)#Get bytes of image

    imgArray = imgArray & 1#Get LSB
    imgArray = np.packbits(imgArray)#Pack binary array into 8 bit array.

    message = ''
    endStatementEncrypt = messageEncrypt(endStatement)#Encrypt end flag to check for encrypted messages too

    for i in imgArray:
        c = chr(i)#Change unicode character from image into character
        
        message = message + c#Add character to message string
        
    print(message)#print all bytes to check manually from text

    while True:
        print("Press enter to continue")
        a = input()
        break
    
    print("Returning to menu\n")


def getMessage(imgArray):#Function to get the message out of an image
    imgArray = imgArray & 1#Get LSB
    imgArray = np.packbits(imgArray)#Pack binary array into 8 bit array.

    message = ''
    endStatementEncrypt = messageEncrypt(endStatement)#Encrypt end flag to check for encrypted messages too

    for i in imgArray:
        c = chr(i)#Change unicode character from image into character
        
        message = message + c#Add character to message string
        
        #print(message) #uncomment to show what is being found + encrypted vs non-encrypted difference
        if len(message) > len(endStatement):#checks message is long enough to contain end statement before checking if end statement is there so only one check performed rather than 2 when the subsequent checks are not needed
            if message[-len(endStatement):] == endStatement:#Check the last characters of the message to see if they are the end of message flag
                message = message[:-len(endStatement)]#Strip the last characters as not part of message
                return message, False#Set isEncrypted to False

            elif message[-len(endStatementEncrypt):] == endStatementEncrypt:#Check the last characters of the message to see if they are the end of message flag (encrypted)
                message = message[:-len(endStatementEncrypt)]#Strip the last characters as not part of message
                return message, True#Set isEncrypted to True

    print("No message found\n")
    return None, None#Return None if no message found


#Pure function
def messageEncrypt(text):#Function to encrypt message
    textList = list(text)#Convert message to array so each character can be 

    count = 0#Variable to increment each item in the message
    for i in textList:
        i = ord(i)#Convert character to unicode code
        i = (i + cShift)%128#Caeser shift - mod 128 to avoid errors with nonprintable characters (0-127 unicode is ASCII)
        #(Ebrahim, 2020)
        i = i + uShift#Add 128 so characters are not printable (as looking at bits from image with no hidden message will look like this)
        i = chr(i)#Change unicode back to character
        textList[count] = i#Change original character to new character
        count += 1#Increment count

    text = "".join(textList)#Change the list of characters back into a string
    return text


#Pure function
def messageDecrypt(text):#Function to decrypt encrypted message
    textList = list(text)#Convert message to array so each character can be used individually

    count = 0#Variable to increment each item in the message
    for i in textList:
        i = ord(i)#convert character to unicode code
        # - instead of + as reverse of encrypt (order reversed also) \/
        i = i - uShift#Caeser shift mod 128 to avoid errors with nonprintable characters (0-127 unicode is ASCII)
        #(Ebrahim, 2020)
        i = (i - cShift)%128#Add 128 so characters are not printable (as looking at bits from image with no hidden message will look like this)
        i = chr(i)#Change unicode back to character
        textList[count] = i#Change original character to new character
        count += 1#Increment count

    text = "".join(textList)#Change the list of characters back into a string
    return text


def getFile():#Seperate this from just images so expansion easy (e.g. use same function to get path to sound files, text files...)
    print("Choose an image!\n")
    filePath = askopenfilename()#(From tkinter library)
    #(Choosing a file in Python with simple Dialog, 2010)
    return filePath

                      
def getImage():#Function to get the image the user wants to use
    imageFilePath = ''
    isImage = False#Flag to check that chosen file is an image
    while isImage == False:
        time.sleep(.5)
        clear()
        imageFilePath = getFile()

        if imageFilePath.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):#Make sure file selected is an image
            #(How can I check the extension of a file?, 2011)
            isImage = True
            return imageFilePath

        else:#If chosen file not valid or no file chosen then give user option to cancel and show valid file formats
            print("Choose an image file (png, jpg, bmp)(press enter to continue)\nor [C]ancel\n")
            cancelChoice = input()
            if cancelChoice == 'C':
                print("Returning to menu\n")
                return False


def getText():#Function to get message to hide
    time.sleep(.4)
    clear()
    message = ''
    while len(message) == 0:#Check user enters non null message
        clear()
        print("Enter text to hide in your file:\n")
        message = input()
        if len(message) == 0:
            print("Enter at least some text!")
            time.sleep(1)
        
    return message


#Pure function
def textToBinary(message):#Function to convert text into binary
    messageBinary = ''.join(format(ord(i), '08b') for i in message)
    #(Python | Convert String to Binary - GeeksforGeeks, 2021)
    return messageBinary


#Pure function
#(Werli, 2021)
def openImageBytes(path):#Function to get byte array of an image
    with Image.open(path) as img:#Open image
        width, height = img.size#Get width and height to be able to reshape array (change dimensions) to get data
        data = np.array(img)
        numBands = len(img.getbands())

    data = np.reshape(data, width*height*(len(img.getbands())))
    return data, width, height, numBands


def binaryToImage(binary, width, height, numBands):#Function to turn array of bytes to image
    binary = np.reshape(binary, (height, width, numBands))#Reshape byte array

    saveImg = Image.fromarray(binary)#Make image from array

    saveImage(saveImg)

def saveImage(image):
    #(Python Examples of tkinter.filedialog.asksaveasfile, n.d.)
    validDir = False
    while validDir == False:
        clear()
        print("Choose where to save image:")
        saveDir = asksaveasfilename(defaultextension=".png", filetypes = (("png files","*.png"),("all files","*.*")))
        clear()
        if saveDir:
            #(Regular expression for valid filename, 2012)
            filePathRegEx = re.findall('COM|CON|LPT|NUL|PRN|AUX|NUL|com|con|lpt|nul|prn|aux|nul', str(saveDir))#Check filename is not windows reserved words, tkinter already checks for invalid characters 
            if filePathRegEx:
                print("Filename cannot be that\n")
                print("Choose where to save image or [C]ancel (press enter to continue)\n")
                choice = input()
                if choice == 'C':
                    break
            else:
                validDir = True
                image.save(saveDir)#Save image
                print("Saved")
        else:
            print("Choose where to save image or [C]ancel (press enter to continue)\n")
            choice = input()
            if choice == 'C':
                break


def changeImageBytes(textBytes, imageBytes):#Function to put the bytes of the text in the bytes of the image
    pos = 0#Position variable to increment
    for i in textBytes:
        imageBytes[pos] = ((imageBytes[pos] & ~1) | int(i))#Replace LSB with correct bit from text bytes
        #(Replace least significant bit with bitwise operations, 2011)
        pos += 1#Increment to next byte
    #print(imageBytes)
    return imageBytes


    
exitVar = False#Global
while not exitVar:#loop outside of main so quit can function
    exitVar = main()


#Ref for image.getbands() (NumPy Array Reshaping, n.d.)
    #Get bands for reshaping image correctly
    
    
##References
##Ebrahim, M., 2020. Caesar Cipher in Python (Text encryption tutorial). [online] LikeGeeks. Available at: <https://likegeeks.com/python-caesar-cipher/ --> [Accessed April 2022].
##
##GeeksforGeeks. 2021. Python | Convert String to Binary - GeeksforGeeks. [online] Available at: <https://www.geeksforgeeks.org/python-convert-string-to-binary/> [Accessed April 2022].
##
##Programcreek.com. n.d. Python Examples of tkinter.filedialog.asksaveasfile. [online] Available at: <https://www.programcreek.com/python/example/95889/tkinter.filedialog.asksaveasfile> [Accessed May 2022].
##
##Stack Overflow. 2010. Choosing a file in Python with simple Dialog. [online] Available at: <https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog> [Accessed April 2022].
##
##Stack Overflow. 2011. How can I check the extension of a file?. [online] Available at: <https://stackoverflow.com/questions/5899497/how-can-i-check-the-extension-of-a-file> [Accessed April 2022].
##
##Stack Overflow. 2011. Replace least significant bit with bitwise operations. [online] Available at: <https://stackoverflow.com/questions/6059454/replace-least-significant-bit-with-bitwise-operations> [Accessed April 2022].
##
##Stack Overflow. 2012. Regular expression for valid filename. [online] Available at: <https://stackoverflow.com/questions/11794144/regular-expression-for-valid-filename> [Accessed May 2022].
##
##Stack Overflow. 2019. Is there a python 3 command to clear the output console?. [online] Available at: <https://stackoverflow.com/questions/59497109/is-there-a-python-3-command-to-clear-the-output-console> [Accessed April 2022].
##
##W3schools.com. n.d. NumPy Array Reshaping. [online] Available at: <https://www.w3schools.com/python/numpy/numpy_array_reshape.asp> [Accessed May 2022].
##
##Werli, S., 2021. Image Steganography with Python. [online] Medium. Available at: <https://medium.com/@stephanie.werli/image-steganography-with-python-83381475da57> [Accessed April 2022].
