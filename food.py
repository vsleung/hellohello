from gevent import monkey
monkey.patch_all()
import gevent,requests, bs4, csv
from gevent.queue import Queue

work = Queue()
url_1 = 'http://www.boohee.com/food/group/{type}?page={page}'
for x in range(1, 11):
    for y in range(1, 11):
        real_url = url_1.format(type=x, page=y)
        work.put_nowait(real_url)

url_2 = 'http://www.boohee.com/food/view_menu?page={page}'
for x in range(1,11):
    real_url = url_2.format(page=x)
    work.put_nowait(real_url)

def crawler():
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    while not work.empty():
        url = work.get_nowait()
        res = requests.get(url, headers=headers)
        bs_res = bs4.BeautifulSoup(res.text, 'html.parser')
        foods = bs_res.find_all('li', class_='item clearfix')
        for food in foods:
            food_name = food.find_all('a')[1]['title']
            food_url = 'http://www.boohee.com' + food.find_all('a')[1]['href']
            food_calorie = food.find('p').text
            writer.writerow([food_name, food_calorie, food_url])
            #借助writerow()函数，把提取到的数据：食物名称、食物热量、食物详情链接，写入csv文件。
            print(food_name)

csv_file= open('boohee.csv', 'w', newline='')
#调用open()函数打开csv文件，传入参数：文件名“boohee.csv”、写入模式“w”、newline=''。
writer = csv.writer(csv_file)
# 用csv.writer()函数创建一个writer对象。
writer.writerow(['食物', '热量', '链接'])
#借助writerow()函数往csv文件里写入文字：食物、热量、链接

tasks_list = []
for x in range(5):
    task = gevent.spawn(crawler)
    tasks_list.append(task)
gevent.joinall(tasks_list)
