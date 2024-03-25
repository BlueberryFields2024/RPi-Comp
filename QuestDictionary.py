
#This file contains data about all of the possible quests which the QuestMaster could generate via generateQuest, including their dialogue lines,
# and other key information about them. Each type of quest will be stored in a separate dictionary so that they can be imported separately when needed.

#---------------------------------------------------------------NOTICE TO DIALOGUE WRITERS--------------------------------------------------------------------------
#In order to make the implementation of the QuestUtils module possible, as well as to better reflect how dialogue is internally processed,
# I have had to slightly edit the way in which narrated lines are stored in the quest dictionary. Henceforth, if you wish for a line in a set of dialogue
# to be narrated instead of spoken by a character, such as if you want to convey that the player is picking up an item, you should start that line
# with:
#
#"__narrator__: "
#
#By doing this, you will mark the line as one which should be displayed as narration rather than as dialogue, however you can also still include dialogue
# spoken by an actual character named "narrator" if you so desire.
#
#The above does not apply to guidance text, which is not spoken by a character but instead always displayed as narration.
# Writing "__narrator__: " in guidance text will have no affect other than to display "__narrator__: " at the beginning of the guidance actually written onscreen.
#
#------------------------------------------------------PLEASE READ THE ABOVE BEFORE WRITING NEW DIALOGUE------------------------------------------------------------

#Here is a list of the google maps API Place Types:

gmapsLocationTypes = [
  "template",
  "other",
  "accounting",
  "airport",
  "amusement_park",
  "aquarium",
  "art_gallery",
  "atm",
  "bakery"
  "bank"
  "bar"
  "beauty_salon",
  "bicycle_store",
  "book_store",
  "bowling_alley",
  "bus_station",
  "cafe",
  "campground",
  "car_dealer",
  "car_rental",
  "car_repair",
  "car_wash",
  "cemetery",
  "church",
  "city_hall",
  "clothing_store",
  "convenience_store",
  "courthouse",
  "dentist",
  "department_store",
  "doctor",
  "drugstore",
  "electrician",
  "electronics_store",
  "embassy",
  "fire_station",
  "florist",
  "funeral_home",
  "furniture_store",
  "gas_station",
  "gym",
  "hair_care",
  "hardware_store",
  "hindu_temple",
  "home_goods_store",
  "hospital",
  "insurance_agency",
  "jewelry_store",
  "laundry",
  "lawyer",
  "library",
  "light_rail_station",
  "liquor_store",
  "local_government_office",
  "locksmith",
  "lodging",
  "meal_delivery",
  "meal_takeaway",
  "mosque",
  "movie_rental",
  "movie_theater",
  "moving_company",
  "museum",
  "painter",
  "park",
  "parking",
  "pet_store",
  "pharmacy",
  "physiotherapist",
  "plumber",
  "police",
  "post_office",
  "primary_school",
  "real_estate_agency",
  "restaurant",
  "roofing_contractor",
  "rv_park",
  "school",
  "secondary_school",
  "shoe_store",
  "shopping_mall",
  "spa",
  "stadium",
  "storage",
  "store",
  "subway_station",
  "supermarket",
  "synagogue",
  "taxi_stand",
  "tourist_attraction",
  "train_station",
  "transit_station",
  "travel_agency",
  "university",
  "veterinary_care",
  "zoo",
  "archipelago",
  "finance",
  "food",
  "general_contractor",
  "health",
  "intersection",
  "landmark",
  "natural_feature",
  "place_of_worship",
  "point_of_interest",
  "political",
  "post_box",
  "town_square"
  ]

