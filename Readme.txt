Project Name: Email Service 
Author: Mahmoud Assi 
Creation Date: 09/21/2014
Programming Language used: Python (Beginner level of experience, just completed a Coursera course a month ago)
Solution Focus: Backend

1. Problem Description
----------------------
Create a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

Example Email Providers:

    SendGrid - Simple Send Documentation
    Mailgun - Simple Send Documentation
    Mandrill - Simple Send Documentation

All three services are free to try and are pretty painless to sign up for, so please register your own test accounts on each.

2. Solution Description:
------------------------
A web service interface that follow RESTful services guidelines written in Python, The post method was implemented for sending a new email, here are details

 2.1. Send Mail Service
 ----------------------
 - Service URL: http://mazmsa.pythonanywhere.com/email/send
 - HTTP Method: POST
  
  2.1.1. Parameters:
  ------------------
   - from (String): sender email, example: "sender123@yahoo.com", "<sender123@yahoo.com>","Sender Name <sender123@yahoo.com>", ["Sender Name <sender123@yahoo.com>"] 
   - to (String or list of strings): the receiver email, example: "receiver123@yahoo.com","<receiver123@yahoo.com>","recierver 123 Name<receiver123@yahoo.com>", "recierver 123 Name<receiver123@yahoo.com>; recierver 124 Name<receiver124@yahoo.com>", ["recierver 123 Name<receiver123@yahoo.com>","recierver 124 Name<receiver124@yahoo.com>"]
   - subject (String): subject of the email, example : Happy Birthday
   - messageText(String): email body 
   
   2.1.1.1. Request Example
   ------------------------
   - result = requests.post("http://mazmsa.pythonanywhere.com/email/send",
      data={"from": "sender123@yahoo.com",
            "to": "receiver123@yahoo.com",
            "subject": "Test Email message",
            "messageText": "How are you, did you get my message?"})

  
  2.1.2. Responses:
  -----------------
   - 200: in case message was sent Successfully
   - 400: in case there was an error on sending the message
   - 500: In case of internal server error
   - text: Error message in case of error, empty string in case of successful transactions 

  
 2.2 Architecture
 ----------------
 
 