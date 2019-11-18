import sys
from tkinter import messagebox
import API
import GUIsupport
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk


class GUI:
    def __init__(self,  top=None):
        self.ship = API.API()

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        top.geometry("600x450+507+175")
        top.title("Where to eat?")
        top.configure(background="#d8b2a8", highlightbackground="#d9d9d9", highlightcolor="black")

        self.mainFrame = tk.Frame(top, bg="#d8b2a8")
        self.mainFrame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)

        self.restaurantFrame = tk.Frame(top, background="#d8b2a8", relief='flat')
        self.restaurantFrame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)

        self.detailFrame = tk.Frame(top, bg="#d8b2a8")
        self.detailFrame.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)

        self.mainFrame.lift()


        i = Image.open('taco-512.png', mode='r')
        photo = ImageTk.PhotoImage(i)

        populateButton = tk.Button(self.mainFrame, bg="#97b3d8", activebackground="#c3edb4", relief='groove',
                                   image=photo, command=self.fetchRestaurants)
        populateButton.image = photo
        populateButton.place(relx=0.35, rely=0.5)

        exitButton = tk.Button(self.mainFrame, text="Exit/Cancel", activebackground="#c3edb4", background="#97b3d8",
                               font=("Arial", 12), command=GUIsupport.destroy_window)
        exitButton.place(relx=0.75, rely=0.8, height=70, width=140)

        locationLabel = tk.Label(self.mainFrame, background="#d8b2a8", relief="groove",
                                 text='''Enter an Address, City, or State:''')
        locationLabel.place(relx=0.06, rely=0.07, height=31, width=187)

        termLabel = tk.Label(self.mainFrame, background="#d8b2a8", relief="groove", text='''Enter a keyword:''')
        termLabel.place(relx=0.567, rely=0.067, height=31, width=197)

        radiusLabel = tk.Label(self.mainFrame, background="#d8b2a8", relief="groove", text='''Enter a radius:''')
        radiusLabel.place(relx=0.567, rely=0.3, height=31, width=197)

        self.locationEntry = tk.Entry(self.mainFrame, background="white", selectbackground="#c4c4c4",
                                      selectforeground="black")
        self.locationEntry.place(relx=0.04, rely=0.2, relheight=0.07, relwidth=0.4)

        self.termEntry = tk.Entry(self.mainFrame, background="white", selectbackground="#c4c4c4",
                                  selectforeground="black")
        self.termEntry.place(relx=0.55, rely=0.2, relheight=0.07, relwidth=0.4)

        self.radiusBox = ttk.Combobox(self.mainFrame, takefocus='', values=['2 miles', '5 miles', '15 miles', '30 miles', '50 miles'])
        self.radiusBox.place(relx=0.65, rely=0.4, relheight=0.07, relwidth=0.2)

        optionButtons = []
        self.optionLabels = []
        place = [.021, 0.144, 0.268, 0.392, 0.515, 0.639, 0.763, 0.887]
        optionButtons.extend([tk.Button(self.restaurantFrame, wraplength=60, activebackground="#c3edb4",
                                        background="#97b3d8", text='Pick #%s' % i,
                                        command=lambda idx=i: self.showRestaurantDetails(idx)) for i in range(7)])
        self.optionLabels.extend(
            [tk.Label(self.restaurantFrame, activebackground="#c3edb4", background="#97b3d8", font=("Arial", 10)) for i
             in range(7)])

        for i in range(len(optionButtons)):
            optionButtons[i].place(relx=0.08, rely=place[i], height=42, width=68)
            self.optionLabels[i].place(relx=0.208, rely=place[i], height=42, width=457)

        resToMain = tk.Button(self.restaurantFrame, text="Back to main menu",
                              command=lambda: self.changeFrames(self.mainFrame, self.restaurantFrame),
                              activebackground="#c3edb4", background="#97b3d8")
        resToMain.place(relx=.5, rely=0.90, height=42, width=130)

        self.display = tk.Text(self.detailFrame, bg="#ffd2c7", relief="groove", width=580, font=("Arial", 12))
        self.display.place(relx=0.017, rely=0.089, relheight=0.66, relwidth=.95)

        self.backButton = tk.Button(self.detailFrame, text='Go back',
                                    command=lambda: self.changeFrames(self.restaurantFrame, self.detailFrame),
                                    activebackground="#c3edb4", background="#97b3d8", wraplength=60)
        self.backButton.place(relx=0.417, rely=0.822, height=52, width=84)

    def __clear_boxes__(self):
        self.termEntry.delete(0, 'end')
        self.locationEntry.delete(0, 'end')
        self.display.delete(1.0, 'end')

    def changeFrames(self, lift, lower):
        self.__clear_boxes__()
        lift.lift(aboveThis=lower)

    #retrieves list of restaurants from API and displays them on restaurant frame
    def fetchRestaurants(self):
        if self.locationEntry.get() == "":
            messagebox.showerror("Entry Error", "Please input a location to find restaurants")
            return
        if self.termEntry.get() == "":
            messagebox.showerror("Keyword Error", "Please input a keyword to find restaurants")
            return

        self.restaurants, error = self.ship.getRestaurants(self.locationEntry.get(), self.termEntry.get(), self.radiusBox.get().split(' '))
        if error == 0:
            messagebox.showerror("API ERROR", "Please wait awhile before trying again")
            GUIsupport.destroy_window()
            return

        for i in range(len(self.restaurants)):
            self.optionLabels[i].config(text=self.restaurants[i][1] + "'s rating: " + str(self.restaurants[i][2])
                                        + " and price: " + str(self.restaurants[i][3]) +  ", distance: " + self.restaurants[i][4] + " miles\n")
        self.changeFrames(self.restaurantFrame, self.mainFrame)

    #displays details of a restaurant on detail frame
    def showRestaurantDetails(self, index):
        self.changeFrames(self.detailFrame, self.restaurantFrame)

        data =self.ship.getFinerDetails(self.restaurants[index][0])
        hours = self.__format_hours__(data['hours'][0]['open'])

        self.display.insert(1.0, data['name'] + "\t pricing: " + str(data['price']) + " ,\t rating: "
                            + str(data['rating']) + ',\tCuisine: ' + data['categories'][0]['title'])
        self.display.insert(2.0, "\nAddress: " + data['location']['address1'] + " " + data['location']['city']
                            + " " + data['location']['state'] + ' ' + data['location']['postal_code'])
        self.display.insert(3.0, "\n Hours: ")

        for h in hours:
            self.display.insert(3., h['day'] + "= " + h['start'] + '-' + h['end'] + ', ')

        self.display.insert(4.0, '\n\nReview Snippets:\n')
        for i in data['reviews']:
            self.display.insert(6.0, i['text'] + '\n\n')


    def __format_hours__(self, data):
        weekdays = {0:"M", 1:"T", 2:"W", 3:"Th", 4:"F", 5:"Sat", 6:"Sun"}

        for i in data:
            i['day'] = weekdays[i['day']]

            if int(i['start']) > 1200:
                i['start'] = int(i['start']) - 1200
                i['start'] = str(i['start']) + "PM"
            else:
                i['start'] += 'AM'

            if int(i['end']) > 1200:
                i['end'] = int(i['end']) - 1200
                i['end'] = str(i['end']) + "PM"
            else:
                i['end'] += 'AM'

        current = 1
        for i in range(len(data[1:])):
            if data[0]['start'] == data[i+1]['start'] and data[0]['end'] == data[i+1]['end']:
                data[0]['day'] += ", " + data[i+1]['day']
                data[i + 1] = False
            else:
                for j in range(current):
                    if data[j+1]:
                        if data[j+1]['start'] == data[i+1]['start'] and data[j+1]['end'] == data[i+1]['end']:
                            data[j+1]['day'] += ", " + data[i+1]['day']
                            data[i+1] = False
                            break
                    elif not data[j+1]:
                        if i != j:
                            data[current] = data[i + 1]
                            data[i + 1] = False
                            current += 1
                            break
        return data[:current]



