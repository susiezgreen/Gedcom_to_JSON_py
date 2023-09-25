from readgedcom import *
import os
import textwrap
from PIL import ImageFont


#names formatting
namewrap = 10 #max letters before wrapping
placewrap = 15
font = "BKANT.TTF"
#textSize = ImageFont.truetype(font, 12).getsize('Hello world')


#relative sizes of text
nameTextSize = 1
space1Px = 2
placeTextSize = 0.75
space2Px = 2
dateTextSize = 0.75

padding = 6

#Substitutions in place names
placeSubs=((", England",""),
            (", United Kingdom",""),
            (", Northern Ireland","",),
            (", Ireland",""),
            (", Co Down",", Co.Down"),
            (", Co. Down",", Co.Down"),
            (", Down",", Co.Down"),
            (", Ireland",""),
            (", Unknown",""),
            ("Unknown",""),
            ("?",""))


def directAncestorsGenerationDict(root,people):
    generations = {}
    for p in people:
        generations[p]=0
    generations[root]=1
    trunk = tree.get_ancestors(root)
    
    for t in trunk:
        #try:print "\n\n\ntrunk person is: " + t.name()[0]+" "+t.name()[1]+" ancestors: "
        #except:print "exception"
        anc = tree.find_path_to_anc(root,t)
        #for a in anc:
        ##   try:print a.name()[0]+" "+a.name()[1]
        #    except:print "exception"
        if anc != None:
            generations[t]=len(anc)
            #print generations[t]
            #for a in anc:
            #    print a.name()[0]+" "+a.name()[1]
    return generations

def removeKnownGen(dict, removed):
    newremoved = []
    for r in removed:
        #print r.,": ",dict[r]
        if dict[r] == 0:
            newremoved.append(r)
    return newremoved

def allnames(names,yPos,gen):
    surname = names[1]
    forenames = textwrap.wrap(names[0],namewrap)
    allnames = []
    name = ""
    size = 0
    xScale = 0
    yScale = 0
    
    j = 0
    while j < 3:
        try: 

            name = forenames[j]
            size = min(textresize(name,"nametext",gen),8)
            textSize = (ImageFont.truetype(font, int(size)).getsize(name))
            xScale = textSize[0]+padding*2
            yScale = size
            yPos += float(textSize[1])
            
        except: 
            name = ""
            size = 0
            yPos+= 0
            xScale = 0
            yScale = 0

        namearray = [name,size, yPos,xScale,yScale]  
        allnames.append(namearray)
        j+=1
        

    size = min(textresize(surname,"nametext",gen),8)
    textSize = ImageFont.truetype(font, int(size)).getsize(surname)
    xScale = textSize[0]+padding*2
    yScale = size
    yPos += textSize[1]
    allnames.append([surname,size, yPos,xScale,yScale])
    #print surname," ",gen," ",size," ",xScale
    return allnames

def allyears(birthyear,deathyear,yPos,gen):
        allyears = []
        years = ""
        if birthyear != -1:
            years+= str(birthyear)
            if deathyear != -1:
                years += ("-"+str(deathyear)+" ")
        
        if birthyear == -1 and deathyear != -1:        
                years += ("died "+str(deathyear)+" ")
        size = textresize(years,"datetext",gen)
        textSize = ImageFont.truetype(font, int(size)).getsize(years)
        xScale = textSize[0]+padding*2
        yScale = size
        yPos += textSize[1]
        
        allyears=[years,size, yPos, xScale,yScale]
        #for y in allyears:
        #    print y,
        return allyears

