import requests
from bs4 import BeautifulSoup,Tag
import datetime

data = requests.get("http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des")

soup = BeautifulSoup(data.content, "html.parser")

table = soup.findChildren('table')[0]

rows = table.findChildren(['th','tr'])
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
    date = datetime.datetime.strptime(topass,r"%m/%d/%Y %I:%M:%S %p")
    incidentID = data[1]
    priority = data[2]
    apparatus = data[3]
    address = data[4]
    incidentType = data[5]
    if corresponding[0]['class'] == ['active']:
      incidentActivity = True
    else:
      incidentActivity = False
    
    
