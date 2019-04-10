import json
import pyperclip
import clipmonitor
from wox import Wox,WoxAPI

def copy_to_clipboard(text):
    pyperclip.copy(text.strip())

def json_wox(title, subtitle, icon, action=None, action_params=None, action_keep=None):
    json = {
        'Title': title,
        'SubTitle': subtitle,
        'IcoPath': icon
    }
    if action and action_params and action_keep:
        json.update({
            'JsonRPCAction': {
                'method': action,
                'parameters': action_params,
                'dontHideAfterAction': action_keep
            }
        })
    return json

class BetterClip(Wox):
    dataList = []

    def check_clipboard(self,text):
        with open("filter", "r") as f:
            for line in f:
                if text == line:
                    return False
                return True

    def append_datalist(self,text):
        dataList = self.dataList
        new_item = json_wox(text,
                            'working',
                            'Images/app.png')
        dataList.append(new_item)

    def __init__(self):
        Wox.__init__(self)
        watcher = clipmonitor.ClipboardWatcher(self.check_clipboard, 
                               self.append_datalist,
                               5.)
        watcher.start()
        while True:
            try:
                time.sleep(10)
            except Exception as e:
                watcher.stop()
                WoxAPI.show_msg('Error ' + str(e))
                break
        
    def query(self, query):
        dataList = self.dataList
        dataList.append(json_wox('A Test',
                            'working',
                            'Images/app.png'))
        return dataList

    def copy_clip(self, query):
        #copy to clipboard after pressing enter
        copy_to_clipboard(query)
        WoxAPI.hide_app()

if __name__ == "__main__":
    BetterClip()