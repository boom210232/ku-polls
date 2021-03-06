[![Build Status](https://travis-ci.com/boom210232/ku-polls.svg?branch=main)](https://travis-ci.com/boom210232/ku-polls) 
[![codecov](https://codecov.io/gh/boom210232/ku-polls/branch/main/graph/badge.svg?token=HH9U768Q44)](https://codecov.io/gh/boom210232/ku-polls)    
# ku-polls         

## About this application       
This web application is made for KU community to collect and show the result of survey that answered the requirements of KU community.

## Link
[Home](https://github.com/boom210232/ku-polls/wiki)      
[Vision Statement](https://github.com/boom210232/ku-polls/wiki/Vision-Statement)     
[Requirements](https://github.com/boom210232/ku-polls/wiki/Requirements)    
## Iteration           
### Iteration 1        
- [Iteration 1 plan](https://github.com/boom210232/ku-polls/wiki/Iteration-1-Plan)          
- [Task Board](https://github.com/boom210232/ku-polls/projects/1)              
### Iteration 2        
- [Iteration 2 plan](https://github.com/boom210232/ku-polls/wiki/Iteration-2-Plan)          
- [Task Board](https://github.com/boom210232/ku-polls/projects/2)          
### Iteration 3        
- [Iteration 3 plan](https://github.com/boom210232/ku-polls/wiki/Iteration-3-Plan)          
- [Task Board](https://github.com/boom210232/ku-polls/projects/3)           
  

## Running KU Polls        
Before starting the process, Create a virtual environment using these command      
 
For MacOS and Linux    
```
python3 -m venv env
```         
For Windows      
``` 
python -m venv env
``` 

Make sure that virtual environment are ready and activated.              
For Linux and MacOS    
```
. env/bin/activate
```     
     
For Windows     
```
env\Scripts\activate
```      
        
Then type this command:       
```
python -m pip install -r requirements.txt 
```              

Please use these command first to initiation polls database.
```
python manage.py migrate
python manage.py loaddata users polls
```

After load data you need to activate key by go to `mysite > note_env.txt ` then change this file to `.env` for allow to use this application.     
Then,For running in your localhost 127.0.0.1 please use command below.
``` 
python manage.py runserver
```       
Users provided by the initial data (users.json):     
Here is a demo accounts for testing this application.         

| Username  | Password    |
|-----------|-------------|
| demo001     | Tester001    |
| demo002     | Tester002    |        
  