def wraptext(text,yPos,gen,wrap):

    places = textwrap.wrap(text,wrap)

    allbirthplaces = []
    name = ""
    size = 0
    yPos += 0
    xScale = 0
    yScale = 0
    
    j = 0
    while j < 4:
        try: 
            name = places[j].strip(",").strip(" ")
            size = min(textresize(name,"placetext",gen),10)
            textSize = ImageFont.truetype(font, int(size)).getsize(name)
            xScale = textSize[0]+padding*2
            yScale = size
            yPos += textSize[1]

        except: 
            name = ""
            size = 0
            yPos+= 0
            xScale = 0
            yScale = 0
            
        namearray = [name,size, yPos,xScale,yScale]  
        allbirthplaces.append(namearray)
        j+=1        
    return allbirthplaces

    
def textresize(text,type,gen):
    if type == "nametext":
        if len(text)==0:
            return 0
        return (6+30/(len(text)+1))*genresize(gen) 
    if type == "placetext":
        if len(text)==0:
            return 0
        return (6+30/(len(text)+1))*genresize(gen)*placeTextSize 
    if type == "datetext":
        if len(text)==0:
            return 0
        return (6+30/(len(text)+1))*genresize(gen)*dateTextSize 
    else: return 10*genresize(gen) 
    
    
    
def genresize(gen):
    return (0.5*(2-((gen+2.0)/30)))
        
family = "d3js"                                               
#treeFile = "C:/Users/susie/Dropbox/code/d3js/python-gedcom-0.1.1dev/trees/GreenSloweyToanAnderson.ged"
#treeFile = "C:/Users/susie/Dropbox/code/d3js/python-gedcom-0.1.1dev/trees/trees/Mossie Family Tree.ged"
#treeFile = "C:/Users/susie/Dropbox/code/d3js/python-gedcom-0.1.1dev/trees/trees/Toan Family Tree.ged"

#treeFile = "C:/Users/susie/OneDrive/familytree/GEDCOM/Mossie Family Tree.ged"
#treeFile = "C:/Users/susie/Dropbox/Web/FamilyTreeDisplay/d3js/d3EarlyToans/Early Toan Tree.ged"
treeFile = "../d3js/d3HollandGTA/Dean and Holland Family Tree.ged"


branchLength = 7
treeName = os.path.basename(treeFile).split(".")[0].replace(" ","_")

print treeName

currentPath = os.path.dirname(__file__)
#outputFile = currentPath + "/"+treeName+".json"
outputFile = "../d3js/d3HollandGTA/"+treeName+".json"
target = open(outputFile, 'w')


target.write("{\n")
target.write("\"Nodes\": [\n")

tree = Gedcom(treeFile)
elements =  Gedcom.element_list(tree)
elementsDict = Gedcom.element_dict(tree)


people = tree.people()
families = []

for count, element in enumerate(elements,1):
    if element.is_family():
        families.append(element)

root = tree.root()
print "\nroot person is: " + root.name()[0]+" "+root.name()[1]+":"

trunk = tree.trunk()
print "TRUNK: "
#for t in trunk:
#        print t.name()[0],t.name()[1],t.birth_year()
#print "               /TRUNK: "

generations = directAncestorsGenerationDict(root,people)
#for u in generations:  
        #try:print u.name()[0]," ",u.name()[1]," ",u.birth_year()," GEN ",generations[u]
        #except:print "                                   exception"
strays = removeKnownGen(generations,people[0:len(people)])

branches = {}
for p in people: branches[p]=0
for t in tree.trunk(): branches[t]=0
for f in families: branches[f]=0

#find the generation of each person in the tree, and remove those with no connections
loop = 1
branch = 0