#The SimpleFetchQuest Dictionary accounts for all types of target locations first and foremost, with each target location containing a list of quest
# details. To access a single piece of data from it, use the following syntax:
#
# QuestDictionary.SimpleFetchQuests[targetPlaceType][questNo][detail]
# Where:
#   - targetPlaceType is the Google Maps API Place Type of the endpoint of the fetch quest, stored as a string, e.g. "library"
#     A full list of place types is available online.
#
#   - questNo is a number between 1 and the number of quest types for the chosen endpoint which is the index of the quest to be fetched,
#     e.g. 3 if you want to fetch the third quest.
#
#   - detail is the piece of information which you wish to retrieve about the quest, stored as a string, e.g. "start_text"
#     Here is a list of details which a quest will store:
#       - "name": The name of the quest to be displayed to the user. The program should use ID and NOT name to identify a quest.
#       - "start_text": A list of strings containing the initial dialogue to be displayed before a quest is either accepted or rejected by the user.
#       - "acceptance_text": A list of strings containing the dialogue to be displayed if the quest is accepted.
#       - "rejection_text": A list of strings containing the dialogue to be displayed if the quest is rejected.
#       - "initial_guidance_text": A list of strings containing a description of what must be done to clear the first stage of the quest.
#       - "midpoint_text": A list of strings containing the dialogue to be displayed when the user arrives at the location the quest sent them to.
#       - "rewards": A list of the rewards issued for quest completion. Any integer values in this list are blueberry (gold) values to be given
#            to the player, whereas any string values will represent items. Please comment after an item HEX code what item it refers to.
#       - "secondary_guidance_text": A list of strings containing a description of what must be done to clear the second stage of the quest.
#       - "end_text": A list of strings containing the dialogue to be displayed when a quest is successfully completed.
#
#
SimpleFetchQuests = {
  "template":{
    1:{
      "name": [
        "A Test Quest"
        ],
      "start_text": [
        "Some Character: Hello World"
        ],
      "acceptance_text": [
        "Some Other Character: YE-HAW!"
        ],
      "rejection_text": [
        "Some Other Other Character: Y THO?!"
        ],
      "initial_guidance_text": [
        "Go to {location}."
        ],
      "midpoint_text": [
        "__narrator__: You found the holy grail!"
        ],
      "rewards": [
        9999999999999999999999999999999,
        "#FFFF" #Some Rubbish Item
        ],
      "secondary_guidance_text": [
        "Return to the start point."
        ],
      "end_text": [
        "Some Character: Hello World"
        ]
      }
    },
  "other":{
      1:{
      "name": [
        "A Noble Request"
        ],
      "start_text": [
        "*: You, there! Commoner!",
        "*: Yes, you!",
        "*: What do you mean, what? The insolence! Do you not know who I am?",
        "Claire François: I am Claire François, next head of the house of Count François. And do not forget it, lowly commoner.",
        "Claire François, The Annoying Young Noble Lady: [Irritatedly] Hey, I can tell you are insulting me in your head, you know! Cut that out AT ONCE!",
        "Claire François: Anyway, I am hungry, so fetch me some Sausage Rolls from {location}. You will be duly rewarded.",
        "Claire François: [Indignantly] What do you mean, \"That's not a very noble food to request?\" A noble can eat whatsoever they desire!",
        "Claire François: Now will you go, or not?!"
        ],
      "acceptance_text": [
        "Claire François: Good, it appears you have some sort of respect for nobles in that head of yours at least.",
        "Claire François: Now remember, I require a pack of sausage rolls from {location}. I will not accept inferior sausage rolls from anywhere else.",
        "Claire François: What do you mean, the ones at another store are better? I will have you know that-",
        "Claire François: Hey, where do you think you are going?",
        "Claire François: Do you not know that it is impolite to walk off whilst another person - noble or otherwise - is speaking? Have you no manners whatsoever?",
        "Claire François: *Sigh* Never mind, just go and fetch the sausage rolls.",
        "Claire François: And return post-haste, mind you - I truly am famished.",
        "Claire François: Oh, and in case you lack the funds, here is the money you will require. You had better buy those sausage rolls for me using it, mind you.",
        "__narrator__: You obtain a small sum of blueberries.",
        "__narrator__: However, thinking it would be unwise to accidentally spend them incorrectly, you instead separate them from your other blueberries as a designated 'Sausage Roll Fund.'"
        ],
      "rejection_text": [
        "Claire François: Whatever do you mean, \"No?\" A commoner cannot just refuse a noble like that!",
        "Claire François: Although I suppose that if you are busy, it would be unjust of me to disturb you for my little errand...",
        "Claire François: Fine, commoner. I will fetch the sausage rolls myself. Just leave my sight at once.",
        "Claire François, Who Actually Has Compassion?!: [Extremely Irritatedly] And for the last time, stop insulting me in your head! I can tell by your face, you know!"
        ],
      "initial_guidance_text": [
        "Go to {location} to fetch some sausage rolls for Claire François."
        ],
      "midpoint_text": [
        "__narrator__: You enter the store and use the 'Sausage Roll Fund' which Claire gave you to obtain a pack of sausage rolls."
        ],
      "rewards": [
        500,
        "#CF00" #The Emblem of House François
        ],
      "secondary_guidance_text": [
        "Deliver the sausage rolls to Claire, who is waiting for you at {start_location}."
        ],
      "end_text": [
        "Claire François: Is that you, Commoner? Took you long enough, considering my only request was that you fetch a pack of sausage rolls.",
        "Claire François: Now pass them over, if you please - I truly am famished!",
        "__narrator__: With a practiced motion, Claire opens the pack of sausage rolls and delicately takes a small bite, ensuring to chew it carefully before swallowing.",
        "__narrator__: Sighing with contentment, she turns her attention back to you.",
        "Claire François: I suppose I should thank you, Commoner. Were it not for you, I would never have received these sausage rolls.",
        "Claire François: Hm, what was that, Commoner?",
        "Claire François: Why could I not just fetch the sausage rolls myself? What insolence! Need I explain my every action to you? I think not!",
        "Claire François: [Blushing] Although, I suppose it would not matter if you did know...",
        "Claire François: Ah, fine, I will tell you. Much as I hate to admit it, Commoner, you were right - sausage rolls are not a very noble food to request.",
        "Claire François: As such, my servants would not allow me to purchase any, despite them being my favour- I mean, a very enjoyable food.",
        "Claire François, With Sheepish Sincerity: And so, I must th-thank you once again for- HOW MANY TIMES MUST I TELL YOU TO STOP THAT?",
        "Claire François, Lady Of Sheepish Sincerity: [Enragedly] What does that even mean, anyway?! What even is \"Sheepish Sincerity\"? I am not a sheep!",
        "Claire François: [Somewhat Annoyed Still, But Undeterred] A-anyway, here is your reward for the service you have rendered me.",
        "Claire François, In A Rare Act Of Kindness: I have also included my family's seal alongside your reward. If you should ever truly need my help, I would be willing to-",
        "Claire François: *Sigh* It appears I cannot hold a sensible conversation with you after all. Just get out of my sight."
        ]
      }
    },
  "accounting":{
    1:{
      "name": [
        "Jim, The Uncalculating Accountant"
        ],
      "start_text": [
        "__narrator__: Whilst walking along, you come across a group of people in the midst of a discussion.",
        "Businessman: [Speaking On Behalf Of A Group] So, what does your assistance cost then?",
        "Salesman: [Speaking To The Group, Unaware Of Your Presence] Uhh, well...",
        "Salesman: You see...",
        "Salesman: I... I have to... [Notices You] ...! Speak to my manager over here!",
        "Salesman: Yes, that's what I need to do first.",
        "Salesman: [To You] Shh, play along, pretty please.",
        "__narrator__: The Salesman pulls you over to one side.",
        "Salesman: Please, I need your help!",
        "Salesman: Me? The name's Jim. You can call me... JIM THE ACCOUNTANT!",
        "__narrator__: *crickets*",
        "Jim The Accountant: Ahem.",
        "Jim The Accountant: [Flustered] A-anyway, I am in dire need of your assistance.",
        "Jim The Accountant: You see, I am currently trying to sell this client the assistance of my accounting company.",
        "Jim The Accountant: Usually, my superior would do the job, but she's busy at the moment, so I must be brave and take it on myself.",
        "Jim The Accountant: The problem is, though, that I was so nervous that I forgot my calculator!",
        "Jim The Accountant: Without it, I can't calculate how much it would cost the client to make use of our company...",
        "Jim The Accountant: If you have a moment, could you please fetch it for me from {location}?",
        "Jim The Accountant: I'll keep the client busy in the meantime, and will also see to it that you're duly rewarded for your help to us.",
        "Jim The Accountant: So whaddya say? Will you help out a poor, lost accountant like me?"
        ],
      "acceptance_text": [
        "Jim The Accountant: Truly? Thank you so very much!",
        "Businessman: Is everything okay over there?",
        "Businessman: Whilst I wish not to pressure you, I will require a price point promptly in order to know whether or not I can continue discussing a contract...",
        "Jim The Accountant: Sorry, I must go and attend to the client, or else I will lose this opportunity to sell our company's services.",
        "Jim The Accountant: I will keep them occupied as best I can whilst you fetch my calculator, so please, return quickly!"
        ],
      "rejection_text": [
        "Jim The Accountant: Oh... that's too bad then...",
        "Jim The Accountant: [Turning Back To The Group] So, about the pricing... I think it would sum up to about...",
        "Businessman: Really? That seems rather cheap...",
        "Jim The Accountant: Truth be told, sir, I am not exactly sure of our pricings; discussions with clients are not usually part of my job, and I forgot the pricing guide...",
        "Businessman: So THAT was the problem! I understand now why you were having so much trouble giving us an estimate.",
        "Businessman: Worry not; I am sure that we can discuss pricing later in negotiations.",
        "Jim The Accountant: Wait... 'later in negotiations'?",
        "Businessman: [Smiling] Yes, I am sure that whatever your cost is, it will be well worth the service you provide.",
        "Businessman: After all, you yourself seem to be a dedicated person willing to do whatever it takes to benefit your company.",
        "Businessman: You looked visibly worried about losing the deal, and that's a trait I like to see in any loyal employee.",
        "Businessman: And besides, if your company's price is remotely like the figure you just quoted me, then the benefits of this venture will far oughtweigh its cost.",
        "Jim The Accountant: Truly? [The Businessman Nods] Thank you so very much, Sir!",
        "__narrator__: And so, Jim's negotiations with the Businessman end fruitfully for both parties, though your rejection of his request weighs upon your conscience...",
        "__narrator__: However, looking back at you, he smiles and gives a nod, as if to thank you for helping him to boost his self-confidence.",
        "__narrator__: Renewed with confidence in your decision, you set out again as Jim wanders off back towards {location}."
        ],
      "initial_guidance_text": [
        "Go to {location} to fetch Jim's Calculator."
        ],
      "midpoint_text": [
        "__narrator__: Arriving in front of Jim's office, you realise that you have no way to prove that Jim sent you.",
        "*: Excuse me, but can I help you at all? What brings you to our humble accountancy firm?",
        "*: Oh, Jim forgot his calculator AGAIN? Doesn't surprise me one bit. He's always leaving it lying around.",
        "*: But on the day of a meeting with a client? Really? He needs to get his act together.",
        "*: Anyway, I'll just be a minute.",
        "__narrator__: A minute passes with you waiting outside the building, and the employee returns.",
        "*: Heya, I'm back!",
        "*: I managed to find his calculator too - he left it on his desk.",
        "__narrator__: You obtain Jim's Golden Calculator."
        ],
      "rewards": [
        1000,
        "#0022", #Golden Groat
        "#F123" #Jim The Accountant's Business Card
        ],
      "secondary_guidance_text": [
        "Return Jim's Golden Calculator to him at {start_location}."
        ],
      "end_text": [
        "Jim The Accountant: [Clearly Struggling] Our company's skills are... skillful... and our intelligence is... intelligence... and-",
        "Jim The Accountant: [Noticing You] Oh, manager! Thank goodness you're here.",
        "__narrator__: You hand the Golden Calculator to Jim.",
        "Jim The Accountant: [To You] Now if you'll excuse me, I'll be just a moment whilst I talk to the client.",
        "Jim The Accountant: [To The Businessman] Sorry it took so long, but I can now run the numbers for you to give you a quote.",
        "Businessman: No worries. What will your assistance cost then?",
        "Jim The Accountant: [Typing On Calculator] Well, for a business of your size... with your current state... and your current income...",
        "Jim The Accountant: [Looking Up] Our service should cost around...",
        "Businessman: Yes, that should be fine, thank you very much.",
        "Businessman: I hereby officially request the assistance of your company to help with our company's finances.",
        "Jim The Accountant: [Relieved] Th-thank you so much, sir!",
        "Businessman: Ah, but before I go, I must first speak to your 'manager' over there.",
        "Businessman: [To You] Thank you so very much for stepping in despite not having anything to do with the situation.",
        "Businessman: Without your help, I would not have been able to raise young Jim's confidence in dealing with clients.",
        "Jim The Accountant: Wait... you knew?!",
        "Businessman: Yes, for I am not just any businessman.",
        "Jim The Accountant Senior: Jim, I am your father.",
        "Jim The Accountant: What?! But how?!",
        "Jim The Accountant Senior: [Ignores Him] Anyway, as I was saying, I will ensure that you are duly rewarded for running that little errand for my Son.",
        "Jim The Accountant Senior: You greatly helped in his training after all.",
        "Jim The Accountant Senior: Anyway, I am sure that I will seew you again some time, so I leave you to speak to Jim for a minute for the time being.",
        "Jim The Accountant: Wow... I had no idea...",
        "Jim The Accountant: Anyway, I feel I must reward you for helping me above what my Father gave to you...",
        "Jim The Accountant: So here, take this Golden Groat as a token of my appreciation.",
        "Jim The Accountant: I collect coins, you see, but I had a duplicate of this rare one, so you can have it for helping me.",
        "Jim The Accountant: Oh, and before I forget, here's my business card.",
        "Jim The Accountant: Anyway, thank you so much once again for your help, and I hope to meet you again some day.",
        "__narrator__: Jim wanders off, overjoyed with his succes, though dumbfounded at his father's deception."
        ]
      }
    },
  "airport":{
    1:{
      "name": [
        "Monsieur Bonjour"
        ],
      "start_text": [
        "Monsieur Bonjour: Hello, I am hoping for item from my friend waiting at {location}. *whispered* He's a bit crazy. Is you able to help me?"
        ],
      "acceptance_text": [
        "Monsieur Bonjour: I will see you soon!"
        ],
      "rejection_text": [
        "Monsier Bonjour: OK, I guess I'm going back to *very French* Paris."
        ],
      "initial_guidance_text": [
        "Go to {location}."
        ],
      "midpoint_text": [
        "__narrator__: You reached the airport! You see a small man muttering to himself in the distance. You approach him and he turns around to face you.",
        "Monsieur Au Revoir: Qu'est-ce que c'est ce que vous voulez?",
        "Monsieur Au Revoir: Pouvez-vous voir que je suis occupé?... [You stare at him blankly]... You don't speak French? You poor thing...",
        "Monsieur Au Revoir:  Monsieur Bonjour sent you?... Unbelievable. He's too self-centred to take the half hour to come and see me himself.",
        "Monsieur Au Revoir: I assume he wants the Red Baguette, yes?... Ok fine, take it."
        "__narrator__: He hands you the Red Baguette and two Pains au Chocolat."
        ],
      "rewards": [
        1000,
        "#AAAA", #A Pain au Chocolat
        "#AAAA", #A Pain au Chocolat
        ],
      "secondary_guidance_text": [
        "Return to the start point."
        ],
      "end_text": [
        "Monsieur Bonjour: Thank you so much! Take these for yourself. I'll see you round! [He hands you two Pains au Chocolat]."
        ]
      }
    },
  "amusement_park":{

    },
  "aquarium":{

    },
  "art_gallery":{

    },
  "atm":{

    },
  "bakery":{
    1:{
      "name": [
        "A Test Quest"
        ],
      "start_text": [
        "Some Character: Hello World"
        ],
      "acceptance_text": [
        "Some Other Character: YE-HAW!"
        ],
      "rejection_text": [
        "Some Other Other Character: Y THO?!"
        ],
      "initial_guidance_text": [
        "Go to {location}."
        ],
      "midpoint_text": [
        "__narrator__: You found the holy grail!"
        ],
      "rewards": [
        9999999999999999999999999999999,
        "#FFFF" #Some Rubbish Item
        ],
      "secondary_guidance_text": [
        "Return to the start point."
        ],
      "end_text": [
        "Some Character: Hello World"
        ]
    }
    },
  "bank":{

    },
  "bar":{

    },
  "beauty_salon":{

    },
  "bicycle_store":{

    },
  "book_store":{

    },
  "bowling_alley":{

    },
  "bus_station":{

    },
  "cafe":{

    },
  "campground":{

    },
  "car_dealer":{

    },
  "car_rental":{

    },
  "car_repair":{

    },
  "car_wash":{
    1:{
      "name": [
        "A Test Quest"
        ],
      "start_text": [
        "Some Character: Hello World"
        ],
      "acceptance_text": [
        "Some Other Character: YE-HAW!"
        ],
      "rejection_text": [
        "Some Other Other Character: Y THO?!"
        ],
      "initial_guidance_text": [
        "Go to {location}."
        ],
      "midpoint_text": [
        "__narrator__: You found the holy grail!"
        ],
      "rewards": [
        9999999999999999999999999999999,
        "#FFFF" #Some Rubbish Item
        ],
      "secondary_guidance_text": [
        "Return to the start point."
        ],
      "end_text": [
        "Some Character: Hello World"
        ]
      }
    },
  "cemetery":{

    },
  "church":{

    },
  "city_hall":{

    },
  "clothing_store":{

    },
  "convenience_store":{

    },
  "courthouse":{

    },
  "dentist":{

    },
  "department_store":{

    },
  "doctor":{

    },
  "drugstore":{

    },
  "electrician":{

    },
  "electronics_store":{

    },
  "embassy":{

    },
  "fire_station":{

    },
  "florist":{

    },
  "funeral_home":{

    },
  "furniture_store":{

    },
  "gas_station":{

    },
  "gym":{

    },
  "hair_care":{

    },
  "hardware_store":{

    },
  "hindu_temple":{

    },
  "home_goods_store":{

    },
  "hospital":{

    },
  "insurance_agency":{

    },
  "jewelery_store":{

    },
  "laundry":{

    },
  "lawyer":{

    },
  "library":{

    },
  "light_rail_station":{

    },
  "liquor_store":{

    },
  "local_government_office":{

    },
  "locksmith":{

    },
  "lodging":{

    },
  "meal_delivery":{

    },
  "meal_takeaway":{

    },
  "mosque":{

    },
  "movie_rental":{

    },
  "movie_theater":{

    },
  "moving_company":{

    },
  "museum":{

    },
  "painter":{

    },
  "park":{

    },
  "parking":{

    },
  "pet_store":{

    },
  "pharmacy":{

    },
  "physiotherapist":{

    },
  "plumber":{

    },
  "police":{

    },
  "post_office":{

    },
  "primary_school":{

    },
  "real_estate_agency":{

    },
  "restaurant":{

    },
  "roofing_contractor":{

    },
  "rv_park":{

    },
  "school":{

    },
  "secondary_school":{

    },
  "shoe_store":{

    },
  "shopping_mall":{

    },
  "spa":{

    },
  "stadium":{

    },
  "storage":{

    },
  "store":{

    },
  "subway_station":{

    },
  "supermarket":{
      1:{
      "name": [
        "A Noble Request"
        ],
      "start_text": [
        "*: You, there! Commoner!",
        "*: Yes, you!",
        "*: What do you mean, what? The insolence! Do you not know who I am?",
        "Claire François: I am Claire François, next head of the house of Count François. And do not forget it, lowly commoner.",
        "Claire François, The Annoying Young Noble Lady: [Irritatedly] Hey, I can tell you are insulting me in your head, you know! Cut that out AT ONCE!",
        "Claire François: Anyway, I am hungry, so fetch me some Sausage Rolls from {location}. You will be duly rewarded.",
        "Claire François: [Indignantly] What do you mean, \"That's not a very noble food to request?\" A noble can eat whatsoever they desire!",
        "Claire François: Now will you go, or not?!"
        ],
      "acceptance_text": [
        "Claire François: Good, it appears you have some sort of respect for nobles in that head of yours at least.",
        "Claire François: Now remember, I require a pack of sausage rolls from {location}. I will not accept inferior sausage rolls from anywhere else.",
        "Claire François: What do you mean, the ones at another store are better? I will have you know that-",
        "Claire François: Hey, where do you think you are going?",
        "Claire François: Do you not know that it is impolite to walk off whilst another person - noble or otherwise - is speaking? Have you no manners whatsoever?",
        "Claire François: *Sigh* Never mind, just go and fetch the sausage rolls.",
        "Claire François: And return post-haste, mind you - I truly am famished.",
        "Claire François: Oh, and in case you lack the funds, here is the money you will require. You had better buy those sausage rolls for me using it, mind you.",
        "__narrator__: You obtain a small sum of blueberries.",
        "__narrator__: However, thinking it would be unwise to accidentally spend them incorrectly, you instead separate them from your other blueberries as a designated 'Sausage Roll Fund.'"
        ],
      "rejection_text": [
        "Claire François: Whatever do you mean, \"No?\" A commoner cannot just refuse a noble like that!",
        "Claire François: Although I suppose that if you are busy, it would be unjust of me to disturb you for my little errand...",
        "Claire François: Fine, commoner. I will fetch the sausage rolls myself. Just leave my sight at once.",
        "Claire François, Who Actually Has Compassion?!: [Extremely Irritatedly] And for the last time, stop insulting me in your head! I can tell by your face, you know!"
        ],
      "initial_guidance_text": [
        "Go to {location} to fetch some sausage rolls for Claire François."
        ],
      "midpoint_text": [
        "__narrator__: You enter the store and use the 'Sausage Roll Fund' which Claire gave you to obtain a pack of sausage rolls."
        ],
      "rewards": [
        500,
        "#CF00" #The Emblem of House François
        ],
      "secondary_guidance_text": [
        "Deliver the sausage rolls to Claire, who is waiting for you at {start_location}."
        ],
      "end_text": [
        "Claire François: Is that you, Commoner? Took you long enough, considering my only request was that you fetch a pack of sausage rolls.",
        "Claire François: Now pass them over, if you please - I truly am famished!",
        "__narrator__: With a practiced motion, Claire opens the pack of sausage rolls and delicately takes a small bite, ensuring to chew it carefully before swallowing.",
        "__narrator__: Sighing with contentment, she turns her attention back to you.",
        "Claire François: I suppose I should thank you, Commoner. Were it not for you, I would never have received these sausage rolls.",
        "Claire François: Hm, what was that, Commoner?",
        "Claire François: Why could I not just fetch the sausage rolls myself? What insolence! Need I explain my every action to you? I think not!",
        "Claire François: [Blushing] Although, I suppose it would not matter if you did know...",
        "Claire François: Ah, fine, I will tell you. Much as I hate to admit it, Commoner, you were right - sausage rolls are not a very noble food to request.",
        "Claire François: As such, my servants would not allow me to purchase any, despite them being my favour- I mean, a very enjoyable food.",
        "Claire François, With Sheepish Sincerity: And so, I must th-thank you once again for- HOW MANY TIMES MUST I TELL YOU TO STOP THAT?",
        "Claire François, Lady Of Sheepish Sincerity: [Enragedly] What does that even mean, anyway?! What even is \"Sheepish Sincerity\"? I am not a sheep!",
        "Claire François: [Somewhat Annoyed Still, But Undeterred] A-anyway, here is your reward for the service you have rendered me.",
        "Claire François, In A Rare Act Of Kindness: I have also included my family's seal alongside your reward. If you should ever truly need my help, I would be willing to-",
        "Claire François: *Sigh* It appears I cannot hold a sensible conversation with you after all. Just get out of my sight."
        ]
      }
    },
  "synagogue":{

    },
  "taxi_stand":{

    },
  "tourist_attraction":{

    },
  "train_station":{

    },
  "transit_station":{

    },
  "travel_agency":{

    },
  "university":{

    },
  "vetinary_care":{

    },
  "zoo":{

    },
  "archipelago":{

    },
  "finance":{

    },
  "food":{

    },
  "general_contractor":{

    },
  "health":{

    },
  "intersection":{

    },
  "landmark":{

    },
  "natural_feature":{

    },
  "place_of_worship":{

    },
  "point_of_interest":{

    },
  "political":{
    1:{
      "name": [
        "Message for the Man with No Name"
        ],
      "start_text": [
        "*: Psst! Hey, you there!",
        "*: Yes, I am talking to you; come over here.",
        "*: I have this very important message which I just must deliver to my acquaintance at {location}, but I do not have the time to make it there myself.",
        "*: Would you please deliver it for me?"
        ],
      "acceptance_text": [
        "*: Good. Thank you for agreeing to assist me.",
        "*: Hm, how will you know my acquaintance when you find him, you ask?",
        "*: Unfortunately, he asked me not to give you his name, but he should immediately ask you for the message upon seeing it, so worry not, my friend.",
        "*: Now hurry, there is no time to lose!",
        "__narrator__: You obtain a sealed envelope."
        ],
      "rejection_text": [
        "*: Oh, oh dear - whatever will I do now?"
        ],
      "initial_guidance_text": [
        "Take the sealed envelope to the mysterious man awaiting you at {location}."
        ],
      "midpoint_text": [
        "*: Psst! Halloa, over there!",
        "*: That letter you have in your hand... it seems to be the one which I seek.",
        "*: Could you give it to me, please?",
        "__narrator__: You hand the sealed envelope over to the mysterious man.",
        "*: Thank you very much!",
        "*: Ah, and could you please pass this letter back to the first man you met to confirm that I have received this letter?",
        "*: I am sure that he will make it worth your while.",
        "__narrator__: You obtain <i>another</i> sealed envelope."
        ],
      "rewards": [
        10000,
        "#FFFE" #Honour and Pride
        ],
      "secondary_guidance_text": [
        "Deliver the second sealed envelope back to the first mysterious man you found near {start_location}."
        ],
      "end_text": [
        "*: Hm, is that for me?",
        "__narrator__: You hand the second sealed envelope over to the mysterious man.",
        "*: [Reading] Yes, yes... hmm...",
        "*: Thank you very much for delivering these important messages between us.",
        "*: Your actions today have been instrumental in maintaining global peace, though I cannot confer to you the details as to why.",
        "*: As such, you must be justly rewarded: here, take this and go forth in the knowledge that you have done a great deed on this fine day."
        ]
      }
    },
  "post_box":{

    },
  "town_square":{

    }
  }

