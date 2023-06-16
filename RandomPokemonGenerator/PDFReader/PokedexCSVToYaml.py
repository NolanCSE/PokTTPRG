import yaml
import csv

def removeCharacter(word, removeChar):
    if removeChar not in word:
        return word
    if word[0] == removeChar[0]:
        return word[len(removeChar):]
    elif word[len(word) - 1] == removeChar[-1]:
        return word[:len(word)-len(removeChar)]
    return word[:word.index(removeChar)] + word[word.index(removeChar) + len(removeChar):]
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
#CTYNAME ----------
def spaceOut(camelCase):
    #if there is no space between a lower and upper case letter, insert one
    i = 0
    while i < len(camelCase) - 1:
        if (not camelCase[i].isupper()) and camelCase[i + 1].isupper():
            camelCase = camelCase[:i + 1] + " " + camelCase[i + 1:]
            i += 1
        i += 1
    return camelCase
#CTYName -- string
def CTYNames(name : str):
    #Special cases
    if name == "QUIILLADIN":
        name = "QUILLADIN"
    if name == "SLIGGOO":
        name = "SLIGOO"
    elif name == "NIDORAN(F)":
        name = "NIDORAN F"
    elif name == "NIDORAN(M)":
        name = "NIDORAN M"
    elif "MIMEJR." in name:
        return "MIME JR."
    elif "MR.MIME" in name:
        return "MR. MIME"
    elif "FARFETCH" in name:
        return "FARFETCH'D"

    #Form cases
    if "Form" in name:
        startForm = 0
        for ind, letter in enumerate(name):
            if not letter.isupper():
                startForm = ind - 1
                break
        actName = name[:startForm]
        formName = name[startForm:]
        name = actName + " (" + spaceOut(formName) + ")"
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
    miscDict = {}
    beenIn = False
    if "Female" in line or "Male" in line:
        #import pdb; pdb.set_trace()
        if "Female" in line:
            strVar = "Female"
        else:
            strVar = "Male"
        line = removeCharacter(line, strVar)
        miscDict["GENDER"] = strVar
        beenIn = True
    if "Night" in line:
        if "Night" in line:
            strVar = "Night"
        else:
            strVar = "Day"
        line = removeCharacter(line, strVar)
        miscDict["TIME"] = strVar
        beenIn = True
    if "Holding" in line:
        line = removeCharacter(line, "Holding")
        miscDict["HOLDING"] = removeAllNonsense(line)
        beenIn = True
    if "Stone" in line:
        miscDict["HOLDING"] = removeAllNonsense(line)
        beenIn = True
    if "Learn" in line:
        line = removeCharacter(line, "Learn")
        miscDict["LEARN"] = removeAllNonsense(line)
        beenIn = True
    if not beenIn:
        miscDict["MISC"] = removeAllNonsense(line)
    return miscDict
def pokemonInside(line : str, pokemonNames : str):
    pokemonsInside = []
    for pokemon in pokemonNames:
        if "(" in pokemon:
            if removeAllNonsense(pokemon.lower()[:pokemon.index("(")]) in line.lower():
                pokemonsInside.append(removeAllNonsense(pokemon.lower()[:pokemon.index("(")]))
        elif pokemon.lower() in line.lower():
            pokemonsInside.append(pokemon.lower())
    return pokemonsInside
def getMinLength(strArray : str):
    minLength = len(strArray[0])
    minInd = 0
    for index, string in enumerate(strArray):
        if len(string) < minLength:
            minLength = len(string)
            minInd = index
    return minInd
def getClosest(searchWord : str, listOfWords : list):
    #import pdb; pdb.set_trace()
    closestInd = searchWord.index(listOfWords[0])
    wordLength = len(listOfWords[0])
    for word in listOfWords:
        if searchWord.index(word) < closestInd or (searchWord.index(word) == closestInd and len(word) > wordLength):
            closestInd = searchWord.index(word)
            wordLength = len(word)
    return closestInd, wordLength
