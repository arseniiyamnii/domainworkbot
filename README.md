How to use? 
0-clone  
```
git clone git@github.com:arseniiyamnii/domainworkbot.git && cd domainworkbot
``` 
1.0 - run env
```
sudo apt install python3-venv
source env/bin/activate || python3 -m venv env && source env/bin/activate
```

1-install dependencys
dep  
```
sudo apt install python3-pip
```
```
pip3 install -r requirements.txt
```  
2- ./main.py init for download repo  
```
./main.py init
``` 
3-export vars  
```
export TELEGRAMM_API_BOT_TOKEN=""
export GITLAB_ACCESS_TOKEN=""
export GITLAB_PROJECT_ID=""
export GITLAB_REPO_SSH=""
export DOMAIN_MAIN_URL_START=""
export DOMAIN_MAIN_URL_END=""
```
example:  
```
export TELEGRAMM_API_BOT_TOKEN="xxx777xxx777"
export GITLAB_ACCESS_TOKEN="777xxx777xxx"
export GITLAB_PROJECT_ID="123456"
export GITLAB_REPO_SSH="git@gitlab.com/1xbet/1xbet"
export DOMAIN_MAIN_URL_START="1xbet"
export DOMAIN_MAIN_URL_END=".com"
```

4-run ./main.py start  
```
./main.py start
```  
  
  
