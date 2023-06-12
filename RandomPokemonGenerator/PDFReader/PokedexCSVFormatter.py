import csv
CSV_NAME = "pokedexCSV.csv"

def getFrontDigits(name : str):
    count = 0
    for character in name:
        if character.isdigit():
            count = count + 1
        else:
            return count
def eliminateNewlines(name : str):
    while "\n" in name:
        if name.index("\n") != len(name) - 1 and name.index("\n") != 0:
            name = name[:name.index("\n")] + " " + name[name.index("\n") + 1:]
        elif name.index("\n") == 0:
            name = name[1:]
        else:
            name = name[:name.index("\n")]
    return name
def eliminateSpacesAndNewlines(name : str):
    while " " in name:
        if name.index(" ") == len(name) - 1:
            name = name[:name.index(" ")]
        else:
            name = name[:name.index(" ")] + name[name.index(" ") + 1:]
    while "\n" in name:
        name = name[:name.index("\n")]
    if "Forme" in name:
        name = name[:name.index("Forme")] + "Form"
    return name
def b_nothing(string :str):
    nothings = ["\t","\n"," "]
    for character in string:
        if character not in nothings:
            return False
    return True
def getStatBlock(statBlock : str):
    statBlockF = ""
    while "\n" in statBlock:
        #import pdb; pdb.set_trace()
        statBlockF = statBlockF + statBlock[statBlock.index("\n") + 3:statBlock.index("\n",statBlock.index("\n") + 2)] + "\n"
        statBlock = statBlock[statBlock.index("\n",statBlock.index("\n")+2):]
        if b_nothing(statBlock):
            return statBlockF
    return statBlockF

def parseInfoBlock(infoBlock : str, typeSpace=False, typeSynSpace=False):
    infoBlockF = ""
    #Types
    if "/" in infoBlock:
        if not typeSpace:
            infoBlockF = infoBlockF + "[" + "T: " + infoBlock[infoBlock.index("Type : ") + len("Type : "):infoBlock.index(" /")]
            infoBlockF = infoBlockF + ", " + infoBlock[infoBlock.index("/") + 2:infoBlock.index(" ", infoBlock.index("/") + 2)] + "]\n"
        else:
            infoBlockF = infoBlockF + "[" + "T: " + infoBlock[infoBlock.index("Type : ") + len("Type : "):infoBlock.index("/")]
            infoBlockF = infoBlockF + ", " + infoBlock[infoBlock.index("/") + 1:infoBlock.index(" ", infoBlock.index("/") + 1)] + "]\n"
    else:
        if not typeSynSpace:
            infoBlockF = infoBlockF + "[" + "T: " + infoBlock[infoBlock.index("Type : ") + len("Type : "):infoBlock.index(" ", infoBlock.index("Type : ") + len("Type : "))] + "]\n"
        else:
            infoBlockF = infoBlockF + "[" + "T: " + infoBlock[infoBlock.index("Type: ") + len("Type: "):infoBlock.index(" ", infoBlock.index("Type: ") + len("Type: "))] + "]\n"
    #Basic Abilities
    infoBlockF = infoBlockF + "[" + "BA: "
    i = 1
    while "Basic Ability " + str(i) in infoBlock:
        if i > 1:
            infoBlockF = infoBlockF + ", "
        bALoc = infoBlock.index("Basic Ability " + str(i))
        bAlen = len("Basic Ability " + str(i) + ": ")
        if "Basic" in infoBlock[infoBlock.index(" ", bALoc + bAlen) + 1:infoBlock.index(" ", bALoc + bAlen) + 9] or "Adv" in infoBlock[infoBlock.index(" ", bALoc + bAlen) + 1:infoBlock.index(" ", bALoc + bAlen) + 9]:
            infoBlockF = infoBlockF + infoBlock[bALoc + bAlen:infoBlock.index(" ", bALoc + bAlen)]
        else:
            extraLength = len(infoBlock[bALoc+bAlen:infoBlock.index(" ", bALoc + bAlen)]) + 1
            infoBlockF = infoBlockF + infoBlock[bALoc + bAlen:infoBlock.index(" ", bALoc + bAlen + extraLength)]
        i += 1
    infoBlockF = infoBlockF + "]\n"
    #Advanced Abilities
    infoBlockF = infoBlockF + "[" + "AA: "
    i = 1
    while "Adv Ability " + str(i) in infoBlock:
        if i > 1:
            infoBlockF = infoBlockF + ", "
        bALoc = infoBlock.index("Adv Ability " + str(i))
        bAlen = len("Adv Ability " + str(i) + ": ")
        if "Adv" in infoBlock[infoBlock.index(" ", bALoc + bAlen) + 1:infoBlock.index(" ", bALoc + bAlen) + 5] or "High" in infoBlock[infoBlock.index(" ", bALoc + bAlen) + 1:infoBlock.index(" ", bALoc + bAlen) + 5]:
            infoBlockF = infoBlockF + infoBlock[bALoc + bAlen:infoBlock.index(" ", bALoc + bAlen)]
        else:
            extraLength = len(infoBlock[bALoc+bAlen:infoBlock.index(" ", bALoc + bAlen)]) + 1
            infoBlockF = infoBlockF + infoBlock[bALoc + bAlen:infoBlock.index(" ", bALoc + bAlen + extraLength)]
        i += 1
    infoBlockF = infoBlockF + "]\n"
    #High Abilities
    infoBlockF = infoBlockF + "[" + "HA: "
    if "High Ability" in infoBlock:
        HALoc = infoBlock.index("High Ability: ")
        HALen = len("High Ability: ")
        if "\n" in infoBlock[HALoc + HALen:]:
            infoBlockF = infoBlockF + infoBlock[HALoc + HALen:infoBlock.index("\n")]
        else:
            infoBlockF = infoBlockF + infoBlock[HALoc + HALen:]
    infoBlockF = infoBlockF + "]"
    return infoBlockF

