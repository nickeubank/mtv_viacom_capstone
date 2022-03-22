import pandas as pd
import glob

def isLA(output):
    for i,r in output.iterrows():
        if output.loc[i,'state']=='LA':
            print(output.loc[i,'address'][-2:])
            if output.loc[i,'address'][-2:]!='LA':
                
                output.loc[i,'address']=output.loc[i,'address']+", LA"

    return output
                



def isMA(output):
    
    '''
    First the first occuracne of Vote and the last occurance of . Remove all text in between that position
    Remove Words before - in the begining 
    e.g. SCHOOL - 165 
    '''
  
    for i,r in output.iterrows():
        if output.loc[i,'state']=='MA':
            if "vote" in output.loc[i,'address'].lower() or "voter" in output.loc[i,'address'].lower():
                start_pos=output.loc[i,'address'].lower().find("vote")
                end_pos=output.loc[i,'address'].rfind(".")
                address=output.loc[i,'address']
           
                if end_pos==len(output.loc[i,'address'])-1:

                    address=output.loc[i,'address'][:start_pos]+""+"MA"

                else:
                    address=output.loc[i,'address'][:start_pos]+" "+output.loc[i,'address'][end_pos+2:]
                
                address=address.replace(".",",")

                if address[-2:]!='MA':
                    address=address+' MA'
                output.loc[i,'address']=address
            
            if "enter" in output.loc[i,'address'].lower():
                start_pos=output.loc[i,'address'].lower().find("enter")
                end_pos=output.loc[i,'address'].rfind(".")
                address=output.loc[i,'address']
           
                address=output.loc[i,'address'][:start_pos]+" "+output.loc[i,'address'][end_pos+2:]
                
                address=address.replace(".",",")
       
      
            if "-" in output.loc[i,'address'].lower():
                address=output.loc[i,'address']
        
                end_pos=output.loc[i,'address'].lower().find("-")
                address=address[end_pos+1:]
         
                output.loc[i,'address']=address

            if output.loc[i,'address'][-2:]!='MA':
                output.loc[i,'address']=output.loc[i,'address']+", MA"

    return output
     
  
def isME(output):

    '''
    reducing the gap between the , and the city/road name
    '''
    for i,r in output.iterrows():
        if not pd.isnull(output.loc[i,'state']):
            if "ME" in output.loc[i,'state']:
                address=output.loc[i,'address']
                comma_pos=address.rfind(",")
                if address[comma_pos-1]==' ':
    
                    address=address[:comma_pos-1]+address[comma_pos:]
            
                    output.loc[i,'address']=address
    return output




import numpy as np
def isMS(output):
    '''
    Put a comma before MS
    remove text before the - and Number
    '''
    for i,r in output.iterrows():
        if not pd.isnull(output.loc[i,'state']):
            if 'MS' in output.loc[i,'state']:
                address=output.loc[i,'address']
                state_pos=address.find('MS') 
                if address[state_pos-1]==" ":
                    address=address[:state_pos-1]+", "+address[state_pos:]
                    output.loc[i,'address']=address

                if '-' in output.loc[i,'address']:
                    s_pos=output.loc[i,'address'].find("-")
                    output.loc[i,'address']=output.loc[i,'address'][s_pos+1:]
    return output



import re
def isNH(output):
    """
    1. Remove all words before the first number
    2. Add comma before state and city

    """
    for i,r in output.iterrows():
        if not pd.isnull(output.loc[i,'state']):
            if 'NH' in output.loc[i,'state']:
                address=output.loc[i,'address']
                if isinstance(address[0],str):
                 
                    m = re.search(r"\d", address)
                    address=address[m.start():]
            
                #Add comma before state
                state_pos=address.find('NH')
                address=address[:state_pos-1]+", "+address[state_pos:]

                space_pos=address.rfind(" ",0,state_pos)
                address=address[:space_pos]+","+address[space_pos:]
                output.loc[i,'address']=address

    return output

def isKY(output):
    for i,r in output.iterrows():
        try:
            if 'KY' in output.loc[i,'state']:
                if 'KY' in output.loc[i,'address']:
                    address= output.loc[i,'address']
                    s_pos=address.find(" KY ")
                    address=address[:s_pos]+","+address[s_pos:]
                    
                    l_pos=address.rfind(',')
                    a=address[:l_pos]
                    s_pos=a.rfind(" ")
                    a=a[:s_pos]+","+a[s_pos:]
                    address=a+address[l_pos:]
                    #print(address)
                    output.loc[i,'address']=address



        except:
            continue
    return output

    


output=pd.DataFrame(columns=['state','address'])
for filename in glob.glob("../../00_source_data/Polling Data By Year 2016/*"):
    data=pd.read_csv(filename)

    #Rename Columns
    if 'Address' in data.columns:
        data=data.rename(columns={'Address':'address'})
    
    if 'State' in data.columns:
        data=data.rename(columns={'State':'state'})

    #Where state is mentioned in the data
    if 'state' in data.columns:
        data=data[['address','state']]
        output=pd.concat([output,data], ignore_index=True)
    else:
        data=data[['address']]
        output=pd.concat([output,data], ignore_index=True)


output=output.drop_duplicates()

output=output.dropna(subset=['address'])

'''
First check if there is a zip code present
If so,
    then check to see if there is a commma present between the zipcode and the state
Else
    Check to see if State is present in Address.
    if state is not present address,
        then append state to the string
    else

'''
#checking if there is a comma between State and ZipCode and remove it
#remove all content inside parathesis
a = set()
for i,r in output.iterrows():

    address=output.loc[i,'address']

    #Remove content inside paranthesis
    if '(' in address:
        s_pos=address.find('(')
        e_pos=address.find(')')
        address=address[:s_pos]+address[e_pos+1:]
    

    try:
        if isinstance(address[0],str):
            if re.search(r"\d", address).start()!=0:
        
                m = re.search(r"\d", address)
                address=address[m.start():]
           
    except:
        continue


    if address[-2:-1].isnumeric():
        
        if address[-7:-6]==',':
            a.add(output.loc[i,'state'])
            address=address[:-7]+" "+address[-5:]
    
    else:
        
        try:
            if output.loc[i,'state'] in address and not pd.isna(output.loc[i,'state']):
                pass
            else:
                a.add(output.loc[i,'state'])
                address=address+", "+str(output.loc[i,'state'])
        except:
            continue
    output.loc[i,'address']=address


output=isMA(output)
output=isME(output)
output=isMS(output)
output=isNH(output)
output=isKY(output)
output=isLA(output)

    
    

#return a

#MA has extra text
    #Remove the words from Vote till a period.
#ME has extra space between ,
#MS add , before the state
#NH add , before the state and also before the city (word before the state)


#------
# KY needs to add , before city and state
# LA add states to all


output=output['address']

_=output.to_csv("../../00_source_data/2016_polling_data_cpi/2016_final_geocoded.csv")


#return a

#MA has extra text
    #Remove the words from Vote till a period.
#ME has extra space between ,
#MS add , before the state
#NH add , before the state and also before the city (word before the state)
