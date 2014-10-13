import tkinter
import math
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
from arrestinfo import *
import time
global Arrestlist
global aitem

#global whichPin
global pos

pos = 0

global newlatLong1
global newlatLong2
global newlatLong3

global arrestv1
global arrestv2
global arrestv3

global displayArrestList1
global displayArrestList2
global displayArrestList3

global tempArrestType1
global tempArrestType2
global tempArrestType3

tempArrestType1 = None
tempArrestType2 = None
tempArrestType3 = None

aitem = ''

newlatLong1 = []
newlatLong2 = []
newlatLong3 = []

displayArrestList1 = []
displayArrestList2 = []
displayArrestList3 = []

global result
result = displayArrestList1 + displayArrestList2 + displayArrestList3


def arrestType1():
  global newlatLong1
  global displayArrestList1
  global tempArrestType1
  if arrestv1.get()==0:
    newlatLong1 = []
    displayArrestList1 = []
    tempArrestType1 = None
  if arrestv1.get()==1:
    #print('arrest1 called')
    #newlatLong1 = getArrestLocation(13500)
    #displayArrestList1 = getArrestInfo(13500)
    tempArrestType1 = 97600
    

def arrestType2():
  global newlatLong2
  global displayArrestList2
  global tempArrestType2
  if arrestv2.get()==0:
    newlatLong2 = []
    displayArrestList2 = []
    tempArrestType2 = None
  if arrestv2.get()==1:
    #print('arrest2 called')
    #newlatLong2 = getArrestLocation(97600)
    #displayArrestList2 = getArrestInfo(97600)
    tempArrestType2 = 94000
    

def arrestType3():
  global newlatLong3
  global displayArrestList3
  global tempArrestType3 
  if arrestv3.get()==0:
    newlatLong3 = []
    displayArrestList3 = []
    tempArrestType3 = None
  if arrestv3.get()==1:
    #print('arrest3 called')
    #newlatLong3 = getArrestLocation(95000)
    #displayArrestList3 = getArrestInfo(95000)
    tempArrestType3 = 95000

def listOfAddresses(charge):
  AddressList1 = []
  results1 = getArrestInfo(charge)
  for item in results1:
    address = item[5]
    #print(address)
    AddressList1.append(address)
  return(AddressList1)

def ListOfIAAddresses(charge):
  NewAddressList1 = []
  IAaddresses = listOfAddresses(charge)
  for addresses in IAaddresses:
    if addresses[-2:] == 'IA':
      NewAddressList1.append(addresses)
    if addresses[-2:] != 'IA':
      addresses = addresses +' Iowa City, IA'
      NewAddressList1.append(addresses)
  return NewAddressList1

def getArrestLocation(charge):
  global latLongList
  latLongList = []
  results = ListOfIAAddresses(charge)
  for result in results:
    tempResult = result
    gAddress = geocodeAddress(result)
    time.sleep(.2)
    try:
      if gAddress[0] > 42.5 or gAddress[0] < 41: #if way outside of Iowa City
        betterResult = geocodeIowaCityPlace(tempResult)
        latLongList.append(betterResult)
      else: #address close to Iowa City'
        latLongList.append(gAddress)
    except TypeError:
      latLongList.append([41.6611277,-91.5301683]) #Maclean Hall aka center of ICity
  #print(latLongList)
  return(latLongList)

# Code to start from for HW12, 22c80/104, Fall 2012, Google Maps. 
#
# The main map creation function is "createMapFromAddress"
# createMapFromAddress creates a Google Static Maps (gif) image 
# and stores it in tmp_file
# 
# To *display* the map, we use a Label GUI widget, since Label
# GUI widgets can have images associated with them.  See the function
# updateLabelMapImage.
#
# To test GUI-based map making, see the last function in this file
# simpleMapGUI().  When you run it, you'll get a very simple GUI
# in which you can enter a location, press the submit button and see
# the corresponding map.

