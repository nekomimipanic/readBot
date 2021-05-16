import subprocess
import re
import tempfile

# ************************************************
# remove_custom_emoji
# 絵文字IDは読み上げない
# ************************************************
def remove_custom_emoji(text):
    
    #pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    pattern = r'<:'    # カスタム絵文字のパターン
    text = re.sub(pattern,'',text)   # 置換処理
    pattern = r':[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# url_shouryaku
# URLなら省略
# ************************************************
def url_shouryaku(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URLは省略するのデス！',text)   # 置換処理

# ************************************************
# remove_picture
# 画像ファイルなら読み上げない
# ************************************************
def remove_picture(text):
    pattern = r'.*(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_command
# コマンドは読み上げない
# ************************************************
def remove_command(text):
    pattern = r'^\!.*'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_log
# 参加ログは読み上げない
# ************************************************
def remove_log(text):
    pattern = r'(\【VC参加ログ\】.*)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_nl
# 改行殺し 
# ************************************************
def remove_lf(text):
    return ''.join(text.splitlines())   # 置換処理

# ************************************************
# user_custom
# ユーザ登録した文字を読み替える
# ************************************************
def user_custom(text):

    f = open('/opt/readBot-master/dic.txt', 'r')
    line = f.readline()

    while line:
        pattern = line.strip().split(',')
        if pattern[0] in text and len(pattern) >= 2:
            text = text.replace(pattern[0], pattern[1])
            print('置換後のtext:'+text)
            break
        else:
            line = f.readline()
    f.close()

    return text



# ************************************************
# creat_WAV
# message.contentをテキストファイルと音声ファイルに書き込む
# 引数：inputText
# 書き込みファイル：input.txt、output.wav
# ************************************************
def creat_WAV(inputText,voice_path):
        # message.contentをテキストファイルに書き込み

    inputText = remove_custom_emoji(inputText)   # 絵文字IDは読み上げない
    inputText = remove_command(inputText)   # コマンドは読み上げない
    inputText = url_shouryaku(inputText)   # URLなら省略
    inputText = remove_picture(inputText)   # 画像なら読み上げない
    inputText = remove_log(inputText)   # 参加ログなら読み上げない
    inputText = remove_lf(inputText)   # 改行削除 
    inputText = user_custom(inputText)   # ユーザ登録した文字を読み替える
    with tempfile.NamedTemporaryFile(mode='w') as tmp:
        tmp.write(inputText)
        tmp.seek(0)
    speed = 0.8 
    dic_path = "/var/lib/mecab/dic/open-jtalk/naist-jdic/"
    model_path = "/usr/share/hts-voice/mei/mei_normal.htsvoice"
    model_path = "/usr/share/hts-voice/tohoku-f01/tohoku-f01-neutral.htsvoice"
#    voice_path="/tmp/output.wav"

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        tmp.write(inputText)
        tmp.seek(0)
        command = 'open_jtalk -g -5 -a 0.6 -x {} -m {} -r {} -ow {} {}'.format(dic_path, model_path, speed, voice_path, tmp.name)
        print(command)
#        tmp.close()
        proc = subprocess.run(
            command,
            shell  = True,
        )

if __name__ == '__main__':
    creat_WAV('テスト')
