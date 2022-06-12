"""
This code is for training purpose only, it cannot be used on unauthorized webpages.
The main trick for scraping a webpage with lots of Java code lies here:
innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
"""
import time
import datetime
import yagmail
import smtplib  
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def find_alert_date(src_str):
    
    search_word1='<time>'
    sub_index = src_str.find(search_word1)
    src_str=src_str[sub_index+len(search_word1):]
    search_word2='</time>'
    sub_index = src_str.find(search_word2)
    date=src_str[:-len(src_str) + sub_index]
    
    return date

def alert_extraction1(src_str):
    
    search_word1='filters'
    sub_index = src_str.find(search_word1)
    src_str=src_str[sub_index+len(search_word1):]
    
    search_word4='Previous'
    sub_index = src_str.find(search_word4)
    src_str=src_str[:-len(src_str)+sub_index]
    
    src_str=src_str.replace("View all notifications                         Informational Message  Normal  Systems Affected  Critical Issue          Close",'')
    src_str=src_str.replace('\n', ' ')
    src_str=src_str[:-1]
    src_str=src_str.replace('   ', ' ')
    
    return src_str[:-1]

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    return message.as_string()

link_consolidated_tape_association = 'https://www.ctaplan.com/'
print(link_consolidated_tape_association)
link_alerts = "https://www.ctaplan.com/alerts#110000144324"
print(link_alerts)
client_email = 'artem_ponomarev@yahoo.com' # subsitute this with your client's email
#client_email = 'shalunov@shlang.com' # use this email is to send messages to Stas
print(client_email)
message_old=""
browser = webdriver.Firefox()

i=0
while True:

    message_old="" # comment this line to start monitoring new alerts only
# is the line is on, then the daemon sends the latest alert every min.

    while True:

        browser.get(link_alerts) #navigate to the page
        innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
        f = open('CTA_full.html', 'w')
        f.write(str(innerHTML))
        f.close
        date=find_alert_date(innerHTML)
        print(date)
        if date != '':
            break
        
    page = html.document_fromstring(innerHTML.replace('>','> ')) #parse innerHTML
    fset = page.get_element_by_id("business-unit-history")
    fset_text = fset.text_content()
    alert=alert_extraction1(fset_text)
    email="Alert Date: " + date +"\n" + alert + "\n\nBanzai!"
    message=create_message("artemponomarevjetski@gmail.com", client_email, "News alert #"+str(i), email)
    print("Emailed to client:\n" + message)
    if message != message_old:
        yagmail.SMTP('artemponomarevjetski@gmail.com').send(client_email, "News alert #"+str(i), message)
    message_old = message
    
    i+=1
    print(i, datetime.datetime.now())
    time.sleep(60) # delay the next scrape by a reasonable time
