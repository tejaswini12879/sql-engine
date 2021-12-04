#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import os
import sys
filepath="."
filename="metadata.txt"
path=os.path.join(filepath,filename)
file=open(path,'r')
l=file.readlines()
read_table=False
dict_mine1={}
dict_mine2={}
for i in l :
    i=i[:-1].lower()
    if(i=="<begin_table>"):
        read_table=True
        vec=[]
        continue
    if(i=="<end_table>"):
        read_table=False
        dict_mine2[table]=vec
        continue
    if(read_table):
        table=i
        read_table=False
        continue
    dict_mine1[i]=table
    vec.append(i)
#print(dict_mine1,dict_mine2)


# In[2]:


from collections import defaultdict
def read(table):
    with open('./{0}.csv'.format(table), 'r') as file:
        reader = csv.reader(file)
        dict_obj=defaultdict(list)
        for r in reader:
            for i in range(len(r)):
                dict_obj[dict_mine2[table][i]].append(int(r[i]))
        table1=list([v[1] for v in dict_obj.items()])
        tab1=[[row[i] for row in table1] for i in range(len(table1[0]))]
    return tab1


# In[3]:


def table(com):
    arr=['where','order','group']
    st=''
    while(len(com) and com[0] not in arr):
        st=st+com[0]
        com.pop(0)
    #print(st,com)
    st=st.split(',')
    n=len(st)
    l=[]
    cols=[]
    for i in range(n):
        if(i==0):
            l=read(st[i])
            #print(l)
        else :
            m=read(st[i])
            ll=[l[ii]+m[j] for ii in range(len(l)) for j in range(len(m))]
            l=ll
        cols.extend(dict_mine2[st[i]])
    return [l,cols],com


# In[4]:


def int_me(a,arr,cols):
    try : 
        int(a)
        return int(a)
    except :
        for i in range(len(cols)):
            if(cols[i]==a):
                return arr[i]
        print('column not exist')
        sys.exit()
def where(arr,cols,comm):
    if(len(comm)==0 or 'where' not in comm):
        return [arr,cols],comm
    if('where'!=comm[0]):
        print('where not present next to tables')
        sys.exit()
    comm.pop(0)
    st1=''
    st2=''
    o=0
    a=0
    ##print('hi')
    if('or' in comm):
        for i in range(len(comm)):
            if(comm[0].lower()=='or'):
                comm.pop(0)
                break
            st1=st1+comm[0]
            comm.pop(0)
        for i in range(len(comm)):
            if(comm[0].lower()=='group' or comm[0].lower()=='order'):
                break
            st2=st2+comm[0]
            comm.pop(0)
        o=1
    elif('and' in comm):
        for i in range(len(comm)):
            if(comm[0].lower()=='and'):
                comm.pop(0)
                break
            st1=st1+comm[0]
            comm.pop(0)
        for i in range(len(comm)):
            if(comm[0].lower()=='group' or comm[0].lower()=='order'):
                break
            st2=st2+comm[0]
            comm.pop(0)
        a=1
    else:
        for i in range(len(comm)):
            if(comm[0].lower()=='group' or comm[0].lower()=='order'):
                break
            st2=st2+comm[0]
            comm.pop(0)
        st1=st2
        a=1
    st11=''
    st12=''
    st21=''
    st22=''
    op1=''
    op2=''
    for i in range(len(st1)):
        if(st1[i]+st1[i+1]=='<='):
            op1='<='
            st11=st1[:i]
            st12=st1[i+2:]
            break
        if(st1[i]=='<'):
            op1='<'
            st11=st1[:i]
            st12=st1[i+1:]
            break
        if(st1[i]+st1[i+1]=='>='):
            op1='>='
            st11=st1[:i]
            st12=st1[i+2:]
            break
        if(st1[i]=='>'):
            op1='>'
            st11=st1[:i]
            st12=st1[i+1:]
            break
        if(st1[i]=='='):
            op1='='
            st11=st1[:i]
            #print("please1")
            st12=st1[i+1:]
            break
    for i in range(len(st2)):
        if(st2[i]+st2[i+1]=='<='):
            op2='<='
            st21=st2[:i]
            st22=st2[i+2:]
            break
        if(st2[i]=='<'):
            op2='<'
            st21=st2[:i]
            st22=st2[i+1:]
            break
        if(st2[i]+st2[i+1]=='>='):
            op2='>='
            st21=st2[:i]
            st22=st2[i+2:]
            break
        if(st2[i]=='>'):
            op2='>'
            st21=st2[:i]
            st22=st2[i+1:]
            break
        if(st2[i]=='='):
            op2='='
            st21=st2[:i]
            #print("please2")
            st22=st2[i+1:]
            break
    l=[]
    #print(st11,st12,st21,st22,op1,op2)
    for i in range(len(arr)):
        score=0
        temp11=int_me(st11,arr[i],cols)
        temp12=int_me(st12,arr[i],cols)
        temp21=int_me(st21,arr[i],cols)
        temp22=int_me(st22,arr[i],cols)
        if(op1=='<='):
            if(temp11<=temp12):
                score=score+1
        if(op1=='>='):
            if(temp11>=temp12):
                score=score+1
        if(op1=='<'):
            if(temp11<temp12):
                score=score+1
        if(op1=='>'):
            if(temp11>temp12):
                score=score+1
        if(op1=='='):
            if(temp11==temp12):
                score=score+1
        if(op2=='<='):
            if(temp21<=temp22):
                score=score+1
        if(op2=='>='):
            if(temp21>=temp22):
                score=score+1
        if(op2=='<'):
            if(temp21<temp22):
                score=score+1
        if(op2=='>'):
            if(temp21>temp22):
                score=score+10
        if(op2=='='):
            if(temp21==temp22):
                score=score+1
        #print(temp11,temp12,temp21,temp22)
        if(a==1 and score==2):
            l.append(arr[i])
        if(o==1 and score>0):
            l.append(arr[i])
    return [l,cols],comm


