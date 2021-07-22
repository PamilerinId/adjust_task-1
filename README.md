# Adjust Home Task Solution [Python/Flask]

## Setup 
* run `pip install pipenv`
* run `cd adjust_task-1` then run `ls` and make sure you see config, main, static etc. folders
* run `pipenv shell` then `pipenv install`
* finally to launch the app run `flask run`


Common API use-cases:
1. http://127.0.0.1:5000/metrics?date_from=06-01-2017&group_by=channel&group_by=country&sort_by=clicks&sort_order=DESC&columns=channel,country,impressions,clicks
2. http://127.0.0.1:5000/metrics?date_from=05-01-2017&date_to=05-31-2017&sort_by=date&group_by=date&sort_order=DESC&columns=date,os,installs&os=ios
3. http://127.0.0.1:5000/metrics?date_from=06-01-2017&date_to=06-01-2017&sort_by=revenue&group_by=os&sort_order=DESC&columns=date,os,country,revenue&country=US
4. http://127.0.0.1:5000/metrics?sort_by=cpi&group_by=channel&sort_order=DESC&columns=country,channel,spend&country=CA&cpi=True


* `.env` file is also commited to repo for ease of use