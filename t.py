import module as SFDModule
latestIncident = SFDModule.getIncidentInformation(SFDModule.getLatestIncidentID())
fixedDict = {}
for apparatus in latestIncident['apparatusStatuses']:
  fixedDict[SFDModule.replaceApprv(apparatus)] = latestIncident['apparatusStatuses'][apparatus]
dispatchedUnits = list(fixedDict.keys())
callNature = latestIncident['incidentType'].split(" - ")[1]

print(callNature)