import requests
from bs4 import BeautifulSoup,Tag
import datetime
import json

def getTodaysIncidents(filter=None):
  data = requests.get("http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des")

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
  data = requests.get("https://www2.seattle.gov/fire/IncidentSearch/incidentDetail.asp?ID="+ID)
  #https://www2.seattle.gov/fire/IncidentSearch/incidentDetail.asp?ID=F220064835
  soup = BeautifulSoup(data.content, "html.parser")

  table = soup.findChildren('table')[3]

  rows = table.findChildren(['th','tr'])
  incidents = []
  data = []
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
