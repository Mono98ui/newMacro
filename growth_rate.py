from database import database
import time
import os
from private import Private


#Param:
#datas: data's form indicators
#diff: interval of days of data's update
#This function compute the three month growthrate
#Return: the growth rate
#
def computethreemonth(datas, diff):

    results = []
    #diffrence entre les date pour determiner l<intervalle de date
    #print(diff)
    #Nombre de donnee
    #print(datas)
    for i in range(len(datas)):
        try:
        #day = indice 90/0
        #Pour calculer le 3 mois, pour les donnee journaliere, on calcule a partir de la prmier donn/e jusqua la 90 jours ce qui fait 3 mois
            if diff == 1 and i-90 >= 0:
                growth = (((datas[i][1]/datas[i-90][1])**(12/3))-1)*100
            #12 weeks
            #week = indice 12/0
            elif diff == 7 and i-12 >= 0:
                growth = (((datas[i][1]/datas[i-12][1])**(12/3))-1)*100
            #3 mois
            #month = indice 3/0
            elif diff == 30 and i-3 >= 0:
                growth = (((datas[i][1] /datas[i-3][1])**(12/3))-1)*100
            # 1 regroupement de 3 mois
            #3 month = indice 1/0   
            elif diff > 30 and i-1 >= 0:
                growth = (((datas[i][1]/datas[i-1][1])**(12/3))-1)*100
            else:
                growth= None
        except ZeroDivisionError:
            growth = 0
        except:
            print("Something went wrong")
        results.append({"timestamp":datas[i][0],"value":growth,"intervalMonth":3 })
        
    return results
#Param:
#datas: data's form indicators
#diff: interval of days of data's update
#This function compute the twelve month growthrate
#Return: the growth rate
#
def computetwelvemonth(datas, diff):

    results = []

    for i in range(len(datas)):
        try:
            #day = indice 261/0
            if diff == 1 and i-261 >= 0:
                growth = (((datas[i][1]/datas[i-261][1])**(12/12))-1)*100

            #week = indice 52/0
            elif diff == 7 and i-52 >= 0:
                growth = (((datas[i][1]/datas[i-52][1])**(12/12))-1)*100

            #month = indice 12/0
            elif diff == 30 and i-12 >= 0:
                growth = (((datas[i][1] /datas[i-12][1])**(12/12))-1)*100

            #3 month = indice 4/0
            elif diff > 30 and i-4 >= 0:
                growth = (((datas[i][1] /datas[i-4][1])**(12/12))-1)*100
            else:
                growth= None
        except ZeroDivisionError:
            growth = 0
        except:
            print("Something went wrong")

        results.append({"timestamp":datas[i][0],"value":growth, "intervalMonth":12})

    return results

pr = Private()


db = database(os.getenv('DB_NAME'),os.getenv('DB_USER'),os.getenv('DB_PASSWORD'))

list_links = db.fetch_links("length(show_more)",">","2")
indicators = db.fetch_indicators()
db.update_status("process_investing", 3)

#Calculate growth rate data from investing.com
for link in list_links:
    datas = db.fetch_table_Main(link[4],"","", "")
    results = computethreemonth(datas, link[3])
    db.insert_value_component_gr(link[4]+"_gr",results)
    results = computetwelvemonth(datas, link[3])
    db.insert_value_component_gr(link[4]+"_gr",results)

db.update_status("process_investing", 4)

db.update_status("process_fred", 3)

#Calculate growth rate data from Fred
for indicator in indicators:
    datas = db.fetch_table_Main(indicator[3].lower(),"","", "")
    results = computethreemonth(datas, indicator[2])
    db.insert_value_component_gr(indicator[3].lower()+"_gr",results)
    results = computetwelvemonth(datas, indicator[2])
    db.insert_value_component_gr(indicator[3].lower()+"_gr",results)

db.update_status("process_fred", 4)

pr.clean()