def findNextNonColonSpace(index, string):
    currentCharInd = index
    if len(string) == 0:
        return -1
    while string[currentCharInd] == " " or string[currentCharInd] == ":":
        currentCharInd += 1
        if currentCharInd == len(string):
            return currentCharInd
    return currentCharInd
def getWordBeforeSeparator(totalWord, startIndex, separator):
    return totalWord[startIndex:totalWord.index(separator, startIndex)]
def removeCharacter(word, removeChar):
    if removeChar not in word:
        return word
    if word[0] == removeChar:
        return word[1:]
    elif word[len(word) - 1] == removeChar:
        return word[:len(word)-1]
    return word[:word[word.index(removeChar)]] + word[word.index(removeChar) + 1:]
def removeAllCharacters(word, removeChar):
    while removeChar in word:
        word = removeCharacter(word, removeChar)
    return word
def eliminateEndSpaces(word):
    if len(word) == 0:
        return word
    while word[-1] == " " or word[-1] == "\n":
        word = word[:-1]
        if len(word) == 0:
            return word
    return word
#data cleaners
def cleanNames(names : list):
    i = 0
    while i < len(names):
        frDigits = getFrontDigits(names[i])
        names[i] = eliminateSpacesAndNewlines((names[i])[frDigits:])
        i += 1
    return names
def cleanStats(stats : list):
    for index, stat in enumerate(stats):
        if index == 546 or index == 547:
            stats[index] = "MANUAL ENTRY"
        else:
            stats[index] = getStatBlock(stat)
    return stats
def cleanInfo(info : list):
    count = 0
    typeSpace = False
    typeSynSpace = False
    for index, infoBlock in enumerate(info):
        count += 1
        if count == 712:
            infoBlock = "Type : Psychic Basic Ability 1: Conqueror  Adv Ability 1: Download  Adv Ability 2: Telepathy  High Ability: Transporter"
        elif count == 711:
            infoBlock = "Type : Psychic Basic Ability 1: Pressure  Adv Ability 1: Download  Adv Ability 2: Telepathy  High Ability: Transporter"
        elif count == 681:
            infoBlock = "Type : Ice  Basic Ability 1: Clear Body  Adv Ability 1: Ice Body  Adv Ability 2: Battle Armor  High Ability: Adaptability"
        elif count==680:
            infoBlock = "Type : Rock Basic Ability 1: Clear Body  Adv Ability 1: Sturdy  Adv Ability 2: Battle Armor  High Ability: Adaptability"
        elif count==410:
            typeSynSpace = True
        elif count == 365:
            typeSpace = True
        info[index] = parseInfoBlock(eliminateNewlines(infoBlock), typeSpace, typeSynSpace)
        typeSynSpace = False
        typeSpace = False
    return info
def cleanEvol(evol : list):
    evolBlock = ""
    for index, evolution in enumerate(evol):
        evolution = eliminateNewlines(evolution)
        i = 1
        while str(i) + " - " in evolution:
            begin = evolution.index(str(i) + " - ") + len(str(i) + " - ")
            end = len(evolution)
            if str(i + 1) + " - " in evolution:
                end = evolution.index(str(i + 1) + " - ")
            evolBlock = evolBlock + str(i) + ": " + evolution[begin:end] + "\n"
            i += 1
        evol[index] = evolBlock
        evolBlock = ""
    return evol
