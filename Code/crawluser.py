from os import walk
import json
path = "../crawling_results/data/"

paths = []
for (dirpath, dirnames, files) in walk(path):
    paths.append(dirpath)

    #print(dirnames)
paths.pop(0)
print(paths)

# variables for statistics
locations = []
locationCount = {}
filterlocationCount = {}
urls = []
totalentries = 0
hasagecount = 0
femalecount = 0
malecount = 0
nogendercount = 0

uniqueusers = {}
uniquelocations = 397

# find the number of unique locations and its frequency. Filter if needed.
# filterlocation: stores unique locations in a list. It is used to find the index later when we construct the location vector
# filterlocationCount: contains the unique locations and its frequency
# TODO: remove repeating elements of California from LocationCount
# TODO: do the above with locationCount (optional) because it is only used for printing results
for folder in paths:
    filesname = []
    for (dirpath, dirnames, files) in walk(folder):
        #print(len(files))
        for jsonfile in files:
            with open(folder + '/' + jsonfile) as data_file:
                data = json.load(data_file)
                print(data)
            try:
                #print(data["user"]["location"])
                loc = data["user"]["location"]
                if loc not in locationCount:  # TODO: and not in list of variations
                    locationCount[loc] = 0
                locationCount[loc] += 1 # TODO: increment also if loc is in list of variation (optional but hard
                                        # TODO: because variation might come before real index exists)

            except KeyError:
                print('cannot find location2')
filterlocation = []
for key,value in locationCount.items():
    if value > 0:
        filterlocation.append(key)
        filterlocationCount[key] = value

uniquelocations = len(filterlocationCount)



# Goes through every JSON file and generate the corresponding agegenderlocvec
# TODO: see location part
for folder in paths:
    filesname = []
    for (dirpath, dirnames, files) in walk(folder):
        #print(len(files))
        for jsonfile in files:
            agegenderlocvector = (2+uniquelocations)*[0]   # [locationvector  gender  age]

            totalentries += 1

            print('extracting: ' + folder + '/' + jsonfile)
            with open(folder + '/' + jsonfile) as data_file:
                data = json.load(data_file)
            print(data["user"])

            try:
                # try to get age
                txt = data["user"]["info"].split()[0]
                if txt.isnumeric():
                    age = int(txt)
                    hasagecount += 1
                else:
                    age = 0
                agegenderlocvector[uniquelocations + 1] = age
                print('age: ' + str(age))

                # try to get gender
                txt = data["user"]["info"]
                if "girl" in txt:
                    gender = 1
                    femalecount += 1
                elif "guy" in txt:
                    gender = -1
                    malecount += 1
                else:
                    gender = 0
                    nogendercount += 1
                agegenderlocvector[uniquelocations] = gender
                print("gender: " + str(gender))

            except KeyError:
                print('cannot find info')
            # get location

            try:
                #print(data["user"]["location"])
                loc = data["user"]["location"]
                if loc in filterlocation:
                    agegenderlocvector[filterlocation.index(loc)] = 1
                # TODO: if loc is an variation of California or other places
                # TODO: find the corresponding correct index


            except KeyError:
                print('cannot find location')

            # url
            try:
                #print(data["user"]["url"])
                url = data["user"]["url"]
                if url not in urls:
                    urls.append(url)
                    uniqueusers[url] = agegenderlocvector
            except KeyError:
                print('cannot find user url')

            print('vector: ' + str(agegenderlocvector))

with open('userdata.json', 'w') as f:
    json.dump(uniqueusers, f)




# Statistics

print('unique location: ' + str(len(locationCount)))
with open('uniquelocation.json', 'w', encoding="utf-8") as f:
    for key,value in filterlocationCount.items():
        f.write(str(key) + ': ' + str(value) +'\n')

print('unique users: ' + str(len(urls)))
print('total entries: ' + str(totalentries))
print('female count: ' + str(femalecount))
print('male count: ' + str(malecount))
print('no gender count: ' + str(nogendercount))
print('has age count: ' + str(hasagecount))




