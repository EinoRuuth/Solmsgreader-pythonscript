# command line arguments:

# --time SECONDS / -t SECONDS
# --goid GOID / -g GOID
# --node ID / Id: ID / -n ID
# --failed / -f
# --path / -p
# --file / -f
# --graph


# search the groups by how long the process took: --time (seconds)
# (for example --time 10)

# search the groups by GOID: --goid (the goid you want to search)
# (for example --goid 1,1242,1,303)
# in the goid you can be specific or broad for example:
# goid 1 will give you all the groups that have a GOID that starts with 1
# and then so fourth

# search the groups by Id: with --node ID or Id: ID
# (for example Id: 3 / --node 3)

# search for all failed processes using --failed
# (for example --failed)

# use --path to specify the file path
# (for example --path C:\Users\user\Documents\solmsg)
# this searches for folders named tscn* by default

# use --file to specify the file/files you want to go through
# (for example
# --file C:\Users\user\Documents\solmsg\tsnc\tsnc_master\solmsg.out)

# use --graph to make a visual graph on a given goid or node
# (for example --graph -g 1,123,2,204)


# pip installs:
# pip install --upgrade plotly
# pip install --upgrade pandas
# pip install --upgrade numpy

# import glob for file searching.
import glob
# re for searching for stuff in the files.
import re
# sys for python command line arguments.
import sys
# datetime for process time convertion.
from datetime import datetime
# plotly, pandas and numpy for graphs
import plotly.express as px
import pandas as pd
import numpy as np


# base all globally used variables
dictionary = {}
args = (sys.argv)
args.pop(0)
seenlist = []
processtimes = []
datetimes = []
times = []
wantedfile = []
start = datetime.now()
today = datetime.today()
year = today.year

# base all args as None so they can be checked if they are set
helptext = None
wantedtime = None
wantedgoid = None
wantedpath = None
wantednode = None
wantedgoid2 = None
failed = None
graph = None


# get the command line arguments as a list.
# go through the arguments list and find any matching
# arguments.
# set the matching argument values to the rigth variable
argslenght = len(args)
for index, obj in enumerate(args):
    if obj.lower() == '--help' or obj.lower() == '-h':
        helptext = True
        print(
            'list of arguments:\n'
            '   --goid or -g\n   --time or -t\n   --failed or -f\n   '
            '--node, -n or Id:\n'
            '   --path or -p\n   --file or -f\n'
            '   --graph\n'
            '* goid is used to search for a certain goid from'
            ' the files. (example --goid 1,2145,0,303)\n'
            '  goid can also be searched directly by pasting'
            ' in the given goid (example GOID:[1,1234,0,103])'
            ' without giving the --goid parameter.\n'
            '* time is used to print only goids that took'
            ' longer than the set time. (example --time 60)\n'
            '* node is used to search for the set node id.'
            '(example --node 2 / Id: 2)\n'
            '* failed will print all goids that has failed.'
            '(example --failed)\n'
            '* path will set the searched folder as the given string.'
            '(example --path C:/Users/user/Documents/solmsg)\n'
            '* file will search only the given file.'
            '(example --file C:/Users/user/Documents/solmsg'
            '/tsnc/tsnc_master/solmsg.out)\n'
            '* graph can be used with a single given goid '
            'or a node id, and it will make a timeline '
            'graph out of that '
            'which will open in a browser window.\n'
            '  (example --graph GOID:[1,1234,0,103]) or '
            '(example --graph Id: 2)'
        )
    elif obj.lower() == '--goid' or obj.lower() == '-g':
        if index < (argslenght - 1):
            next = args[index + 1]
            wantedgoid = next
        else:
            sys.exit('to use --goid/-g give a goid after.')
    elif obj.lower() == '--time' or obj.lower() == '-t':
        if index < (argslenght - 1):
            next = args[index + 1]
            wantedtime = next
        else:
            sys.exit('to use --time/-t give a time in seconds after.')
    elif obj.lower() == '--failed':
        failed = True
    elif obj.lower() == '--node' or obj == 'Id:' or obj.lower() == '-n':
        if index < (argslenght - 1):
            next = args[index + 1]
            wantednode = next
        else:
            sys.exit('to use --node/-n give a node id after.')
    elif obj.lower() == '--path' or obj.lower() == '-p':
        if index < (argslenght - 1):
            next = args[index + 1]
            wantedpath = next
        else:
            sys.exit('to use --path/-p give a path after.')
    elif obj.lower() == '--file' or obj.lower() == '-f':
        if index < (argslenght - 1):
            next = args[index + 1]
            wantedfile.append(next)
        else:
            sys.exit('to use --file/-f give a file location after.')
    elif obj.lower() == '--graph':
        graph = True
    elif 'GOID:[' in obj:
        wantedgoid2 = obj


# this converts the seconds give in the args,
# to datetime usable format.
def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)


