#---------------------------------------------------------------------OMBOT--------------------------------------------------


#things to do:

#       Finish FE process Function dictionary
#       RetrieveBio - am unsure about DPO, is it better to recall on each process or store as global variables
#       FE-PROCESS, "missing info on application?" if yes then continue until "missing info recieved?" email, stuff all sorted within rems
#       FE-PROCESS, "EHCP?" if yes then Continue until "EHCP recieved from council?", break, signal and loop to new ID after
#       FE-PROCESS, "ASN?" If yes then continue until "ASN form recieved?", break, signal and loop to new ID after
#       FE-PROCESS, "Criminal conviction?" If yes then continue until "complete D1 or D2", break, signal and loop to new ID after
#       FE-PROCESS, "Age Suitable?" Need access to database, either make own or access activate learning course list to verify.
#       FE-PROCESS, "Assesment required?" apparently only GCSE or ACCESS have assesments. so see if course has GCSE or ACCESS in name. act accordingly
#       FE-PRROCESS, "Applied to 3 or more?" if yes then continue until "send book for triage comms", break, signal and loop to new ID after
#       Start with basic Feprocess and then add fail states as we go
#       Figure out error handeling - abandon the process and go to next learner if fail for anyreason, flag it somehow for manual processing
#       python library log4 - some sort of log system to see what where failure occurs/where the program is at - check points mabye?


from selenium import webdriver 
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd 
import time



#-----------------------------------------------------------------FUNCTION DICTIONARY--------------------------------------------------




def searchnames (searchfirstname, searchlastname, searchdob):

    driver.switch_to.default_content()

    learnersbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/input[1]")))
    learnersbutton.click()

    appdetailsbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[6]/div/div[11]")))
    appdetailsbutton.click()

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
    
    driver.implicitly_wait(2)
    submitbutton = driver.find_element(By.ID, "sub1")
    submitbutton.click()


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
    
    submitbutton =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Submit1")))
    submitbutton.click()
    
    checkname = str(clicklastname) + " " + str(clickfirstname)
    rowposit = 1
    match_count = 0 
    total_rows = 0
    twofound = False


    wait = WebDriverWait(driver, 10)
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
    
    
    
    selectbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "select1"  )))
    selectbutton.click()
    

def retrievebio():
    
    iframeoverpage = driver.find_element(By.ID, "overpage")
    driver.switch_to.frame(iframeoverpage)

    #list of learner data and their respective variable names.

    #BIOGRAPHICAL data locations

    Firstname = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[1]").text
    Lastname = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[1]").text

    Homeaddress1 = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[9]/div[1]").text
    Homeaddress2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[10]/div[1]").text
    Homeaddress3 = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[11]/div[1]").text
    Towncity = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[12]/div[1]").text
    Country = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[14]/div[1]").text
    Postcode = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[8]/div[1]/a").text

    Hometel = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[16]/div[1]").text
    Mobiletel = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[17]/div[1]/a").text
    Personalemail = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[19]/div[1]/a").text

    DoB = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[23]/div[1]").text
    AgeinAUG = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[25]/div[1]").text
    

    additionalbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[16]/input")))
    additionalbutton.click()

    visadetailsbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[2]/div[2]/div[12]/a"))))                        
    visadetailsbutton.click()

    iframevisa = driver.find_element(By.ID, "pVisa")
    driver.switch_to.frame(iframevisa)
    
   

    visa = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]").text
    if visa == False:
        visa = " "
    else:
        pass

    driver.switch_to.parent_frame()
    appliedto = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[2]/div[20]/input"))))
    appliedto.click()

    course_table = driver.find_element(By.XPATH, "//table[@id='PROVlisttable']")  # Adjust XPath as per your page
    course_rows = course_table.find_elements(By.XPATH, "./tbody/tr")  # Get all rows in the table
    
    courses = []

    for row in course_rows:
        try:
            # Assuming columns: Course Code in column 1, Course Name in column 2 (adjust as needed)
            course_code = row.find_element(By.XPATH, "./td[1]").text
            course_name = row.find_element(By.XPATH, "./td[3]").text

            courses.append({
                'course_code': course_code,
                'course_name': course_name
            })
        except Exception as e:
            print(f"Error extracting course data: {e}")

    try:
        ageinaugint = int(AgeinAUG.strip()) 
    except ValueError:
        print("Error: AgeInAug data is invalid!")
        ageinaugint = -1 

    return {
        'firstname' : Firstname,
        'lastname' : Lastname,
        'Homeaddress 1': Homeaddress1,
        'Homeaddress 2' : Homeaddress2,
        'Homeaddress 3' : Homeaddress3,
        'towncity' : Towncity,
        'country' : Country,
        'postcode' : Postcode,
        'hometel' : Hometel,
        'mobiletel' : Mobiletel,
        'personalemail' : Personalemail,
        'dob' : DoB,
        'AgeInAug' : ageinaugint,
        'visa' : visa,
        'courses' : courses
     }


