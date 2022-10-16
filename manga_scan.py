def sub_text(s):

    s = s.lower()
    s = re.sub('\W+','',s)
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('đ', 'd', s)
    return s

def fau_nettruyen_new_chap():
    list_new_chap = {}
    manga_file = open("list_favorite_manga.txt","r")
    list_manga = json.loads(manga_file.read())
    manga_file.close()
    
    class MyHTMLParser(HTMLParser):
        runs = True
        current_manga = ""
        def handle_starttag(self, tag, attrs):
            if tag == "a" and self.runs:
                try:
                    if attrs[0][0] == "href" and attrs[1][0] == "data-id":
                        i = len(attrs[0][1]) - 1
                        while attrs[0][1][i] != "/":
                            i-=1
                        j = i - 1
                        while attrs[0][1][j] != "-":
                            j -= 1
                        chap = float(attrs[0][1][j+1:i])
                        if chap > list_manga[self.current_manga]["chapter"]:
                            list_new_chap[self.current_manga] = chap
                        self.runs = False
                except:
                    pass
        
    parser = MyHTMLParser()
    for fau_manga in list_manga:
        parser.current_manga = fau_manga
        url = "http://www.nettruyen.com/truyen-tranh/" + fau_manga + "/"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        res = response.read().decode('utf-8')
        parser.feed(res)
        parser.runs = True
    
    words = "The mangas that have new chapters are\n"
    for new in list_new_chap:
        words += new + "  chapter " + str(list_new_chap[new]) +"\n"

    return words
    
