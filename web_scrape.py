#     Delivery Date:  2017.10.11
#     Author:         tabrett
#     Purpose:        Programatically scrape HTML source code to retrieve
#                     Attorney State Licensing data

import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import glob

# url to be scraped
webpg = 'https://www.insidearm.com/state-laws/'

# lists
A=[]    # State Name
B=[]    # License Data
C=[]    # Bond Data
D=[]    # Fees Data
E=[]    # Exemptions Data

# query page and return html to variable
page = urllib.request.urlopen(webpg)
soup = BeautifulSoup(page, 'html.parser')

# pulls hidden cards for each state
hidden_card = soup.find_all(class_='card hiddenstate')

# loop through each state card
for ea_card in hidden_card:
    # find/identify state
    find_h2 = ea_card.find('h2')

    # find table for state's license/bond/fee info 
    all_tables = ea_card.find_all('table')

    # recurse through table rows
    for row in all_tables:
        # create list of <tr> tags
        col2 = row.find_all('tr')

        # append State to list.  placed here incase of multiple lines needing State ID
        A.append(find_h2.get_text())

        # loop through each <tr> tag
        for data in col2:
            # create list of <td> tags
            head = data.find_all('td')

            # loop through each <td> tag
            for title in head:
                # <strong> tag identifies header for data elements
                if title.find('strong'):
                    # append to correct data list
                    if title.get_text() == 'License':
                        hdr = title.next_element.next_element.next_element.next_element
                        B.append(hdr.get_text())
                    elif title.get_text() == 'Bond':
                        hdr = title.next_element.next_element.next_element.next_element
                        C.append(hdr.get_text())
                    elif title.get_text() == 'Fees':
                        hdr = title.next_element.next_element.next_element.next_element
                        D.append(hdr.get_text())

        # find the 'Exemptions' <h3> tag
        find_h3 = ea_card.find_all(string='Exemptions')

        # check if 'Exemptions' was found...
        if find_h3:
            for ea_h3 in find_h3:
                if ea_h3 == 'Exemptions':
                    li_string = ''
                    i = 1
                    
                    # find first <p> tag after 'Exemptions' (contains Exemptions data)
                    post_h3 = ea_h3.find_next('p')
                    content = post_h3.get_text()
                    
                    # identify if there is a list under the 'Exemptions header
                    if ':\n' in content:
                        post_ul = ea_h3.find_next('ul')
                        post_li = post_ul.find_all('li')
                        
                        # loop through each <li> tag in <ul>
                        for ea_li in post_li:
                            # create string of each <li>, incrementing.
                            li_string = li_string + str(i) + '. ' + ea_li.get_text() + ' '
                            i+=1
                    
                    # replace newline characters with space
                    content = content.replace('\n', ' ')
                    
                    # append to 'Exemption' array
                    E.append(content + li_string)
        # if not found, append 'None.' (keeps list length consistent)
        else:
            E.append('None.')

# create panda dataframe, appending each list as a column
df = pd.DataFrame(A,columns=['State'])
df['License']=B
df['Bond']=C
df['Fees']=D
df['Exemptions']=E
 
# export dataframe to tab-delimited csv
df.to_csv(r'C:\Users\tabrett\Desktop\Scripts\Py Scripting\PyOut\State_License_Info.txt', index=None, sep='\t', mode='a')
print("State_License_Info.txt complete.")



# verify that file was created
if glob.glob('./PyOut/State_License_Info.txt'):
    print("Proceeding to database load.")
else:
    print("No file...exiting.")
    exit()


# completion message
print('Complete.')