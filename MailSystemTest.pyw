import json
import requests
#************************************* Start of Test Cases *************************
#URL = "http://localhost:8080/email/send"
URL = "http://mazmsa.pythonanywhere.com/email/send"
#------------------------------ Test Case 1 --------------------------

sender = "Joe Black <Joe.black@toyland.com>"
receiver = "The king <nkingm1@yahoo.com>"
subject = "hello from heroku 1"
messageText = "How are you King ?"

result = requests.post(URL,
    data={"from": sender,
          "to": receiver,
          "subject": subject,
          "messageText": messageText})
print (result)
print (result.text)


#------------------------------ Test Case 2 --------------------------

sender = ["Joe Black <Joe.black@toyland.com>"]
receiver = "The king <nkingm1@yahoo.com>"
subject = "hello from heroku 2"
messageText = "How are you King ?"

result = requests.post(URL,
    data={"from": sender,
          "to": receiver,
          "subject": subject,
          "messageText": messageText})
print (result)
print (result.text)



#------------------------------ Test Case 3 --------------------------

sender = ["Joe Black <Joe.black@toyland.com>"]
receiver = ["The king <nkingm1@yahoo.com>"]
subject = "hello from heroku 3"
messageText = "How are you King ?"

result = requests.post(URL,
    data={"from": sender,
          "to": receiver,
          "subject": subject,
          "messageText": messageText})
print (result)
print (result.text)



#------------------------------ Test Case 4 --------------------------

sender = "Joe Black <Joe.black@toyland.com>"
receiver = "The king <nkingm1@yahoo.com>; The prince <nkingm2@yahoo.com>"
subject = "hello from heroku 4"
messageText = "How are you King ?"

result = requests.post(URL,
    data={"from": sender,
          "to": receiver,
          "subject": subject,
          "messageText": messageText})
print (result)
print (result.text)

#------------------------------ Test Case 5 --------------------------

sender = "Joe Black <Joe.black@toyland.com>"
receiver5 = [" The prince <nkingm2@yahoo.com>;","The king <nkingm1@yahoo.com>"]
subject = "hello from heroku 5"
messageText = "How are you King ?"

result = requests.post(URL,
    data={"from": sender,
          "to": receiver5,
          "subject": subject,
          "messageText": messageText})
print (result)
print (result.text)

