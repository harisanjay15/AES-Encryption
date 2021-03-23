# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:02:40 2021

@author: Hari Sanjay
"""
def generate_keys(hexa_key):
    words=[]  
    rconst=["01000000", "02000000", "04000000", "08000000", "10000000", "20000000", 
            "40000000", "80000000", "1B000000", "36000000", "6C000000", "D8000000", 
            "AB000000", "4D000000"]
    for i in range (0,len(hexa_key),8):
        words.append(hexa_key[i:i+8])
        
    ite=0
    if(len(hexa_key)==32):
        ite=11
    elif(len(hexa_key)==48):
        ite=13
    elif(len(hexa_key)==64):
        ite=15
    for i in range(1,ite):
        temp=words[(i*4)-1]
        temp=temp[2:]+temp[:2]
        temp=sbox_value(temp)
        temp1=""
        for j in temp:
            for k in j:
                temp1+=k    
        temp=temp1
        temp=xor_bin(hexa_to_bin(temp),hexa_to_bin(rconst[i-1]))
        temp=temp[-8:]
        for j in range(4):
            w=(i*4)+j       
            if(w%4==0):
                ttttt=xor_bin(hexa_to_bin(temp),hexa_to_bin(words[w-4]))
                words.append(ttttt[-8:])
            else:
                ttttt=xor_bin(hexa_to_bin(words[w-1]),hexa_to_bin(words[w-4]))
                words.append(ttttt[-8:])             
    keysss=[]
    for i in range(0,len(words),4):
        sample=""
        for j in range(4):
            sample=sample+words[i+j]
        keysss.append(sample)
    return keysss

def bitwise_multiplication(a,b):
    fx=[]
    gx=[]
    f=hexa_to_bin(a)[::-1]
    g=hexa_to_bin(b)[::-1]
    m="00011011"
    
    for i in range(len(f)):
        if(f[i]=='1'):
            fx.append(i)
        if(g[i]=='1'):
            gx.append(i)
    fx=fx[::-1]
    gx=gx[::-1]
    f=f[::-1]
    g=g[::-1]
   
    mx=[]
    mx.append(g)
    for i in range(1,fx[0]+1):
        shiftmx=mx[i-1][1:]+'0' 
        if(mx[i-1][0]=="1"):
            shiftmx=xor_bin(shiftmx,m)
            shiftmx=hexa_to_bin(shiftmx)[-8:]
        mx.append(shiftmx)
    result="00000000"   
    for i in fx:
        result=xor_bin(result,mx[i])
        result=hexa_to_bin(result)[-8:]   
    return result
    

def mix_column(Y):
    X=[["02","03","01","01"],
       ["01","02","03","01"],
       ["01","01","02","03"],
       ["03","01","01","02"]]
    result=[]
    for i in range(len(X)):
        tt=[]
        for j in range(len(Y[0])):   
            r="00000000"
            for k in range(len(Y)):     
                t=bitwise_multiplication(X[i][k],Y[k][j])     
                r = xor_bin(r,t)
                r = hexa_to_bin(r)[-8:] 
            tt.append(bin_to_hexa(r)[-2:].upper())
        result.append(tt)
    return result

def shift_row(s):
    t=[]
    t.append(s[0])
    for i in range(1,len(s)):
        temp=s[i]
        temp=temp[i:]+temp[:i]
        t.append(temp)       
    return t


def sbox_value(s):
    
    a=[]
    sbox=['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB',
   '76', 'CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4',
   '72', 'C0', 'B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71',
   'D8', '31', '15', '04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2',
   'EB', '27', 'B2', '75', '09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6',
   'B3', '29', 'E3', '2F', '84', '53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB',
   'BE', '39', '4A', '4C', '58', 'CF', 'D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45',
   'F9', '02', '7F', '50', '3C', '9F', 'A8', '51', 'A3', '40', '8F', '92', '9D', '38', 'F5',
   'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2', 'CD', '0C', '13', 'EC', '5F', '97', '44',
   '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73', '60', '81', '4F', 'DC', '22', '2A',
   '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB', 'E0', '32', '3A', '0A', '49',
   '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79', 'E7', 'C8', '37', '6D',
   '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08', 'BA', '78', '25',
   '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A', '70', '3E',
   'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E', 'E1',
   'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF',
   '8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
    t=""
    
    for i in range(0,len(s),2):
        temp=s[i:i+2]
        
        if(temp[0].isalpha()):
            sbox_row=ord(temp[0])-55
        else:
            sbox_row=int(temp[0])
            
        if(temp[1].isalpha()):
            sbox_column=ord(temp[1])-55
        else:
            sbox_column=int(temp[1])
        t=sbox[(sbox_row*16)+sbox_column]
        a.append(t)
    
    X=[]
    for i in range(0,len(a),4):
        X.append(a[i:i+4])
    result = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    return result

#convert 32 hexa to  128 binary 
def hexa_to_bin(s):
    t=""
    for i in s:
        a=format(int(i,16), '0>42b')    
        t=t+a[-4:]
    return t

#convert 128 binary to 32 hexa
def bin_to_hexa(s): 
    t=str(hex(int(s,2)))[2:]
    t=((32-len(t))*'0')+t
    return t

#xor two binary values
def xor_bin(a,b):
    t=""
    for i in range(len(a)):
        t=t+str(int(a[i])^int(b[i]))    
    return (bin_to_hexa(t)).upper()

#convert 16 deciaml to  32 hexa
def tohexa(s):
    hexa_text=""
    for i in s:
       t=str(hex(ord(i)-65))[2:]
       t=((2-len(t))*'0')+t
       hexa_text=hexa_text+t
    return hexa_text

def tobinary(s):
    return format(int(s,16), '0>42b')
    
        
def array_to_str(s):
    mixcolumn=""
    for j in s:
            for k in j:
                mixcolumn+=k
    return mixcolumn

    
def encrypt(hexa_key,hexa_text):
    
    print("\n\n\n*******************************")
    #key generation
    key=generate_keys(hexa_key)
    
    print("Round 0")
    print("key- ",hexa_key)
    print("pre round",hexa_text)
    
    #preorder add round key
    pre_round_text=xor_bin(hexa_to_bin(hexa_text),hexa_to_bin(hexa_key))
         
    #round
    for i in range(1,len(key)-1):
        print("Round---",i)
        sboxed_text=sbox_value(pre_round_text)
        kshift=shift_row(sboxed_text)
        X=kshift=mix_column(kshift)
        Yy=[[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
        mixcolumn=array_to_str(Yy)
        print("key-",key[i])
        pre_round_text=xor_bin(hexa_to_bin(mixcolumn),hexa_to_bin(key[i]))
        print("pre round",pre_round_text,"\n") 
    X=sboxed_text=sbox_value(pre_round_text)
    X=kshift=shift_row(sboxed_text)
    Yy=[[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    X=array_to_str(Yy)
    pre_round_text=xor_bin(hexa_to_bin(X),hexa_to_bin(key[-1]))
    print("Final Result....")
    print(pre_round_text)
    return pre_round_text
    


def main():
    
    hexa_key=input("Enter key\nKey should a hex of size 32 or 48 or 64\n").upper()
    #hexa_key="000102030405060708090a0b0c0d0e0f".upper()
    lk=len(hexa_key)
    if not(lk==32 or lk==48 or lk==64):
        print("Key should a hex of size 32 or 48 or 64\n")
        main()
    
    hexa_text=input("Enter plain Text\n").upper()
    #hexa_text="00112233445566778899aabbccddeeff0".upper()
    a=""
    
    lt=len(hexa_text)
      
    if(lk>lt):
        hexa_text=hexa_text + ((lk-lt)*'0')
        a=encrypt(hexa_key,hexa_text)
        print(a)
    elif(lk<lt):
        ite=lt/lk
        ite=int(ite)
        for i in range(ite):
            text=hexa_text[lk*i : lk*(i+1)]
            a=a+""+encrypt(hexa_key,text)
        
        text=hexa_text[ite*lk :]
        if(len(text)!=0):
            text=text+((lk-len(text))*'0')
            a=a+" "+ encrypt(hexa_key,text)
        print(a)
    else:
        a=encrypt(hexa_key,hexa_text)
        print(a)
        
    

if __name__ == "__main__":
    main()



