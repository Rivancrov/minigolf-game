from tkinter import *
from datetime import date

def showLeaderboard(headings, scores):
    dat=date.today()
    print(str(dat))
    BG = "#000000"
    root = Tk()
    root.configure(background=BG)
    root.geometry("800x600")

    cols = len(headings)
    rows = len(scores)
   
    for headi in range(len(headings)):
        curhead = headings[headi]
        Label(root, text=curhead, font="Helvetica 15 underline", width=20, fg="white", bg=BG).grid(row=0, column=headi)

    for i in range(1,rows+1): #rows
        for j in range(cols): #column
            currentText = scores[i-1][j]

            border_color = Frame(root, background="white")
            cell = Label(border_color, text=currentText, font=("Helvetica", 15), width=20, height=3, bg=BG, fg="white")

            border_color.grid(row=i, column=j)
            cell.grid(row=i, column=j, padx=1, pady=1)

    mainloop()

showLeaderboard(['level','strokes','par'],[['1','5','3'],['2','1','3'],['3','4','3'],['4','3','3'],['5','2','3']])