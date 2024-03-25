import googlemaps
import geopy.distance
from geographiclib.geodesic import Geodesic as geographiclib_Geodesic
import random
import regex

import QuestDictionary
import Logger

class QuestMaster():
  logger = Logger.Logger("QuestMaker-QuestMaster", active = True)
  gmaps = googlemaps.Client(key='AIzaSyC48kW3kb2qfwYL5yLoV_HB2ALfVBYHbWg')
  BANNED_PLACE_TYPES = [
      "administrative_area_level_1",
      "administrative_area_level_2",
      "administrative_area_level_3",
      "administrative_area_level_4",
      "administrative_area_level_5",
      "administrative_area_level_6",
      "administrative_area_level_7",
      "colloquial_area",
      "continent",
      "country",
      "establishment",
      "floor",
      "geocode",
      "locality",
      "neighborhood",
      "plus_code",
      "postal_code",
      "postal_code_prefix",
      "postal_code_suffix",
      "postal_town",
      "premise",
      "room",
      "route",
      "street_address",
      "street_number",
      "sublocality",
      "sublocality_level_1",
      "sublocality_level_2",
      "sublocality_level_3",
      "sublocality_level_4",
      "sublocality_level_5",
      "subpremise"
    ]
  SUPER_BANNED_PLACE_TYPES = [
      "casino",
      "night_club"
    ]
  QuestDistance = 1000
  GmapsPlaceTypes = QuestDictionary.gmapsLocationTypes
  SimpleFetchQuests = QuestDictionary.SimpleFetchQuests
  DecisionFetchQuests = QuestDictionary.DecisionFetchQuests
  @classmethod
  def generateQuest(cls, location, questType=None):
    #Quest Types:
    #   1kmFetch: Sends the user to a location 1km away.
    lat, lng = location
    if questType==None:
      #This is how I do random in my personal projects: using weighting with a number from 1 to 10000 or more if necessary
      # to help specify the percentage chance of a given outcome.
      randomInt = random.randint(1,10000)
      if randomInt in range(1,8001):
        questType = "SimpleFetch"
      elif randomInt in range(8001,10001):
        questType = "Special"

    cls.logger("Quest Type:", questType)

    if questType=="SimpleFetch":
      #Generating the target distance of the quest to be a random value in the range of 0.75-1.25 times the quest distance to give randomosity to quest generation.
      questDistance = random.randint(round(cls.QuestDistance*0.75),round(cls.QuestDistance*1.25))
      cls.logger("Quest Distance:", questDistance)
      #Using the Maps API to find nearby places.
      places = cls.gmaps.places_nearby(
        location=location,
        radius=questDistance
      )
      minDifferenceToQuestDistance = 999999999999
      placeMatch = None
      for place in places["results"]:
        for placeType in cls.SUPER_BANNED_PLACE_TYPES:
          if placeType in place["types"]:
            continue
        placeLat = float(place["geometry"]["location"]["lat"])
        placeLng = float(place["geometry"]["location"]["lng"])
        placeDistance = geopy.distance.distance(location, (placeLat, placeLng)).m
        #print(place["name"], placeDifference)
        #print(place["name"], place["types"])
        placeDifferenceToQuestDistance = abs(questDistance-placeDistance)
        if placeDifferenceToQuestDistance < minDifferenceToQuestDistance:
          minDifferenceToQuestDistance = placeDifferenceToQuestDistance
          placeMatch = place
      startLocationMatch = None
      places = cls.gmaps.places_nearby(
        location=location,
        radius=100
      )
      minDifferenceTo0 = 999999999999
      for place in places["results"]:
        for placeType in cls.SUPER_BANNED_PLACE_TYPES:
          if placeType in place["types"]:
            continue
        placeLat = float(place["geometry"]["location"]["lat"])
        placeLng = float(place["geometry"]["location"]["lng"])
        placeDifference = geopy.distance.distance(location, (placeLat, placeLng)).m
        if placeDifference < minDifferenceTo0:
          minDifferenceTo0 = placeDifference
          startLocationMatch = place
      cls.logger("Target Location:", placeMatch["name"], "Inaccuracy:", minDifferenceToQuestDistance)
      cls.logger("Start Location:", startLocationMatch["name"], "Inaccuracy:", minDifferenceTo0)
      for placeType in placeMatch["types"]:
        if placeType in cls.BANNED_PLACE_TYPES:
          pass
        else:
          placeTypeMatch = placeType
          break
      else:
        placeTypeMatch = "other"
      cls.logger("Target Location Type:", placeTypeMatch)
      try:
        questID = random.randint(1, len(cls.SimpleFetchQuests[placeTypeMatch]))
        questDetails = cls.SimpleFetchQuests[placeTypeMatch][questID]
      except:
        questID = random.randint(1, len(cls.SimpleFetchQuests["other"]))
        questDetails = cls.SimpleFetchQuests["other"][questID]
      placeMatchLat = float(placeMatch["geometry"]["location"]["lat"])
      placeMatchLng = float(placeMatch["geometry"]["location"]["lng"])
      return SimpleFetchQuest(
        startLocation = location,
        startLocationDetails = startLocationMatch,
        targetLocation = (placeMatchLat, placeMatchLng),
        targetLocationDetails = placeMatch,
        questDetails = questDetails
        )
    elif questType=="Special":
      randomInt = random.randint(1,10000)
      if randomInt in range(1,10001):
        questType = "DecisionFetch"

      if questType=="DecisionFetch":
        #places = cls.gmaps.places_nearby(
        #  location=location,
        #  radius=cls.QuestDistance
        #)

        targetPlaces = []
        for placeNo in range(0,2):
          placeTargetDistance = random.randint(round(cls.QuestDistance*0.75),round(cls.QuestDistance*1.25))
          places = cls.gmaps.places_nearby(
            location=location,
            radius=placeTargetDistance
          )
          minDifferenceToTargetDistance = 999999999999
          placeMatch = None
          cls.logger("Decision Fetch Target Distance", str(placeNo) + ":", placeTargetDistance)
          for place in places["results"]:
            if place in targetPlaces:
              continue
            for placeType in cls.SUPER_BANNED_PLACE_TYPES:
              if placeType in place["types"]:
                continue
            placeLat = float(place["geometry"]["location"]["lat"])
            placeLng = float(place["geometry"]["location"]["lng"])
            placeDifference = geopy.distance.distance(location, (placeLat, placeLng)).m
            #print(place["name"], placeDifference)
            #print(place["name"], place["types"])
            placeDifferenceToTargetDistance = abs(placeTargetDistance-placeDifference)
            if placeDifferenceToTargetDistance < minDifferenceToTargetDistance:
              minDifferenceToTargetDistance = placeDifferenceToTargetDistance
              placeMatch = place
          targetPlaces.append(placeMatch)
          #places["results"].remove(placeMatch)
        startLocationMatch = None
        places = cls.gmaps.places_nearby(
          location=location,
          radius=100
        )
        minDifferenceTo0 = 999999999999
        for place in places["results"]:
          for placeType in cls.SUPER_BANNED_PLACE_TYPES:
            if placeType in place["types"]:
              continue
          placeLat = float(place["geometry"]["location"]["lat"])
          placeLng = float(place["geometry"]["location"]["lng"])
          placeDifference = geopy.distance.distance(location, (placeLat, placeLng)).m
          if placeDifference < minDifferenceTo0:
            minDifferenceTo0 = placeDifference
            startLocationMatch = place

        questID = random.randint(1, len(cls.DecisionFetchQuests))
        questDetails = cls.DecisionFetchQuests[questID]
        return DecisionFetchQuest(
          startLocation = (startLocationMatch["geometry"]["location"]["lat"],startLocationMatch["geometry"]["location"]["lng"]),
          startLocationDetails = startLocationMatch,
          targetLocation1 = (targetPlaces[0]["geometry"]["location"]["lat"],targetPlaces[0]["geometry"]["location"]["lng"]),
          targetLocation1Details = targetPlaces[0],
          targetLocation2 = (targetPlaces[1]["geometry"]["location"]["lat"],targetPlaces[1]["geometry"]["location"]["lng"]),
          targetLocation2Details = targetPlaces[1],
          questDetails = questDetails
          )