# To use this code:
#  1) change the tmp_file value to a filename that makes sense
#     on your machine/account
#  2) execute simpleMapGUI()
#

################################################################################

tmp_file = 'pic.gif'

# Given a string representing a location, return 2-element 
# [latitude, longitude] list for that location (or print
# an error message when Google doesn't find the location)
#
def geocodeAddress(addressString):
  url = getGeocodeUrl(addressString)
  resultFromGoogle = urlopen(url).read()
  resultFromGoogle = resultFromGoogle.decode('utf-8')
  data = resultFromGoogle.split(',')
  # The URL asked Google to return information in "csv" form. 
  # data[0] contains: HTTP status code. 200 is good, others are errors.
  # data[1] contains: some "accuracy" information - ignore this for now.
  # data[2] contains: latitude 
  # data[3] contains: longitude
  if data[0] != "200":
    errorCode = int(data[0])
    print("Google Maps Exception: %s" % getGeocodeError(errorCode))
    return
  else:
    # if no error return a [latitude, longitude] list
    return [float(data[2]),float(data[3])]


  
 
# Construct a URL that represents a query to google for the 
# location of the given addressString.
#
def getGeocodeUrl(addressString):
  urlbase = "http://maps.google.com/maps/geo"
  return "%(urlbase)s?%(params)s" % {'params': urlencode({'q':addressString.encode("UTF-8"),
                                      'output':'csv'
                                    }),
             'urlbase': urlbase}

import json
# Some of the arrest locations in the Arrest Blotter are place locations
# or vague street addresses.   This function *might* work better
# for converting that location to a lat/long.
#
def geocodeIowaCityPlace(placenameString):
  query = urlencode({'q' : placenameString + ' near Iowa City, IA'})
  url = 'http://ajax.googleapis.com/ajax/services/search/local?v=1.0&%s&rsz=large' \
  % (query)
  resultFromGoogle = urlopen(url).read()
  resultFromGoogle = resultFromGoogle.decode('utf-8')
  jsonresult = json.loads(resultFromGoogle)
  res = jsonresult['responseData']['results'][0]
  return([res['lat'], res['lng']])

def getGeocodeUrlNewAPI(addressString):
  urlbase = "http://maps.googleapis.com/maps/api/geocode/json"
  return "%(urlbase)s?%(params)s" % {'params': urlencode({'address':addressString.encode("UTF-8"),
                                      'sensor':'false',
                                        }),
             'urlbase': urlbase}

def getGeocodeError(errorCode):
  errorDict = {400: "Bad request",
               500: "Server error",
               601: "Missing query",
               602: "Unknown address",
               603: "Unavailable address",
               604: "Unknown directions",
               610: "Bad API key",
               620: "Too many queries"}
 
  
  if errorCode in errorDict:
    return errorDict[errorCode]
  else:
    return "Unknown error"
 
# First construct a URL suitable for the Google Static Maps API
# Then use the URL to request a map from Google, storing the 
# resulting image in tmp_file
# 
def retrieveStaticMap(width, height, lat, long, zoom):
  url = getMapUrl(width, height, lat, long, zoom)
  urlretrieve(url, tmp_file)
  return tmp_file

