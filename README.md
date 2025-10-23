# Application Automator - // - 23/10/2025 - WE ARE SO BACK - //


Application helper - scrapes data from Student BIO and completes application flowchart based on it. We complete hundreds of applications a day by hand - in theory automating the process would save us at least 2 hrs a day *EACH*. 

all written in python using selenium for all the browser interaction (scraping and inputting) and pandas for any data it needs to drag in (Applicant list + age requirement list)

Consists of two main sections - Function dictionary containing each step of application process and Controller. FE process is the only process pathway it can handle at the moment however structure was deliberate in order to allow sequence of functions executed to be be re-ordered in the controller to allow for application in other process pathways such as LLD or short course offer. 

Two source Excel files are required for the program to function:

- "Age requirements" which defines all of the age requirements for each coursecode, a stand-in as i had not been granted access to marketings course information database
- "New Applications" a large table containing details required to locate the students application within REMS. PANDAs is used to process this data so please be aware it is very particular about which columns contain what.





*additional features* 

- Retry on stale wrapper + stale click + stale dropedowns: pretty neat little thing that increases process success rate, selenium can be a little fickle therefore having the extra buffer before the whole thing crashes out is great.
- Get_element_text(locator) function - slight adjustment to seleniums default get element text command which helps reduce crash due to white space syntax errors.
- action router - really cool little function that reads what step the application is on and then runs the associated function.




  