while loop > 0:
    loop = 0
    branch += 1
    for u in strays:  
        
        parents = tree.get_parents(u)
        minbranch = 50
        #for p in parents:
        #        try:print "          ",p.name()[0]," ",p.name()[1]," ",p.birth_year()," BRA",branches[p]," GEN ",generations[p],",    ",
        #        except:print "                                   exception"
        #print " "
        for p in parents:
            if generations[p] != 0:     
                generations[u] = generations[p]-1
                branches[u]= (min(branches[p],minbranch)+1)
                loop += 1
                #print "; generation",generations[u], " br:", branches[u], " ---- parent: ",p.name()[0]," ",p.name()[1]," ",p.birth_year(),"; gen",generations[p],"; br ", branches[p]    
                minbranch = branches[u]
                break                   
       
    strays =removeKnownGen(generations,strays)
    branch += 1
    for u in strays:
        #print u.name()[0]," ",u.name()[1]," ",u.birth_year()," BRA",branches[u],": ",
        for family in tree.families(u, "FAMS"):
            spouse = tree.get_family_members(family, mem_type="PARENTS")
            for s in spouse:
                if generations[s] != 0 and s != u:
                      generations[u] = generations[s]
                      branches[u]= branch
                      loop += 1
                      #print u.name()[0]," ",u.name()[1],
                      #print "; generation",generations[u], " branch:", branches[u], " ---- spouse: ",s.name()[0]," ",s.name()[1],"; generation",generations[s],"; branches ", branches[s]     
                      break

            
    strays = removeKnownGen(generations,strays)
    branch += 1

    for u in strays:
        for family in tree.families(u, "FAMS"):
            children = tree.get_family_members(family, mem_type="CHIL")
            for c in children:
                if generations[c] != 0:
                    generations[u] = generations[c]+1
                    branches[u]= branches[c]+1
                    loop += 1
                    #print u.name()[0]," ",u.name()[1],
                    #print "; generation",generations[u], " branch:", branches[u], " ---- child: ",c.name()[0]," ",c.name()[1],"; generation",generations[c],"; branches ", branches[c]  
                    break     
    strays = removeKnownGen(generations,strays)
    #print loop
    #print "\nstrays people: ",len(strays)

    

            
            
for s in strays:
    #del generations[s]
    people.remove(s)
    
#for g in generations:
   # print  g.name()[0],g.name()[1],": ",generations[g]


print "len(people) ",len(people)
print "len(strays) ",len(strays)
print len(generations)

b=[0,0,0,0]
total=0
l=0
while l < 4:
    for person in people:
        if branches[person]==l:
            b[l]+=1
            total+=1
    print "People in branch",str(l),": ",b[l],"\ttotal: ",total
    l+=1
    
treeHeight = 0

#people nodes