# Contruct a Google Static Maps API URL for a map that:
#   has size width x height in pixels
#   is centered at latitude lat and longitude long
#   is "zoomed" to the give Google Maps zoom level (0 <= zoom <= 21)
#    
def getMapUrl(width, height, lat, lng, zoom):
  global pos
  truncResult = 44
  counter = 0
  iclat = str(41.6611277)
  iclng = str(-91.5301683)
  urlbase = "http://maps.google.com/maps/api/staticmap"
  params = ["center=%(iclat)s,%(iclng)s" % {"iclat":iclat,"iclng":iclng}]
  #check list 1
  if len(lat) != 0 and pos < len(lat):
    newPos = pos
    #if len(lat) != 0:
      #print('getMap',lat[newPos],lng[newPos])
    params.append("markers=color:red|" + str(lat[newPos]) + "," +str(lng[newPos]))
    #print('getMapURL marke pos',lat[newPos],lng[newPos])
  #print(lat)
  if len(lat) < 45:
    if len(newlatLong1) != 0:
      for i in range(len(newlatLong1)):
        #print(lat[i],lng[i])
        params.append("markers=color:yellow|" + str(lat[i]) + "," +str(lng[i]))
    if len(newlatLong2) != 0:
      for i in range(len(newlatLong2)):
        #print('list2 i', i)
        params.append("markers=color:blue|" + str(lat[i]) + "," +str(lng[i]))
    if len(newlatLong3) != 0:
      for i in range(len(newlatLong3)):
        params.append("markers=color:green|" + str(lat[i]) + "," +str(lng[i]))
  else: # if len(lat) > 45
    warningMessage.configure(text='List truncated!')
    if len(newlatLong1) != 0:
      for i in range(len(newlatLong1)):
        counter +=1
        if counter < truncResult:
          params.append("markers=color:yellow|" + str(lat[i]) + "," +str(lng[i]))
        else:
          pass
    if len(newlatLong2) != 0:
      for i in range(len(newlatLong2)):
        counter +=1
        if counter < truncResult:
          params.append("markers=color:blue|" + str(lat[i]) + "," +str(lng[i]))
        else:
          pass
    if len(newlatLong3) != 0:
      for i in range(len(newlatLong3)):
        counter +=1
        if counter < truncResult:
          params.append("markers=color:green|" + str(lat[i]) + "," +str(lng[i]))
        else:
          pass
      

    
  #check list 2

  
  params.append("zoom=%(zoom)s" % {"zoom":zoom})
  params.append("size=%(width)sx%(height)s" % {"width":width,"height":height})
  params.append("format=%(format)s" % {"format":"gif"})  
  params.append("sensor=false")
  #print("%(urlbase)s?%(params)s" % {"urlbase":urlbase,"params":"&".join(params)})
  return  "%(urlbase)s?%(params)s" % {"urlbase":urlbase,"params":"&".join(params)}
 

# Create a map image, built via Google Static Maps API, based on the location
# specified by "addressString" and zoomed according to the 
# given zoom level (Google's zoom levels range from 0 to 21).
# The location will be in the center of the map.
#
def createMapFromAddress(addressString, zoom):
  #latLong = geocodeAddress(addressString)
  
  #global arrest1
  #global arrest2
  #global arrest3
  #assign arrests in GUI and pass into this function
  global newlatLong1
  global newlatLong2
  global newlatLong3
  global pos
    
  #newlatLong1 = getArrestLocation(13500)
  #print('97600: ', newlatLong1)
  #newlatLong2 = getArrestLocation(97600)
  #newlatLong3 = getArrestLocation(95000)
  newlatLong = newlatLong1 + newlatLong2 + newlatLong3
  x = 0
  y = 0
  latList = []
  longList = []
  #print(latLong)
  #print(latLong[0])
  #print(latLong[1])
  # For informal addresses, e.g., "Bread Garden near Iowa City",
  # the following will often work significantly better:
  #latLong = geocodeIowaCityPlace(addressString)
  for i in range(len(newlatLong)):
    try:
      #print(newlatLong[x][0], newlatLong[y][1])
      latList.append(newlatLong[x][0])
      longList.append(newlatLong[y][1])
      x += 1
      y += 1
    except TypeError:
      latList.append(41.6611277)
      longList.append(-91.5301683) #Maclean Hall is the epicenter of Iowa City? :)
      x += 1
      y += 1
  #print(latList)
  #print(longList)
  retrieveStaticMap(400, 400, latList, longList, zoom)

  #if len(latList) != 0:
    #print('createMap GUI address',latList[pos])
    #print('createMap GUI add',longList[pos])


