import difflib
import tokiponadict as tpd
import json
import sys
from operator import itemgetter

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ct: correct translation
# ew: english words
# ec: english checked
# tw: toki words

def spellcheck(ew):
    accept = True
    if ew in tpd.toki:
        ec = ew
    else:
        try:
            closest_key = difflib.get_close_matches(ew, tpd.toki.keys())
            print "Did you mean: " + bcolors.WARNING + str(closest_key[0]) + bcolors.ENDC + "?"
            if len(closest_key) > 1:
                print "Other hits:"
                for i in range(len(closest_key)-1):
                    print closest_key[i+1]
            checkacc = raw_input("y/n: ")
            if checkacc == "y":
                accept = True
                ec = closest_key[0]
            elif checkacc == "n":
                print "Well, I don't know what that means, though"
                accept = False
                ec = closest_key[0]
        except:
            print "New entry"
            correction = raw_input("What does \"" + str(ew) + "\" mean? ")
            tokinew = tpd.toki
            tokinew[ew] = []
            tokinew[ew].append((str(correction), 2))
            writetoki(tokinew)
            sys.exit(0)
    return ec, accept

def translate(ec, accept):
    maxi = sorted(tpd.toki[ec], key=itemgetter(1))
    tw = maxi[-1][0]
    if accept:
        print ec + " ---> "  + bcolors.OKBLUE + tw + bcolors.ENDC
    else:
        print ew + " ---> "  + bcolors.OKBLUE + tw + bcolors.ENDC
    return tw

def writetoki(tokinew):
    with open("Code/tokiponadict.py", "w") as file:
        file.write("toki = " + json.dumps(tokinew))

def correct(tw, ct, ec, ew, accept):
    tokinew = tpd.toki
    if tw == ct:
        maxi = sorted(tokinew[ec], key=itemgetter(1))
        maxi[-1][1] += 1
        writetoki(tokinew)
    else:
        if accept:
            print ec + " ---> "  + bcolors.OKGREEN + ct + bcolors.ENDC
            tokinew[ec].append([str(ct), 2])
        else:
            print "New entry: "
            print ew + " ---> "  + bcolors.OKGREEN + ct + bcolors.ENDC
            tokinew[ew].append([str(ct), 2])
    writetoki(tokinew)

eng = raw_input("English word: ")
ew = eng
ec, accept = spellcheck(ew)
tw = translate(ec, accept)
correction = raw_input("Offer a better translation: ")
if correction != "":
    ct = correction
    if accept:
        tokinew = tpd.toki
        for i in range(len(tokinew[ec])):
            if tokinew[ec][i][0] == ct:
                tokinew[ec][i][1] += 1
                writetoki(tokinew)
                sys.exit(0)
    else:
        tokinew = tpd.toki
        tokinew[ew] = []
        tokinew[ew].append((str(ct), 2))
        writetoki(tokinew)
        sys.exit(0)
    correct(tw, ct, ec, ew, accept)
else:
    if accept:
        tokinew = tpd.toki
        maxi = sorted(tokinew[ec], key=itemgetter(1))
        maxi[-1][1] += 1
        writetoki(tokinew)
    else:
        tokinew = tpd.toki
        tokinew[ew] = []
        tokinew[ew].append((str(tw), 2))
        writetoki(tokinew)
        sys.exit(0)
