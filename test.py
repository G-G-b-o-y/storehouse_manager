html_raw = {}
page_list = ["model.html", "signItem.html", "itemInto.html", "outItem.html", "reportTable.html"]
for fileName in page_list:
    with open(f'htmlpages/{fileName}', 'r', encoding='utf-8') as f:
        data = f.read()   #读取文本
    
    html_raw[fileName[0:-5]] = data

print(html_raw['signItem'])