import requests
from bs4 import BeautifulSoup,Tag
import datetime
import json

def getTodaysIncidents(filter=None):
  try:
    data = requests.get("http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des")
  except:
    return
  soup = BeautifulSoup(data.content, "html.parser")

  table = soup.findChildren('table')[0]

  rows = table.findChildren(['th','tr'])
  incidents = []
  for row in rows:
    cells = row.findChildren('td')
    data = []
    corresponding = []
    for cell in cells:
      data.append(cell.string)
      corresponding.append(cell)
    if data[0] == None or data[0] == "Date/Time":
      pass
    else:
      topass = data[0].replace("/0", "/").replace(" 0"," ").replace(":0",":")
      incidentActivity=None
      if topass.startswith("0"):
        topass=topass[1:]
      date = data[0]
      #date = datetime.datetime.strptime(topass,r"%m/%d/%Y %I:%M:%S %p")
      incidentID = data[1]
      priority = data[2]
      apparatus = data[3].split(" ")
      address = data[4]
      incidentType = data[5]
      if corresponding[0]['class'] == ['active']:
        incidentActivity = True
        
      else:
        incidentActivity = False
      if filter=="active":
        if incidentActivity == True:
          incidents.append({"incidentDate":date,"incidentID":incidentID,"incidentPriority":priority,"incidentApparatus":apparatus,"incidentAddress":address,"incidentType":incidentType,"incidentActivity":incidentActivity,"message":"For more specific information about the statuses of different apparatus, utilizwe the \"getLatestIncidents\" endpoint."})
        else:pass
      elif filter=="inactive":
        if not incidentActivity:
          incidents.append({"incidentDate":date,"incidentID":incidentID,"incidentPriority":priority,"incidentApparatus":apparatus,"incidentAddress":address,"incidentType":incidentType,"incidentActivity":incidentActivity,"message":"For more specific information about the statuses of different apparatus, utilizwe the \"getLatestIncidents\" endpoint."})
        else:pass
      else:
        incidents.append({"incidentDate":date,"incidentID":incidentID,"incidentPriority":priority,"incidentApparatus":apparatus,"incidentAddress":address,"incidentType":incidentType,"incidentActivity":incidentActivity,"message":"For more specific information about the statuses of different apparatus, utilizwe the \"getLatestIncidents\" endpoint."})
  return incidents




def getIncidentInformation(ID):
  apparatuses = {}
  try:
    data = requests.get("https://www2.seattle.gov/fire/IncidentSearch/incidentDetail.asp?ID="+ID)
  except:
    return
  #https://www2.seattle.gov/fire/IncidentSearch/incidentDetail.asp?ID=F220064835
  soup = BeautifulSoup(data.content, "html.parser")
  try:
    table = soup.findChildren('table')[3]

    rows = table.findChildren(['th','tr'])
    incidents = []
    data = []
  except:
    return ""
  for row in rows[1:]:
    cells = row.findChildren('td')

    for cell in cells:
      data.append(cell.getText().strip())

  for x in range(1,int(len(data)/4)+1):
    itr = data[x*4-4:x*4]
    apparatus = itr[0]
    dispatchTime = itr[1]
    arrivalTime = "NOT ON SCENE" if itr[2] == "" else itr[2]
    clearTime = "NOT CLEARED" if itr[3] == "" else itr[3]
    status = ""
    if arrivalTime == "NOT ON SCENE" and clearTime == "NOT CLEARED":
      status = "ENROUTE"
    elif arrivalTime == "NOT ON SCENE" and clearTime != "NOT CLEARED":
      status = "DIVERTED AT "+dispatchTime
    elif arrivalTime != "NOT ON SCENE" and clearTime == "NOT CLEARED":
      status = "ON SCENE"
    elif clearTime != "NOT CLEARED":
      status = "CLEARED AT "+str(clearTime)
    primaryStatus = True if apparatus.endswith("*") else False
    if primaryStatus == True:
      apparatus = apparatus.replace("*","")
    else:pass
    apparatuses[apparatus] = {"dispatchTime":dispatchTime,"arrivalTime":arrivalTime,"clearTime":clearTime,"status":status,"primaryStatus":primaryStatus}
  table = soup.findChildren('table')
  for tb in table:
    if tb.attrs.get("width",None)=="538":
      data = []
      for row in tb.findChildren(['tr','th']):
        for cell in row.findChildren(['td']):
          data.append(cell.getText().strip())

  incidentID = data[1]
  incidentDate = data[3]
  incidentTime = data[5]
  incidentAddress = data[7]
  incidentType = data[9]
  incidentAlarms = int(data[11])

  return {"apparatusStatuses":apparatuses,"incidentID":incidentID,"incidentDate":incidentDate,"incidentTime":incidentTime,"incidentAddress":incidentAddress,"incidentType":incidentType,"incidentAlarms":incidentAlarms}