for person in people:

        if person.pointer()== "@P6@":
            print "p6 is",person.name()
            branches[person]=0

        
        try:
            birth_year = str(person.birth_year())
            if birth_year == "-1":
                birth_year = ""
        except: birth_year = ""
        try: 
            birth_place = str(person.birth()[1])
            if birth_place == "-1":
                birth_place = ""
            for r in placeSubs:
                birth_place = birth_place.replace(r[0],r[1])
        except: birth_place = ""
        try: 
            birth_day = str(person.birth()[0])
            if birth_day == "-1":
                birth_day = ""
        except: birth_day = ""
            
        try: 
            death_year = str(person.death_year())
            if death_year == "-1":
                death_year = ""
        except: death_year = ""        
        try: 
            death_place = str(person.death()[1])
            if death_place == "-1":
                death_place = ""
            for r in placeSubs:
                death_place = death_place.replace(r[0],r[1])
        except:death_place = ""        
        try: 
            death_day = str(person.death()[0])
            if death_day == "-1":
                death_day = ""
        except:death_day = "" 
        try: 
            occupation = str(person.occupation())
            if occupation == "-1":
                occupation = ""
        except:occupation = "" 
        try: 
            customText = str(person.customFact()[0])
            if customText == "-1":
                customText = ""
        except:customText = "" 
        try: 
            customType = str(person.customFact()[1])
            if customType == "-1":
                customType = ""
        except:customType = "" 
        try: 
            customDate = str(person.customFact()[2])
            if customDate == "-1":
                customDate = ""
        except:customDate = "" 
        try: 
            customPlace = str(person.customFact()[3])
            if customPlace == "-1":
                customPlace = ""
        except:customPlace = "" 
        
        maxXScale = 0
        upYHeight = 0
        downYHeight = 0
        
        ###NAMES####        
        target.write("{\n")
        names = person.name()
        
        target.write("\t\"id\": \""+str(person.pointer()).replace("@","")+"\",\n")
        target.write("\t\"name\": \""+person.name()[0]+" "+person.name()[1]+"\",\n")
        
        namestext = allnames(names,-20,generations[person])
        
        yPos = 0
       
        for n in range(4):
            yPos += namestext[n][4]
            target.write("\t\"name"+str(n+1)+"\": \""+namestext[n][0]+"\",\n")
            target.write("\t\"name"+str(n+1)+"size\": "+str(namestext[n][1])+",\n")
            target.write("\t\"name"+str(n+1)+"yPos\": "+ str(yPos) +",\n")
            target.write("\t\"name"+str(n+1)+"yScale\": "+str(namestext[n][4])+",\n")
            maxXScale = max(maxXScale,namestext[n][3])
            
            #target.write("\t\MarkA")
            
            #if len(namestext[n][0])!=0:print "\t\tXScale:",round(namestext[n][3],1),"\tYPos:",str(yPos),"\t\tYScale:",round(namestext[n][4],1)," \t"," \t",str(namestext[n][0])
            
            upYHeight = min(upYHeight, min(namestext[n][1],1) * namestext[n][2])
            downYHeight = max(downYHeight, min(namestext[n][1],1) * namestext[n][2])
            
            
        
        ###YEARS###
        yPos += space1Px
        
        years = allyears(person.birth_year(),person.death_year(),yPos,generations[person])
        yPos += years[4]
        target.write("\t\"years\": \""+str(years[0])+"\",\n")
        target.write("\t\"yearssize\": "+str(years[1])+",\n")
        target.write("\t\"yearsyPos\": "+str(yPos)+",\n")
        target.write("\t\"yearsyScale\": "+str(years[4])+",\n")
        maxXScale = max(maxXScale,years[3])
        
        
        #if len(years[0])!=0:print "\t\tXScale:",round(years[3],1),"\tYPos:",str(yPos),"\t\tYScale:",round(years[4],1)," \t"," \t",str(years[0])
        
        upYHeight = min(upYHeight, min(years[1],1) * years[2])
        downYHeight = max(downYHeight, min(years[1],1) * years[2])
        
        smallXScale = maxXScale
        smallYScale = yPos + (years[4])/2
        smUpYHeight = upYHeight
        smDownYHeight = downYHeight
        
        ###PLACES###
        yPos += space2Px
        places = wraptext(birth_place,yPos,generations[person],18)
        

        for n in range(4):
            yPos += places[n][4]
            target.write("\t\"place"+str(n+1)+"\": \""+str(places[n][0])+"\",\n")
            target.write("\t\"place"+str(n+1)+"size\": "+str(places[n][1])+",\n")
            target.write("\t\"place"+str(n+1)+"yPos\": "+str(yPos)+",\n")
            target.write("\t\"place"+str(n+1)+"yScale\": "+str(places[n][4])+",\n")
            maxXScale = max(maxXScale,places[n][3])
            
            
            #if len(places[n][0])!=0:print "\t\tXScale:",round(places[n][3],1),"\tYPos:",str(yPos),"\t\tYScale:",round(places[n][4],1)," \t"," \t",str(places[n][0])
            
            upYHeight = min(upYHeight, min(places[n][1],1) * places[n][2])
            downYHeight = max(downYHeight, min(places[n][1],1) * places[n][2])
        
        
        
        ###OCCUPATIONS###
        occupations = wraptext(occupation,yPos,generations[person],22)
        
        for n in range(4):
            yPos += occupations[n][4]
            target.write("\t\"occupation"+str(n+1)+"\": \""+str(occupations[n][0])+"\",\n")
            target.write("\t\"occupation"+str(n+1)+"size\": "+str(occupations[n][1])+",\n")
            target.write("\t\"occupation"+str(n+1)+"yPos\": "+str(yPos)+",\n")
            target.write("\t\"occupation"+str(n+1)+"yScale\": "+str(occupations[n][4])+",\n")
            maxXScale = max(maxXScale,occupations[n][3])
            #if len(occupations[n][0])!=0:print "\t\tXScale:",round(occupations[n][3],1),"\tYPos:",str(yPos),"\t\tYScale:",round(occupations[n][4],1)," \t"," \t",str(occupations[n][0])

            upYHeight = min(upYHeight, min(occupations[n][1],1) * occupations[n][2])
            downYHeight = max(downYHeight, min(occupations[n][1],1) * occupations[n][2])
        
        yScale = yPos
        
        target.write("\t\"maxXScale\": \""+str(maxXScale)+"\",\n")
        target.write("\t\"upYHeight\": \""+str(upYHeight)+"\",\n")
        target.write("\t\"yHeight\": \""+str(abs(upYHeight)+abs(downYHeight)+12)+"\",\n")
        target.write("\t\"smYHeight\": \""+str(abs(smUpYHeight)+abs(smDownYHeight)+12)+"\",\n")
        target.write("\t\"smallXScale\": \""+str(smallXScale)+"\",\n")
        target.write("\t\"smallYScale\": \""+str(smallYScale)+"\",\n")
        target.write("\t\"YScale\": \""+str(yScale)+"\",\n")
        target.write("\t\"smallYScaleRect\": \""+str(smallYScale+padding*2)+"\",\n")
        target.write("\t\"YScaleRect\": \""+str(yScale+padding*2)+"\",\n")
        target.write("\t\"birthday\": \""+birth_day+"\",\n")
        target.write("\t\"birthyear\": \""+birth_year+"\",\n")
        target.write("\t\"birthplace\": \""+birth_place+"\",\n")
        target.write("\t\"deathday\": \""+death_day+"\",\n")
        target.write("\t\"deathyear\": \""+death_year+"\",\n")
        target.write("\t\"deathplace\": \""+death_place+"\",\n")      
        target.write("\t\"occupation\": \""+occupation+"\",\n")    
        target.write("\t\"customtext\": \""+customText+"\",\n")
        target.write("\t\"customtype\": \""+customType+"\",\n")   
        target.write("\t\"customdate\": \""+customDate+"\",\n")
        target.write("\t\"customplace\": \""+customPlace+"\",\n")   
        target.write("\t\"nodetype\": \""+person.gender()+"\",\n")
        target.write("\t\"gen\": " + str(generations[person]) + ",\n")
        target.write("\t\"branch\": " + str(branches[person]) + ",\n")
        target.write("\t\"family\": \"" + str(person.coreFamily()) + "\"\n")
        target.write("},\n")
        treeHeight = max(treeHeight,generations[person])
        
        #print maxXScale," ",smallXScale,"\n"
        