##########
#
# Most of the code from here down to the GUI section can be ignored on your
# first look.
#
# Code below is extended/modified/adapted from code found
# at http://wiki.forum.nokia.com/index.php/PyS60_Google_Maps_API
#
# some code useful for lat/long <--> x/y conversion
#
magic_number = 128<<21 # this is half the earth's circumference *in pixels*
                         # at Google zoom level 21
radius = magic_number / math.pi

# Return a list [winX, winY] of window coordinates corresponding to the 
# given lat/long location for a google map of winWidth-by-winHeight pixels
# centered at lat/long [winCenterLat, winCenterLng] and with the given zoom level
#
# This function should make it easy to place additional text on your maps - 
# in particular, it will make it pretty easy to annotate the graph edges with 
# their lengths/distances
#
def latLongToWindowXY(lat, lng, winCenterLat, winCenterLng, winWidth, winHeight, zoom):
  winCenterX = winWidth/2
  winCenterY = winHeight/2
  winX = winCenterX + ((longToGoogleX(lng) - longToGoogleX(winCenterLng))>>(21-zoom))
  winY = winCenterY + ((latToGoogleY(lat) - latToGoogleY(winCenterLat))>>(21-zoom))
  return [winX, winY]

def longToGoogleX(lng):
  return int(round(magic_number + (lng / 180.0) * magic_number))
 
def latToGoogleY(lat):
  return int(round(magic_number - 
                   radius * math.log( (1 + math.sin(lat * math.pi / 180)) /
                                      (1 - math.sin(lat * math.pi / 180)) ) / 2))
 
def googleXToLong(x):
  return 180.0 * ((round(x) - magic_number) / magic_number)
 
def googleYToLat(y):
  return ( (math.pi / 2) - (2 * math.atan(math.exp( (round(y)-magic_number)/radius ))) ) * 180 / math.pi

########## 
# very basic GUI code

rootWindow = tkinter.Tk()

arrestv1 = tkinter.IntVar()
arrestv1.set(0)

arrestv2 = tkinter.IntVar()
arrestv2.set(0)

arrestv3 = tkinter.IntVar()
arrestv3.set(0)


def click():
    global zoomval
    print(zoomval)
    global pos
    global list
    #global whichPin

    global newlatLong1
    global displayArrestList1

    global newlatLong2
    global displayArrestList2
    global newlatLong3
    global displayArrestList3

    global tempArrestType1
    global tempArrestType2
    global tempArrestType3
    global result
    #result = displayArrestList1 + displayArrestList2 + displayArrestList3

    if tempArrestType1 != None:
      newlatLong1 = getArrestLocation(tempArrestType1)
      displayArrestList1 = getArrestInfo(tempArrestType1)
      #print(newlatLong1)

    if tempArrestType2 != None:
      newlatLong2 = getArrestLocation(tempArrestType2)
      displayArrestList2 = getArrestInfo(tempArrestType2)

    if tempArrestType3 != None:
      newlatLong3 = getArrestLocation(tempArrestType3)
      displayArrestList3 = getArrestInfo(tempArrestType3)
    
    
    #createMapFromAddress(entry.get(), zoomval)
    createMapFromAddress("Iowa City, IA", zoomval)  
    mapimage = tkinter.PhotoImage(file=tmp_file)
    maplabel.image = mapimage
    maplabel.configure(image=mapimage)

    if len(result) != 0:
      aitem= result[pos]
      alabel.configure(text=aitem)



frame = tkinter.Frame(rootWindow, width=500)
frame.pack()

#label = tkinter.Label(frame, text="Enter a location for Iowa City, IA:")
#label.pack()

#entry = tkinter.Entry(frame)
#entry.pack()

label2 = tkinter.Label(frame, text="Select an Arrest Type:")
label2.pack()

#atypebutton3 = tkinter.Button(frame, text="PAULA")
#atypebutton3.pack()
#command assign arrest 1 value

#atypebutton4 = tkinter.Button(frame, text="OWI")
#atypebutton4.pack()
#command assign arrest 2 value

#atypebutton5 = tkinter.Button(frame, text="Public Intox")
#atypebutton5.pack()

