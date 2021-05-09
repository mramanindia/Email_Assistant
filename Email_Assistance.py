import numpy as np
import pandas as pd 
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

data=pd.read_csv("Data.csv")


#At the place of name put the name of what you have in the csv file like your name or Name or First name and 
#same with the mail, what is the name of that column you have putten

name_list = data["name"].tolist() 
mail_list = data["mail"].tolist() 

for name, mail in zip(name_list, mail_list):
    im = Image.open('cer.png') #over here put what is the name of your certificate template like cer.png
    #make sure the csv file and certificate is in same folder
    
    d = ImageDraw.Draw(im)
    location = (170, 900)
    text_color = (0, 137, 209)
    font = ImageFont.truetype("arial.ttf", 120)
    d.text(location, name, fill = text_color, font = font)
    im.save( name + ".png")


    fromaddr = "xyz@gmail.com"  #put you mail here.
    password="blabla" #put your password here
    toaddr = mail   #it waill take name from csv file

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "The certificates left"

    # string to store the body of the mail
    body = '''Here is your certificate attach with this mail!
     Well, I apolozise for the delay : )'''

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # open the file to be sent
    filename = name+".png"
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)  

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    print("sent")
    
