import tweepy
import module as SFDModule
import time
latestIncidentID = SFDModule.getLatestIncidentID()
client = tweepy.Client(consumer_key='pOMcjdsvzMh7HyhlACNsoVYz5',
                       consumer_secret='SA7Jfa5WAzvgfEIq2BFiznX7SQznm54CnGprxJcY0Hv08som3k',
                       access_token='1533985836743610370-Aa91oUMqLh2SQHUejSsSkri57OvycC',
                       access_token_secret='EaoAjHCo3W4VQ2bIwMkpM3nnecqn4Jo78SNzU6zARM63z')

# Replace the text with whatever you want to Tweet about

while True:
  print(SFDModule.getLatestIncidentID(),latestIncidentID)
  if SFDModule.getLatestIncidentID() == latestIncidentID:
    pass
  else:
    if int(SFDModule.getLatestIncidentID().replace("F","")) <int((latestIncidentID).replace("F","")):
      pass
    else:
      print("New incident detected.",SFDModule.getLatestIncidentID())
      #there is a new incident to post about
      latestIncidentID = SFDModule.getLatestIncidentID()
      latestIncident = SFDModule.getIncidentInformation(SFDModule.getLatestIncidentID())
      fixedDict = {}
      for apparatus in latestIncident['apparatusStatuses']:
        fixedDict[SFDModule.replaceApprv(apparatus)] = latestIncident['apparatusStatuses'][apparatus]
      dispatchedUnits = list(fixedDict.keys())
      callNature = latestIncident['incidentType'].split(" - ")[1]
      latestIncident['incidentAddress'] = latestIncident['incidentAddress'].replace("LOBBY"," LOBBY")
      latestIncident['incidentAddress'] = latestIncident['incidentAddress'].replace("FLOOR"," FLOOR")
      sendString = "NEW SFD DISPATCH\nCALL ADDRESS: {}\nCALL TYPE: {}\nRESPONDING UNITS: {}".format(latestIncident['incidentAddress'],callNature,', '.join(dispatchedUnits))
      for i in range(0,10):
        while True:
          try:
            print(sendString)
            response = client.create_tweet(text=sendString)
            print("SENDING TWEET")
          except Exception as e:
            print(e)
          break

    print(response,sendString)
  time.sleep(20)