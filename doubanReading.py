# -*- coding: utf-8 -*-

import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

api_key = 'please enter your api_key'

class DoubanDataFetcher:

  def __init__(self, user_id):
    if user_id == None:
      raise ValueError("\"" + user_id + "\"" + " : can not be empty.")
    else:
      self.user_id = user_id
      if api_key != None:
        self.api_key = api_key
    self.base_url = 'https://api.douban.com/v2/book/user/' + self.user_id + '/collections?'

  def get_nums_by_status(self, status):
    #status: wish, read, reading
    #https://api.douban.com/v2/book/user/81024152/collections?status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      url = self.base_url + 'status=' + status + '&apikey=' + self.api_key
    else:
      url = self.base_url + 'status='+ status
    r = requests.get(url)
    return r.json()["total"]

  '''def get_wish_nums(self):
    #https://api.douban.com/v2/book/user/81024152/collections?status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      wish_url = self.base_url + 'status=wish&apikey=' + self.api_key
    else:
      wish_url = self.base_url + 'status=wish'
    r = requests.get(wish_url)
    return r.json()["total"]

  def get_reading_nums(self):
    if self.api_key != None:
      reading_url = self.base_url + 'status=reading&apikey=' + self.api_key
    else:
      reading_url = self.base_url + 'status=reading'
    r = requests.get(reading_url)
    return r.json()["total"]

  def get_read_nums(self):
    #https://api.douban.com/v2/book/user/81024152/collections?status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      read_url = self.base_url + 'status=read&apikey=' + self.api_key
    else:
      read_url = self.base_url + 'status=read'
    r = requests.get(read_url)
    return int(r.json()["total"])'''

  def get_month_infos(self):
    read_nums = self.get_nums_by_status('read')
    print read_nums
    #https://api.douban.com/v2/book/user/81024152/collections?count=48&status=wish&apikey=0ee5fc17c5bc35d92cb1f4475134a18b
    if self.api_key != None:
      read_url = self.base_url + 'count=' + str(read_nums) + '&status=read&apikey=' + self.api_key
    else:
      read_url = self.base_url + 'count=' + str(read_nums) +  + '&status=read'
    r = requests.get(read_url)
    print "got it"
    '''latest_date = r.json()["collections"][0].get("updated")
    latest_month = int(latest_date[5:7])
    max_month = latest_date
    print latest_date'''
    month_nums = [0 for i in range(33)]

    for t in r.json()["collections"]:
      updated_time = t.get("updated")
      if updated_time >= "2013-01-01" and updated_time <= "2015-09-01":
        #print updated_time
        if updated_time[0:4] == '2013':
          month_nums[int(updated_time[5:7])-1] = month_nums[int(updated_time[5:7])-1] + 1
        if updated_time[0:4] == '2014':
          month_nums[int(updated_time[5:7])-1+12] = month_nums[int(updated_time[5:7])-1+12] + 1
        if updated_time[0:4] == '2015':
          #print int(updated_time[5:7])-1+24
          month_nums[int(updated_time[5:7])-1+24] = month_nums[int(updated_time[5:7])-1+24] + 1

    return month_nums


def show_month_nums(month_nums):
  date1 = datetime.date(2013, 1, 1)
  date2 = datetime.date(2015, 8, 31)
  years = YearLocator()   # every year
  months = MonthLocator()  # every month
  yearsFmt = DateFormatter('%m/%d/%y')

  delta = datetime.timedelta(days=30)
  dates = drange(date1, date2, delta)
  print len(dates)
  #opens = [2,4,3,5,6,2,4,3,5,6,2,4,3,5,6,2,4,3,5,6,2,4,3,5,2,4,3,8,7]
  #seconds = [4,3,5,6,2,4,3,5,6,2,4,3,5,6,2,4,3,5,6,2,4,3,5,2,4,3,8,7,2]
  #sss = [4,3,3,1,2,4,3,5,6,2,4,3,5,6,2,4,3,5,6,2,4,3,5,2,4,3,8,7,2]
  fig, ax = plt.subplots()
  ax.plot_date(dates, month_nums, color='blue', linewidth=3, linestyle='-.')
  #ax.plot_date(dates, seconds, color='red', linewidth=3, linestyle=':')
  #ax.plot_date(dates, sss, color='yellow', linewidth=3, linestyle='--')

  # format the ticks
  ax.xaxis.set_major_locator(months)
  ax.xaxis.set_major_formatter(yearsFmt)
  #ax.xaxis.set_minor_locator(months)
  ax.autoscale_view()

  # format the coords message box
  #def price(x): return '$%1.2f'%x
  ax.fmt_xdata = DateFormatter('%Y-%m-%d')
  #ax.fmt_ydata = price
  ax.grid(True)

  fig.autofmt_xdate()
  #plt.title('blue:wish_read')# give plot a title
  plt.show()


def show_read_nums(wish_nums, reading_nums, read_nums):
  labels = 'to_read', 'be_reading', 'has_read'
  sizes = [wish_nums, reading_nums, read_nums]
  #sizes = [46, 12, 41]
  colors = ['yellowgreen', 'gold', 'lightskyblue']
  #explode = (0, 0.1, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
  #plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
  #plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
  plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
  # Set aspect ratio to be equal so that pie is drawn as a circle.
  plt.axis('equal')
  plt.show()


def main():
  #douban_id here
  dataer = DoubanDataFetcher('TualatriX')
  show_read_nums(dataer.get_nums_by_status('wish'), dataer.get_nums_by_status('reading'), dataer.get_nums_by_status('read'))
  show_month_nums(dataer.get_month_infos())

if __name__ == '__main__':
  main()