import os
from tkinter import *

def showFile(filename : str):
    if not filename.endswith(".key"):
        filename += ".key"

    # hiding for windows 
    if os.name == "nt":
        os.system("attrib -h "+ filename)
    else:
        os.rename(filename, filename[1:])

def hideFile(filename : str):
    if not filename.endswith(".key"):
        filename += ".key"

    # hiding for windows 
    if os.name == "nt":
        # hiding file with windows subshell
        os.system("attrib +h "+ filename)
    else:
        os.rename(filename, "."+filename)
    
    return filename

def writeHidden(fileName : str, data):

    if not fileName.endswith(".key"):
        fileName += ".key"
    
    # prefix for linux
    pre = "." if os.name != "nt" else ""
    fileName = pre + fileName

    with open(fileName, "wb") as f:
        f.write(data + "\n".encode())
    
    # hiding for windows 
    if os.name == "nt":
        # hiding file with windows subshell
        os.system("attrib +h "+ fileName)

def readData(filename :str):

    if not filename.endswith(".key"):
        filename = filename + ".key"

    with open(filename, "rb") as f:
        data = f.readlines()
    
    return data

def getFileNameByExt(ext):
    names = list()
    for file in os.listdir("."):
        if file.endswith("."+ext):
            names.append(file[:len(file)-len(ext)-1])
    return names

def leaveBlank(window):
    Label(window, text="").pack()

if __name__ == "__main__":
    getFileNameByExt("key")