print "generations deep: ",treeHeight        

#marriage nodes
for count,family in enumerate(families,1):

        w = tree.get_family_members(family,"WIFE")
        h = tree.get_family_members(family,"HUSB")
        c = tree.get_family_members(family,"CHIL")

        qw = False
        if len(w) > 0:
            qw = w[0] in people
        qh = False
        if len(h) > 0:
            qh = h[0] in people            
        if qw or qh:
            target.write("{\n")
            names = family.name()
            maxbranch = 0
            
            target.write("\t\"id\": \""+str(family.pointer()).replace("@","")+"\",\n")
            target.write("\t\"name\": \""),
            #use initials to name the marriage
            for names in w:
                surname = w[0].coreFamily()
                for name in names.name():
                    
                    if name != "":
                            name = name.replace("\"","")
                            name = name.replace("(","")
                            name = name.replace(")","")
                            target.write(str(name)[0]),
                maxbranch = max(maxbranch,int(branches[names]))
            target.write("_")
            for names in h:
                surname = h[0].coreFamily()
                for name in names.name():
                    if name != "":
                        name = name.replace("\"","")
                        name = name.replace("(","")
                        name = name.replace(")","")
                        target.write(str(name)[0]),
                maxbranch = max(maxbranch,int(branches[names]))
                
                
            for names in c:
                maxbranch = max(maxbranch,int(branches[names]))
                
            target.write("\",\n")
            target.write("\t\"nodetype\": \"marriage\",\n")
            target.write("\t\"branch\": " + str(maxbranch) + ",\n")
            
            ###marriages###
            marriagedate = ""
            marriageplace = ""
            gen = 0
            if len(w) > 0:                
                if len(tree.marriages(w[0])) > 0:
                    try:marriagedate = str(tree.marriages(w[0])[0][0])
                        print "marriage: ",tree.marriages(w[0])[0][0]," ",
                    except:marriagedate = ""
                    try:marriageplace = str(tree.marriages(w[0])[1][1])
                        print tree.marriages(w[0])[1][1]
                    except:marriageplace = ""
                gen = generations[w[0]]
            
            marriagedate = marriagedate.replace("-","").replace(",","").replace(".","").replace("\\","").replace("?","").replace("`","").replace("(","").replace(")","").replace("'","")
            marriageplace = marriageplace.replace("-","").replace(",","").replace(".","").replace("\\","").replace("?","").replace("\`","").replace("(","").replace(")","").replace("'","")
            
            marriagedates = wraptext(marriagedate,-10,gen,22)
            marriageplaces = wraptext(marriageplace,-10,gen,22)
            
            target.write("\t\"myears\": \""+marriagedates[0][0]+"\",\n")
            target.write("\t\"myearssize\": \""+str(marriagedates[0][1])+"\",\n")
            target.write("\t\"myearsyPos\": \""+str(marriagedates[0][2])+"\",\n")
            for n in range(4):
                target.write("\t\"marriageplaces"+str(n+1)+"\": \""+str(marriageplaces[n][0])+"\",\n")
                target.write("\t\"marriageplaces"+str(n+1)+"size\": "+str(marriageplaces[n][1])+",\n")
                target.write("\t\"marriageplaces"+str(n+1)+"yPos\": "+str(marriageplaces[n][2])+",\n")
            
            if len(w)>0 and len(h)==0:
                target.write("\t\"gen\": " + str(float(generations[w[0]])) + ",\n")
                #target.write("\t\"branch\": " + str(int(branches[w[0]])+1) + ",\n")
                branches[family] = branches[w[0]]
            if len(h)>0 and len(w)==0:
                target.write("\t\"gen\": " + str(float(generations[h[0]])) + ",\n")
                #target.write("\t\"branch\": " + str(int(branches[h[0]])+1) + ",\n")
                branches[family] = branches[h[0]]
            elif len(w)>0:
                target.write("\t\"gen\": " + str(float(generations[w[0]])) + ",\n")
                #target.write("\t\"branch\": " + str(maxbranch) + ",\n")
                branches[family] = branches[w[0]]
            elif len(h)>0:
                target.write("\t\"gen\": " + str(float(generations[h[0]])) + ",\n")
                #target.write("\t\"branch\": " + str(maxbranch) + ",\n")
                branches[family] = branches[h[0]]
            elif len(c)>0:
                target.write("\t\"gen\": " + str(float(generations[c[0]])) + ",\n")
                #target.write("\t\"branch\": " + str(int(branches[c[0]])) + ",\n")
                branches[family] = branches[h[0]]

            else:
                target.write("\t\"gen\": 0,\n")
                target.write("\t\"branch\": 0,\n")
                
            target.write("\t\"family\": \"" + surname + "\"\n")
            target.write("}"),
            if count < len(families):
                target.write(",")
            target.write("\n")