def numberColonOrDashExists(text : str):
    for ind, character in enumerate(text):
        if (ind == len(text) - 1) or (ind == len(text) - 2):
            return False
        if (ind != len(text) - 1) and (character.isdigit() and text[ind + 1] == ":") or (character.isdigit() and text[ind + 2] == "-"):
            return True
    return False
def getIndexFirstNum(text : str):
    for ind, character in enumerate(text):
        if ind == len(text) - 1 or ind == len(text) - 2:
            return -1
        elif (character.isdigit() and text[ind + 1] == ":") or (character.isdigit() and text[ind + 2] == "-"):
            return ind
    return -1
def convertFloatToString(num : float):
    #import pdb; pdb.set_trace()
    return str(num.__round__(2))
def formatMultipleEvols(evolText : str):
    copyEvolText = ""
    wholeTrackers = []
    #import pdb; pdb.set_trace()
    while numberColonOrDashExists(evolText):
        ind = getIndexFirstNum(evolText)
        if len(wholeTrackers) < int(evolText[ind]):
            wholeTrackers.append(float(evolText[ind]))
        else:
            wholeTrackers[int(evolText[ind]) - 1] += 0.01
        evolText = removeAllNonsense(evolText)
        if getIndexFirstNum(evolText[ind + 1:]) == -1:
            endInd = len(evolText)
        else:
            endInd = getIndexFirstNum(evolText[ind + 1:]) + len(evolText[:ind + 1])
        potentialText = removeAllNonsense(evolText[ind:endInd])
        if "-" in potentialText:
            potentialText = convertFloatToString(wholeTrackers[int(potentialText[0]) - 1]) + ": " + potentialText[4:]
        copyEvolText += potentialText + "\n"
        evolText = evolText[0:ind] + evolText[endInd:]
    return removeAllNonsense(copyEvolText)
#CTYEvol -- dictionary
    #Stage: NUMBER
    #Name: NAME
    #Level: LEVEL
    #Misc: Miscellaneous
def CTYEvol(pokemonNames : list, evols : str):
    if "Y anma" in evols:
        evols = "1: Yanma\n2: Yanmega Learn Ancient Power"
    if "Farfetch’ d" in evols:
        evols = "1: Farfetch'd"
    if "Poliwrath" in evols:
        evols = "1: Poliwag\n2: Poliwhirl Minimum 25\n3: Poliwrath Water Stone Minimum 30 3 - Politoed Holding King's Rock Minimum 30"
    evolList = []
    evolDict = {"STAGE" : "", "NAME" : "", "LEVEL" : "", "MISC" : ""}
    if "-" in evols and "-Z" not in evols and "-oh" not in evols:
        #import pdb; pdb.set_trace()
        evols = formatMultipleEvols(evols)
    
    for line in evols.splitlines():
        betterLine = removeAllNonsense(line) #  \n 2: Abomasnow Minimum 30 \n --> 2: Abomasnow Minimum 30
        if not betterLine[0].isdigit():
            break
        if betterLine[1] != ".":
            evolDict["STAGE"] = betterLine[0]
            betterLine = betterLine[3:]
        else:   
            evolDict["STAGE"] = betterLine[0:4]
            betterLine = betterLine[6:]
        pokemonsInside = pokemonInside(betterLine, pokemonNames)
        if len(pokemonsInside) == 0:
            import pdb; pdb.set_trace()
        pokI, pokL = getClosest(betterLine.lower(), pokemonsInside) #GOTTA FINISH
        pokemon = betterLine[pokI:pokI + pokL]
        if pokemon.lower() in betterLine.lower():
            evolDict["NAME"] = pokemon
            nameInd = betterLine.lower().index(pokemon.lower())
            betterLine = betterLine[nameInd + len(pokemon) + 1:]
        if "Minimum" not in betterLine:
            evolDict["LEVEL"] = 0
            evolDict["MISC"] = {}
            evolList.append(evolDict.copy())
        else:
            minimumLoc = betterLine.index("Minimum")
            evolDict["LEVEL"] = findDigits(betterLine[minimumLoc + len("Minimum "):])
            betterLine = removeCharacter(betterLine, "Minimum: " + evolDict["LEVEL"]) # Minimum 30 --> /0
            betterLine = removeCharacter(betterLine, "Minimum " + evolDict["LEVEL"]) # Minimum 30 --> /0
            if len(removeAllNonsense(betterLine)) == 0:
                evolDict["MISC"] = {}
                evolList.append(evolDict.copy())
            else:
                evolDict["MISC"] = handleMisc(betterLine)
                evolList.append(evolDict.copy())
    return evolList
