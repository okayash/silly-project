import requests

url = "https://www.popmart.com/us/products/1604/Hirono-×-Le-Petit-Prince-Series-Figures"
response = requests.get(url)
print(response.text[:2000]) 