target.write("],\n")
target.write("\"Links\": [\n")

for count,family in enumerate(families,1):
        w = tree.get_family_members(family,"WIFE")
        h = tree.get_family_members(family,"HUSB")
        c = tree.get_family_members(family,"CHIL")

        size = len(w)+len(h)+len(c)
        #print family.name()," family size = ", size, " ",
        branch = 0
        for wife in w:
            if wife in people:
                size -= 1
                for husb in h:
                    if husb in people:
                        target.write("{\n")
                        target.write("\t\"source\": \""+str(husb.pointer()).replace("@","")+"\",\n")
                        target.write("\t\"target\": \""+str(wife.pointer()).replace("@","")+"\",\n")
                        #target.write("\t\"value\": \"wife\",\n")
                        #print wife.name()[0]," ",wife.name()[1]," ",branches[wife], " ",husb.name()[0]," ",husb.name()[1]," ",branches[husb],
                        #print (" branch: " + str(max(branches[wife],branches[husb])))
                        target.write("\t\"branch\": " + str(max(branches[wife],branches[husb])) + ",\n")
                        target.write("\t\"gen\": " + str(max(int(generations[wife]),int(generations[husb]))) + ",\n")
                        target.write("\t\"family\": \"" + str(wife.coreFamily()) + "\",\n")
                        target.write("\t\"type\": \"marriage\"\n")
                        target.write("},\n")
                target.write("{\n")
                target.write("\t\"source\": \""+str(family.pointer()).replace("@","")+"\",\n")
                target.write("\t\"target\": \""+str(wife.pointer()).replace("@","")+"\",\n")
                #target.write("\t\"value\": \"wife\",\n")
                target.write("\t\"branch\": " + str(max(branches[wife],branches[family])) + ",\n")
                target.write("\t\"gen\": " + str(int(generations[wife])) + ",\n")
                target.write("\t\"family\": \"" + str(wife.coreFamily()) + "\",\n")
                target.write("\t\"type\": \"wife "+wife.name()[0]+" "+wife.name()[1]+"\"\n")
                target.write("}"),
                if count >= len(families) and size < 1:
                    target.write("")
                else: target.write(",")
                target.write("\n")



        for husb in h:
            if husb in people:
                size -= 1
                target.write("{\n")
                target.write("\t\"source\": \""+str(family.pointer()).replace("@","")+"\",\n")
                target.write("\t\"target\": \""+str(husb.pointer()).replace("@","")+"\",\n")
                #target.write("\t\"value\": \"husband\",\n")
                target.write("\t\"branch\": " + str(max(branches[husb],branches[family])) + ",\n")
                target.write("\t\"gen\": " + str(float(generations[husb])) + ",\n")
                target.write("\t\"family\": \"" + str(husb.coreFamily()) + "\",\n")
                target.write("\t\"type\": \"husband "+husb.name()[0]+" "+husb.name()[1]+"\"\n")
                target.write("}"),
                if count >= len(families) and size < 1:
                    target.write("")
                else: target.write(",")
                target.write("\n")
    
        for child in c:
            if child in people:
                size -= 1
                target.write("{\n")
                target.write("\t\"source\": \""+str(family.pointer()).replace("@","")+"\",\n")
                target.write("\t\"target\": \""+str(child.pointer()).replace("@","")+"\",\n")
                #target.write("\t\"value\": \"child\"\n")
                target.write("\t\"branch\": " + str(max(branches[child],branches[family])) + ",\n")
                target.write("\t\"gen\": " + str(float(generations[child])+1) + ",\n")
                target.write("\t\"family\": \"" + str(child.coreFamily()) + "\",\n")
                target.write("\t\"type\": \"child "+child.name()[0]+" "+child.name()[1]+"\"\n")
                target.write("}"),
                if count >= len(families) and size < 1:
                    target.write("")
                else: target.write(",")
                target.write("\n")

                
                
target.write("]\n")
target.write("}\n")     
target.close()
print "success!"
wait = input("PRESS ENTER TO CONTINUE.")
