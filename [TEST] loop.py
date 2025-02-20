from selenium import webdriver 
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import pandas as pd 
import time

def retry_on_stale(max_retries=3):
    def decorator(func):  
        def wrapper(*args, **kwargs): 
            for attempt in range(max_retries): 
                try:
                    return func(*args, **kwargs)  
                except Exception as e:  
                    if attempt < max_retries - 1: 
                        print(f"Retrying {func.__name__}, attempt {attempt + 1}")
                    else:
                        print(f"Failed after {max_retries} retries. {e}")
                        raise  
        return wrapper 
    return decorator  



#Handles Stale clicks
@retry_on_stale(max_retries=3)
def click_element(locator):
    """Clicks an element specified by a locator."""
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator)).click()


def searchnames (searchfirstname, searchlastname, searchdob):
    
    driver.switch_to.default_content()

    click_element((By.XPATH, "/html/body/div/div[4]/input[1]"))

    click_element((By.XPATH, "/html/body/div/div[6]/div/div[11]"))

    print(f"Searching for {searchfirstname} {searchlastname} {searchdob}...")

    driver.switch_to.default_content()
    iframepagewin = driver.find_element(By.ID, "pagewin")
    driver.switch_to.frame(iframepagewin)

    inputboxforename = driver.find_element(By.ID, "Forename").clear()
    inputboxsurname = driver.find_element(By.ID, "Surname").clear()
    inputboxdob = driver.find_element(By.ID, "DoB").clear()


    inputboxforename = driver.find_element(By.ID, "Forename")
    inputboxsurname = driver.find_element(By.ID, "Surname")
    inputboxdob = driver.find_element(By.ID, "DoB")

    inputboxforename.send_keys(searchfirstname)
    inputboxsurname.send_keys(searchlastname)
    inputboxdob.send_keys(searchdob)
    
    click_element((By.ID, "sub1"))
    


def checkname(checklastname, checkfirstname,):

    print("Looking for dupes in 'Check'...")
    
    checkname = str(checklastname) + " " + str(checkfirstname)
    rowposit = 1
    match_count = 0 
    twofound = False
    total_rows = 0
    
    time.sleep(2)

    wait = WebDriverWait(driver, 10) 
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="LSlisttable"]/tbody/tr')))
    
    total_rows = len(rows)
    print(f'number of entries = {total_rows}')

    
    while rowposit <= total_rows:
        try:
                
            activerow = driver.find_element(By.ID, "LSrow"+ str(rowposit) ).text
        
            if checkname in activerow: 
                match_count +=1
                print (f"Found entry in row {rowposit}")
                
                if match_count == 2:
                    twofound = True
                    print("Duplicate found!")
                    return twofound 
                
            else:
                print(f"Match not found in row {rowposit}. Moving to next row.")
            
            rowposit += 1
        
        except Exception as e:
            print (f"Error checking row {rowposit}:")
            break

               
def listname(clickfirstname, clicklastname):

    print("Looking for dupes in 'list'...")
    
    click_element((By.ID, "Submit1"))

    checkname = str(clicklastname) + " " + str(clickfirstname)
    rowposit = 1
    match_count = 0 
    total_rows = 0
    twofound = False


    wait = WebDriverWait(driver, 10)
    time.sleep (1)
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="LSlisttable"]/tbody/tr')))
    total_rows = len(rows)
    print(f'number of entries = {total_rows}')
   
    while rowposit <= total_rows:
        try:
                
            activerow = driver.find_element(By.ID, "LSrow"+ str(rowposit) ).text
            StuID = activerow[0:9] #its a little unstable around here
            print (f"Checking StuID = {StuID}")#log

            if checkname in activerow: 
                match_count +=1
                print (f"Found entry in row {rowposit}")
                
                if match_count == 2:
                    twofound = True
                    print("Duplicate found!")
                    return twofound 
                
            else:
                print(f"Match not found in row {rowposit}. Moving to next row.")
            
            rowposit += 1
        
        except Exception as e:
            print (f"Error checking row {rowposit}:")
            break
    
    
    click_element((By.ID, "select1" ))


def processlearner(firstname, lastname, dob, coursecode):
    
    print(f"Processing learner: {firstname} {lastname} {dob}")
    searchnames(firstname, lastname, dob)
    
    #2. Check 'Check' for duplicates
    dupecheck1 = checkname(lastname, firstname)
    if dupecheck1 == True:
        print("Duplicate found in 'Check'. //HUMAN// Please process manually")
        
        return False
    else:
         print(f"No duplicates found for {firstname} {lastname}. Proceeding...\n")
        

    #3. Check 'list' for duplicates
    dupecheck2 = listname(firstname, lastname)
    if dupecheck2 == True:
        print("Duplicate found in 'list'. //HUMAN// Please process manually")
        return  False
    else:
         print(f"No duplicates found for {firstname} {lastname}. Proceeding...\n")


    #4. click process

    iframeoverpage = driver.find_element(By.ID, "overpage")
    driver.switch_to.frame(iframeoverpage)

    click_element((By.ID, "Button1" )) #click process
    
    
    #5. do stuff
    print("doing stuff")
    time.sleep(1)
    #6. click cancel
    

    print("returned to search screen ")

    return True

















driver = webdriver.Edge()

driver.get('https://eds.activatelearning.ac.uk/portal/html/HOM/portalhome.htm#LNR_learnerstart')
driver.refresh()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/input[1]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[6]/div/div[11]"))).click()


Applicationlist = 'New Applications.xlsx'
df2 = pd.read_excel(Applicationlist, usecols="D, F, G, H, I, J, O")

entries = int(df2.shape[0])
print(f"Total Applications = {entries}")



    #init loop

loopcounter = 0
while loopcounter < entries:
    dffirstname = df2.iloc[loopcounter]['Forename']
    dflastname = df2.iloc[loopcounter]['Surname']
    dfcc = df2.iloc[loopcounter]['ProvCodeParent']

    dfdob = df2.iloc[loopcounter]['DoB']
    tempdob = datetime.strptime(str(dfdob), "%Y-%m-%d %H:%M:%S")
    stripdob = tempdob.strftime("%d/%m/%Y")


    print(f"--------[BULK] Processing: {dffirstname} {dflastname} {stripdob} {dfcc}--------")
        


    processedchek = processlearner(dffirstname, dflastname, stripdob, dfcc,)
    
    if processedchek == True:

        print(f"Processed {dffirstname} {dflastname} successfully.\n")
        loopcounter += 1

        continue
        
    else:
        print(f"Skipping {dffirstname} {dflastname} Human Intervention required.\n")
        loopcounter += 1
        continue  

print("All learners processed.")
driver.quit()