#CTYSize -- dictionary
def CTYSize(sizes : str):
    sizeDict = {"HEIGHT" : "", "WEIGHT" : ""}
    for line in sizes.splitlines():
        if "Height:" in line:
            sizeDict["HEIGHT"] = line[8:]
        else:
            sizeDict["WEIGHT"] = line[8:]
    return sizeDict
#CTYBreedingInformation -- dictionary of lists
def CTYBreedInfo(breedInf : str):
    breedDict = {}
    for ind, line in enumerate(breedInf.splitlines()):
        if ind == 0: #Gender Ratio
            potential = removeAllNonsense(line[len("Gender Ratio: "):])
            if potential == "-1":
                potential = "No Gender"
            elif "No Gender" in potential:
                potential = "No Gender"
            elif "Genderless" in potential:
                potential = "No Gender"
            breedDict["MALE RATIO"] = potential
            pass
        elif ind == 1: #Egg Group
            breedDict["EGG GROUP"] = processCommaList(removeAllNonsense(line[len("Egg Group: "):]))
            pass
        elif ind == 2: #Average Hatch Rate
            breedDict["HATCH RATE"] = removeAllNonsense(line[len("Average Hatch Rate: "):])
            pass
    return breedDict
#Diet -- List
def CTYDiet(diets : str):
    diet = []
    for line in diets.splitlines():
        diet.append(removeAllNonsense(line))
    return diet
#Habitat -- List
def CTYHabit(habits : str):
    habitats = []
    for line in habits.splitlines():
        habitats.append(removeAllNonsense(line))
    return habitats
#CTYCAPABILITIES -------
def handleException(text : str, exception : str):
    text = removeAllNonsense(text)
    diction = {}
    tDict = {}
    if exception == "Jump": 
        text = text[len("Jump") + 1:]
        diction["ABILITY"] = "Jump"
        tDict["LONG JUMP"] = text[0]
        if len(text) > 2:
            tDict["HIGH JUMP"] = text[2]
        diction["VALUE"] = tDict.copy()
    elif exception == "Naturewalk" or exception == "Na-turewalk":
        text = text[len("Naturewalk") + 1:]
        text = removeCharacter(text, "(")
        text = removeCharacter(text, ")")
        natureList = processCommaList(text)
        diction["ABILITY"] = "Naturewalk"
        diction["VALUE"] = natureList.copy()
    return diction.copy()

def hasDigit(text : str):
    for character in text:
        if character.isdigit():
            return True
    return False

#Capabilities -- Dictionary
def CTYCapabilities(capabilities : str):
    exceptions = ["Jump", "Naturewalk", "Na-turewalk"]
    capList = []
    tempDict = {}
    for line in capabilities.splitlines():
        tempDict = {}
        isException = False
        for exception in exceptions:
            if exception in line:
                tempDict = handleException(line, exception).copy()
                isException = True
        if hasDigit(line) and not isException:
            #deal with the digit
            tempLine = removeAllNonsense(line)
            tempDict["ABILITY"] = tempLine[0:-2]
            tempDict["VALUE"] = tempLine[-1]
        elif not isException:
            #remove nonsense and stick in the list
            tempDict["ABILITY"] = removeAllNonsense(line)
        if len(line) != "":
            capList.append(tempDict.copy())
    return capList.copy()