def choosecourse(course): #need to loop and check if course has already been processed or not - if it is second course processed then need to change location of "progress button" mabye function out progress and add loop counter
    
    driver.implicitly_wait(2)
    
    processbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Button1")))
    processbutton.click() #click process


    iframemodpop1 = driver.find_element(By.ID, "modpop1")
    driver.switch_to.frame(iframemodpop1)

    applicanttypebutton =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/table/tbody/tr[1]/td[5]/a")))
    applicanttypebutton.click() #click "applicanttype?"

    iframeModpopup = driver.find_element(By.CLASS_NAME, "mcsspopupframe")
    driver.switch_to.frame(iframeModpopup)

    dropdown =  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "1_Provision_Title")))

    select = Select(dropdown)
    for option in select.options:
    
        if course in option.get_attribute('value'):
            select.select_by_value(option.get_attribute('value'))
            print(f"Selected course: {option.get_attribute('value')}")

    submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Submit1")))
    submitbutton.click()

    driver.switch_to.parent_frame()


def applicanttype():

    #FE-PROCESS, "Applicant type?"for now always yes for simplicity can be configured later to multioption
    driver.implicitly_wait(2)

    processbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    processbutton.click()

    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)

    submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
    submitbutton.click() 

    submitbutton.click()

    print ("FE-Process selected")

    driver.switch_to.parent_frame()


def currentstudentcheck():

    driver.implicitly_wait(2)

    #dupe checks mean that this is ALWAYS no - any current students will be approved by hand
    progressbutton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    progressbutton.click()
    
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]")))
    driver.switch_to.frame(iframenextstep)

    submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
    submitbutton.click() 
    submitbutton.click()

    print("Applicant is not current student")

    driver.switch_to.parent_frame()


def applicantrts(bio): 
    
    driver.implicitly_wait(2)

    progressbutton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    progressbutton.click()
    
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)

    visa = bio.get('visa', '')
    
    if "Student" in visa:
        
        submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
        submitbutton.click() 
        submitbutton.click()
        print ("applicant does NOT have provisional RTS")
        driver.switch_to.parent_frame()
        return False

    else:
        
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ENTER) 

        submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
        submitbutton.click() 
        submitbutton.click()
        driver.switch_to.parent_frame()

        return True


def missinginfo(bio): 

    time.sleep(1)

    progressbutton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    progressbutton.click()
    
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)
    
    issues = []

    if not bio.get('firstname') or not bio.get('lastname'):
        issues.append("Missing full name (firstname and/or lastname).")

    if not (bio.get('Homeaddress 1') or bio.get('Homeaddress 2') or bio.get('Homeaddress 3')):
        issues.append("Missing home address (at least one line of the address).")

    if not bio.get('postcode'):
        issues.append("Missing postcode.")

    if not bio.get('towncity'):
        issues.append("Missing town/city.")

    if not (bio.get('hometel') or bio.get('mobiletel')):
        issues.append("Missing contact telephone number (either home or mobile).")

    if not bio.get('personalemail'):
        issues.append("Missing personal email.")

    if not bio.get('dob'):
        issues.append("Missing date of birth (DoB).")

    if not issues:
        
        submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
        submitbutton.click() 
        submitbutton.click()

        driver.switch_to.parent_frame()
        return "All required information is present."
    else: 
        driver.switch_to.parent_frame()
    
    
    dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/select")))
    
    dropdown.send_keys(Keys.ARROW_DOWN)
    dropdown.send_keys(Keys.ARROW_DOWN)

    submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
    submitbutton.click() 
    submitbutton.click()

    return issues


def agesuitable(bio, course):
    
    agesuitability = 'Age requirements.xlsx'
    df = pd.read_excel(agesuitability, usecols="C, E")
    df["Course code"] = df["Course code"].str.strip()
    df_indexed = df.set_index("Course code") 

    age_requirement = df_indexed.loc[course, 'Age suitable']


    progressbutton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    progressbutton.click()
    
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)

    studentage = bio.get('AgeInAug', -1)
    
    if studentage == -1:
        print("Age in August is not provided in the bio.")
        return False
    
    if studentage is None:
        raise ValueError("Student age not found in BIO dictionary.")
    
    if age_requirement == '19+':
        if studentage >= 19:
            
            driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
            driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
            submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
            submitbutton.click() 
            submitbutton.click()

            
            return True
        else:
            print(f"The applicant does not meet the age requirement (19+) for course {course}.")
            submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
            submitbutton.click() 
            submitbutton.click()

            
            return False 
        
    elif age_requirement == '16-18':
        if 16 <= studentage <= 18:
            
            driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
            driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
            submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
            submitbutton.click() 
            submitbutton.click()
        
            return True 
        else:
            print(f"The applicant does not meet the age requirement (16-18) for course {course}.")
            submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
            submitbutton.click() 
            submitbutton.click()
            
            return False  
    

