import fastapi
import string
import random
import secrets
import module as SFDModule
import json
letters = string.ascii_lowercase
def randomString(length):
  return ''.join(random.choice(letters) for i in range(length))
def generateAPIKey():
  key = secrets.token_urlsafe(30)
  api_keys[key] = {"key":key,"uses":0}
  return key


def checkAuthenticity(key):
  if key in api_keys.keys():
    return True
  else:
    return False

app = fastapi.FastAPI()

api_keys = {"BACKENDKEY":{"key":"BACKENDKEY","uses":0}}

@app.get('/getAPIKey')
async def getKey():
  return {"api_key":generateAPIKey(),"acknoledgements":"This API Key cannot be recovered as it is not stored in plain text."}

@app.get("/")
async def test(key):
  return {"Token":key,"Authorized":key in api_keys.keys()}

@app.get('/fire/getLatestIncidents')
async def latestIncidents(key,count:int,filter=None):
  if checkAuthenticity(key):
    if filter == None:
      return {"incidents":SFDModule.getTodaysIncidents()[:count],"acknoledgements":"This use has been charged to your account as a **regular** use. Filter None."}
    else:
      if filter in ['active','inactive']:
        return {"incidents":SFDModule.getTodaysIncidents(filter)[:count],"acknoledgements":"This use has been charged to your account as a **regular** use. Filter in Use."}
      else:
        return {"error":"Invalid filter","acknoledgements":"This use has not been charged to your account."}
  else:
    return {"incidents":[],"error":"Invalid API Key"}

@app.get('/fire/getIncidentInformation')
async def getIncidentInformation(key,id):
  if checkAuthenticity(key):
    print(SFDModule.getIncidentInformation(id))
    return {"incident":SFDModule.getIncidentInformation(id),"acknoledgements":"This use has been charged to your account as a **regular** use."}
  else:
    return {"incident":{},"error":"Invalid API Key"}