arrestT1 = tkinter.Checkbutton(frame, text="PAULA",variable=arrestv1,command=arrestType1)
arrestT1.pack()

arrestT2 = tkinter.Checkbutton(frame, text="OWI",variable=arrestv2, command=arrestType2)
arrestT2.pack()

arrestT3 = tkinter.Checkbutton(frame, text="Public Intox",variable=arrestv3, command=arrestType3)
arrestT3.pack()
#command assign arrest 3 value

zoomval = 12
def inczoom():
  global zoomval
  if (zoomval < 22):
    zoomval = zoomval + 1
    zlabel.configure(text="zoom: " + str(zoomval))
    createMapFromAddress("Iowa City, IA", zoomval)    
    mapimage = tkinter.PhotoImage(file=tmp_file)
    maplabel.image = mapimage
    maplabel.configure(image=mapimage)
  
  
def deczoom():
  global zoomval
  if (zoomval > 0):
    zoomval = zoomval - 1
    zlabel.configure(text="zoom: " + str(zoomval))
    createMapFromAddress("Iowa City, IA", zoomval)    
    mapimage = tkinter.PhotoImage(file=tmp_file)
    maplabel.image = mapimage
    maplabel.configure(image=mapimage)

    
# the line below is simply used to ensure that "tmp_file" exists
# when the maplabel is initially created (avoiding a possible error)
# On most systems, the Iowa City map won't actually show up on the 
# initial GUI.  Most won't see a map until a new address is entered
# and the GUI button is pressed.


  
def moveRight():
  global displayArrestList1
  global displayArrestList2
  global displayArrestList3
  global zoomval
  global lat
  global lng
  result = displayArrestList1 + displayArrestList2 + displayArrestList3
  global pos
  global aitem
  
  
  if (pos >= 0 and pos < len(result)):
    aitem= result[pos]
    #print('right pos', pos)
    
    namelabel.configure(text=aitem[0])
    homelabel.configure(text=aitem[1])
    arrestdlabel.configure(text=aitem[2])
    dateofbirth.configure(text=aitem[3])
    arrestlocation.configure(text=aitem[5])
    createMapFromAddress("Iowa City, IA", zoomval)    
    mapimage = tkinter.PhotoImage(file=tmp_file)
    maplabel.image = mapimage
    maplabel.configure(image=mapimage)
    pos += 1
    
    
    


createMapFromAddress("Iowa City, IA", zoomval)

maplabel = tkinter.Label(frame, image=tkinter.PhotoImage(tmp_file))
maplabel.pack()

zoomframe = tkinter.Frame(frame)
zoomframe.pack()

inczbutton = tkinter.Button(zoomframe, text="+", command=inczoom)
inczbutton.pack(side='right')

deczbutton = tkinter.Button(zoomframe, text="-", command=deczoom)
deczbutton.pack(side='right')

zlabel = tkinter.Label(zoomframe, text="zoom: 12")
zlabel.pack(side='right')

alistlabel = tkinter.Label(frame, text="cycle through arrests")
alistlabel.pack()

#rightabutton = tkinter.Button(frame, text="<<", command=moveLeft)
#rightabutton.pack()

rightabutton = tkinter.Button(frame, text=">>", command=moveRight)
rightabutton.pack()

namelabel = tkinter.Label(frame,text="Name")
namelabel.pack()

homelabel = tkinter.Label(frame,text="Home Add.")
homelabel.pack()

arrestdlabel = tkinter.Label(frame,text="Arrest date")
arrestdlabel.pack()

dateofbirth = tkinter.Label(frame,text="DOB")
dateofbirth.pack()

arrestlocation = tkinter.Label(frame,text="Arrest Loc")
arrestlocation.pack()

warningMessage = tkinter.Label(frame,text="")
warningMessage.pack()

button = tkinter.Button(frame, text="Update the map!", command=click)
button.pack(side='bottom')

def mapGUI(): #call this
  rootWindow.mainloop()


