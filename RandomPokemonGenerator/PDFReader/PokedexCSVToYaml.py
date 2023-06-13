import yaml
import csv

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
def findIndexNonExcludedString(fullWord : str, exclusions : list):
    i = 0
    eliminate = False
    while i < len(fullWord):
        for exclusion in exclusions:
            if fullWord[i] == exclusion[0]:
                if len(exclusion) == 1:
                    eliminate = True
                    j = i
                else:
                    k = 1
                    j = i + 1
                while not eliminate and k < len(exclusion) and j < len(fullWord):
                    if fullWord[j] == exclusion[k]:
                        if k == len(exclusion) - 1:
                            eliminate = True
                        j += 1
                        k += 1
                if eliminate:
                    i += j-i + 1
        if not eliminate:
            return i
        eliminate = False
    return i
#this removes random spaces and newlines before the first character and after the last character in the string
# "   a thing   \n  " will become "a thing"
def removeNonsenseBeginning(word : str):
    ind = findIndexNonExcludedString(word, [" ", "\n", "\t"])
    return word[ind:]
def removeNonsenseEnd(word : str):
    nonsense = [" ", "\n", "\t"]
    i = len(word) - 1
    while i >= 0 and word[i] in nonsense:
        i = i - 1
    return word[:i + 1]
def removeAllNonsense(word : str):
    return removeNonsenseEnd(removeNonsenseBeginning(word))
# the string passed in here has to be formatted: commaStr = "Apple, Banana, Canteloupe"
def processCommaList(commaStr : str):
    ls = []
    while "," in commaStr:
        ls.append(removeAllNonsense(commaStr[:commaStr.index(",")]))
        commaStr = commaStr[commaStr.index(",") + 1:]
    ls.append(removeAllNonsense(commaStr))
    return ls

#CTYName -- string
def CTYNames(name : str):
    return removeAllNonsense(removeAllCharacters(name, "."))
#CTYSTATS --------

#parseStatValue just returns the integer in the string as a string w/o spaces
def parseStatValue(line : str):
    numStr = ""
    i = 0
    while i < len(line):
        if line[i].isdigit():
            numStr += line[i]
        i += 1
    return numStr

#CTYStats -- dictionary {HP: 2, AT: 3, DF: 10, SA: 6, SD: 9, SP: 7}
def CTYStats(statBlockStr : str):
    statBlock = {}
    statLabel = ""
    for line in statBlockStr.splitlines():
        if "HP" in line:
            statLabel = "HP"
        elif "Special Attack" in line:
            statLabel = "SA"
        elif "Special Defense" in line:
            statLabel = "SD"
        elif "Attack" in line:
            statLabel = "AT"
        elif "Defense" in line:
            statLabel = "DF"
        elif "Speed" in line:
            statLabel = "SP"
        statBlock[statLabel] = parseStatValue(line)
    return statBlock

#CTYBasicInformation -- dictionary of lists
def CTYBasicInfo(basInf : str):    
    basInfDict = {"T" : [], "BA" : [], "AA" : [], "HA" : []}
    for line in basInf.splitlines():
        label = "T"
        if "T:" in line:
            label = "T"                
        elif "BA:" in line:
            label = "BA"
        elif "AA:" in line:
            label = "AA"
        elif "HA:" in line:
            label = "HA"
        lT = line[findIndexNonExcludedString(removeAllCharacters(line, "["), [label + ": ", label + ":"]):]
        lT = removeAllCharacters(lT, "]")
        basInfDict[label] = processCommaList(lT)
    return basInfDict.copy()
#CTYEVOL-----
#must begin with digits
def findDigits(line : str):
    i = 0
    while i < len(line) and line[i].isdigit():
        i += 1
    return line[:i]
def handleMisc(line : str):
    pass
#CTYEvol -- dictionary
    #Stage: NUMBER
    #Name: NAME
    #Level: LEVEL
    #Misc: Miscellaneous
def CTYEvol(pokemonNames : list, evols : str):
    evolDict = {"STAGE" : "", "NAME" : "", "LEVEL" : "", "MISC" : ""}
    for line in evols.splitlines():
        betterLine = removeAllNonsense(line) #  \n 2: Abomasnow Minimum 30 \n --> 2: Abomasnow Minimum 30
        evolDict["STAGE"] = betterLine[0]
        betterLine = betterLine[3:] # 2: Abomasnow Minimum 30 --> Abomasnow Minimum 30
        evolDict["NAME"] = betterLine[:betterLine.index(" ")]
        betterLine = betterLine[betterLine.index(" ") + 1:] # Abomasnow Minimum 30 --> Minimum 30
        minimumLoc = betterLine.index("Minimum")
        evolDict["LEVEL"] = findDigits(betterLine[minimumLoc + len("Minimum "):])
        betterLine = removeCharacter(betterLine, "Minimum: " + evolDict["LEVEL"]) # Minimum 30 --> /0
        if len(betterLine) == 0:
            evolDict["MISC"] = {}
            return evolDict
        evolDict["MISC"] = handleMisc(line)
    return evolDict
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

def main():
    pokeEntry = {}
    names = []
    with open("pokedexCLEANEDCSV.csv", encoding="UTF-8") as csv_file:
        cleanedPokedex = csv.DictReader(csv_file)
        for pokemon in cleanedPokedex:
            pokeEntry["NAME"] = CTYNames(pokemon['Species Name'])
            names.append(pokeEntry["NAME"])
        for pokemon in cleanedPokedex:
            pokeEntry["STATS"] = CTYStats(pokemon['Stats'])
            pokeEntry["BASIC_INFO"] = CTYBasicInfo(pokemon['Basic Information'])
            pokeEntry["EVOLUTIONS"] = CTYEvol(names, pokemon['Evolutions'])
            print(pokeEntry["EVOLUTIONS"])
if __name__ == "__main__":
    main()


