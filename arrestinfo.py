import urllib.request

# Charge 94000 = OWI
# Study the Iowa City Arrest Blotter page's html source to discover what
# numbers correspond to other charges ...
def getArrestInfo(chargenum):
 global Arrestlist
 global locs
 baseurl = "http://www.iowa-city.org/icgov/apps/police/blotter.asp?charge="
 url = baseurl + str(chargenum)
 
 # You can also do retrieve records by date. E.g.
 #
 # url = "http://www.iowa-city.org/icgov/apps/police/blotter.asp?date=11102012"

 connection = urllib.request.urlopen(url)
 resultbytes = connection.read()
 pageofresults = resultbytes.decode('utf-8')
 
 connection.close()

 begtable = pageofresults.find("tbody") 
 endtable = pageofresults.find("</tbody", begtable+1)
 table = pageofresults[begtable:endtable]

 # Go to first record
 currrecordstart = getnextrecordindex(table, 0);
 # Actually, first record is just a template.  Skip and go to first
 # real record
 currrecordstart = getnextrecordindex(table, currrecordstart + 1)

 
 locs = []
 numrecords = 0
 while (currrecordstart >= 0):
  numrecords = numrecords + 1
  
  locs.append(processrecord(table, currrecordstart))
  currrecordstart = getnextrecordindex(table, currrecordstart + 1)

 # Useful during debugging. Remove at some point ...
 #print()
 #print("Total number of records found: ", numrecords)
 
 return(locs)


def getnextrecordindex (inputstring, startindex):
 return inputstring.find("<tr", startindex)

def processrecordstub(inputstring, recordindex):
 print("I am processing a record")
 return("this is a placeholder for arrest info")
 
def processrecord(inputstring, recordindex):
 namestart = inputstring.find("<strong>", recordindex) + 8
 nameend = inputstring.find("</strong>", namestart)
 addressstart = inputstring.find("/>", nameend) + 2
 addressend = inputstring.find("</", addressstart)
 adatestart = inputstring.find("<strong>", addressend) + 8
 adateend = inputstring.find("&", adatestart)
 bdatestart = inputstring.find("dob",addressend) + 6
 bdateend = inputstring.find("</", bdatestart)
 offstart = inputstring.find("--", bdateend) + 10
 offend = inputstring.find("</", offstart)
 alocstart = inputstring.find("-->",bdateend) + 3
 alocend = inputstring.find("</", alocstart)

 # Printing like this is *very* useful for debugging.  Do
 # this first but then comment out the printing when you connect
 # this code to the map code.
 #print()
 #print("Name: ", inputstring[namestart:nameend])
 #print("  Date of birth: ", inputstring[??], ", Home address: ", inputstring[??])
 #print("  was arrested on: ", inputstring[??])
 #print("  by officer: ", inputstring[??])
 #print("  at location: ", inputstring[??])
 global Arrestlist
 
 Arrestlist = [inputstring[namestart:nameend],
                 inputstring[addressstart:addressend],
                 inputstring[adatestart:adateend],
                 inputstring[bdatestart:bdateend],
                 inputstring[offstart:offend],
                 inputstring[alocstart:alocend]]
 return(Arrestlist)
                 
                 
 
 #return("something different than this string")