# In[5]:


def function(arr,b):
    if(b=='sum'):
        return sum(arr)
    elif(b=='min'):
        return min(arr)
    elif (b=='max'):
        return max(arr)
    elif (b=='avg'):
        return sum(arr)/len(arr)
    else :
        return len(arr)
def group(arr,col,req,com):
    if('group' not in com):
        return [arr,col],com,False
    if('group' in com):
        if(com[0]=='group' and com[1]=='by'):
            com.pop(0)
            com.pop(0)
        temp=com[0]
        com.pop(0)
        #print('hiii',temp)
        #req.append(temp)
        cnt=0
        mee=['count','avg','sum','min','max']
        cols=['' for i in range(len(req)+1)]
        index=0
        cols[len(req)]=temp
        aggs_here=cols.copy()
        for i in range(len(req)):
            if(req[i][:3] in mee):
                cols[i]=req[i][4:-1]
                aggs_here[i]=req[i][:3]
            elif(req[i][:5] in mee):
                cols[i]=req[i][6:-1]
                aggs_here[i]=req[i][:5]
            else :
                cols[i]=req[i]
                cnt=cnt+1
                index=i
        if(cnt>1):
            print('multiple columns in group by')
        arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
        arr=[]
        #cols.append(temp)
        #print(cols)
        #print(req,aggs_here)
        for i in range(len(cols)):
            for j in range(len(col)):
                if(cols[i]==col[j]):
                    arr.append(arr1[j])
                    break
        arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
        arr=arr1
        if(len(arr[0])!=len(cols)):
            print('not found some column')
            sys.exit()
        arr.sort(key=lambda x:x[len(req)])
        final=[]
        n=len(req)
        while(len(arr)!=0):
            m=len(arr)
            if(m==0):
                break
            hell=arr[0][n]
            temp=[[]for i in range(len(req))]
            for i in range(m):
                if(arr[0][n]==hell):
                    for j in range(n):
                        temp[j].append(arr[0][j])
                    arr.pop(0)
            here=[0 for i in range(n)]
            for i in range(n):
                if(aggs_here[i]):
                    here[i]=function(temp[i],aggs_here[i])
                else :
                    here[i]=temp[i][0]
            final.append(here)
        temp=[]
        for i in range(len(cols[:-1])):
            if(aggs_here[i]):
                temp.append(aggs_here[i]+'('+cols[i]+')')
            else:
                temp.append(cols[i])
        return [final,temp],com,True
        #arr=extract_table(arr,col,req)


# In[6]:


