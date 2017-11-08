import os,sys
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
    sInFdr=sys.argv[1]
    print (GetFileNum(sInFdr))
