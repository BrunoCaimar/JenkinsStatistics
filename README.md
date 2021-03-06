[![Build Status](https://travis-ci.org/BrunoCaimar/JenkinsStatistics.svg)](https://travis-ci.org/BrunoCaimar/JenkinsStatistics)
[![Coverage Status](https://coveralls.io/repos/BrunoCaimar/JenkinsStatistics/badge.svg?branch=master&service=github)](https://coveralls.io/github/BrunoCaimar/JenkinsStatistics?branch=master)
[![Code Health](https://landscape.io/github/BrunoCaimar/JenkinsStatistics/master/landscape.svg?style=flat)](https://landscape.io/github/BrunoCaimar/JenkinsStatistics/master)

## JenkinsStatistics
Generate some statistics from a Jenkins CI Server

## What is this? 
Python script to extract data from a Jenkins-CI Server and generate some statistics like:

```python
---------------------------------------------------------------------------------------
------------------ ACTIVE JOBS BY MONTH ( ACTIVE = AT LEAST ONE BUILD ) ---------------
---------------------------------------------------------------------------------------
01/2015 | 02/2015 | 03/2015 | 04/2015 | 05/2015 | 06/2015 | 07/2015 | 08/2015 | 09/2015
---------------------------------------------------------------------------------------
   6    |    5    |    4    |    7    |    6    |    6    |    5    |    9    |    6
---------------------------------------------------------------------------------------

------------------------------------------------------------------
------------------- BUILDS BY MONTH  -----------------------------
------------------------------------------------------------------
| MONTH/YEAR|  ABORTED   |  FAILURE   |  SUCCESS   |  UNSTABLE  |
------------------------------------------------------------------
|  01/2015  |      0     |     13     |     25     |      0     |
|  02/2015  |      0     |      1     |     28     |      0     |
|  03/2015  |      0     |      2     |     15     |      0     |
|  04/2015  |      0     |     11     |     45     |      0     |
|  05/2015  |      1     |     29     |     96     |      0     |
|  06/2015  |      0     |      3     |     44     |      0     |
|  07/2015  |      1     |      0     |     30     |      0     |
|  08/2015  |      1     |      2     |     105    |     21     |
|  09/2015  |      0     |      9     |     41     |      0     |
------------------------------------------------------------------

-------------------------------------------------------------------------
|  TOP JOBS BY BUILDS: 9/2015  |
-------------------------------------------------------------------------
|                            CLOUD-XISTO: 19                            |
|                              Victor: 14                               |
|                           Massive Attack: 4                           |
-------------------------------------------------------------------------
```

# How to use? 
- Config jenkins_statistics_config.py

-- Add url on jenkins_url

-- Add user and password (if necessary )

-- Change the number of month's that you want to report

-- Inform if you want to include the current month 

- Run jenkins_statistics_reports.py

## To do
- Reports in HTML
- Add parameters using command line params 

## Dependencies
- Python Jenkins Library - https://pypi.python.org/pypi/python-jenkins

```python
pip install python-jenkins 
or 
pip install -r requirements.txt
```

## License
- MIT License 

