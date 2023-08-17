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
            results.append(growth)
            print(growth)
        #12 weeks
        #week = indice 12/0
        elif diff == 7 and i-12 >= 0:
            growth = (((datas[i][1]/datas[i-12][1])**(12/3))-1)*100
            results.append(growth)
            #print(growth)
        #3 mois
        #month = indice 3/0
        elif diff == 30 and i-3 >= 0:
            growth = (((datas[i][1] /datas[i-3][1])**(12/3))-1)*100
            results.append(growth)
            #print(growth)
        # 1 regroupement de 3 mois
        #3 month = indice 1/0   
        elif diff > 30 and i-1 >= 0:
            #print(datas[i])
            #print(datas[i-1])
            growth = (((datas[i][1]/datas[i-1][1])**(12/3))-1)*100
            results.append(growth)
            #print(growth)
        else:
            results.append(None)
        
    return results

def computetwelvemonth(datas, diff):

    results = []

    for i in range(len(datas)):

        #day = indice 261/0
        if diff.days == 1 and i-261 >= 0:
            idIndex = 0
            growth = (((datas[i]/datas[i-261])**(12/12))-1)*100
            results.append(growth)
            #print(growth)

        #week = indice 52/0
        elif diff.days <= 7 and diff.days >=5 and i-52 >= 0:
            idIndex = 1
            growth = (((datas[i]/datas[i-52])**(12/12))-1)*100
            results.append(growth)
            #print(growth)

        #month = indice 12/0
        elif diff.days > 28 and diff.days < 32 and i-12 >= 0:
            idIndex = 2
            growth = (((datas[i] /datas[i-12])**(12/12))-1)*100
            results.append(growth)
            #print(growth)

        #3 month = indice 4/0
        elif diff.days >= 32 and i-4 >= 0:
            idIndex = 3
            growth = (((datas[i] /datas[i-4])**(12/12))-1)*100
            results.append(growth)
            #print(growth)
    
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
        if scraper[2] == 0:
            nbrScrapperOk+=1
        elif scraper[2] == 2:
            print("Something went wrong to the scrapper: code 2")
            exit()
    if nbrScrapperOk == len(scrapers):
        isScraperNormal = True
    nbrScrapperOk = 0 """

list_links = db.fetch_links("inter","30")
#print(diff)
for link in list_links:
    datas = db.fetch_table(link[4],"", "")
    results = computethreemonth(datas, link[3])
    print(results)