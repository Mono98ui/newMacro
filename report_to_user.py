from database import database
import re
import numpy as np
import pandas as pd
from email.message import EmailMessage
from email import encoders
import ssl
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

#
#Param:
#t_name: table name
#desc:description of the table
#datas: growth rate of the table
#results: tuple of table
#This function organize the datas into their modules
#return: results
#
def organizeDataPerModule(t_name, desc ,datas, results):
    money_credit = "^T_(M1SL|M2SL|BOGZ1FL893169105Q|BUSLOANS|TOTALSL)".lower()
    econo = ("^T_(INDPRO|NOCDFSA066MSFRBPHI|PCE|PAYEMS|AWHMAN|USALOLITONOSTSAM|HOUST|PERMIT|RETAIL"
+"|IC4WSA|GACDFSA066MSFRBPHI|HTRUCKSSA|TCU|BOGZ1FL145020011Q)"
+"|us_leading_index_1968|building_permits_25|chicago_pmi_38|total_vehicle_sales_85").lower()
    inflation = "^T_(CPIAUCSL|PPIACO|AHETPI)".lower()
    fed_pol= "^T_(NFORBRES|BOGNONBR|REQRESNS|T10YFF|DTB3|FEDFUNDS|INTDSRUSM193N)".lower()

    moneyCreditGrowth= "MoneyCreditGrowth"
    economicGrowth="EconomicGrowth"
    inflationTxt = "Inflation"
    fedPolicy= "Fed Policy"
    nameIndicator = t_name.replace("t_","")

    if re.search(money_credit,t_name):
        datas[0] = (moneyCreditGrowth,nameIndicator, desc)+datas[0]
        results[0].append(datas[0])

    elif re.search(econo,t_name,):
        datas[0] = (economicGrowth,nameIndicator, desc)+datas[0]
        results[1].append(datas[0])

    elif re.search(inflation,t_name):
        datas[0] = (inflationTxt,nameIndicator, desc)+datas[0]
        results[2].append(datas[0])

    elif re.search(fed_pol,t_name):
        datas[0] = (fedPolicy,nameIndicator, desc)+datas[0]
        results[3].append(datas[0])
    else:
         print("Not Catagorize: "+t_name)

    return results
#
#Param:
#email_sender: emails of the bot email
#email_receiver: emails of the receiver
#filename: the filename of the growth rate report
#This function send the emails to the email_receiver
#return: results
#
def sendEmail(email_sender,email_receiver,filename):
    pwd = "nucgpfaiqqnhypmw"

    subject =" Growth Rate Report"

    message = """
    Good morning,\n
    This is the growth rate report.\n
    Have a nice day\n
    macroBot.
    """

    em = MIMEMultipart()

    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    em.attach(part)


    em.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, pwd)
        smtp.sendmail(email_sender,email_receiver, em.as_string())

db = database("MacroDB","Test_user","test")
list_links = db.fetch_links("length(show_more)",">","2")
indicators = db.fetch_indicators()
results=([], [], [], [])

#Organise the growth rate for investing
for link in list_links:
    datas = db.fetch_table_show_gr(link[4]+"_gr","t1"
+" inner join " +link[4]+"_gr"+ " t2"
+" on t1.date = t2.date and t2.intervalmonth = 12"
+" where t1.value is not NULL and t1.intervalmonth = 3 and  t2.value is not NULL"
+" order by t1.date desc"
+" limit 1")
    results = organizeDataPerModule(link[4].lower(),link[5] ,datas, results)

#Organise the growth rate for fred
for indicator in indicators:
    datas = db.fetch_table_show_gr(indicator[3].lower()+"_gr","t1"
+" inner join " +indicator[3].lower()+"_gr"+ " t2"
+" on t1.date = t2.date and t2.intervalmonth = 12"
+" where t1.value is not NULL and t1.intervalmonth = 3 and  t2.value is not NULL"
+" order by t1.date desc"
+" limit 1")
    results = organizeDataPerModule(indicator[3].lower(), indicator[1], datas, results)

mainDf = []
#Concatenate the data into one dataframe
for result in results:

    my_array = np.array(result)

    df = pd.DataFrame(my_array, columns = ['Module','Indicator','Description','3 Month Ann.','12 Month Ann.', 'Has crossover', 'Date'],)

    mainDf.append(df)

#Create the csv
pd.concat(mainDf, ignore_index=True).to_csv("./reportGrowthrate.csv")

sendEmail("macrobot165@gmail.com","Jdannypham@gmail.com","reportGrowthrate.csv")

db.update_status("process_investing", 0)
db.update_status("process_fred", 0)