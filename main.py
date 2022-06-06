import requests
from bs4 import BeautifulSoup,Tag
import datetime



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

print(getIncidentInformation("F220064855"))