#####From here onwards in the file are shorter dictionaries designed for special quest types.
#####They are not designed to be coherent with the world and only appear very rarely.

#The DecisionFetchQuest Dictionary contains a list of generic quests to be used in any location; it requires only a quest ID as an input to
# get a specific quest from it. You can access it, therefore, as follows:
#
# QuestDictionary.SimpleFetchQuests[questNo][detail]
# Where:
#   - questNo is a number between 1 and the number of quests,
#     e.g. 3 if you want to fetch the third quest.
#
#   - detail is the piece of information which you wish to retrieve about the quest, stored as a string, e.g. "start_text"
#     Here is a list of details which a quest will store:
#       - "name": The name of the quest to be displayed to the user. The program should use ID and NOT name to identify a quest.
#       - "start_text": A list of strings containing the initial dialogue to be displayed before a quest is either accepted or rejected by the user.
#       - "acceptance_text": A list of strings containing the dialogue to be displayed if the quest is accepted.
#       - "rejection_text": A list of strings containing the dialogue to be displayed if the quest is rejected.
#       - "initial_guidance_text": A list of strings containing a description of what must be done to clear the first stage of the quest.
#       - "midpoint_text": A list of strings containing the dialogue to be displayed when the user arrives at the location the quest sent them to.
#       - "rewards": A list of the rewards issued for quest completion. Any integer values in this list are blueberry (gold) values to be given
#            to the player, whereas any string values will represent items. Please comment after an item HEX code what item it refers to.
#       - "secondary_guidance_text": A list of strings containing a description of what must be done to clear the second stage of the quest.
#       - "end_text": A list of strings containing the dialogue to be displayed when a quest is successfully completed.
#
#

