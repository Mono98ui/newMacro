from database import database
import re
import numpy as np
import pandas as pd
from email import encoders
import ssl
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from private import Private

nbrHawkish = 0;
nbrDovish = 0
#
#Param:
#t_name: table name
#desc:description of the table
#isOsc: is it an oscillator
#datas: growth rate of the table
#results: tuple of table
#This function organize the datas into their modules
#return: results
#
def organizeDataPerModule(t_name, desc, isOsc ,datas, results, sourceData):
    money_credit = "^T_(M1SL|M2SL|BOGZ1FL893169105Q|BUSLOANS|TOTALSL)".lower()
    econo = ("^T_(INDPRO|NOCDFSA066MSFRBPHI|PCE|PAYEMS|AWHMAN|USALOLITONOSTSAM|HOUST|PERMIT"
+"|IC4WSA|GACDFSA066MSFRBPHI|HTRUCKSSA|BOGZ1FL145020011Q"
+"|us_leading_index_1968|building_permits_25|chicago_pmi_38|total_vehicle_sales_85"
+"|ism_manufacturing_pmi_173|durable_goods_orders_86|retail_sales_256)").lower()
    inflation = "^T_(CPIAUCSL|PPIACO|AHETPI)".lower()
    fed_pol= "^T_(NFORBRES|BOGNONBR|REQRESNS|T10YFF|DTB3|FEDFUNDS|INTDSRUSM193N)".lower()

    moneyCreditGrowth= "MoneyCreditGrowth"
    economicGrowth="EconomicGrowth"
    inflationTxt = "Inflation"
    fedPolicy= "Fed Policy"
    nameIndicator = t_name.replace("t_","")

    listTmp = list(datas[0])
    listTmp[len(listTmp)-1] = datas[0][len(datas[0])-1].strftime("%Y-%m-%d")

    if listTmp[len(listTmp)-3]:
        global nbrHawkish
        nbrHawkish+=1
    else:
        global nbrDovish
        nbrDovish+=1

    datas[0] = tuple(listTmp)

    if re.search(money_credit,t_name):
        datas[0] = (moneyCreditGrowth,nameIndicator, desc, sourceData)+datas[0]
        results[0].append(datas[0])

    elif re.search(econo,t_name):
        print(t_name)
        print(datas)
        datas[0] = (economicGrowth,nameIndicator, desc, sourceData)+datas[0]
        results[1].append(datas[0])

    elif re.search(inflation,t_name):
        datas[0] = (inflationTxt,nameIndicator, desc, sourceData)+datas[0]
        results[2].append(datas[0])

    elif re.search(fed_pol,t_name):
        datas[0] = (fedPolicy,nameIndicator, desc, sourceData)+datas[0]
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
    pwd = os.getenv('MAIL_BOT_PWD')

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

pr = Private()


db = database(os.getenv('DB_NAME'),os.getenv('DB_USER'),os.getenv('DB_PASSWORD'))
list_links = db.fetch_links("length(show_more)",">","2")
indicators = db.fetch_indicators()
results=([], [], [], [])
#Organise the growth rate for investing
for link in list_links:
    datas = db.fetch_table_show_gr(link[4]+"_gr","t1"
+" inner join " +link[4]+"_gr"+ " t2"
+" on t1.date = t2.date and t2.intervalmonth = 12"
+" join (select tb.t_name , tb.is_oscillator from"
+" (select tl.t_name, tl.is_oscillator from t_links_inv tl"
+" union"
+" select ti.t_name, ti.is_oscillator from t_indicators_fred ti) tb) tb"
+" on tb.t_name = '"+link[4]+"'"
+" where t1.value is not NULL and t1.intervalmonth = 3 and  t2.value is not NULL"
+" order by t1.date desc"
+" limit 1")
    results = organizeDataPerModule(link[4].lower(),link[5], link[6] ,datas, results, "investing")

#Organise the growth rate for fred
for indicator in indicators:
    datas = db.fetch_table_show_gr(indicator[3].lower()+"_gr","t1"
+" inner join " +indicator[3].lower()+"_gr"+ " t2"
+" on t1.date = t2.date and t2.intervalmonth = 12"
+" join (select tb.t_name , tb.is_oscillator from"
+" (select tl.t_name, tl.is_oscillator from t_links_inv tl"
+" union"
+" select ti.t_name, ti.is_oscillator from t_indicators_fred ti) tb) tb"
+" on tb.t_name = '"+indicator[3]+"'"
+" where t1.value is not NULL and t1.intervalmonth = 3 and  t2.value is not NULL"
+" order by t1.date desc"
+" limit 1")
    results = organizeDataPerModule(indicator[3].lower(), indicator[1], indicator[4], datas, results, "fred")

mainDf = []
sum_CBStance = []
padding_of_sum= 2

empty_string_list = [""] * padding_of_sum
empty_string_list.append("Sum of Hawkish: ")
empty_string_list.append(nbrHawkish)
sum_CBStance.append(empty_string_list)

empty_string_list = [""] * 2
empty_string_list.append("Sum of Dovish: ")
empty_string_list.append(nbrDovish)
sum_CBStance.append(empty_string_list)

padding_column = len(sum_CBStance) * padding_of_sum
index_CBStance = 0
columnNames= ['Module','Indicator','Description',"Source of Data",'3 Month Ann.','12 Month/ 1 Year Growth', 'Has crossover/is Positive', 'CB Stance', 'Date']+[""] * padding_column

#Concatenate the data into one dataframe
for result in results:
    for i in range(len(result)):
        temp_res = list(result[i])
        if(index_CBStance < len(sum_CBStance)):
            temp_res+= sum_CBStance[index_CBStance]
            result[i] = tuple(temp_res)
            index_CBStance+=1
        else:
            temp_res+= [""] * padding_column
            result[i] = tuple(temp_res)

        #print("fini")

    print(result)
    my_array = np.array(result)
    exit
    df = pd.DataFrame(my_array, columns = columnNames,)
    mainDf.append(df)

#Documenter metter data vertical
#empty_string_list = [""] * (len(columnNames)-2)
#empty_string_list.append("Sum of Hawkish: ")
#empty_string_list.append(nbrHawkish)
#dfsumHawk=np.array(empty_string_list)
#tableau 2d avec une rangee
#reshape_df= dfsumHawk.reshape(1,9)
#df = pd.DataFrame(reshape_df, columns = columnNames)
#mainDf.append(df)

#empty_string_list = [""] * (len(columnNames)-2)
#empty_string_list.append("Sum of Dovish: ")
#empty_string_list.append(nbrDovish)
#dfsumDov=np.array(empty_string_list)
#reshape_df= dfsumDov.reshape(1,9)
#df = pd.DataFrame(reshape_df, columns = columnNames)
#mainDf.append(df)

#Create the csv
if os.path.isfile("./reportGrowthrate.csv"):
    os.remove("./reportGrowthrate.csv")
currentPath = os.getcwd()
pd.concat(mainDf, ignore_index=True).to_csv(currentPath+"\\reportGrowthrate.csv", index=False)

sendEmail(os.getenv('MAIL_BOT'),os.getenv('MAIL_BOT_DEST'),"reportGrowthrate.csv")

db.update_status("process_investing", 0)
db.update_status("process_fred", 0)
pr.clean()