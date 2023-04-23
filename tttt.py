import subprocess

# Git logコマンドでコミットログを取得する
vagrant_result = subprocess.run(
    ['rm', '-R', 'test.py'], stdout=subprocess.PIPE)