# this converts the given times to datetime format,
# which can be used to compare process lenght.
def time_conveter(var1, var2):
    convtime = convert(int(var1))+".000"
    convtime = datetime.strptime(convtime, '%H:%M:%S.%f')
    timedict = dictionary[var2]
    if timedict[-1] == "0:00:00":
        timedict[-1] = timedict[-1]+".000"
    try:
        convtimedict = datetime.strptime(timedict[-1], '%H:%M:%S.%f')
    except (ValueError):
        timedict = timedict[-1] + ".000"
        convtimedict = datetime.strptime(timedict, '%H:%M:%S.%f')
    return convtime, convtimedict


def fileparser(givenfile):
    # get the file that is to be parsed
    lasttime = datetime.now() - start
    x = ['based here']
    with open(givenfile) as f:
        # go through the file.
        previousline = ''
        for line in f:
            if line[0:4] != str(year):
                previousline = previousline.strip("\n")
                line = previousline + line
            else:
                previousline = line
            # check if the line is valid (has year at the start)
            # combine last and current line if is not valid
            if goidsearch in line.strip("\n"):
                # find all lines that have the given search in them.
                if len(x) > 1 and x[0] in line:
                    # if it has been seen, add it as a value to the given key.
                    dictionary[i].append(line)
                else:
                    x = re.findall(r"GOID.*?]", line)
                    if x in seenlist:
                        for i in x:
                            dictionary[i].append(line)
                    else:
                        for i in x:
                            # if it has not been seen,
                            # add it as a dictionary key.
                            dictionary[i] = [line]
                        seenlist.append(x)
                        # and add it to the seen list.
    print("parsing done on file " + givenfile)
    print("time spent", datetime.now() - start - lasttime)
    lasttime = datetime.now() - start


def textprinter():
    for y, l in zip(dictionary.values(), dictionary.keys()):
        processtimes.append(y[0])
        processtimes.append(y[-1])
        # get the first and last line of a key, split it.
        for item in processtimes:
            split = item.split()
            inttime = datetime.strptime(split[1], '%H:%M:%S.%f')
            datetimes.append(inttime)
            # take only the time from it.
        processlenght = (datetimes[1] - datetimes[0])
        # get the time it took for the GOID,
        # by subracting the starting time from the ending time.
        times.append(str(processlenght))
        dictionary[l].append(str(processlenght))
        # add it to the end of the dictionarys value.
        list.clear(datetimes)
        list.clear(processtimes)
        # clear the 2 lists for usage in the next loop.

    if failed is None:
        if wantedtime is None:
            # check if time arg is set or not
            # if it is not set, go through normally and show all data
            for x, y in zip(dictionary.keys(), dictionary.values()):
                print("")
                print(x)
                for i in y:
                    print(i, end="")
                print("")
            if helptext is not True:
                print("\n"+"__________________________________")
                print("start of times")
            for g, t in zip(dictionary.keys(), times):
                x = dictionary[g]
                print(x[0], end="")
                print(x[-2], end="")
                print(g)
                print("process took:", t[:-3])
                print('-------------------------------------------------')
        else:
            # if its set, then send the variables needed to the time_converter,
            # to turn the values into datetime format so they can be compared,
            # and only wanted data will show.
            # do the same for all the lines from the files,
            # and a compacted version for easier searching
            for o in dictionary.keys():
                convertedtimes = time_conveter(wantedtime, o)
                if convertedtimes[1] >= convertedtimes[0]:
                    print("")
                    print(o)
                    for i in dictionary[o]:
                        print(i, end="")
                    print("")
            print("\n"+"__________________________________")
            print("start of times")
            for o in dictionary.keys():
                convertedtimes = time_conveter(wantedtime, o)
                if convertedtimes[1] >= convertedtimes[0]:
                    printtime = str(convertedtimes[1]).split(" ")
                    millisecondtest = printtime[1].split(".")
                    if len(millisecondtest) < 2:
                        printtime = printtime[1]
                    else:
                        printtime = printtime[1][:-3]
                    x = dictionary[o]
                    print(x[0], end="")
                    print(x[-2], end="")
                    print(o)
                    print(printtime)
                    print('-------------------------------------------------')
    else:
        print("failed processes. search using goid for more info")
        for x in dictionary.keys():
            for i in dictionary[x]:
                if "failed:" in i:
                    if x not in seenlist:
                        print(i, end="")
                        seenlist.append(x)
    list.clear(seenlist)


# graphbuilder gets the dict from graphmaker,
# and then shows the completed graph.
def graphbuilder(graphlist, yname):
    df = pd.DataFrame(graphlist)
    cm = {x: x for x in df.color.unique()}
    fig = px.timeline(data_frame=df,
                      x_start="start", x_end="finish",
                      y=yname, hover_name="info",
                      color='color',
                      color_discrete_map=cm)
    fig.update_yaxes(autorange="reversed")
    fig.show()