DecisionFetchQuests = {
  1:{
    "name": [
      "A Leisurely Stroll With Mr. Greilo"
      ],
    "start_text": [
      "*: Why hello there, young one! My name is Mr. Greilo, pronounced \"gray-low\".",
      "Mr. Greilo: It's been a while since I've seen such a young whippersnapper as yourself 'round these parts, and it brings me joy to see you out and about like you should be.",
      "Mr. Greilo: Say, you look a little like my grandson, so how do ya feel about going for a walk to humour an old-timer like me?",
      "Mr. Greilo: We could go to either {location1} or {location2}, so whaddaya say?"
      ],
    "acceptance_text": [
      "Mr. Greilo: To {location}, you say? Fine by me.",
      "Mr. Greilo: Let's get going then, whippersnapper. Don't leave me behind, now!"
      ],
    "rejection_text": [
      "Mr. Greilo: Aww, that's too bad - I was looking forward to having a little jaunt with a young 'un like in the good old days.",
      "Mr. Greilo: Welp, I must be going; perhaps we'll meet again some day, youngster."
      ],
    "initial_guidance_text": [
      "Walk with gramps to {location}."
      ],
    "midpoint_text": [
      "Mr. Greilo: So here we are, then, at {location}.",
      "Mr. Greilo: It's been a while since I was last here. Boy, does this take me back...",
      "Mr. Greilo: I used to go all over with my grandson, just to do this and that together; to show him my favourite places.",
      "Mr. Greilo: But no matter where we went, he always seemed to like coming here the most.",
      "Mr. Greilo: See over there? That's where we used to stand together, chatting away non-stop.",
      "Mr. Greilo: He always told the funniest of jokes. Oh, how I miss those days we spent together.",
      "Mr. Greilo: What happened to my grandson, you ask?",
      "Mr. Greilo: Oh, I do apologise, my nostalgia must have given you the wrong impression!",
      "Mr. Greilo: My grandson is alive and well; in fact, right now, he's doing better than I could ever have hoped.",
      "Mr. Greilo: He has found himself a great job and a loving family, and is currently busy working on a project which may some day change the world as we know it!",
      "Mr. Greilo: But the bad must come with the good, I suppose. With him being so busy, we can no longer spend so long together these days...",
      "Mr. Greilo: Welp, we'd better be heading back to {start_location}, where we set out.",
      "Mr. Greilo: I'm sure you have much better things to be doing than listening to me blabber on all day."
      ],
    "rewards": [
      0,
      "#0000" #Rare Candy
      ],
    "secondary_guidance_text": [
      "Return to {start_location} with gramps."
      ],
    "end_text": [
      "Mr. Greilo: Thank you for humouring an old man and accompanying me to {location}.",
      "Mr. Greilo: It really did feel just like the good ol' days when I used to spend lots of time with my grandson.",
      "Mr. Greilo: Welp, I must be going; perhaps we'll meet again some day, youngster.",
      "Mr. Greilo: Oh, but first, I feel I must give you this candy.",
      "Mr. Greilo: These candies were a favourite of my grandson. He would always ask me for one whenever we went on a walk together.",
      "Mr. Greilo: I hope it will serve you well some day in the future."
      ]
    }
  }