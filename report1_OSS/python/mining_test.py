# 「pip install requests」などが必要
import requests
import json
# import numpy as np

# リポジトリマイニングしたいURL
TensorFlow_URL = "https://api.github.com/repos/tensorflow/tensorflow/commits?per_page=100"

def get_git_data(url):
  print(url)
  response = requests.get(url)
  data = json.loads(response.text) # json文字列を辞書に変換 第一引数に文字列を指定すると辞書に変換される
  
  return data

# ===main関数部分開始==== #
print("TEST")

dict = get_git_data(TensorFlow_URL)

# f = open('../json_file/myfile.txt', 'w')
# f.write(get_git_data(TensorFlow_URL))
# f.close()
# np.save('../json_file/test.json', dict)
tf = open("../json_file/test.json", "w")
json.dump(dict,tf,  indent=2, ensure_ascii=False)
tf.close()