def cleanSize(sizes : list):
    sizeBlock = ""
    for index, size in enumerate(sizes):
        heightLoc = size.index("Height")
        heightLen = len("Height : ")
        weightLoc = size.index("Weight")
        weightLen = len("Weight : ")

        sizeBlock += "Height: " + size[heightLoc + heightLen:size.index(" / ")] + "\n"
        sizeBlock += "Weight: " + size[weightLoc + weightLen:size.index(" / ", weightLoc + weightLen)]
        sizes[index] = sizeBlock
        sizeBlock = ""
    return sizes
def cleanBreed(breeds : list):
    breedBlock = ""
    for index, breed in enumerate(breeds):
        genderRatioLoc = breed.index("Gender Ratio")
        gRLen = len("Gender Ratio")
        maleLoc = findNextNonColonSpace(genderRatioLoc + gRLen, breed)
        eggRatioLoc = breed.index("Egg Group")
        eggRLen = len("Egg Group")
        eggLoc = findNextNonColonSpace(eggRatioLoc + eggRLen, breed)
        if "Average Hatch Rate" in breed:
            ahrLoc = breed.index("Average Hatch Rate")
            ahrLen = len("Average Hatch Rate")
            ahrTrueLoc = findNextNonColonSpace(ahrLoc + ahrLen, breed)
        if "M" not in breed:
            breedBlock += "Gender Ratio: -1\n"
        else:
            breedBlock += "Gender Ratio: " + breed[maleLoc:breed.index(" M")] + "\n"
        
        if "/" in breed[eggLoc:]:
            if " / " in breed[eggLoc:]:
                word = getWordBeforeSeparator(breed, eggLoc, " / ")
                fullLen = breed.index(word) + len(word) + len(" / ") 
                wordAfter = breed[fullLen:breed.index(" ", fullLen)]
            elif "/ " in breed[eggLoc:]:
                word = getWordBeforeSeparator(breed, eggLoc, "/ ")
                fullLen = breed.index(word) + len(word) + len("/ ") 
                wordAfter = breed[fullLen:breed.index(" ", fullLen)]
            elif " /" in breed[eggLoc:]:
                word = getWordBeforeSeparator(breed, eggLoc, " /")
                fullLen = breed.index(word) + len(word) + len(" /") 
                wordAfter = breed[fullLen:breed.index(" ", fullLen)]
            else:
                word = getWordBeforeSeparator(breed, eggLoc, "/")
                fullLen = breed.index(word) + len(word) + len("/") 
                wordAfter = breed[fullLen:breed.index(" ", fullLen)]
            breedBlock += "Egg Group: " + word + ", " + wordAfter + "\n"
        else:
            word = getWordBeforeSeparator(breed, eggLoc, " ")
            breedBlock += "Egg Group: " + word + "\n"

        if "Average Hatch Rate" in breed:
            ahrStat = breed[ahrTrueLoc:]
            breedBlock += "Average Hatch Rate: " + ahrStat + "\n"
        breeds[index] = breedBlock
        breedBlock = ""
    return breeds
def cleanDiet(diet : list):
    dietBlock = ""
    for index, dietIns in enumerate(diet):
        if "," in dietIns:
            threeWords = False
            start = findNextNonColonSpace(0, dietIns)
            firstWord = getWordBeforeSeparator(dietIns, start, ",")
            if "," in dietIns[dietIns.index(firstWord) + len(firstWord + ","):]:
                nextWord = getWordBeforeSeparator(dietIns, dietIns.index(firstWord) + len(firstWord + ", "), ",")
                threeWords = True
            if threeWords:
                if "\n" not in dietIns:
                    lastWord = getWordBeforeSeparator(dietIns, dietIns.index(nextWord) + len(nextWord + ", "), "\n")
                else:
                    lastWord = getWordBeforeSeparator(dietIns, dietIns.index(nextWord) + len(nextWord + ", "), " ")
                threeWords = False
                dietBlock = firstWord + "\n" + nextWord + "\n" + lastWord
            else:
                if "\n" not in dietIns:
                    lastWord = getWordBeforeSeparator(dietIns, dietIns.index(firstWord) + len(firstWord + ", "), " ")
                else:
                    #import pdb; pdb.set_trace()
                    lastWord = getWordBeforeSeparator(dietIns, dietIns.index(firstWord) + len(firstWord + ", "), "\n")
                dietBlock = firstWord + "\n" + lastWord
            diet[index] = dietBlock
            dietBlock = ""
        else:
            if "\n" not in dietIns:
                diet[index] = getWordBeforeSeparator(dietIns, findNextNonColonSpace(0, dietIns), " ")
            else:
                diet[index] = getWordBeforeSeparator(dietIns, findNextNonColonSpace(0, dietIns), "\n")
    return diet
