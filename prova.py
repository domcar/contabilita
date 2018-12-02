import json
from dateutil.parser import parse

# categorie e sottocategorie
categorie = {
  "abbigliamento" : ["h+m","woolworth","crocs","geox","baby walz","c+a","Ernsting","stoffe","schuhcenter","totale"],
  "acasa"         : ["segmueller","galeria","bauhaus","toom","hornbach",
                     "fliesen","kibek","ikea","xxxl","obi","karstadt","staples",
                     "weku","bm offenbach","tende","gries","idee.creativ","moemax","totale","BDSK HANDELS"],
  "appartamento"  : ["energieversorgung","evo","thomas reinecke","energievers","XENOS",
                     "friedrich sommer","tilgung","zinsen","miete","taeglich",
                     "giornaliero","baufinanzierung","weg","lanio","fbw","totale"],
  "assicurazioni" : ["arag","huk","axa","totale","kfz versicherung","techniker krank"],
  "bici"          : ["b.o.c","montimare","fahrrad","totale"],
  "entrate"       : ["entrate","totale"],
  "farmaci"       : ["apotheke","farmacia","totale"],
  "internet"      : ["unitymedia","totale"],
  "macchina"      : ["driver center","akf bank","esso","aral","park","parking",
                     "calpam","shell","fraport","totale"],
  "nina"          : ["tagtraume","TAGTRAEUME","familien kasse","toys","nanu","primigi","piccoli","totale"],
  "nocat"         : ["totale"],
  "prelievo"      : ["ING-DiBa-AG","totale"],
  "spesa"         : ["rewe", "dm","tegut","scheck in","rossmann","meta","giovo",
                     "penny","supermercato","kafein","basic","europa commerciale","hema","totale"],
  "tasse"         : ["hcc","vanessa","gerichtskasse","totale"],
  "trasporto"     : ["vgf","verkehrs","db vertrieb","totale"],
  "uscite"        : ["HESSEWIRTSCHAFT","LEONHARDS","GASTRONOMIE","TIGER","restaurant",
                     "pizzeria","jamys","WILLYS BAR","vapiano","biomarkt","coffee",
                     "azurro","belge","dolce vita","speckwirt","aplofoods","TURM-BRAEU","totale","gastronom"],
  "fuori-casa"    : ["opel zoo","senckenberg","totale"],
  "vacanze"       : ["hotel","totale"],
  "varie"         : ["ofc fanshop","gulliver","relay","totale"]
}

def assign_to_cat (richiedente):

  for cat in categorie.keys():
    for subcat in categorie[cat]:
      if subcat.upper() in richiedente.upper():
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

def check_richiedente(line,richiedente,importo):
  if importo > 0:
    return "entrate"

  non_buono = ["Lastschrift aus","Caruso","Belyaeva","First Data"]
  causali_note = ["tilgung","zinsen","miete","taeglich","giornaliero","baufinanzierung"]
  for each in non_buono:
    if each.upper() in richiedente.upper():
      causale = line.split(";")[4]
      for noto in causali_note:
        if noto.upper() in causale.upper():
          return noto.upper()
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
          dizionario[mesanno][cat]["totale"] = 0

      data2 = line.split(";")[1]
      try:
        importo = line.split(";")[5]
        importo = importo.replace(".","")
        importo = float(importo.replace(",","."))
      except Exception as e:
        print "importo errato, ignorato"
        print e
        continue


      richiedente = line.split(";")[2].upper()
      richiedente = check_richiedente(line,richiedente,importo)
      categoria = assign_to_cat(richiedente)
      modalita = line.split(";")[3]
      try:
        causale = line.split(";")[4]
      except:
        print "causale sbagliata"
        print line
      valuta = line.split(";")[6]
      if not richiedente in dizionario[mesanno][categoria]:
        dizionario[mesanno][categoria][richiedente] = importo
      else:
        dizionario[mesanno][categoria][richiedente] += importo
      dizionario[mesanno][categoria]["totale"] += importo
    else:
      continue

#print json.dumps(dizionario,sort_keys=True, indent=4)

ris_tot = open("risultato_totale.csv","w")
ris_sot = open("risultato_sottocategoria.csv","w")
for data in sorted(dizionario.keys()):
  for cat in dizionario[data].keys():
    for subcat in dizionario[data][cat].keys():
      if subcat == "totale": 
        if not dizionario[data][cat][subcat] == 0:
          ris_tot.write(data+";"+cat+";"+str(abs(dizionario[data][cat][subcat]))+"\n")
      else:
        ris_sot.write(data+";"+cat+";"+subcat+";"+str(dizionario[data][cat][subcat])+"\n")
