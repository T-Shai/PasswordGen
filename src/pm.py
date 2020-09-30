import os
from utils import *
from crypto import *

def _digestData(bdata : list, bdict = dict()):
    if bdata == list():
        return bdict
    
    if len(bdata)%3 != 0:
        raise IndexError("Length of binary data not multiple of 3")

    for i in range(0,len(bdata), 3):
        # {link : [(username, password),(username1, password1),(username2, password2), }
        if bdata[i] in bdict :
            delete = None
            for infos in bdict[bdata[i]]:
                if infos[0] == bdata[i+1]: # if username already exist for this website
                    delete = infos
            if delete != None:
                bdict[bdata[i]].remove(delete)

            bdict[bdata[i]].add((bdata[i+1], bdata[i +2]))
        else :
            bdict[bdata[i]] = {(bdata[i+1], bdata[i +2])}
    
    return bdict

def prettyRepDict(d : dict):
    s = ""

    for blink in d:
        s += """
        link : {} :
        """.format(blink)
        for user,passw in d[blink]:
            s += """
            username : {} password : {}
            """.format(user, passw)
    return s


class PassManager:

    def __init__(self, username : str, token : bytes, data : list):

        self.username = username
        self.btoken = token
        self.bdict = _digestData(data)
    
    def append(self, link : str, link_username : str, password : str):

        self.bdict = _digestData([link.encode(), link_username.encode(), password.encode()], self.bdict)
        self.dump()
    
    def delete(self, link : str, link_username : str):
        blink = link.encode()
        buser = link_username.encode()
        
        delete = None
        for infos in self.bdict[blink]:
            if infos[0] == buser:
                delete = infos
        if delete != None:
            self.bdict[blink].remove(delete)
            if self.bdict[blink] == {}:
                del self.bdict[blink]
        
        self.dump()
    
    def getUsers(self, link : str):
        blink = link.encode()

        return [user for users,_ in self.bdict[blink]]
    
    def getPass(self, link : str, link_username : str):
        blink = link.encode()
        buser = link_username.encode()

        for infos in self.bdict[blink]:
            if infos[0] == buser:
                return infos[1]
        return b''


    def dump(self):
        
        showFile(self.username+".key")
        with open(self.username+".key", "wb") as f:
            f.write(self.btoken+"\n".encode())
            for blink in self.bdict:
                for user, passw in self.bdict[blink]:
                    f.writelines([blink+"\n".encode(), user+"\n".encode(), passw+"\n".encode()])
        hideFile(self.username+".key")

        return self.username+".key"
    
    def __repr__(self):

        return \
"""
username    :   {}
token       :   {}
bdict       :   {}
""".format(self.username, self.btoken, prettyRepDict(self.bdict))
    

    def getlinks(self):
        links = list()

        return [link.decode() for link in self.bdict]
    
    def getInfos(self, link : str):

        link = link.encode()

        if link not in self.bdict:
            return []
        else:
            return [(user.decode(), passw.decode()) for user,passw in self.bdict[link]]
            
    @staticmethod
    def loadPM(filename):

        if not filename.endswith(".key"):
            filename += ".key"
        
        showFile(filename)
        with open(filename, "rb") as f:
            data = f.readlines()
        hideFile(filename)

        data = [i.strip("\n".encode()) for i in data] # stripping \n

        return PassManager(filename[:len(filename)-4], data[0], data[1:])
    


if __name__ == "__main__":
    pm = PassManager("pablo", b'token', list())
    pm.append("facebook.com", "username", "1234566789")
    pm.append("facebook.com", "username", "123456789")
    pm.append("google.com", "username", "123456789")
    pm.append("facebook.com", "usernamenew", "123456789")
    pm.append("yahoo.com", "username", "123456789")
    pm.append("facebook.com", "username", "123456789")

    print(pm.getlinks())
    print(pm.getInfos("facebook.com"))

    filename = pm.dump()

    pm2 = PassManager.loadPM(filename)
    assert(str(pm) == str(pm2))
    