def ageselect(bio): 
    
    driver.switch_to.parent_frame()

    progressbutton = driver.find_element(By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))
    driver.implicitly_wait(5)
    progressbutton.click()
   
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)
   
    age = bio.get('AgeInAug')
    if age >= 19:

        
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/select").send_keys(Keys.ARROW_DOWN)

        submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
        submitbutton.click() 
        submitbutton.click()
        driver.switch_to.parent_frame()
        print ("19+ selected")
       
    
    else:

        submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
        submitbutton.click() 
        submitbutton.click()
        driver.switch_to.parent_frame()
        print ("16-18 Selected")
               

def sendcomms():
    
    progressbutton = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, ("/html/body/div[1]/div[2]/table/tbody/tr/td[8]/a"))))
    progressbutton.click()
   
    iframenextstep = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'mcsspopupframe') and not(@id='modpop1')]"))) 
    driver.switch_to.frame(iframenextstep)
    
    submitbutton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "subm1")))
    submitbutton.click() 
    submitbutton.click()
    driver.switch_to.parent_frame()


def processlearner(firstname, lastname, dob, coursecode):
    
    #1. Learner Lookup #//todo// add error if entries =0
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


    #4. Retrieve bio data
    bio = retrievebio()
   
    #5. Change action
    choosecourse(coursecode)

    #6. Applicant type - EPROCESS always
    applicanttype()

    #7. Check if current student (ALWAYS no as dupe check filters)
    currentstudentcheck()

    #8. Does Applicant have provisional RTS? - falsey response from this point, will be processed to withdraw within function for organisations sake
    rts = applicantrts(bio)
    if rts == False:
        print("No provisional RTS, international comms sent") #//TO CHECK// check process is ok?>
        return  False
    else:
        print("Applicant has provisional RTS")

    #9. Missing information on application?
    info = missinginfo(bio)
    if info == "All required information is present.":
        print("All required information is provided.")
    else:
        print("The following information is missing:")
        for issue in info:
          print(f"- {issue}")
        else:
            print("No Missing info on application")

    #10. Is Age suitable for course?
    age = agesuitable(bio, coursecode)
    if age == False:
        print("Age not suitable for course - //HUMAN// can any other course be offered?")
        return False
    else:
        print("Age is suitable")

    #11. 16-18 or 19
    ageselect(bio)


    #12. 16-18 or 19
    sendcomms()

    #13. Consent given to parent

    #14. send parent comms (sendcomms())

    #15. applied for 3 or more courses?

    return True



#--------------------------------------------------------CONTROLLER--------------------------------------------------------





#Headless choice

print("> Safemode? (Y/N) ")
Headlessinput = input().upper()

edge_options = Options()
if Headlessinput == 'N':
    edge_options.add_argument("--headless")
    edge_options.add_argument("--window-size=1920x1080")  
    print("Running in Normal mode...")
else:
    print("Running in Safemode...")

# Init WebDriver

driver = webdriver.Edge(options=edge_options)

driver.get('https://eds.activatelearning.ac.uk/portal/html/HOM/portalhome.htm#LNR_learnerstart')
driver.refresh()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/input[1]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[6]/div/div[11]"))).click()


#Manual choice - TODO step selection - input number in order to jump to process from/only that section?

print("> Manual override? (Y/N) ")
manual_override = input().upper()


if manual_override == 'Y':
    
    print("Enter the details for the learner you want to process.")
    searchfirstname = input("Enter First Name: ")
    searchlastname = input("Enter Last Name: ")
    searchdob = input("Enter Date of Birth (DD/MM/YYYY): ")
    searchcoursecode = input("Enter course code: ")
    
    print(f"--------[MANUAL] Processing: {searchfirstname} {searchlastname} {searchdob} {searchcoursecode} --------")
    
    

    processedchek = processlearner(searchfirstname, searchlastname, searchdob, searchcoursecode,)

    if processedchek == True:

        print(f"Processed {searchfirstname} {searchlastname} for {searchcoursecode} successfully.\n")

        
        
    else:
        print(f"Issue found with {searchfirstname} {searchlastname}, Human Intervention required.\n")

   
    driver.quit()


else:

    #init pandas

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
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "can1"))).click()
            loopcounter += 1
            continue
        
        else:
            print(f"Skipping {dffirstname} {dflastname} Human Intervention required.\n")
            loopcounter += 1
            continue  

    print("All learners processed.")
    driver.quit()


            


    
    
   





