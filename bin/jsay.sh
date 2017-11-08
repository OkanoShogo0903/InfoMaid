#!/bin/sh
 
# 引数チェック
CMDNAME=`basename $0`
if [ $# -lt 1 ]; then
    echo "Usage: ${CMDNAME} [ text ]" 1>&2
    exit 1
fi
 
 
# 定数定義（出力ファイル名、辞書の場所、音声データの場所）
TMPFILE=`mktemp /tmp/tmp.XXXXXXXX.wav`
DIC=/usr/local/share/open_jtalk/open_jtalk_dic_utf_8-1.08/
VOICE=/usr/local/share/hts_voice/mei/mei_normal.htsvoice
 
 
# 音声データ生成
echo "$1" | open_jtalk \
-x ${DIC} \
-m ${VOICE} \
-ow ${TMPFILE} && \
 
 
# 生成した音声データを再生する
aplay --quiet ${TMPFILE}
 
 
# 生成した音声データを削除する
rm -f ${TMPFILE}
 
# 終了
exit 0
