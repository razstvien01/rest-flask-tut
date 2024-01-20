import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld")\
# # response = requests.post(BASE + "helloworld")
# print(response.json())

# response = requests.put(BASE + "video/1", {"likes": 10, "name": "Nico", "views": 100000})
# print(response.json())

data = [{"likes": 72020, "name": "Nico", "views": 100000}, 
        {"likes": 593932, "name": "How to sleep", "views": 200240}, 
        {"likes": 23221, "name": "Kimo", "views": 782423}]

for i in range(len(data)):
  response = requests.put(BASE + "video/" + str(i), data[i])
  print(response.json())

input()

response = requests.delete(BASE + "video/0")
print(response)

input()

response = requests.get(BASE + "video/2")
print(response.json())