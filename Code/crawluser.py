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
urls = []
totalentries = 0
hasagecount = 0
femalecount = 0
malecount = 0
nogendercount = 0

uniqueusers = {}
uniquelocations = 397

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
                if loc not in locations:
                    locations.append(loc)
                agegenderlocvector[locations.index(loc)] = 1

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




print('unique location: ' + str(len(locations)))
print('unique users: ' + str(len(urls)))
print('total entries: ' + str(totalentries))
print('female count: ' + str(femalecount))
print('male count: ' + str(malecount))
print('no gender count: ' + str(nogendercount))
print('has age count: ' + str(hasagecount))