def graphmaker():
    if wantedgoid or wantedgoid2:
        # check if either of the goid args are set
        nodes = {}
        nodeseenlist = []
        for x in dictionary.keys():
            # group the lines by node
            for u in dictionary[x]:
                y = re.findall(r"Id:..", u)
                if y not in nodeseenlist:
                    for i in y:
                        nodes[i] = [u]
                    nodeseenlist.append(y)
                else:
                    for i in y:
                        nodes[i].append(u)
        list.clear(nodeseenlist)
        graphlist = []
        pluslastone = False
        # sort the dict before making the dataframe for the graph
        sorted_nodes = sorted(nodes.items(), key=lambda x: x[0])
        nodes = dict(sorted_nodes)
        for x in nodes.keys():
            nodelista = nodes[x]
            nodeindex = 0
            lastone = np.datetime64('2023-01-01 00:00:00.000')
            color = 'lightgreen'
            for y in range(len(nodelista)):
                # this makes the dataframe for the graphbuilder.
                # it gets the start time of itself,
                # and the end time is the start time of the next one.
                now = nodelista[nodeindex]
                try:
                    next = nodelista[nodeindex+1]
                except IndexError:
                    next = nodelista[nodeindex]
                    pluslastone = True
                now = now.split(" ")
                next = next.split(" ")
                now = now[0]+"T"+now[1]
                next = next[0]+"T"+next[1]
                startime = np.datetime64(now)
                endtime = np.datetime64(next)
                if startime <= lastone:
                    startime = lastone+1
                if endtime <= startime:
                    endtime = startime+1
                lastone = startime
                # check if lastone check is set.
                # add the data into the dataframe.
                if pluslastone is False:
                    graphlist.append(dict(Node=x[4],
                                          start=startime,
                                          finish=endtime,
                                          info=nodelista[nodeindex],
                                          color=color))
                else:
                    graphlist.append(dict(Node=x[4], start=startime,
                                          finish=endtime+1,
                                          info=nodelista[nodeindex],
                                          color=color))
                if color == 'lightgreen':
                    color = 'lightblue'
                else:
                    color = 'lightgreen'
                nodeindex = nodeindex+1
        graphbuilder(graphlist, 'Node')
    if wantednode:
        # check if node is set.
        graphlist = []
        color = 'lightgreen'
        lastend = np.datetime64('2023-01-01 00:00:00.000')
        lastend2 = np.datetime64('2023-01-01 00:00:00.000')
        for x in dictionary.keys():
            # get all the goids with the wanted node id.
            # make them into start and end times.
            goid = dictionary[x]
            first = goid[0]
            last = goid[-1]
            first = first.split(" ")
            last = last.split(" ")
            first = first[0]+"T"+first[1]
            last = last[0]+"T"+last[1]
            startime = np.datetime64(first)
            endtime = np.datetime64(last)
            # add them into the dataframe.
            # put them on 3 different lines to avoid,
            # overlapping as much as possible.
            if startime <= lastend:
                if startime <= lastend2:
                    graphlist.append(dict(row='3',
                                          start=startime,
                                          finish=endtime,
                                          info=x,
                                          color=color))
                else:
                    graphlist.append(dict(row='2',
                                          start=startime,
                                          finish=endtime,
                                          info=x,
                                          color=color))
                    lastend2 = endtime
            else:
                graphlist.append(dict(row='1',
                                      start=startime,
                                      finish=endtime,
                                      info=x,
                                      color=color))
                lastend = endtime
            if color == 'lightgreen':
                color = 'lightblue'
            else:
                color = 'lightgreen'
        graphbuilder(graphlist, 'row')


# check which way the wanted goid or node is set
# and set the used goidsearch variable as that.
if wantedgoid2 is None:
    if wantedgoid is None:
        if wantednode is None:
            goidsearch = "GOID:"
        else:
            goidsearch = "Id: "+wantednode
    elif "GOID:[" in wantedgoid:
        goidsearch = wantedgoid
    elif "[" in wantedgoid:
        goidsearch = "GOID:"+wantedgoid
    else:
        goidsearch = "GOID:["+wantedgoid
else:
    goidsearch = wantedgoid2


# see if path argument and file argument were given.
# if not then default folder and path.
if helptext is not True:
    if wantedpath is None:
        if len(wantedfile) < 1:
            path = 'tsnc*'
            for outfile in glob.glob(path):
                for innerfile in glob.glob(outfile+'/tsnc_master/solmsg.*'):
                    x = fileparser(innerfile)
    # if path is give search file from the given path.
    else:
        path = wantedpath+'/tsnc*'
        path = path.replace(r" \ ", "/")
        for outfile in glob.glob(path):
            for innerfile in glob.glob(outfile+'/tsnc_master/solmsg.*'):
                x = fileparser(innerfile)
    # if file is given search through the given file.
    if len(wantedfile) > 0:
        for x in wantedfile:
            file = x
            file = file.replace(r" \ ", "/")
            for innerfile in glob.glob(file):
                x = fileparser(innerfile)
    # clear the seenlist for further use.
    list.clear(seenlist)


# sort the dictionarys value lists in order of time,
# the sort the dictionary keys in order of time aswell.
for x in dictionary.values():
    x.sort(key=lambda x: x.split()[1])
sorted_dict = sorted(dictionary.items(), key=lambda x: x[0])
dictionary = dict(sorted_dict)

if graph is None:
    textprinter()
else:
    graphmaker()
