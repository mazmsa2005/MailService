
# A Application done by MAZ to for a mail server
import sys
import requests
import random
from bottle import default_app,route, error, response, request as req
#************************************* Start of Message Class *************************
# Class to represent the email message
class Message:
    # Constructor
    #------------------------------- Start of Constructor Method ----------------------
    def __init__(self, sender, receiver, subject, messageText):
        self.sender = sender
        self.receiver = receiver
        self.messageText = messageText
        self.subject = subject
        #self.senderService = senderService
    #------------------------------- End of Constructor Method ------------------------
    #------------------------------- Start of toString Method ----------------------
    def __str__(self):
        Line_Seperator = '\n'
        string = ''
        string += 'Sender: '+ self.sender
        string += Line_Seperator
        string += 'Receiver: ' + self.receiver
        string += Line_Seperator
        string += 'Subject: ' + self.subject
        string += Line_Seperator
        string += 'Body: ' + self.messageBody
        return string
    #------------------------------- End of toString Method ------------------------

#************************************* End of Message Class ***************************

#************************************* SendResponse of Message Class *************************
# Class to represent the email message
class SendResponse:
    # Constructor
    #------------------------------- Start of Constructor Method ----------------------
    def __init__(self, messageSent = '', statusCode = '', errorMessage = ''):
        self.messageSent = messageSent
        self.statusCode = statusCode
        self.errorMessage = errorMessage
    #------------------------------- End of Constructor Method ------------------------
    #------------------------------- Start of toString Method ----------------------
    def __str__(self):
        Line_Seperator = '\n'
        string = ''
        string += 'message Sent: '+ str(self.messageSent)
        string += Line_Seperator
        string += 'Code: ' + str(self.statusCode)
        if (self.statusCode != requests.codes.ok):
            string += Line_Seperator
            string += 'Error Message: ' + str(self.errorMessage)
        return string
    #------------------------------- End of toString Method ------------------------

#************************************* End of SendResponse Class ***************************

#------------------------------- Start of send_Message_MailGun Method -------------
def send_Message_MailGun (message):
    #Constants
    API_KEY = "key-a355cb73e04f1215ba936e898303d892"
    PUBLIC_API_KEY = "pubkey-ab5ad30e7e6d0be0e78bfd722c954db3"
    SANDBOX_NAME = "sandbox4bab228b6d1041f69be920e16db1328a.mailgun.org"
    URL = "https://api.mailgun.net/v2/" + SANDBOX_NAME + "/messages"
    # variables
    sendResult = SendResponse()
    messageSent = False
    serviceIdentifier = "Service 1, "
    try:

        result = requests.post(URL,
        auth=("api",API_KEY ),
        data={"from": message.sender,
              "to": message.receiver,
              "subject": message.subject,
              "text": message.messageText})

        if (result.status_code == requests.codes.ok):
            messageSent = True

        sendResult.statusCode = result.status_code
        sendResult.messageSent = messageSent
        sendResult.errorMessage = ''

        if (sendResult.statusCode != requests.codes.ok):
            sendResult.errorMessage = "Service 1, " + result.json()["message"]
    except:
        sendResult.statusCode = 500
        sendResult.messageSent = False
        sendResult.errorMessage = serviceIdentifier + sys.exc_info()[0]

    return sendResult
#------------------------------- End of send_Message_MailGun Method ---------------

#---------------------------- Start of seperate_User_Email_List Method ------------
### to convert input of emails in the form of a list or a string into a seperate two list for name and email adjacent to each other at the same index
def seperate_User_Email_List (inputString):

    compinedList = inputString
    if (isinstance(inputString, (str,bytes))):
        compinedList = str(inputString).split(';')
    names = list()
    emails = list()
    seperator = '<'
    for useremail in compinedList:
        temp = useremail.split(seperator,1)
        if (len(temp) > 1):
            names.append(temp[0])
            emails.append(seperator + temp[1])
        else:
            if (len(temp[0].replace(' ','')) > 0): ### Filter empty string case
                names.append(temp[0])
                emails.append(temp[0])
    resultArray = {}
    resultArray ["names"] = names
    resultArray ["emails"] = emails

    return resultArray

#---------------------------- End of seperate_User_Email_List Method --------------

#------------------------------- Start of send_Message_SendGrid Method ------------
def send_Message_SendGrid (message):
    #message.senderService = self.serverNumber
    messageSent = False
    #Constants
    API_USER = "nkingm"
    API_KEY = "SendGrid1"
    URL = "https://api.sendgrid.com/api/mail.send.json"
    # variables
    sendResult = SendResponse()
    messageSent = False
    serviceIdentifier = "Service 2, "

    try:
        sender = seperate_User_Email_List (message.sender)
        receiversList = seperate_User_Email_List (message.receiver)
        result = requests.post(URL,
        data={"api_user": API_USER,
              "api_key": API_KEY,
              "from": sender["emails"],
              "fromname": sender["names"],
              "to": receiversList["emails"],
              "toname": receiversList["names"],
              "subject": message.subject,
              "text": message.messageText})

        if (result.status_code == requests.codes.ok):
            messageSent = True

        sendResult.statusCode = result.status_code
        sendResult.messageSent = messageSent
        sendResult.errorMessage = ''

        if (sendResult.statusCode != requests.codes.ok):
            sendResult.errorMessage = serviceIdentifier + result.json()["errors"]
    except:
        sendResult.statusCode = 500
        sendResult.messageSent = False
        sendResult.errorMessage = serviceIdentifier + sys.exc_info()[0]

    return sendResult
#------------------------------- End of send_Message_SendGrid Method --------------


#------------------------------- Start of Send_Message Method ---------------------
# Add Message to the Queue
def send_Message ( message):
    ### Constants
    Total_Services_Number = 2
    ### Variables
    sendResult = SendResponse()
    sendResult.messageSent = False

    startServiceNumber = random.randrange(0, Total_Services_Number)
    counter = 0

    while ((counter < Total_Services_Number) and (sendResult.messageSent == False)):
        choice = (startServiceNumber + counter ) % Total_Services_Number
        if (choice == 0):
            sendResult = send_Message_MailGun (message)
        else:
            sendResult = send_Message_SendGrid (message)
            
        counter += 1

    return sendResult
#------------------------------- End of Send_Message Method -----------------------


# Define Service Function
@route('/email/send',method='POST')
def SendMessageService():
    sender  = req.forms.get('from')
    receiver = req.forms.getlist('to') # to handle the case of receivers are sent as a list
    subject  = req.forms.get('subject')
    messageText = req.forms.get('messageText')

    message = Message (sender, receiver, subject, messageText)

    sendResult = send_Message(message)

    response.status = sendResult.statusCode
    response.body = sendResult.errorMessage
    return response

# Define Error Page
@error(404)
def error404(error):
    return 'Error Page!, Nothing here, sorry'

# Run Server
application = default_app()

