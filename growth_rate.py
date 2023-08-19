from database import database
import time



def computethreemonth(datas, diff):

    results = []
    #diffrence entre les date pour determiner l<intervalle de date
    #print(diff)
    #Nombre de donnee
    #print(datas)
    for i in range(len(datas)):
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

        results.append({"timestamp":datas[i][0],"value":growth,"intervalMonth":3 })
        
    return results

def computetwelvemonth(datas, diff):

    results = []

    for i in range(len(datas)):

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

        results.append({"timestamp":datas[i][0],"value":growth, "intervalMonth":12})

    return results

def formatrule(nbr, results):
    for i in range(nbr):
        results.insert(i, None)

db = database("MacroDB","Test_user","test")

isScraperNormal= False
nbrScrapperOk = 0

#Locking mechanism
""" while(not isScraperNormal):
    time.sleep(60)
    scrapers = db.fetch_status()
    for scraper in scrapers:
        if scraper[2] == 2:
            nbrScrapperOk+=1
        elif scraper[2] == -1:
            print("Something went wrong to the scrapper: code 2")
            exit()
    if nbrScrapperOk == len(scrapers):
        isScraperNormal = True
    nbrScrapperOk = 0 """

list_links = db.fetch_links("length(show_more)",">","2")
#print(diff)
db.update_status(1, 3)
for link in list_links:
    datas = db.fetch_table(link[4],"","", "")
    results = computethreemonth(datas, link[3])
    print(results)
    db.insert_value_component_gr(link[4]+"_gr",results)
    print("==========================")
    results = computetwelvemonth(datas, link[3])
    print(results)
    db.insert_value_component_gr(link[4]+"_gr",results)

db.update_status(1, 4)