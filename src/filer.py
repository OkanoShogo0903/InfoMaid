import random
import os,sys
# ファイルのurlを渡すと、その中にあるランダムなファイルもしくはディレクトリのurlが返ってくる
def GetFileName(url):
#    pos = ('../etcs/Audio/Init')
    directory = os.listdir(url)
    lenght = len(directory)

    if lenght != 0 :
        r = random.randint(0,lenght-1)
        print(r)
        print(url + '/' + directory[r])
        return url + '/' + directory[r]
    # ファイルが無ければNoneを返す
    else :
        return None

def GetFileNum(sInFdr):
    """ファイル数取得
    Args:
        sInFdr:入力フォルダ
    Returns:
        ファイル数
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

