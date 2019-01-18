import subprocess
import os
import sys
from glob import glob
import re
import unidecode
import codecs

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
        if " " in fileName:
            fileList = fileName.split(" ")
        elif "_" in fileName:
            fileList = fileName.split("_")
        elif "-" in fileName:
            fileList = fileName.split("-")
        else:
            fileList = fileName.split(".")
        txtName = fileName.replace(".pdf",".txt")
        os.system(("pdftotext '%s'") %(path+"/"+fileName))
        titleFound = False
        auteurToBeFound = False
        auteurFound = False
        abstract=False
        introduction = False
        introductionFound = False
        corps = False
        discussion = False
        conclusion = False
        ref = False
        inutile = False
        titleLine = ""
        auteurLine = ""
        abstractText=""
        introductionText = ""
        corpsText = ""
        conclusionText = ""
        discussionText = ""
        refText =""
        with codecs.open(path+"/"+txtName,"r", encoding='utf8') as fichier:
            for line in fichier:
                line = line.replace("\n","")
                if auteurFound == False and any(auteur.lower() in unidecode.unidecode(line).lower() for auteur in fileList):
                    titleFound = True
                    auteurToBeFound = True
                if titleFound == False:
                    titleLine = titleLine + line + " "
                if titleFound == True and abstract == False and introductionFound == False and introduction == False and ("abstract" in line.lower() or "In this article" in line or "This article" in line):
                    auteurFound = True
                    auteurToBeFound = False
                    abstract=True
                if auteurToBeFound == True:
                    auteurLine = auteurLine + line +" "
                if introductionFound == False and abstract == True and (len(line) <= 1 or "1 " in line or "I " in line or "1'\n'" in line or "I'\n'" in line or "Keywords" in line or "keywords" in line or "1. " in line or "I. " in line):
                    abstract = False
                if abstract == True:
                    abstractText += line + " "
                if abstract == True and "1 " in line or "introduction" in line.lower() or "1'\n'" in line or "I'\n'" in line or "I. " in line:
                    introduction = True
                    abstract = False
                if introduction == True and introductionFound == False:
                    introductionText += line + " "
                if introduction == True and corps == False and (discussion == False and conclusion == False and ref == False) and ("2'\n'" in line or "2. " in line or "II. " in line or "2 The" in line or "II.'\n'" in line or "II'\n'" in line or line=="2" or line=="2." or line=="II" or line=="II."):
                    introductionFound = True
                    corps = True
                if corps == True and introductionFound == True:
                    corpsText += line + " "
                if corps == True and ("Discussion" in line or "DISCUSSION" in line):
                    corps = False
                    discussion = True
                if ("Conclusion" in line or "CONCLUSION" in line or "ONCLUSION" in line) and (corps == True or discussion == True):
                    corps = False
                    discussion = False
                    conclusion = True
                if (conclusion == True or discussion == True) and ("Acknowledgements" in line or "ACKNOWLEDGEMENTS" in line or "Follow-Up Work" in line):
                    inutile = True
                    conclusion = False
                    discussion = False
                if (conclusion == True or discussion == True or inutile == True) and ("References" in line or "REFERENCES" in line):
                    conclusion = False
                    discussion = False
                    inutile = False
                    ref = True
                if conclusion == True:
                    conclusionText += line + " "
                if discussion == True:
                    discussionText += line + " "
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
            f = codecs.open("resumes/resume_"+name.replace(".pdf","")+".txt","w", encoding='utf8')
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
            f = codecs.open("resumes/resume_"+name.replace(".pdf","")+".xml","w", encoding='utf8')
            f.write("<article>\n")
            f.write("\t<preamble>"+name+"</preamble>\n")
            f.write("\t<titre>"+titleLine+"</titre>\n")
            f.write("\t<auteur>\n\t\t"+auteurLine+"\n\t</auteur>\n")
            abReplace = re.compile(re.escape('abstract'), re.IGNORECASE)
            abstractText = abReplace.sub("",abstractText,1)
            f.write("\t<abstract>\n\t\t"+abstractText+"\n\t</abstract>\n")
            inReplace = re.compile(re.escape('introduction'), re.IGNORECASE)
            introductionText = inReplace.sub("",introductionText,1)
            f.write("\t<introduction>\n\t\t"+introductionText+"\n\t</introduction>\n")
            f.write("\t<corps>\n\t\t"+corpsText+"\n\t</corps>\n")
            disReplace = re.compile(re.escape('discussion'), re.IGNORECASE)
            discussionText = disReplace.sub("",discussionText,1)
            f.write("\t<discussion>\n\t\t"+discussionText+"\n\t</discussion>\n")
            conReplace = re.compile(re.escape('conclusion'), re.IGNORECASE)
            conclusionText = conReplace.sub("",conclusionText,1)
            f.write("\t<conclusion>\n\t\t"+conclusionText+"\n\t</conclusion>\n")
            refReplace = re.compile(re.escape('references'), re.IGNORECASE)
            refText = refReplace.sub("",refText)
            f.write("\t<biblio>\n\t\t"+refText+"\n\t</biblio>\n")
            f.write("</article>")
        else:
            f = codecs.open("resumes/resume_"+name.replace(".pdf","")+".xml","w", encoding='utf8')
            f.write("<article>\n")
            f.write("\t<preamble>"+name+"</preamble>\n")
            f.write("\t<titre>"+titleLine+"</title>\n")
            f.write("\t<auteur>\n\t\t"+auteurLine+"\n\t</auteur>\n")
            abReplace = re.compile(re.escape('abstract'), re.IGNORECASE)
            abstractText = abReplace.sub("",abstractText,1)
            f.write("\t<abstract>\n\t\t"+abstractText+"\n\t</abstract>\n")
            refReplace = re.compile(re.escape('references'), re.IGNORECASE)
            refText = refReplace.sub("",refText)
            f.write("\t<biblio>\n\t\t"+refText+"\n\t</biblio>\n")
            f.write("</article>")

    for file in glob('./'+path+'/*.txt'):
        os.remove(file)
else:
    print("Argument Invalide")