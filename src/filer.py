import random
import os,sys
# ファイルのurlを渡すと、その中にあるランダムなファイルもしくはディレクトリのurlが返ってくる
def getFileName(_url):
#    pos = ('../etcs/Audio/Init')
    directory = os.listdir(_url)
    lenght = len(directory)

    if lenght != 0 :
        r = random.randint(0,lenght-1)
        print(r)
        print(_url + '/' + directory[r])
        return _url + '/' + directory[r]
    # ファイルが無ければNoneを返す
    else :
        return None

def getFileNum(_sInFdr):
    """ファイル数取得
    Args:
        _sInFdr:入力フォルダ
    Returns:
        ファイル数
    """
    if not os.path.isdir(_sInFdr): return 0
    i=0
    for root, dirs, files in os.walk(_sInFdr):
        i+=len(files)
    return i

if __name__=="__main__":
    print(getFileNames(sys.argv[1]))

#    _sInFdr=sys.argv[1]
#    print (GetFileNum(_sInFdr))