def nettruyen_scan(start = 1,index = 1):

    manga_file = open("list_manga.txt","r")
    list_manga = json.loads(manga_file.read())
    manga_file.close()

    class GetMangaName(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "a":
                try:
                    if attrs[0][0] == "title" and attrs[1][0] == "href":
                        if attrs[1][1][0:38] == "http://www.nettruyen.com/truyen-tranh/" and attrs[1][1] not in list_manga:
                            list_manga[attrs[1][1]] = {"views":0,"genre":[],"status":"","chapter":0.0}
                except:
                    pass

    page = start
    parser = GetMangaName()
    while page <= index:
        try:
            url = "http://www.nettruyen.com/?page=" + str(page)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            res = response.read().decode('utf-8')
            parser.feed(res)
            page += 1
            time.sleep(0.2)
        except:
            time.sleep(0.1)
        
           
    class GetMangaInfor(HTMLParser):
        is_tinhtrang = False
        is_theloai = False
        is_luotxem = False
        current_manga = ""
        is_run = True
        def handle_starttag(self, tag, attrs):
            if self.is_run:
                if tag == "a":
                    try:
                        if attrs[0][0] == "href" and attrs[1][0] == "data-id":
                            data = attrs[0][1]
                            i = len(data)-1
                            while data[i] != "/":
                                i-=1
                            j = i-1
                            while data[j] != "-":
                                j-=1
                            list_manga[self.current_manga]["chapter"] = float(data[j+1:i])
                            self.is_run = False
                    except:
                        pass

        def handle_data(self, data):

            if self.is_luotxem:
                data = sub_text(data)
                if data != "":
                    list_manga[self.current_manga]["views"] = int(data)
                    self.is_luotxem = False

            if self.is_theloai and  "Lượt xem" in data:
                self.is_theloai = False
                self.is_luotxem = True

            if self.is_theloai:
                data = sub_text(data)
                if data != "":
                    list_manga[self.current_manga]["genre"].append(data)

            if self.is_tinhtrang and  "Thể loại" in data:
                self.is_tinhtrang = False
                self.is_theloai = True
            
            if self.is_tinhtrang:
                data = sub_text(data)
                if data != "":
                    list_manga[self.current_manga]["status"] = data

            if "Tình trạng" in data:
                self.is_tinhtrang = True
    
    parser_se = GetMangaInfor()
    for manga_url in list_manga:
        try:
            parser_se.is_run = True
            parser_se.current_manga = manga_url
            request = urllib.request.Request(manga_url)
            response = urllib.request.urlopen(request)

            res = response.read().decode('utf-8')
            parser_se.feed(res)
            time.sleep(0.2)
        except:
            time.sleep(0.1)

    with open("list_manga.txt","w") as f:
        json.dump(list_manga,f)






numbers = "0123456789."
def hocvientruyentranh_scaner(start,index):
    
    manga_file = open("d:\list_manga_beta.txt","r")
    list_manga_beta = json.loads(manga_file.read())
    manga_file.close()
    
    headers = {"authority": "hocvientruyentranh.net",
            "method": "GET",
            "path": "",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}
    
    class GetMangaName(HTMLParser):
        def handle_starttag(self, tag, attrs):
            #print("{} : {}".format(tag,attrs))
            if tag == "a":
                try:
                    if attrs[0][0] == "href" and attrs[1][0] == "title":
                        if attrs[0][1][0:48] == "https://hocvientruyentranh.net/index.php/truyen/" and attrs[0][1] not in list_manga_beta and attrs[0][1][48:51] != "all":
                            list_manga_beta[attrs[0][1]] = {"views":0,"genre":[],"status":"","chapter":[0.0,0],"author":""}
                except:
                    pass

    page = start
    parser_se = GetMangaName()
    while page <= index:
        try:
            url = "https://hocvientruyentranh.net/index.php/truyen/all?page=" + str(page)
            headers["path"] = url
            request = urllib.request.Request(url,headers=headers)
            response = urllib.request.urlopen(request)

            content = brotli.decompress(response.read())
            parser_se.feed(content.decode("utf-8"))
            print("page {}/{}".format(page,index),end="\r")
            page += 1
            time.sleep(0.2)
        except:
            print("error in page: "+page)
    
    print("\n")

    with open("d:\list_manga_beta.txt","w") as f:
        json.dump(list_manga_beta,f)

    class GetMangaInfor(HTMLParser):
        is_tinhtrang = False
        is_theloai = False
        theloai = True
        is_tacgia = False
        is_chapter = False
        is_last_chapter = True
        time = False
        cout_chap = 0
        total_view = 0
        current_manga = ""

        def handle_data(self, data):
            if self.is_chapter:
                if self.time and self.is_last_chapter:
                    data = data.replace("\r","")
                    data = data.replace("\n","")
                    if data != "" and data != " ":
                        c = data.split(" ")
                        if c[1] == "years" or c[1] == "year":
                            list_manga_beta[self.current_manga]["chapter"][1] = int(c[0])*365
                        if c[1] == "month" or c[1] == "months":
                            list_manga_beta[self.current_manga]["chapter"][1] = int(c[0])*30
                        if c[1] == "week" or c[1] == "weeks":
                            list_manga_beta[self.current_manga]["chapter"][1] = int(c[0])*7
                        if c[1] == "day" or c[1] == "days":
                            list_manga_beta[self.current_manga]["chapter"][1] = int(c[0])
                        self.is_last_chapter = False
                        self.time = False


                if "lượt xem" in data:
                    p = 0
                    while data[p] != " ":
                        p += 1
                    self.total_view += float(data[0:p].replace(",",""))
                    self.cout_chap += 1
                    if self.is_last_chapter:
                        self.time = True
                    
            if "/* * *" in data and self.is_chapter:
                self.is_chapter = False
                
    
            if self.is_tinhtrang:
                data = sub_text(data)
                if data != "":
                    list_manga_beta[self.current_manga]["status"] = data
                    self.is_tinhtrang = False

            if "Tình trạng" in data:
                self.is_tinhtrang = True

            if self.is_tacgia:
                data = sub_text(data)
                if data != "":
                    list_manga_beta[self.current_manga]["author"] = data
                    self.is_tacgia = False

            if self.is_theloai and  "Tác giả:" in data:
                self.is_theloai = False
                self.is_tacgia = True
                
            if self.is_theloai:
                data = sub_text(data)
                if data != "":
                    list_manga_beta[self.current_manga]["genre"].append(data)
            if "Thể loại:" in data and self.theloai:
                self.is_theloai = True
                self.theloai = False

            if "Thời gian đăng" in data:
                self.is_chapter = True
    
    manga_file = open("d:\list_manga_beta.txt","r")
    list_manga_beta = json.loads(manga_file.read())
    manga_file.close()
    
    fail_list = []
    parser = GetMangaInfor()
    l = len(list_manga_beta)
    co = 1
    for manga_url in list_manga_beta:
        try:
            headers["path"] = manga_url
            parser.current_manga = manga_url
            request = urllib.request.Request(manga_url,headers=headers)
            response = urllib.request.urlopen(request)
            content = brotli.decompress(response.read())
            parser.feed(content.decode("utf-8"))
            list_manga_beta[manga_url]["chapter"][0] = parser.cout_chap
            list_manga_beta[manga_url]["views"] = int(parser.total_view/parser.cout_chap)
            parser.cout_chap = 0
            parser.total_view = 0
            parser.is_last_chapter = True
            parser.time = False
            parser.theloai = True
            print("manga {}/{}".format(co,l),end="\r")
            co += 1
            time.sleep(0.3)
        except:
            fail_list.append(manga_url)
    with open("d:\list_manga_beta.txt","w") as f:
        json.dump(list_manga_beta,f)

    for manga_url in fail_list:
        try:
            headers["path"] = manga_url
            parser.current_manga = manga_url
            request = urllib.request.Request(manga_url,headers=headers)
            response = urllib.request.urlopen(request)
            content = brotli.decompress(response.read())
            parser.feed(content.decode("utf-8"))
            list_manga_beta[manga_url]["chapter"][0] = parser.cout_chap
            list_manga_beta[manga_url]["views"] = int(parser.total_view/parser.cout_chap)
            parser.cout_chap = 0
            parser.total_view = 0
            parser.is_last_chapter = True
            parser.time = False
            parser.theloai = True
            time.sleep(0.4)
        except:
            print("drop: "+manga_url)

    print("\n\n done")
    with open("d:\list_manga_beta.txt","w") as f:
        json.dump(list_manga_beta,f)