def cleanHabit(habit : list):
    habitBlock = ""
    #import pdb; pdb.set_trace()
    for index, habitIns in enumerate(habit):
        unfinishedDiet = habitIns
        while "," in unfinishedDiet:
            word = getWordBeforeSeparator(unfinishedDiet, findNextNonColonSpace(0, unfinishedDiet), ",")
            unfinishedDiet = unfinishedDiet[unfinishedDiet.index(word) + len(word + ", "):]
            habitBlock += word + "\n"
        habitBlock += eliminateSpacesAndNewlines(unfinishedDiet)
        habit[index] = removeAllCharacters(habitBlock, ":")
        habitBlock = ""
    return habit
def cleanCap(capabilities : list):
    for index, capability in enumerate(capabilities):
        #import pdb; pdb.set_trace()
        capBlock = ""
        un_cap = capability
        while "," in un_cap:
            if "(" in un_cap:
                if un_cap.index("(") < un_cap.index(","):
                    word = getWordBeforeSeparator(un_cap, findNextNonColonSpace(0, un_cap), ")") + ")"
                else:
                    word = getWordBeforeSeparator(un_cap, findNextNonColonSpace(0, un_cap), ",")
            else:
                word = getWordBeforeSeparator(un_cap, findNextNonColonSpace(0, un_cap), ",")
            un_cap = un_cap[un_cap.index(word) + len(word + ", "):]
            capBlock += word + "\n"
        if not findNextNonColonSpace(0, un_cap) == -1:
            capBlock += eliminateEndSpaces(un_cap[findNextNonColonSpace(0, un_cap):])
        capabilities[index] = capBlock
    return capabilities
def cleanSkill(skills : list):
    for index, skill in enumerate(skills):
        #import pdb; pdb.set_trace()
        skillBlock = ""
        un_skill = skill
        while "," in un_skill:
            if "(" in un_skill:
                if un_skill.index("(") < un_skill.index(","):
                    word = getWordBeforeSeparator(un_skill, findNextNonColonSpace(0, un_skill), ")") + ")"
                else:
                    word = getWordBeforeSeparator(un_skill, findNextNonColonSpace(0, un_skill), ",")
            else:
                word = getWordBeforeSeparator(un_skill, findNextNonColonSpace(0, un_skill), ",")
            un_skill = un_skill[un_skill.index(word) + len(word + ", "):]
            skillBlock += word + "\n"
        if not findNextNonColonSpace(0, un_skill) == -1:
            skillBlock += eliminateEndSpaces(un_skill[findNextNonColonSpace(0, un_skill):])
        skills[index] = skillBlock
    return skills
def cleanMoves(moves : list):
    pass

d_names = []
d_stats = []
d_info = []
d_evol = []
d_size = []
d_breed = []
d_diet = []
d_habit = []
d_cap = []
d_skill = []
d_move = []

with open(CSV_NAME, encoding='utf8') as pd_file:
    pokedex = csv.DictReader(pd_file)
    for pokemon in pokedex:
        d_names.append(pokemon["Species Name"])
        d_stats.append(pokemon["Base Stats"])
        d_info.append(pokemon["Basic Information"])
        d_evol.append(pokemon["Evolution"])
        d_size.append(pokemon["Size Information"])
        d_breed.append(pokemon["Breeding Information"])
        d_diet.append(pokemon["Diet"])
        d_habit.append(pokemon["Habitat"])
        d_cap.append(pokemon["Capability List"])
        d_skill.append(pokemon["Skill List"])
        d_move.append(pokemon["Move List"])
c_names = cleanNames(d_names)
c_stats = cleanStats(d_stats)
c_info = cleanInfo(d_info)
c_evol = cleanEvol(d_evol)
c_size = cleanSize(d_size)
c_breed = cleanBreed(d_breed)
c_diet = cleanDiet(d_diet)
c_habit = cleanHabit(d_habit)
c_cap = cleanCap(d_cap)
c_skill = cleanSkill(d_skill)
c_move = cleanMoves(d_move)
