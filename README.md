# Automatic connection to Sferum lessons

## Description

A small script that automatically connects the user to the lessons in Sferum according to given schedule. So that you can not attend lessons in person.

## How to run
Install requirements with ```pip install -r requirements.txt```.

Replace ```SESSION_DATA``` in ```config.py``` with your session_data cookie from Sferum account. Then add in ```main.py``` your lessons with start time, end time and token from join link (ex. https://sferum.ru/?p=join_call_page&callId=sometoken).

```python
lessons = [
    ["starttime", "endtime", "token from link"],
    ["14:40:00", "15:24:00", "1bHkB06jRd8iOdfsdFDGfgfdggdfSD"],
]
```

And launch ```python3 main.py```.