#Quest is an abstract class and should only be inherited from, never used directly.
class Quest():
  def __init__(self, startLocation, startLocationDetails, targetLocation, targetLocationDetails, questDetails):
    self.startLocation = startLocation
    self.startLocationDetails = startLocationDetails
    self.targetLocation = targetLocation
    self.targetLocationDetails = targetLocationDetails
    self.accepted = False
    self.position = 0

    self.name = questDetails["name"]
    self.start_text = questDetails["start_text"]
    self.acceptance_text = questDetails["acceptance_text"]
    self.rejection_text = questDetails["rejection_text"]
    self.initial_guidance_text = questDetails["initial_guidance_text"]
    self.end_text = questDetails["end_text"]

    self.rewards = questDetails["rewards"]

    #All subclasses should then gather any other required information from questDetails.

  def start(self):
    return self.insertDetailsIntoDialogue((self.start_text,))

  def accept(self):
    self.accepted = True
    return self.insertDetailsIntoDialogue((self.acceptance_text,))

  def reject(self):
    rejected = self.insertDetailsIntoDialogue((self.rejection_text,))
    del(self)
    return rejected

  def guide(self):
    return self.insertDetailsIntoDialogue((self.determineGuidanceText(),))[0]

  def advance(self, currentLocation):
    if self.accepted == False:
      raise SyntaxWarning(f"advance() was called on the Simple Fetch Quest \"{self.name[0]}\" before it was accepted.")
    if abs(geopy.distance.distance(self.targetLocation, currentLocation).m) <= 30:
      self.position += 1
      self.determineNextTargetLocation()
      return self.insertDetailsIntoDialogue(self.determineNextDialogueLine())
    else:
      return False

  def determineNextDialogueLine(self):
    if self.position == 0:
      return self.start()
    elif self.position == 1:
      return self.end()
    else:
      return ["ERROR: DIALOGUE NOT FOUND"]

  def insertDetailsIntoDialogue(self, dialogue):
    #Dialogue should be a tuple, the first item of which is the dialogue to insert details into.
    newDialogue = []
    for line in dialogue[0]:
      #Insert target location name:
      line = regex.sub(
        pattern = r"\{location\}",
        repl = str(self.targetLocationDetails["name"]),
        string = line
        )
      #Insert start_location name:
      line = regex.sub(
        pattern = r"\{start_location\}",
        repl = str(self.startLocationDetails["name"]),
        string = line
        )

      newDialogue.append(line)
    if len(dialogue) == 1:
      return (newDialogue,)
    else:
      return (newDialogue,) + tuple(dialogue[1:])

  #TODO: Create determineGuidanceText to determine the next guidance text to be given.
  def determineGuidanceText(self):
    return self.initial_guidance_text

  def determineNextTargetLocation(self):
    if self.position == 1:
      self.targetLocation = self.startLocation

  def getDistance(self, location):
    return geopy.distance.distance(location, self.targetLocation).m

  def getBearing(self, location):
    bearing = geographiclib_Geodesic.WGS84.Inverse(location[0], location[1], self.targetLocation[0], self.targetLocation[1])["azi1"]
    if bearing < 0:
      bearing += 360
    return bearing

  def end(self):
    end_text, rewards = self.insertDetailsIntoDialogue((self.end_text, self.rewards))
    # del(self)
    return (end_text, rewards)
  
  def delete(self):
    del(self)
    return True