def getLatestIncidentID():
  return getTodaysIncidents()[0]["incidentID"]


def replaceApprv(txt):
  if txt.startswith("E"):
    return txt.replace("E","Engine ")
  elif txt.startswith("L"):
    return txt.replace("L","Ladder ")
  elif txt.startswith("A"):
    return txt.replace("A","Aid ")
  elif txt.startswith("M"):
    return txt.replace("M","Medic ")
  elif txt.startswith("B"):
    return txt.replace("B","Battallion Chief ")
  elif txt.startswith("DEP1"):
    return txt.replace("DEP1","Deputy Chief ")
  elif txt.startswith("SAFT2"):
    return txt.replace("SAFT2","Safety Chief ")
  elif txt.startswith("M44"):
    return txt.replace("M44","EMS Supervisor 44")
  elif txt.startswith("M45"):
    return txt.replace("M45","EMS Supervisor 45")
  elif txt.startswith("STAF10"):
    return txt.replace("STAF10","ICS Support Unit 10")
  elif txt.startswith("MAR5"):
    return txt.replace("MAR5","Fire Investigation Unit 5")
  elif txt.startswith("FB"):
    return txt.replace("FB","Fireboat ")
  elif txt.startswith("RB5"):
    return txt.replace("RB5","Rescue Boat 5")
  elif txt.startswith("MRN1"):
    return txt.replace("MRN1","Marine Rescue Unit 1")
  elif txt.startswith("R1"):
    return txt.replace("R1","Technical Rescue Unit 1")
  elif txt.startswith("HAZ1"):
    return txt.replace("HAZ1","Hazmat Unit 1")
  elif txt.startswith("H"):
    return txt.replace("H","Mobile Health ")
  elif txt.startswith("MIH"):
    return txt.replace("MIH","Mobile Health Unit ")
  elif txt.startswith("AIR"):
    return txt.replace("AIR","Air & Light ")
  elif txt.startswith("HOSE"):
    return txt.replace("HOSE","Hose Wagon ")
  elif txt.startswith("P25"):
    return txt.replace("P25","Power Truck 25")
  elif txt.startswith("VAULT1"):
    return txt.replace("VAULT1","Vault Response Team 1")
  elif txt.startswith("DECON1"):
    return txt.replace("DECON1","Decontamination Unit 1")
  elif txt.startswith("REHAB1"):
    return txt.replace("REHAB1","Rehabilitation Unit 1")
  elif txt.startswith("MCI1"):
    return txt.replace("MCI1","Mass Casualty Unit 1")
  elif txt.startswith("MVU1"):
    return txt.replace("MVU1","Mobile Ventilation Unit 1")
  elif txt.startswith("SQ"):
    return txt.replace("SQ","Squad ")
  elif txt.startswith("COMVAN"):
    return txt.replace("COMVAN","Communications Van ")
  elif txt.startswith("CHAP"):
    return txt.replace("CHAP","Chaplain ")
  elif txt.startswith("PIO"):
    return txt.replace("PIO","Public Information Officer ")

