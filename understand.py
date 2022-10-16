import speek
import os
import keyboard
import google_search
import manga_scan

keyh = keyboard.Keyboard()
engine = speek.Engine()
envir = "desktop"





def open(content = ""):
    pass

def check(content = ""):
    pass

def find(content=""):
    pass

def close(content=""):
    pass



class Handle(object):

    def __init__(self):
        self.language = "vi-VN"
        self.is_in_conversation = False
        self.start_command = [["yukino",1],["hello",1],["hi",1]]
        self.list_command = [["yukino",1],["hello",1],["hi",1],["xong",2],["được rồi",2],["mở",3],["tìm kiếm",4],["tìm",4],["kiểm tra",5],["tra cứu",6],["tra",6],["tắt máy",7],["khởi động lại",8],["ngủ",9],["đóng",10],["chuyển",11],["hủy",12],["bật điều khiển tay",13],["tắt điều khiển tay,14"]]
        self.list_function = {1:self.start_conversation,2:self.stop_conversation,3:open,4:self.search,5:self.check_new_manga,6:find,7:self.shutdown,8:self.restart,9:self.sleep,10:close,12:self.cancel,13:self.hand_mode_on,14:self.hand_mode_off}
    
    def handle(self,text):
        if self.is_in_conversation:
            for comamd in self.list_command:
                if text[0:len(comamd[0])] == comamd[0]:
                    self.list_function[comamd[1]](text[len(comamd[0]):])
                    break
        else:
            for comamd in self.start_command:
                if text[0:len(comamd[0])] == comamd[0]:
                    self.list_function[comamd[1]](text[len(comamd[0])+1:])
                    break


    def start_conversation(self,content=""):
        
        if self.is_in_conversation == False:
            engine.text_to_speech("i'm here master \n what can i do for you")
            self.is_in_conversation = True
        else:
            engine.text_to_speech("i'm still here master")
    
    def stop_conversation(self,content=""):
        if self.is_in_conversation:
            engine.text_to_speech("conversation end.")
            self.is_in_conversation = False
    
    def restart(self,content = ""):
        box = content.split(" ")
        time_set = 0
        for i in range(0,len(box)):
            if box[i] == "tiếng" or box[i] == "giờ":
                try:
                    time_set += int(box[i-1])*3600
                except:
                    pass
            elif box[i] == "phút":
                try:
                    time_set += int(box[i-1])*60
                except:
                    pass
            elif box[i] == "giây":
                try:
                    time_set += int(box[i-1])
                except:
                    pass
        if time_set > 0:
            engine.text_to_speech("machine will restart after "+str(int(time_set/60))+" minutes")
        else:
            time_set = 10
            engine.text_to_speech("machine will restart now")

        os.system("shutdown.exe -r -t "+str(time_set))

    def shutdown(self,content = ""):
        box = content.split(" ")
        time_set = 0
        for i in range(0,len(box)):
            if box[i] == "tiếng" or box[i] == "giờ":
                try:
                    time_set += int(box[i-1])*3600
                except:
                    pass
            elif box[i] == "phút":
                try:
                    time_set += int(box[i-1])*60
                except:
                    pass
            elif box[i] == "giây":
                try:
                    time_set += int(box[i-1])
                except:
                    pass
        if time_set > 0:
            engine.text_to_speech("machine will shutdow after "+str(int(time_set/60))+" minutes")
        else:
            time_set = 10
            engine.text_to_speech("machine will shutdown now")

        os.system("shutdown.exe -s -t "+str(time_set))

    def cancel(self,content = ""):
    
        def cancel_shutdown_schedule():
            try:
                os.system("shutdown.exe -a")
            except:
                engine.text_to_speech("for some reason i can't cancel your shutdown schedule")

        list_command = {"tắt máy":1,"khởi động lại":1}
        list_function = {1:cancel_shutdown_schedule}

        for i in list_command:
            if i in content:
                list_function[list_command[i]]()
                break

    def sleep(self,content = ""):
        try:
            os.system("powercfg -h off")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            os.system("powercfg -h on")
        except:
            engine.text_to_speech("i don't have permission to make machine sleep")
            
    def search(self,content=""):
        p = content.find("ẩn danh")
        if p == -1:
            query = content
            mode = ""
        else:
            query = content[0:p]
            mode = "/incognito"
            
        try:
            result = google_search.search(content)
            os.system("start chrome "+mode+" "+result)
        except:
            engine.text_to_speech("i can't search this content.") 

    def check_new_manga(self,content=""):
        result = manga_scan.fau_nettruyen_new_chap()
        try:
            engine.text_to_speech(result)
        except:
            engine.text_to_speech("i can't do this right now")

    
    def hand_mode_on(self,content=""):
        pass

    def hand_mode_off(self,content=""):
        pass
    """
    def move(self,content=""):
        def language_mode(text):
            if "tiếng việt" in text:
                self.language = "vi-VN"
            elif "tiếng anh" in text:
                self.language = "en-US"
        def move_tab(text):
            box = text.split(" ")
            if "phải" in box:
                for i in box:
                    



        list_command = {"ngôn ngữ":language_mode,"trang":3,"ứng dụng":4}
    """