class SpecialQuest(Quest):
  pass
  #This class is an abstract class from which other special quest types are intended to inherit in order to denote that they are special quests
  # as opposed to regular quests.

class SimpleFetchQuest(Quest):
  def __init__(self, startLocation, startLocationDetails, targetLocation, targetLocationDetails, questDetails):
    super().__init__(startLocation, startLocationDetails, targetLocation, targetLocationDetails, questDetails)

    self.midpoint_text = questDetails["midpoint_text"]
    self.secondary_guidance_text = questDetails["secondary_guidance_text"]

  def determineNextDialogueLine(self):
    if self.position == 0:
      return self.start()
    elif self.position == 1:
      return (self.midpoint_text,)
    elif self.position == 2:
      return self.end()
    else:
      return ["ERROR: DIALOGUE NOT FOUND"]

  def determineGuidanceText(self):
    if self.position == 0:
      return self.initial_guidance_text
    elif self.position == 1:
      return self.secondary_guidance_text
    else:
      return ["ERROR: GUIDANCE TEXT NOT FOUND"]

  def determineNextTargetLocation(self):
    if self.position == 1:
      self.targetLocation = self.startLocation

class DecisionFetchQuest(SpecialQuest):
  def __init__(self, startLocation, startLocationDetails, targetLocation1, targetLocation1Details, targetLocation2, targetLocation2Details, questDetails):
    self.startLocation = startLocation
    self.startLocationDetails = startLocationDetails
    self.targetLocation = startLocation
    self.targetLocationDetails = startLocationDetails
    self.targetLocation1 = targetLocation1
    self.targetLocation1Details = targetLocation1Details
    self.targetLocation2 = targetLocation2
    self.targetLocation2Details = targetLocation2Details
    self.accepted = False
    self.position = 0

    self.name = questDetails["name"]
    self.start_text = questDetails["start_text"]
    self.acceptance_text = questDetails["acceptance_text"]
    self.rejection_text = questDetails["rejection_text"]
    self.initial_guidance_text = questDetails["initial_guidance_text"]
    self.midpoint_text = questDetails["midpoint_text"]
    self.secondary_guidance_text = questDetails["secondary_guidance_text"]
    self.end_text = questDetails["end_text"]

    self.rewards = questDetails["rewards"]

  def start(self):
    dialogue = super().start()
    dialogue.append(f"~decision 1/{self.targetLocation1Details['name']}\\1 2/{self.targetLocation2Details['name']}\\2 3/Reject Quest\\3")
    return dialogue

  def accept(self, decision=1):
    if decision == 1:
      self.targetLocation = self.targetLocation1
      self.targetLocationDetails = self.targetLocation1Details
    elif decision == 2:
      self.targetLocation = self.targetLocation2
      self.targetLocationDetails = self.targetLocation2Details
    else:
      return False
    self.accepted = True
    return self.insertDetailsIntoDialogue(self.acceptance_text)

  def advance(self, currentLocation, decision=None):
    if not self.accepted:
      raise SyntaxError(f"advance() was called on the Decision Fetch Quest \"{self.name[0]}\" before it was accepted.")
    else:
      return super().advance(currentLocation)

  def determineNextDialogueLine(self):
    if self.position == 0:
      return self.start()
    elif self.position == 1:
      return (self.midpoint_text,)
    elif self.position == 2:
      return self.end()
    else:
      return ["ERROR: DIALOGUE NOT FOUND"]

  def determineGuidanceText(self):
    if self.position == 0:
      return self.initial_guidance_text
    elif self.position == 1:
      return self.secondary_guidance_text
    else:
      return ["ERROR: GUIDANCE TEXT NOT FOUND"]

  def determineNextTargetLocation(self):
    if self.position == 1:
      self.targetLocation = self.startLocation

  def insertDetailsIntoDialogue(self, dialogue):
    #Dialogue must be a tuple, the first item of which is the actual dialogue to insert details into.
    newDialogue = []
    for line in dialogue:
      #Insert target location name:
      line = regex.sub(
        pattern = r"\{location\}",
        repl = str(self.targetLocationDetails["name"]),
        string = line
        )
      #Insert start_location name:
      line = regex.sub(
        pattern = r"\{start_location\}",
        repl = str(self.startLocationDetails["name"]),
        string = line
        )
      #Insert location1 name:
      line = regex.sub(
        pattern = r"\{location1\}",
        repl = str(self.targetLocation1Details["name"]),
        string = line
        )
      #Insert location2 name:
      line = regex.sub(
        pattern = r"\{location2\}",
        repl = str(self.targetLocation2Details["name"]),
        string = line
        )

      newDialogue.append(line)
    if len(dialogue) == 1:
      return (newDialogue,)
    else:
      return (newDialogue,) + tuple(dialogue[1:])