#CTYSKILLS ----
def getSkill(text : str):
    for ind, char in enumerate(text):
        if not char.isalpha():
            return text[:ind]
def getDice(text : str):
    for ind, char in enumerate(text):
        if not char.isalnum():
            return text[:ind]
    if len(text) == 3:
        return text
#Skills -- Dictionary
def CTYSkills(skillBlock : str):
     skills = []
     skillDict = {}
     if " - " in skillBlock:
         skillBlock = skillBlock[:skillBlock.index(" - ")] + skillBlock[skillBlock.index(" - ") + 3:]
     if "-\n" in skillBlock:
         skillBlock = skillBlock[:skillBlock.index("-\n")] + skillBlock[skillBlock.index("-\n") + 2:]
     if "Per cep" in skillBlock:
         skillBlock = skillBlock[:skillBlock.index("Per cep") + 3] + skillBlock[skillBlock.index("cep"):]
     #import pdb; pdb.set_trace()
     skillBlock = removeAllNonsense(skillBlock)
     while len(skillBlock) > 3:
         skillDict = {}
         plus = False
         skillName = getSkill(skillBlock)
         skillBlock = skillBlock[len(skillName) + 1:]
         dice = getDice(skillBlock)
         #import pdb; pdb.set_trace()
         if len(dice) + 1 >= len(skillBlock):
             skillDict["SKILL NAME"] = skillName
             skillDict["DICE"] = dice
             skills.append(skillDict.copy())
             return skills
         if skillBlock[len(dice)] == "+":
             plus = True
         skillBlock = skillBlock[len(dice) + 1:]
         if plus:
            mod = skillBlock[0]
            if len(mod) + 1 >= len(skillBlock):
                skillDict["SKILL NAME"] = skillName
                skillDict["DICE"] = dice
                skillDict["MOD"] = mod
                skills.append(skillDict.copy())
                return skills.copy()
            skillBlock = skillBlock[len(mod):]
            skillBlock = removeAllNonsense(skillBlock)
            plus = False
            skillDict["SKILL NAME"] = skillName
            skillDict["DICE"] = dice
            skillDict["MOD"] = mod
            skills.append(skillDict.copy())
         else:
            skillDict["SKILL NAME"] = skillName
            skillDict["DICE"] = dice
            skills.append(skillDict.copy())
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
    pokemons = []
    with open("pokedexCLEANEDCSV.csv", encoding="UTF-8") as csv_file:
        cleanedPokedex = csv.DictReader(csv_file)
        for pokemon in cleanedPokedex:
            pokeEntry["NAME"] = CTYNames(pokemon['Species Name'])
            names.append(pokeEntry["NAME"])
            pokemons.append(pokemon)
        for pokemon in pokemons:
            pokeEntry["STATS"] = CTYStats(pokemon['Stats'])
            pokeEntry["BASIC_INFO"] = CTYBasicInfo(pokemon['Basic Information'])
            pokeEntry["EVOLUTIONS"] = CTYEvol(names, pokemon['Evolutions'])
            pokeEntry["SIZE"] = CTYSize(pokemon['Size'])
            pokeEntry["BREED_INFO"] = CTYBreedInfo(pokemon['Breeding Information'])
            pokeEntry["DIET"] = CTYDiet(pokemon['Diet'])
            pokeEntry["HABITAT"] = CTYHabit(pokemon['Habitat'])
            pokeEntry["CAPABILITIES"] = CTYCapabilities(pokemon['Capabilities'])
            pokeEntry["SKILLS"] = CTYSkills(pokemon['Skills'])
            print(pokeEntry["SKILLS"])
if __name__ == "__main__":
    main()


