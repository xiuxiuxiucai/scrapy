import requests
import re
import time
import os

# 爬取
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
response = requests.get("https://www.vmgirls.com/13344.html", headers=headers)
html = response.text
git
# 解析
dirName = re.findall('<h1 class="post-title h1">(.*?)</h1>', html)[-1]
if not os.path.exists(dirName):
    os.mkdir(dirName)
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
print(urls)

# 下载
i = 1
for url in urls:
    time.sleep(1)
    fileName = url.split('/')[-1]
    i += 1
    download = requests.get('https://www.vmgirls.com/' + url, headers=headers)
    with open(dirName + '/' + fileName, 'wb') as f:
        f.write(download.content)

    f.close()
