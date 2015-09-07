# -*- coding: utf-8 -*-

import sys
import requests
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf8')

api_key = 'please enter your douban api_key'

class DoubanDataFetcher:

  def __init__(self, user_id):
    if user_id == None:
      raise ValueError("\"" + user_id + "\"" + " : can not be empty.")
    else:
      self.user_id = user_id
      if api_key != None:
        self.api_key = api_key
    self.base_url = 'https://api.douban.com/v2/book/user/' + self.user_id + '/collections?'

  def get_wish_nums(self):
    #https://api.douban.com/v2/book/user/81024152/collections?status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      wish_url = self.base_url + 'status=wish&apikey=' + self.api_key
    else:
      wish_url = self.base_url + 'status=wish'
    r = requests.get(wish_url)
    return r.json()["total"]

  def get_reading_nums(self):
    if self.api_key != None:
      wish_url = self.base_url + 'status=reading&apikey=' + self.api_key
    else:
      wish_url = self.base_url + 'status=reading'
    r = requests.get(wish_url)
    return r.json()["total"]

  def get_read_nums(self):
    #https://api.douban.com/v2/book/user/81024152/collections?status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      wish_url = self.base_url + 'status=read&apikey=' + self.api_key
    else:
      wish_url = self.base_url + 'status=read'
    r = requests.get(wish_url)
    return int(r.json()["total"])

def show_nums(wish_nums, reading_nums, read_nums):
  labels = 'wish_read', 'be_reading', 'has_read'
  sizes = [wish_nums, reading_nums, read_nums]
  #sizes = [46, 12, 41]
  colors = ['yellowgreen', 'gold', 'lightskyblue']
  #explode = (0, 0.1, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
  #plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
  plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
  # Set aspect ratio to be equal so that pie is drawn as a circle.
  plt.axis('equal')
  plt.show()

def main():
  dataer = DoubanDataFetcher('please enter your douban_id')
  show_nums(dataer.get_wish_nums(), dataer.get_reading_nums(), dataer.get_read_nums())

if __name__ == '__main__':
  main()
