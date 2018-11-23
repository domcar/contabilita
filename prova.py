import json
from dateutil.parser import parse

categorie = {
  "appartamento" : ["energieversorgung","evo","thomas reinecke","energievers","XENOS","friedrich sommer","tilgung","zinsen"],
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
  "uscite" : ["HESSEWIRTSCHAFT","LEONHARDS","GASTRONOMIE","TIGER","restaurant","pizzeria","jamys","WILLYS BAR","vapiano","biomarkt","coffee","azurro","belge"],
  "uscite_istruttive" : ["opel zoo","senckenberg"],
  "prelievo" : ["ING-DiBa-AG"],
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

def clean_up (line):
 try:
   parse(line.split(";")[0])
 except Exception:
   print ("data sbagliata, riga ignorata")
   print line
   return False
   

 return True

def check_richiedente(line,richiedente):
  non_buono = ["Lastschrift aus","Caruso"]
  causali_note = ["tilgung","zinsen"]
  for each in non_buono:
    if each.upper() in richiedente:
      causale = line.split(";")[4]
      for one in causali_note:
        if one in causale:
          return one.upper()
      return causale.split("//")[0].upper()
  return richiedente

dizionario = {}

with open("estrattoConto.csv") as f: 
  for line in f.readlines():
    is_clean = clean_up(line)
    if is_clean:
      data1 = line.split(";")[0]
      mese = data1.split(".")[1]
      anno = data1.split(".")[2]
      mesanno = anno+"-"+mese
      if mesanno not in dizionario.keys():
        dizionario[mesanno] = {}
        for cat in categorie.keys():
          dizionario[mesanno][cat] = {}

      data2 = line.split(";")[1]


      # TODO: chechk if richiedente is undefined
      richiedente = line.split(";")[2].upper()
      richiedente = check_richiedente(line,richiedente)
      categoria = assign_to_cat(richiedente)
      modalita = line.split(";")[3]
      try:
        causale = line.split(";")[4]
      except:
        print line
      valuta = line.split(";")[6]
      try:
        importo = line.split(";")[5]
        importo = importo.replace(".","")
        importo = float(importo.replace(",","."))
      except Exception as e:
        print line
        print e
        continue
      if "ING" in richiedente:
        print categoria,importo
      if not richiedente in dizionario[mesanno][categoria]:
        dizionario[mesanno][categoria][richiedente] = importo
      else:
        dizionario[mesanno][categoria][richiedente] += importo
    else:
      continue

print json.dumps(dizionario,sort_keys=True, indent=4)

