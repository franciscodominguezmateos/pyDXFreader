import sys
from PySide import QtGui, QtCore
import pyHotDraw.Core.Qt

def getPairs(content):
    l=[]
    for i in range(0,len(content),2):
        s1=content[i]
        s2=content[i+1]
        l.append((s1.strip(),s2.strip()))   
    return l         
def noComments(pairs):
    rp=[]
    for p in pairs:
        if not isComment(p):
            rp.append(p)
    return rp
def isS(pair,ss):
    n,s=pair
    if s==ss:
        return True;
    else:
        return False;
def isGroupe(pair,ng):
    n,s=pair
    if n==ng:
        return True
    else:
        return False
def isGroupe0(pair):
    return isGroupe(pair,"0")
def isComment(pair):
    return isGroupe(pair,"999")
def isSECTION(pair):
    return isS(pair,"SECTION")
def isENDSEC(pair):
    return isS(pair,"ENDSEC")
def isBLOCKS(pair):
    return isS(pair,"BLOCKS")
def isLINE(pair):
    return isS(pair,"LINE")
def isLWPOLYLINE(pair):
    return isS(pair,"LWPOLYLINE")
def isARC(pair):
    return isS(pair,"ARC")
def isCIRCLE(pair):
    return isS(pair,"CIRCLE")
def isEOF(pair):
    return isS(pair,"EOF")
def getSection(content):
    l=[]
    pair=content[0]
    while not isENDSEC(pair) and content and not isEOF(pair):
        l.append(pair)
        del content[0]
        if content:
            pair=content[0]
    if isENDSEC(pair):
        l.append(pair)
        del content[0]
    if isEOF(pair):
        del content[0]
    return l
def getSections(content):
    ts={}
    while content:
        l=getSection(content)
        if l:
            n,s=l[1]
            ts[s]=l
    return ts
        
def getEntity(e):
    l={}
    pair=e[0] #LINE,ARC,CIRCLE,LWPOLYLINE
    del e[0]
    l[pair[0]]=pair[1]
    pair=e[0]
    while not isGroupe0(pair) and e and not isENDSEC(pair):
        if not isGroupe0(pair) and not isENDSEC(pair):
            if pair[0] in l:
                if isinstance(l[pair[0]],list):
                    l1=l[pair[0]]
                    v=pair[1]
                    l1.append(v)
                else:
                    s=l[pair[0]]
                    l[pair[0]]=[]
                    l[pair[0]].append(s)
                    l[pair[0]].append(pair[1])
            else:
                l[pair[0]]=pair[1]
            del e[0]
            pair=e[0]
    if isENDSEC(pair):
        del e[0]
    return l
def getEntities(e):
    del e[0] #SECTION
    del e[0] #ENTITIES
    l=[]
    while e:
        et=getEntity(e)
        l.append(et)
    return l

def getEtt(fname):
    #fname="C:\Users\paco\Desktop\mini3DprinterCaseMotoresZdentro13102701.dxf"
    #fname="C:\\Users\\paco\\Desktop\\a4x2laser.dxf"
    #fname="C:\\Users\\paco\\Desktop\\1_set_rasp_pi_case.dxf"
    with open(fname) as f:
        content = f.readlines()
    p0=getPairs(content)
    p=noComments(p0)
    s=getSections(p)
    print s.keys()
    e=getEntities(s["ENTITIES"])
#     for et in e:
#         print et["0"]
    return e

