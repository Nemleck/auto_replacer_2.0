import datetime

class Console:
    def __init__(self):
        pass

    def get_time(self):
        now = datetime.datetime.utcnow()
        return now.hour+1, now.minute, now.second

    def out(self, msg_color: str, msg, msg_type=None):
        color = "0"
        if msg_color == "info":
            color = "32"
        elif msg_color == "warning":
            color = "33"
        elif msg_color == "error":
            color = "31"
        
        if msg_type == None:
            msg_type = msg_color
        
        time = self.get_time()
        print(f"\033[1;{color}m[{time[0]}:{time[1]}:{time[2]}] [{msg_type.capitalize()}]\033[0;{color}m : {msg} \033[0m")