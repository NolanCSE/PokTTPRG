import PyPDF2
import csv
from enum import Enum

def getBody(pageBody : str, endStat : str):
    if endStat != "Misc":
        stat = pageBody[0:pageBody.index(endStat)]
        pageBody = pageBody[len(stat) + len(endStat):]
    elif "Mega Evolution" in pageBody:
        stat = pageBody[0:pageBody.index("Mega Evolution")]
        pageBody = pageBody[len(stat) + len("Mega Evolution")]
    else:
        stat = pageBody[0:]
    return pageBody, stat

def parseEntry(pageBody : str):
    result = []
    header = ["Species Name", "Base Stats", "Basic Information", "Evolution", "Size Information", "Breeding Information", "Diet", "Habitat", "Capability List", "Skill List", "Move List", "Misc"]

    i = 1
    while i < len(header):
        pageBody, stat = getBody(pageBody, header[i])
        result.append(stat)
        i += 1
    print(result[0])
    return result
    pass

#storing names
PDF_NAME = "pokedex.pdf"
CSV_NAME = "pokedexCSV.csv"

#setting csv header
header = ["Species Name", "Base Stats", "Basic Information", "Evolution", "Size Information", "Breeding Information", "Diet", "Habitat", "Capability List", "Skill List", "Move List", "Misc"]

#opening pdfFile
pdfFile = open(PDF_NAME, 'rb')
pdfReader = PyPDF2.PdfReader(pdfFile)

flag = False

with open(CSV_NAME, "w", encoding="UTF-8", newline="") as f:
    #opening csv file and writing
    writer = csv.writer(f)
    writer.writerow(header)

    pageText = []
    for page in pdfReader.pages:
        #if this is the 12th page (index 11), parse the page
        if page is pdfReader.pages[11]:
            flag = True
        if flag == True:
            current_error = 681
            if page is pdfReader.pages[745]:
                break
            elif page is pdfReader.pages[681]:
                #legendary info page; not a pokemon
                pass
            elif page is pdfReader.pages[607]:
               #appliance rotoms; need to input these manually
               pass 
            elif page is pdfReader.pages[162]:
                string = page.extract_text()
                writer.writerow(parseEntry(string[:string.index("Ignition Boost") + len("Ignition Boost")] + "\nEvolution:" + string[string.index("Ignition Boost") + len("Ignition Boost"):]))
            elif page is pdfReader.pages[120]:
                string = page.extract_text()
                writer.writerow(parseEntry(string[:string.index("Biology") - 1] + "Diet : " + string[string.index("Biology : ") + len("Biology : "):]))
            elif page is pdfReader.pages[50]:
                string = page.extract_text()
                writer.writerow(parseEntry(string[:string.index("Courage") + len("Courage")] + "\nEvolution:" + string[string.index("Courage") + len("Courage"):]))
            else:
                writer.writerow(parseEntry(page.extract_text()))

print("TASK COMPLETE")