def aggs(arr,cols,req):
    n=len(req)
    temp=0
    for i in range(n):
        if('('in req[i]):    
            temp=temp+1
    if(temp==n):
        tab1=[[row[i] for row in arr] for i in range(len(arr[0]))]
        arr=tab1
    else :
        return [arr,cols]
    me=[0 for i in range(n)]
    #print(cols)
    for i in range(n):
        flag_here=0
        if(req[i][3]=='('):
            for j in range(len(cols)):
                #print(cols[j],req[i][3:-1])
                if(cols[j]==req[i][4:-1]):
                    flag_here=1
                    me[i]=function(arr[j],req[i][:3])
                    break
        else :
            for j in range(len(cols)):
                if(cols[j]==req[i][6:-1] or req[i][6:-1]=='*'):
                    flag_here=1
                    me[i]=function(arr[j],'count')
                    break
        if(flag_here==0):
            print(req[i])
            print('column not present')
    return [[me],req]


# In[7]:


def dis(arr):
    me=[ele for ind, ele in enumerate(arr) if ele not in arr[:ind]]
    return me


# In[8]:


def order(arr,cols,com):
    if('order' not in com):
        return [arr,cols],com
    com.pop(0)
    com.pop(0)
    here=1
    if(len(com)>1):
        here=com[1]
    if(here=='desc'):
        here=-1
    else :
        here=1
    col=com[0]
    #print(col)
    flag_here=0
    for i in range(len(cols)):
        if(cols[i]==col):
            flag_here=1
            arr.sort(key=lambda x:x[i])
    if(flag_here==0):
        print('column not found in ordering')
        sys.exit()
    return [arr,cols],com


# In[9]:


def select(arr,cols,req):
    arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
    ll=[]
    for i in req:
        flag_here=0
        for j in range(len(cols)):
            if(cols[j]==i):
                flag_here=1
                ll.append(arr1[j])
        if(flag_here==0):
            print('column not present to select')
            sys.exit()
    arr1=[[row[i] for row in ll] for i in range(len(ll[0]))]
    return [arr1,req]


# In[10]:


com=sys.argv[1]
com=com.lower()
com=com.strip()
if(com[-1]!=';'):
    print('semicolon error')
    sys.exit()
com=com[:-1].split()
if(len(com)==0):
    print('no command')
    sys.exit()
if(len(com)<2):
    print('no correct command')
    sys.exit()
if(com[0]!='select'):
    print('no select')
    sys.exit()
com.pop(0)
distinct=0
if(com[0]=='distinct'):
    com.pop(0)
    distinct=1
if('from' not in com):
    print('no from')
    sys.exit()
cols=''
for i in range(len(com)):
    if(com[0]=='from'):
        com.pop(0)
        break
    cols=cols+com[0]
    com.pop(0)
cols=cols.split(',')
if(len(cols)==0):
    print('no columns')
    sys.exit()    
l,com=table(com)
#print(l[1],cols)
if(cols[0]=='*'):
    temp=l[1].copy()
    temp.extend(cols[1:])
    cols=temp
#print(cols)
group_flag=False
l,com=where(l[0],l[1],com)
l,com,group_flag=group(l[0],l[1],cols,com)
#print(l)
l,com=order(l[0],l[1],com)
if(group_flag==False):
    l=aggs(l[0],l[1],cols)
l=select(l[0],l[1],cols)
if(distinct==1):
    l[0]=dis(l[0])
#print(l[0],com)


# In[11]:


#print(l[0])
n=len(l[0][0])
l,req=l[0],l[1]
cols=[]
aggs=[]
for i in range(n):
    if(len(req[i])>3 and req[i][3]=='('):
        cols.append(req[i][4:-1])
        aggs.append(req[i][:3])
    elif(len(req[i])>5 and req[i][5]=='('):
        cols.append(req[i][6:-1])
        aggs.append(req[i][:5])
    else :
        cols.append(req[i])
        aggs.append('')
#print(cols,aggs)
for i in range(n):
    if(i==0):
        if(aggs[i]):
            print(aggs[i],'(',cols[i],')','.',dict_mine1[cols[i]],sep='',end='')
        else:
            print(cols[i],'.',dict_mine1[cols[i]],sep='',end='')
    else :
        if(aggs[i]):
            print(',',aggs[i],'(',cols[i],')','.',dict_mine1[cols[i]],sep='',end='')
        else:
            print(',',cols[i],'.',dict_mine1[cols[i]],sep='',end='')
print()
for i in range(len(l)):
    for j in range(n):
        if(j==0):
            print(l[i][j],sep='',end='')
        else :
            print(',',l[i][j],sep='',end='')
    print()

