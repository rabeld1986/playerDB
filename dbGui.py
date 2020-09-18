'''
Created on Jul 13, 2020

@author: rabel
'''
from pynput import keyboard

import tkinter

from tkinter import StringVar

from PIL import ImageTk, Image

import mysql.connector
from distutils.file_util import write_file

from tkinter import messagebox

import random
#connecting to our database
db = mysql.connector.connect(host = "localhost",user = "root", passwd = "rabel1986", database = "nba")
cursor = db.cursor()

##db_functions##
def Key_Pressed():
    keypress = False
    keyboard.Events().start()
    if keyboard.Events().Press(''):
        keypress = True
        
    if keyboard.Events().Release(''):
            keypress = False
           
    return keypress
def Write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
def pid_generator():
    p_ids = random.randint(1,100)
    pid_search = ("SELECT p_id FROM player")
    cursor.execute(pid_search)
    for row in cursor:
        if row[0] == p_ids:
            p_ids = random.randint(1,100)    
    return p_ids

def text_cap(string: tkinter.Entry):
    string.insert(0, string.get()[0].upper())
    string.delete(1)

## creates a window that adds a player to the database        
def pl_create_win():
    root2 = tkinter.Tk()
    #window size
    root2.geometry("500x700")    
    canvas2 = tkinter.Canvas(root2, width = 500, height = 100)
    canvas2.pack()
    root2.wm_title("player registration")
    
    def _insertPl():
        team_sel = t_list.curselection()
        if pfn.get() == "":
            empty_box = tkinter.Label(root2, text = "* this field is required!")
            empty_box.pack()
            empty_box.config(font = ("Calibri",8),fg = "red")
            empty_box.place(x= 210, y = 130)
            
        if pln.get() == "":
            empty_box1 = tkinter.Label(root2, text = "* this field is required!")
            empty_box1.pack()
            empty_box1.config(font = ("Calibri",8),fg = "red")
            empty_box1.place(x= 210, y = 170)
              
        if p_ppg.get() == "":
            empty_box2 = tkinter.Label(root2, text = "* this field is required!")
            empty_box2.pack()
            empty_box2.config(font = ("Calibri",8),fg = "red")
            empty_box2.place(x= 210, y = 210)
        
        if not team_sel:
            empty_box3 = tkinter.Label(root2, text = "* this field is required!")
            empty_box3.pack()
            empty_box3.config(font = ("Calibri",8),fg = "red")
            empty_box3.place(x= 210, y = 250) 
        ## returns the value of the selected team as a string
     
        if pfn.get() != "" and pln.get() != "" and p_ppg.get() != "" and team_sel:
            #capitalizes entry boxes for f_name and l_name
            text_cap(pfn)
            text_cap(pln)
            ts = t_list.get(team_sel)
            
            try:
    
                t_q = ("""SELECT t_id FROM team WHERE team_name = %s""")
                cursor.execute(t_q,(ts,))
                tid =cursor.fetchone()[0]  
        
                p_id_create = pid_generator()
                p_pg = float(p_ppg.get())
                pl_creation = ("INSERT INTO player(p_id,f_name,l_name,ppg,t_id) VALUES(%s,%s,%s,%s,%s)")
                cursor.execute(pl_creation,(p_id_create,pfn.get(),pln.get(),p_pg,tid))
                db.commit()
                     
                    
                pid_show = tkinter.Label(root2, text = "Your player id is: "+str(p_id_create))
                pid_show.pack()
                pid_show.place(x = 100, y = 400)
                if submit_data.selection_get():
                    submit_data.config(state = "disabled")
                     
            except ValueError:
                empty_box = tkinter.Label(root2, text = "* wrong usage! please use numbers!")
                empty_box.pack()
                empty_box.config(font = ("Calibri",8),fg = "red")
                empty_box.place(x= 210, y = 210)
            

            
    ##window title
 
    win_t = tkinter.Label(root2, text = "Welcome to our player registration page")
    win_t.pack()
    win_t.config(font = ("Times New Roman",15))
    win_t.place(x =1 ,y =8)
    
    ##bottoms
    fn_label= tkinter.Label(root2,text = "first name")
    fn_label.pack()
    fn_label.place(x= 2,y = 130)
        
    pfn = tkinter.Entry(root2,bd = 7)
    pfn.pack()
    pfn.place(x= 70, y = 130)
    
    ln_label= tkinter.Label(root2,text = "last name")
    ln_label.pack()
    ln_label.place(x= 2,y = 170)
    
    
   
    pln = tkinter.Entry(root2,bd = 7)
    pln.pack()
    pln.place(x= 70, y = 170)
    
    
    ppg_label= tkinter.Label(root2,text = "ppg%")
    ppg_label.pack( )
    ppg_label.place(x= 2,y = 210)
        
    p_ppg = tkinter.Entry(root2,bd = 7)
    p_ppg.pack()
    p_ppg.place(x= 70, y = 210)
    
    t_label= tkinter.Label(root2,text = "team")
    t_label.pack( )
    t_label.place(x= 2,y = 250)
    
    scrollbar = tkinter.Scrollbar(root2)
    scrollbar.pack( side = tkinter.RIGHT, fill = tkinter.Y )
    scrollbar.place(x= 70,y = 250)
    
    t_list = tkinter.Listbox(root2,height = 2,yscrollcommand = scrollbar.set)
    t_list.insert(0,"Lakers")
    t_list.insert(1,"Clippers")
    t_list.insert(2,"Rockets")
    t_list.insert(3,"Nets")
    t_list.pack()
    t_list.place(x= 90,y = 250)
    
    
    scrollbar.config(command = t_list.yview)
    ###
    ######
    #database manipulation buttom
    submit_data = tkinter.Button(root2,text = "confirm",command = _insertPl) 
    submit_data.pack()
    submit_data.place(x= 90,y = 350)
    
    
    #left corner logo
    nba_logo2 = ImageTk.PhotoImage(Image.open("NBA-Logo.png"),master = root2)
    logo = tkinter.Label(root2,image = nba_logo2)
    logo.pack()
    logo.place(x = 290, y = 32)
    
    #main loop
    ##exit buttom
    def win_ex():
        if tkinter.messagebox.askokcancel(title= "Exit", message="Are you sure?"):
            root2.destroy()

            
    ex_b = tkinter.Button(root2,text = "exit",command = win_ex)
    ex_b.pack()
    ex_b.place(x= 45,y = 350)
        
    root2.mainloop()
