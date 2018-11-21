import json

dizionario = {}

spese = 0
with open("estrattoConto.csv") as f: 
   for line in f.readlines():
     data1 = line.split(";")[0]
     try:
       mese = data1.split(".")[1]
       anno = data1.split(".")[2]
       mesanno = mese+"-"+anno
     except Exception as e:
       print ("warning", e)
       continue
     if mesanno not in dizionario.keys():
       dizionario[mesanno] = {}


     data2 = line.split(";")[1]
     richiedente = line.split(";")[2].upper()
     testo = line.split(";")[3]
     causale = line.split(";")[4]
     valuta = line.split(";")[6]
     try:
       importo = line.split(";")[5]
       importo = float(importo.replace(",","."))
     except:
       continue
     if not richiedente in dizionario[mesanno].keys():
       dizionario[mesanno][richiedente] = importo
     else:
       dizionario[mesanno][richiedente] += importo

print json.dumps(dizionario,sort_keys=True, indent=4)

