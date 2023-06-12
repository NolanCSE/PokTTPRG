import yaml

def removeCharacter(word, removeChar):
    if removeChar not in word:
        return word
    if word[0] == removeChar:
        return word[1:]
    elif word[len(word) - 1] == removeChar:
        return word[:len(word)-1]
    return word[:word.index(removeChar)] + word[word.index(removeChar) + 1:]
def removeAllCharacters(word, removeChar):
    while removeChar in word:
        word = removeCharacter(word, removeChar)
    return word

#CTYName -- string
def CTYNames(names : list):
    finNames = []
    for name in names:
        finNames.append(removeAllCharacters(name, "."))
    return finNames
#CTYStats -- dictionary {HP: 2, AT: 3, DF: 10, SA: 6, SD: 9, SP: 7}
def CTYStats(stats : list):
    for statBlock in stats:
        for stat in statBlock.splitlines():
            pass
    pass
#CTYBasicInformation -- dictionary of lists
def CTYBasicInfo(basInf : list):
    pass
#CTYEvol -- dictionary
def CTYEvol(evols : list):
    pass
#CTYSize -- dictionary
def CTYSize(sizes : list):
    pass
#CTYBreedingInformation -- dictionary of lists
def CTYBreedInfo(breedInf : list):
    pass
#Diet -- List
def CTYDiet(diets : list):
    pass
#Habitat -- List
def CTYHabit(habits : list):
    pass
#Capabilities -- Dictionary
def CTYCapabilities(capabilities : list):
    pass
#Skills -- Dictionary
def CTYSkills(skills : list):
     pass
#Level Up Moves -- Dictionary of dictionary
def CTYLvlMoves(lvl_moves : list):
    pass
# TM/HM Moves -- Dictionary of dictionary
def CTYTMMoves(tm_moves : list):
    pass
#Tutor Moves -- List
def CTYTutorMoves(tut_moves : list):
    pass