if __name__ == "__main__":
  raise SystemError("Running QuestMaker as Main.")

  # print(QuestDictionary.SimpleFetchQuests)
  # quest = QuestMaster.generateQuest(location=(53.393718088156554, -2.915312376731758), questType = "SimpleFetch")
  # print(quest.name[0])
  # print("##START TEXT##")
  # for line in quest.start()[0]:
  #   print(line)
  # print("##ACCEPTANCE TEXT##")
  # for line in quest.accept()[0]:
  #   print(line)
  # print("##GUIDANCE TEXT 1##")
  # for line in quest.guide():
  #   print(line)
  # print("##ADVANCEMENT FAIL CHECK##")
  # print(quest.getBearing((53.393718088156554, -2.915312376731758)))
  # print(quest.advance((53.393718088156554, -2.915312376731758)))
  # print("##ADVANCEMENT TEXT##")
  # for line in quest.advance(quest.targetLocation)[0]:
  #   print(line)
  # print("##GUIDANCE TEXT 2")
  # for line in quest.guide():
  #   print(line)
  # print("##END TEXT##")
  # ending = quest.end()
  # print(ending)
  # for line in ending[0]:
  #   print(line)
  # for line in ending[1]:
  #   if type(line) == int:
  #     print(f"{line}b")
  #   else:
  #     print(line)