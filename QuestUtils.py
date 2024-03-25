import regex

class Generic():
  #This is a static class and should only have its methods used, never being instantiated.
  CHARACTER_IMAGE_DICTIONARY = {
    #Generic
    "*": "silhouette.png",


    #Simple Fetch:
    #Accountancy:
    
    #Airport:
    
    #Supermarket:
    #Supermarket 1: A Noble Request
    "Claire François": "silhouette.png",
    "Claire François, The Annoying Young Noble Lady": "silhouette.png",
    "Claire François, Who Actually Has Compassion?!": "silhouette.png",
    "Claire François, With Sheepish Sincerity": "silhouette.png",
    "Claire François, Lady Of Sheepish Sincerity": "silhouette.png",
    "Claire François, In A Rare Act Of Kindness": "silhouette.png",


    #Decision Fetch:
    #1
    "Mr. Greilo": "silhouette.png"

  }
  DEFAULT_CHARACTER_IMAGE = "silhouette.png"
  @classmethod
  def DecomposeDialogueLine(cls, dialogueLine):
    #This method decomposes a single dialogue string passed into it via the variable "dialogueLine".
    #To batch decompose dialogue, use "DecomposeDialogue(dialogue)" instead.
    if type(dialogueLine) != str:
      raise AttributeError(f"QuestUtils.Generic.DecomposeDialogueLine attempted to decompose an item of type \'{type(dialogueLine)}\' as if it were a string.")
    if regex.match(
      pattern=r"~decision",
      string=dialogueLine
    ):
      dialogueType = "Decision"
      options = []
      optionNo = 1
      while True:
        pattern = r"(?:" + str(optionNo) + r"/)(.*)(?:\\" + str(optionNo) + r")"
        option = regex.findall(
          pattern=pattern,
          string=dialogueLine
        )
        if option:
          options.append(option[0])
          optionNo += 1
        else:
          break
      return Decision(options)
    else:
      speaker = regex.findall(
        pattern="(?:^)(.*?)(?:: )",
        string=dialogueLine
      )[0]
      text = regex.findall(
        pattern="(?:^.*?)(?:: )(.*)",
        string=dialogueLine
      )[0]
      if speaker == "__narrator__":
        return Narration(text)
      else:
        try:
          speakerImage = cls.CHARACTER_IMAGE_DICTIONARY[speaker]
        except KeyError:
          speakerImage = cls.DEFAULT_CHARACTER_IMAGE
        return Speech(
          speaker=speaker,
          speakerImage=speakerImage,
          text=text
        )

  @classmethod
  def DecomposeDialogue(cls, dialogue):
    return [cls.DecomposeDialogueLine(dialogueLine=dialogueLine) for dialogueLine in dialogue]



class DialogueObject():
  #DialogueObject is an abstract class which other DialogueObject types should inherit from but which should never be instantiated itself.
  def __init__(self, dialogueType="DialogueObject"):
    self.type = dialogueType

class Speech(DialogueObject):
  #A dialogue object which represents direct speech which can be displayed using the normal text box:
  #A Speech object should contain the following attributes about the speech:
  #   - "speaker": A string representing the name of the speaker to be displayed on the relevant portion of the dialogue box.
  #   - "speakerImage": A string containing the name (complete with file ending) of the image file to be used for the speaker of the dialogue.
  #   - "text": A string containing what the speaker is saying so that it can be displayed in the main text box.
  #Additionally, in order to help identify it without the need for a complex type() call, it should have the following constant attached to it:
  #   - "type": A string which should always contain "Speech" and helps you to distinguish a Speech object from other objects which inherit
  #        from QuestUtils.DialogueObject. All Dialogue Objects returned by QuestUtils.Generic.DecomposeDialogueLine or
  #        QuestUtils.Generic.DecomposeDialogueLines will have this attribute, so requesting it from a Dialogue Object of unknown
  #        specific type should not cause the program to crash.
  def __init__(self, speaker, speakerImage, text):
    self.speaker, self.speakerImage, self.text = (speaker, speakerImage, text)
    super().__init__(dialogueType="Speech")

class Narration(DialogueObject):
  #A special type of dialogue object with no speaker or speakerImage to represent narration in a quest, or in other words lines in said quest which
  # describe what is happening to the user without being spoken aloud. These dialouge lines are set apart from regular dialogue, as explained in
  # QuestDictionary, by the fact that they begin with "__narrator__: ".
  #A Narration object should contain the following attribute about the narration:
  #   - "text": A string containing the text to be displayed to the user in the main text box as narration.
  #Additionally, in order to help identify it without the need for a complex type() call, it should have the following constant attached to it:
  #   - "type": A string which should always contain "Narration" and helps you to distinguish a Narration object from other objects which inherit
  #        from QuestUtils.DialogueObject. All Dialogue Objects returned by QuestUtils.Generic.DecomposeDialogueLine or
  #        QuestUtils.Generic.DecomposeDialogueLines will have this attribute, so requesting it from a Dialogue Object of unknown
  #        specific type should not cause the program to crash.
  def __init__(self, text):
    self.text = text
    super().__init__(dialogueType="Narration")

class Decision(DialogueObject):
  #A dialogue object which represents a set of options to be presented to the player via the decision screen of the RaspberryPi UI.
  #A Decision object should contain the following attribute about its options:
  #   - "options": A list of strings containing the options to be displayed on the buttons of the decision screen.
  #        WARNING: Although options is stored as a 0-Indexed List here, options[0] is actually considered as option #1 by QuestMaster and
  #              all other locations in the program, so please ensure that your decision buttons link up to the correct decision to be
  #              passed to the DecisionFetchQuest object which you are using when you call advance after having made your decision after
  #              start().
  #Additionally, in order to help identify it without the need for a complex type() call, it should have the following constant attached to it:
  #   - "type": A string which should always contain "Decision" and helps you to distinguish a Decision object from other objects which inherit
  #        from QuestUtils.DialogueObject. All Dialogue Objects returned by QuestUtils.Generic.DecomposeDialogueLine or
  #        QuestUtils.Generic.DecomposeDialogueLines will have this attribute, so requesting it from a Dialogue Object of unknown
  #        specific type should not cause the program to crash.
  def __init__(self, options):
    self.options = options
    super().__init__(dialogueType="Decision")


if __name__ == "__main__":
  raise SystemError("Running QuestUtils as Main.")