import json

categorie = {
  "appartamento" : ["energieversorgung","evo","thomas reinecke","energievers","XENOS","friedrich sommer"],
  "internet" : ["unitymedia"],
  "spesa" : ["rewe", "dm","tegut","scheck in","rossmann","meta","giovo","penny"],
  "acasa" : ["segmueller","galeria","bauhaus","toom","hornbach","fliesen","kibek","ikea","xxxl","obi","karstadt","staples"],
  "assicurazioni" : ["arag","huk","axa"],
  "macchina" : ["driver center","akf bank","esso","aral","park","parking","calpam","shell","fraport"],
  "tasse" : ["hcc"],
  "nina" : ["tagtraume","familien kasse","toys"],
  "vacanze" : ["hotel"],
  "farmaci" : ["apotheke"],
  "trasporto" : ["vgf","verkehrs","db vertrieb"],
  "uscite" : ["HESSEWIRTSCHAFT","LEONHARDS","GASTRONOMIE","TIGER","restaurant","pizzeria","jamys","WILLYS BAR","vapiano","biomarkt","coffee"],
  "bici" : ["b.o.c"],
  "varie" : [],
  "nocat" : [],
  "abbigliamento" : ["h+m","woolworth","crocs","geox","baby walz","c+a"]
}

def assign_to_cat (richiedente):

  for cat in categorie.keys():
    for subcat in categorie[cat]:
      if subcat.upper() in richiedente:
        return cat
  return "nocat"

dizionario = {}

spese = 0
with open("estrattoConto.csv") as f: 
  for line in f.readlines():
    data1 = line.split(";")[0]
    try:
      mese = data1.split(".")[1]
      anno = data1.split(".")[2]
      mesanno = anno+"-"+mese
    except Exception as e:
      print ("warning", e)
      continue
    if mesanno not in dizionario.keys():
      dizionario[mesanno] = {}
      for cat in categorie.keys():
        dizionario[mesanno][cat] = {}


    data2 = line.split(";")[1]
    # TODO: chechk if richiedente is undefined
    richiedente = line.split(";")[2].upper()
    categoria = assign_to_cat(richiedente)
    testo = line.split(";")[3]
    causale = line.split(";")[4]
    valuta = line.split(";")[6]
    try:
      importo = line.split(";")[5]
      importo = float(importo.replace(",","."))
    except:
      continue
    if not richiedente in dizionario[mesanno][categoria]:
      dizionario[mesanno][categoria][richiedente] = importo
    else:
      dizionario[mesanno][categoria][richiedente] += importo

print json.dumps(dizionario,sort_keys=True, indent=4)

