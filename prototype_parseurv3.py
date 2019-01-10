import subprocess
import os
import sys
from glob import glob
import re

if sys.argv[2] == "-x" or sys.argv[2] == "-t" or sys.argv[2] == "-xp":
    if (os.path.isdir("./resumes")):
        os.system(("rm -R '%s'") %("./resumes"))

    command="mkdir resumes"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    path = sys.argv[1]

    parse = [];
    for fileName in os.listdir(path):
        print("Voulez vous parser "+fileName+" ? (o/n)");
        choice = raw_input("Entrez votre choix:");
        if choice == "o":
            parse.append(fileName);


    for fileName in parse:
            name = fileName
            txtName = fileName.replace(".pdf",".txt")
            protoTitle = fileName.replace(".pdf","")
            title = protoTitle.split('_')
            auteur = title[0]
            title = title[2]
            os.system(("pdftotext '%s'") %(path+"/"+fileName))
            titleNext = False
            abstract=False
            abstractText=""
            found = False
            titleFound = False
            auteurToBeFound = False
            auteurFound = False
            titleLine = ""
            auteurLine = ""
            introduction = False
            introductionFound = False
            introductionText = ""
            corps = False
            corpsText = ""
            conclusionText = ""
            discussion = False
            discussionText = ""
            refText =""
            ref = False
            conclusion = False
            with open(path+"/"+txtName,"r") as fichier:
                for line in fichier:
                    line = line.replace("\n","")
                    if titleFound == False and (title.lower() in line.lower() or line.lower() in title.lower()):
                        titleNext = True
                    if auteurFound == False and auteur in line:
                        titleFound = True
                        titleNext = False
                        auteurToBeFound = True
                    if titleNext == True:
                        titleLine = titleLine + line + " "
                    if found == False and "abstract" in line.lower():
                        auteurFound = True
                        auteurToBeFound = False
                        abstract=True
                        found = True
                    if auteurToBeFound == True:
                        auteurLine = auteurLine + line +" "
                    if abstract == True and (len(line) <= 1 or "1 " in line or "I " in line or "1'\n'" in line or "I'\n'" in line or "Keywords" in line or "keywords" in line or "1." in line or "I." in line):
                        abstract = False
                    if abstract == True:
                        abstractText += line
                    if abstract == True and "1 " in line or "introduction" in line.lower() or "1'\n'" in line or "I'\n'" in line:
                        introduction = True
                    if introduction == True and introductionFound == False:
                        introductionText += line
                    if introduction == True and corps == False and ("2'\n'" in line or ("2." in line and "2. " not in line) or "II.'\n'" in line or "II'\n'" in line or line=="2" or line=="2." or line=="II" or line=="II."):
                        introductionFound = True
                        corps = True
                    if corps == True and introductionFound == True:
                        corpsText += line
                    if "conclusion" in line.lower() and corps == True:
                        corps = False
                        conclusion = True
                    if (conclusion == True or discussion == True) and ("References" in line or "REFERENCES" in line):
                        conclusion = False
                        ref = True
                    if conclusion == True and ("acknowledgement" in line.lower() or "acknowledgments" in line.lower()):
                        conclusion = False
                        discussion = True
                    if conclusion == True and corps == False:
                        conclusionText += line
                    if discussion == True:
                        discussionText += line
                    if ref==True:
                        refText+=line

            auteurLine = auteurLine.replace("\n"," ")
            abstractText = abstractText.replace("\n"," ")
            introductionText = introductionText.replace("\n"," ")
            corpsText = corpsText.replace("\n"," ")
            conclusionText = conclusionText.replace("\n"," ")
            discussionText = discussionText.replace("\n"," ")
            refText = refText.replace("\n"," ")
            if sys.argv[2] == "-t":
                f = open("resumes/resume_"+protoTitle+".txt","w")
                f.write(name+'\n'+'\n')
                f.write(titleLine+'\n'+'\n')    
                f.write(auteurLine+'\n'+'\n')
                abReplace = re.compile(re.escape('abstract'), re.IGNORECASE)
                abstractText = abReplace.sub("Abstract: ",abstractText)
                f.write(abstractText+'\n'+'\n')
                refReplace = re.compile(re.escape('references'), re.IGNORECASE)
                refText = refReplace.sub("References: ",refText)
                f.write(refText+'\n')
            elif sys.argv[2] == "-xp":
                f = open("resumes/resume_"+protoTitle+".xml","w")
                f.write("<article>\n")
                f.write("\t<preamble>"+name+"</preamble>\n")
                f.write("\t<titre>"+titleLine+"</title>\n")
                f.write("\t<auteur>"+auteurLine+"</auteur>\n")
                f.write("\t<abstract>"+abstractText+"</abstract>\n")
                f.write("\t<introduction>"+introductionText+"</introduction>\n")
                f.write("\t<corps>"+corpsText+"</corps>\n")
                f.write("\t<conclusion>"+conclusionText+"</conclusion>\n")
                f.write("\t<discussion>"+discussionText+"</discussion>\n")
                f.write("\t<biblio>"+refText+"</biblio>\n")
                f.write("</article>")
            else:
                f = open("resumes/resume_"+protoTitle+".xml","w")
                f.write("<article>\n")
                f.write("\t<preamble>"+name+"</preamble>\n")
                f.write("\t<titre>"+titleLine+"</title>\n")
                f.write("\t<auteur>"+auteurLine+"</auteur>\n")
                f.write("\t<abstract>"+abstractText+"</abstract>\n")
                f.write("\t<biblio>"+refText+"</biblio>\n")
                f.write("</article>")

    for file in glob('./Papers/*.txt'):
        os.remove(file)
else:
    print("Argument Invalide")