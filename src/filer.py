import random
import os,sys
# $B%U%!%$%k$N(Burl$B$rEO$9$H!"$=$NCf$K$"$k%i%s%@%`$J%U%!%$%k$b$7$/$O%G%#%l%/%H%j$N(Burl$B$,JV$C$F$/$k(B
def GetFileName(url):
#    pos = ('../etcs/Audio/Init')
    directory = os.listdir(url)
    lenght = len(directory)

    if lenght != 0 :
        r = random.randint(0,lenght-1)
        print(r)
        print(url + '/' + directory[r])
        return url + '/' + directory[r]
    # $B%U%!%$%k$,L5$1$l$P(BNone$B$rJV$9(B
    else :
        return None

def GetFileNum(sInFdr):
    """$B%U%!%$%k?t<hF@(B
    Args:
        sInFdr:$BF~NO%U%)%k%@(B
    Returns:
        $B%U%!%$%k?t(B
    """
    if not os.path.isdir(sInFdr): return 0
    i=0
    for root, dirs, files in os.walk(sInFdr):
        i+=len(files)
    return i

if __name__=="__main__":
    print(GetFileNames(sys.argv[1]))

#    sInFdr=sys.argv[1]
#    print (GetFileNum(sInFdr))

