import os
import json
import copy
from matplotlib import pyplot as plt

NAME = ['1MB', '2MB', '4MB', '8MB', '16MB', '32MB', '64MB', '128MB', '256MB', '512MB', '1GB', '2GB', '4GB', '8GB', '16GB', '32GB', '64GB', '128GB', '256GB', '512GB']
INCR = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536, 131072, 262144, 524288]
oneMB = 1048576

def findSize(inputSize):
    for item in INCR:
        if inputSize <= item*oneMB:
            return item*oneMB

counters = {}
for item in INCR:
    summb = item*oneMB
    counters[summb] = 0

def getDict():
    sums = {'0': {}}
    sums['0']['ALL'] = copy.deepcopy(counters)
    with open('allfiles', 'r')  as fd:
        for line in fd:
            spl = line.split()
            if spl[0].startswith('d'):
                continue
            try:
                size = int(spl[4])
                lfn = spl[-1:][0]
                lfnspl = lfn.split('/')
                loc = findSize(size)
                sums['0']['ALL'][loc] += 1
                if lfnspl[1] not in sums.keys():
                    sums[lfnspl[1]] = copy.deepcopy(counters)
                    sums[lfnspl[1]]['l'] = {}
                sums[lfnspl[1]][loc] += 1
                if lfnspl[2] not in sums[lfnspl[1]]['l'].keys():
                    sums[lfnspl[1]]['l'][lfnspl[2]] = copy.deepcopy(counters)
                    sums[lfnspl[1]]['l'][lfnspl[2]]['l'] = {}
                sums[lfnspl[1]]['l'][lfnspl[2]][loc] += 1
                if lfnspl[3] not in sums[lfnspl[1]]['l'][lfnspl[2]]['l'].keys():
                    sums[lfnspl[1]]['l'][lfnspl[2]]['l'][lfnspl[3]] = copy.deepcopy(counters)
                sums[lfnspl[1]]['l'][lfnspl[2]]['l'][lfnspl[3]][loc] += 1
            except IndexError:
                print 'IndexError for %s' % spl
                continue
            except KeyError:
                print 'Got KeyError for %s' % spl
            except ValueError:
                print 'Got ValueError for %s' % spl
    return sums


def makePlot(values, title, savename):
    plt.bar(NAME, values, align = 'center')
    plt.title(title)
    plt.ylabel('Count')
    plt.xticks(rotation=-45)
    plt.xlabel('Size')
    for i in range(len(values)):
        plt.text(x = i-0.5, y = values[i]+0.1, s = values[i], size = 6, rotation=45, color='red')
    plt.savefig(savename)
    plt.close()

def pprinter(inputDict, prefLine):
    for key, val in inputDict.items():
        if key == '0':
            continue
        print "%s%s" % (prefLine, key)
        vals = []
        sumcounts = [0, 0, 0, 0, 0, 0, 0, 0]
        total = 0
        for cKey in counters.keys():
            total += val[str(cKey)]
            for i in enumerate([1,2,4,8,16,32,64,128]):
                if int(cKey) <= int(i[1] * 1048576):
                    sumcounts[i[0]] += val[str(cKey)]
            vals.append(val[str(cKey)])
        print total
        for i in enumerate([1,2,4,8,16,32,64,128]):
            print "%sMB: %s" % (i[1], sumcounts[i[0]])
        for i in enumerate([1,2,4,8,16,32,64,128]):
            print "Percentage lower than %sMB: %s" % (i[1], float(sumcounts[i[0]] * 100.0 / total))
        makePlot(vals, "%s%s" % (prefLine, key), "img-%s%s.png" % (prefLine, key))


allvals = {}
if os.path.isfile('jsondump'):
    print 'WARNING. USING JSON DUMP FILE FROM LAST RUN'
    print 'IF WANT FROM SCRACH, REMOVE jsondump FILE'
    with open('jsondump', 'r') as fd:
        allvals = json.load(fd)
else:
    allvals = getDict()
    with open('jsondump', 'w') as fd:
        fd.write(json.dumps(allvals))


pprinter(allvals['0'], "ALL")
pprinter(allvals, "")
for key in allvals.keys():
    if key == '0':
        continue
    pprinter(allvals[key]['l'], "%s" % key)
    #for key1 in allvals[key]['l'].keys():
    #    pprinter(allvals[key]['l'][key1]['l'], "%s-%s-" % (key, key1))

