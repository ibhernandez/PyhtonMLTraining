#pip install keyboard

import keyboard as kb
import tkinter as tk
from time import sleep
import os
#Q or O -> next iteration
#W or P -> previous iteration


c_index = 0
show = 1
fg_color = "#d3c5c7"
bg_color = "#65343c"
cheatsheet_path = "cheatSheet.txt"
location = "+428+55" 
#forwards
f1 = ","
f2 = "z"
#backwards
b1 = "."
b2 = "x"
#show or hide
sh1 = "-"
sh2 = "c"
#EXIT
ext = "1"

def my_mainloop():
    global f1
    global f2
    global b1
    global b2
    global sh1
    global sh2
    global exit
    global c_index
    global show
    global fg_color
    global cheatsheet_path
    clipboard=""
    matches=[]
    #Leer contenido del portapapeles
    try:
        clipboard = ""+ root.clipboard_get()
        #clipboard ="" + pd.read_clipboard()
    except Exception: 
        clipboard = ""
        #
    #Formatear caracteres especiales
    #print(clipboard)
    intab = "áéíóú"
    outab = "aeiou"
    transtab = str.maketrans(intab, outab)
    clipboard = clipboard.translate(transtab)
    #Buscar las coincidencias
    #print(clipboard)
    with open(cheatsheet_path, 'r', encoding= "UTF-8") as file: 
        lines = file.readlines();
        for line in lines:
            line = line.translate(transtab)
            #print(line)
            if str(clipboard).lower() in str(line).lower():
    
                line_f = str(line).rstrip('\n')
                matches.append(line_f)

    if len(matches)>=1:
        if (c_index >= len(matches)): 
            c_index=0
        l.config(text=matches[c_index], fg=fg_color)
        cnt=0
        while True:
            try:  
                if kb.is_pressed(f1) or kb.is_pressed(f2):  # if key 'q' is pressed 
                    c_index+=1
                    if (c_index >= len(matches)):
                        c_index=0
                    break
                if kb.is_pressed(b1) or kb.is_pressed(b2):  
                    c_index-=1
                    if (c_index <0):
                        c_index=len(matches)-1
                    break
                if kb.is_pressed(sh1) or kb.is_pressed(sh2):  
                    #print(show)
                    if show == 1: 
                        show =0
                        root.withdraw()
                        break
                    else: 
                        root.deiconify()
                        show = 1
                        break
                if kb.is_pressed(ext):  
                   #print("exiting")
                   os.system("taskkill /F /IM python.exe || taskkill /F /IM pythonw.exe")
            except:     
                break 
            sleep(0.001)
            cnt+=1
            if (cnt>=1000):
                break
            
    else:
       l.config(text="/", fg=fg_color)
       while True:
            try:  
                if kb.is_pressed(sh1) or kb.is_pressed(sh2):  
                    #print(show)
                    if show == 1: 
                        show =0
                        root.withdraw()
                        break
                    else: 
                        root.deiconify()
                        show = 1
                        break
                if kb.is_pressed(ext):  
                   #print("exiting")
                   os.system("taskkill /F /IM python.exe || taskkill /F /IM pythonw.exe")
            except:     
                break 

       
    sleep(0.200)
    root.after(100,my_mainloop)

    
#CONFIGURACION DEL CUADRO DE TEXTO    
#letra #d3c5c7
#background #65343c
#Para chrome en modo oscuro...
root = tk.Tk()
root.overrideredirect(True)
root.geometry(location) #This value needs to be adjusted
root.lift() #On the very top
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)

root.attributes('-topmost', True)
l = tk.Label(text='', font=("Helvetica", 10), bg= bg_color)
l.pack(expand=True)
root.bind("1",lambda x: root.destroy())
#BUCLE QUE ACTUALIZA LOS RESULTADOS
root.after(100,my_mainloop)
root.mainloop()   
