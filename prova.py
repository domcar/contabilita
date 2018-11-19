
spese = 0
with open("estrattoConto.csv") as f: 
   for line in f.readlines():
     #print("Line {}: {}".format(cnt, line.strip()))
     data1 = line.split(";")[0]
     try:
       mese = data1.split(".")[1]
       anno = data1.split(".")[2]
     except:
       continue
     data2 = line.split(";")[1]
     richiedente = line.split(";")[2]
     testo = line.split(";")[3]
     causale = line.split(";")[4]
     valuta = line.split(";")[6]
     if "REWE" in richiedente.upper():
       importo = line.split(";")[5]
       importo = float(importo.replace(",","."))
       spese = spese + importo
       print importo
print spese

