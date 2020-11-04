import requests
import pandas as pd
headers={"USER_AGENT":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36",
         "origin":"https://www.premierleague.com"}
equipos_totales=[]
for i in range(0,2):
    url_api='http://footballapi.pulselive.com/football/fixtures?comps=1&compSeasons=42&teams=1,2,127,4,6,7,26,10,11,12,23,14,20,42,29,45,21,33,36,25&pageSize=40&sort=desc&statuses=C&altIds=true&page='+ str(i)
    response=requests.get(url_api,headers=headers)
    data=response.json()
    partidos=data["content"]
    for partido in partidos:
        equipos_totales.append(
            {
                "score": partido["teams"][0]["score"],
                "name": partido["teams"][0]["team"]["name"]
            })
        equipos_totales.append(
            {
                "score": partido["teams"][1]["score"],
                "name": partido["teams"][1]["team"]["name"]
            })
df=pd.DataFrame(equipos_totales)
print(df)
df.to_csv("scores.csv")