def clearText():
    #function that clears text entries
    pid_Tbox.delete(first=0, last=len(pid_Tbox.get()))
    
def get_player():
    print(Key_Pressed())
    player_id = pid_Tbox.get() 
    clearText()
    try:
        pl = ("SELECT f_name, l_name, ppg, t_id  FROM player WHERE p_id = ((%s))" %player_id)
        cursor.execute(pl)
        for row in cursor:
            var = StringVar()
            label = tkinter.Message( root, textvariable=var )
            var.set("first name: "+ "\n"+row[0]+ "\n"+"last name: "+"\n"+row[1]+"\n" + "ppg: "+ "\n"+str(row[2]))
            label.pack()
            label.place(bordermode= tkinter.OUTSIDE, x= 200,y=200)
            t_n = ("select t.team_name from player p inner join team t on t.t_id = p.t_id where p_id = ((%s))"%player_id)
            cursor.execute(t_n)
            for t in cursor:
                var3 = StringVar()
                label3 = tkinter.Message( root, textvariable=var3 )
                var3.set("team: "+ "\n"+t[0])
                label3.pack()
                label3.place(bordermode= tkinter.OUTSIDE, x= 200,y=293)
        q = ("SELECT *  FROM player WHERE p_id = ((%s)) "%player_id)
        cursor.execute(q)
        record = cursor.fetchall()
        try:
            for row in record:
                photo = row[5]
                if photo != None:
                    Write_file(photo,"C:\\Users\\rabel\\workspace\\dbM\\"+row[1]+"_"+row[2]+"1"+".png" ) 
                    pl_pic =  ImageTk.PhotoImage(Image.open(row[1]+"_"+row[2]+"1"+".png"))
                    canvas.create_image(200,60, image=pl_pic)
                    root.mainloop()
               
                      
        except TypeError:
            print("No photo found!")
       
    except:
        tkinter.messagebox.showerror(title= "Error", message="Player Not Found!")
        print("Not found!")
    
                
          
    
          
##########GUI#########

class Window(tkinter.Frame):
    def __init__(self,master = None):
        tkinter.Frame.__init__(self, master)
        self.master = master
#create a window
root = tkinter.Tk()
#window size
root.geometry("500x700")
canvas = tkinter.Canvas(root, width = 500, height = 100)
canvas.pack()


app = Window(root)
##import images
nba_logo = tkinter.PhotoImage(file = "nba_logo_small.png")

#creates the player id text box
pid_label = tkinter.Label(root,text = "Player ID")
pid_label.pack( )


pid_Tbox = tkinter.Entry(root,bd = 7)
pid_Tbox.pack()

root.wm_title("nba player database")

#bottom creation
bottom = tkinter.Button(root,text = "get info", command = get_player)
#bottom gets drawn on screen
bottom.pack()
bottom.place(bordermode= tkinter.OUTSIDE, height=35, width=80, x= 255,y=157)


bottom2 = tkinter.Button(root,text = "add player",command = pl_create_win) 
bottom2.pack()
bottom2.place(bordermode= tkinter.OUTSIDE, height=35, width=80, x= 175,y=157)

canvas.create_image(450,52, image=nba_logo)

#main loop for our window 
root.mainloop()
