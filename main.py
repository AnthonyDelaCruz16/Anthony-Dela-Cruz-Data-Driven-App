# Tools and modules for the creation of the api
from tkinter import *
from PIL import ImageTk, Image
import requests
import json

# function for frame switching 
def switch_to_frame(frame):
    frame.tkraise()

# The main function that is used in order to access the JSON file
def show_entry():
    # Initial Hinding labels would be replaced with the information

    # This would hide the FrameA labels
    for widget in FrameA.winfo_children(): # function used to get child widgets
        if widget != result_label: # If widget not in result label
            widget.place_forget() # this would hide the widget

    # This would hide the FrameB labels
    for widget in FrameB.winfo_children():
        if widget != result_label:
            widget.place_forget()

    # This would hide the FrameC labels
    for widget in FrameC.winfo_children():
        if isinstance(widget, Label) and widget != result_label: # This will hide except 1 button that is used to switch the frames
            widget.place_forget()
    
    # I receive all the lowercase for the exceptions in the dictionary using the custom title case function.
    def custom_title_case(word):
        exceptions = ["and", "the", "of", "da"]  # if there are any other exceptions that is needed this will add them
        return word.title() if word.lower() not in exceptions else word

    # Gather information from the user
    entered_text = UserSearch.get() # Gather the information from entry
    print(entered_text)
    formatted_text = ' '.join(custom_title_case(word) for word in entered_text.split())
    print(formatted_text)
    for country in data: # Loop in order to get all the needed info
        if entered_text == country['name']['common']:  # If the country in the api is matched in the entered text
            official_name = country['name']['official'] # obtaining the data from the API and putting it in a variable for later usage.
            subregion = country.get('subregion', 'Invalid' ) # Some country does not have this data, so I used a get method.
            region = country.get('region', 'Invalid')
            capital = country.get('capital', '')
            continent = country.get('continents', 'Invalid')
            timezone = country.get('timezones', 'Invalid')
            weekstart = country.get('startOfWeek', 'Invalid')

            # This would Extract the information about a countries currency
            try:
                currencies_data = country.get("currencies", "Not Available")
                currencies_info = "\n".join([f"{code}: {info['name']} ({info['symbol']})" for code, info in currencies_data.items()])
            except KeyError as e:
                currencies_info = "Currency info not available."

            # Using this get function it would extract information about the countries flag
            flag_info = country.get('flags', {})
            flag_png_link = flag_info.get('png', 'default_flag.png')  # This would supply a default flag URL

            # Organize the output and store it in a single variable.
            result_text = (
            f"Country Selected: {entered_text}\n"
            f"Official Name Of Country: {official_name}\n"
            f"Countries Continent: {', '.join(continent)}\n"
            f"Region Of Country: {region}\n"
            f"Subregion Of Country: {subregion}\n"
            f"Capitals Of The Country: {', '.join(capital)}\n"
            f"Country's Currency:\n{currencies_info}\n"
            f"Country's Timezone: {', '.join(timezone)}\n"
            f"Start of the Week: {(weekstart)}\n"
            )

            # Verify that flag_info has the 'alt' key. 
            if 'alt' in flag_info:
                flag_alt_text = flag_info['alt']
            else:
                flag_alt_text = 'There is no flag informaton available for the country you have selected.'

            # The output will be in FrameC
            result_label.config(text=result_text, compound="top")

            try:
                # Use Pillow to load the image of the flag
                flag_image = Image.open(requests.get(flag_png_link, stream=True).raw)
                flag_image = ImageTk.PhotoImage(flag_image)
                # Display in FrameA the image of the flag
                flag_label = Label(FrameA, image=flag_image)
                flag_label.image = flag_image
                flag_label.place(x=35, y=0, height=200)
            except Exception as e:
                # If the flag in not available in the API
                print(f"Error in loading of flag image: {e}")
                flag_label = Label(FrameA, text="Flag Image is Unavailable", bg='lightblue')
                flag_label.place(x=35, y=0, height=200)

            # Show Frame B's alt text using line wrapping to make it fit the frame.
            alt_label = Label(FrameB, text=flag_alt_text, font=("Georgia", 13), wraplength=380, bg='lightblue')
            alt_label.place(x=10, y=10) 
            break 
    else:
        result_label.config(text=f"Country Selected: {entered_text}\n is Not Found")

# URL of the API
url= "https://restcountries.com/v3.1/all"

# Gathering the data of the API and then putting it in to a variable
response = requests.get(url)

# Storing the responses into a variable named data
data = response.json()

# The JSON file name that contains the API data
file_name = "Info_of_all_countries.json"

# Save the JSON information in a file.
with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)

# This will open the JSON file for reading
with open(file_name, 'r') as json_file:
    # Load the JSON data from the file
    data = json.load(json_file)

# Main Tkinter window
root = Tk()
root.title("Explorer of the World") #Adding the title
root.geometry('1000x700') #Size of ouput window
root.resizable(0,0) #Output window fixed

# Frame Start
Start_frame = Frame(root, bg='#FF00FB')
img = ImageTk.PhotoImage(Image.open("Logo.png") )
# The logo image will be displayed
label = Label(Start_frame, image=img, bg='#FF00FB')
label.place(x=250, y=0)
Button(Start_frame, text="START", font=("Georgia", 30), bg='#FF00FB', fg='white', bd=0, 
       command=lambda: switch_to_frame(frame1)).place(x=440, y= 500)
Start_frame.place(x=0,y=0, width=1000,height=700)

#  Frame 1 the opening page
frame1 = Frame(root, bg='#FF00FB')
Label(frame1, text="Welcome To Explorer of the World.",fg='white',bg='#FF00FB', font=("Georgia", 40)).place(x=200, y=200)
Label(frame1, text="Explorer of the World is an app that will help you gather more knowledge about the world.",
      fg='white',bg='#FF00FB', font=("Garamond", 20)).place(x=100, y=300)
Label(frame1, text="With Explorer of the World you would be able to find out, interact, and discover:\nYour Entryway to Worldwide Information.",
      fg='white',bg='#FF00FB', font=("Garamond", 20)).place(x=200, y=335)
Label(frame1, text="Created by: Anthony Dela Cruz \n Bathspa University Level 5 Creative Computing ",
      fg='white',bg='#FF00FB', font=("Garamond", 15)).place(x=10, y=30)
Button(frame1, text="Discover The World", font=('Georgia', 30), bg='#FF00FB', fg='#00227A', bd='0',
       command=lambda: switch_to_frame(frame2)).place(x=330, y= 500)
frame1.place(x=0,y=0, width=1000,height=700)

# Frame 2 the tagline page
frame2 = Frame(root, bg='#FF00FB')
Label(frame2, text="Explorer of the World",
      fg='white',bg='#FF00FB', font=("Georgia", 30)).place(x=390, y=30)
Label(frame2, text="Input a country:", fg='white', bg='#FF00FB', 
      font=("Georgia", 20)).place(x=250, y=100)
UserSearch = Entry(frame2, width=25, font=("Garamond", 15))
UserSearch.place(x=450, y=110)
search_button = Button(frame2, text="Search", command=show_entry, font=("Georgia", 20), bg='#FF00FB', fg='white', bd='0')
search_button.place(x=750, y=95)
frame2.place(x=0,y=0, width=1000,height=700)

# Nested Frames, the primary application, inside frame 2.

# Frame 2a which is inside of frame 2
miniframe = Frame(frame2, bg='#FF0000')
miniframe.place(x=30,y=180, width=940,height=500)

# Frame A which is inside of miniframe
FrameA = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameA, text="The Country of The Flag Will Be Displayed Here:", font=("Garamond", 13), bg='white').place(x=10, y=10)
FrameA.place(x=20,y=20, width=400,height=200)

# Frame B inside of miniframe
FrameB = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameB, text="The Description of The Flag Will Be Diplayed Here:", font=("Garamond", 13), bg='white').place(x=10, y=10)
FrameB.place(x=20,y=250, width=400,height=210)

# Frame C, inside miniframe
FrameC = Frame(miniframe, bg='white', bd='1', relief='ridge')
Label(FrameC, text="The Details Will be Displayed Here:", font=("Garamond", 13), bg='white').place(x=10, y=10)
result_label = Label(FrameC, font=("Garamond", 13), justify="left", wraplength=300, bg='white')
result_label.place(x=120, y=30)
Button(FrameC, text="End", font=('Georgia', 30), bg='white', fg='white', bd='0',
       command=lambda: switch_to_frame(lastframe)).place(x=350, y= 350)
FrameC.place(x=450,y=20, width=460,height=440)

# Last Frame
lastframe = Frame(root, bg='#FF00FB')
Label(lastframe, text="Thank you for using Explorer of the World!",fg='white',bg='#FF00FB', font=("Georgia", 40)).place(x=120, y=200)
Button(lastframe, text="Try Again", font=('Georgia', 30), bg='#FF00FB', fg='#00227A', bd=0,
       command=lambda: switch_to_frame(Start_frame)).place(x=400, y= 400)
lastframe.place(x=0,y=0, width=1000,height=700)


# Show Start frame initially
switch_to_frame(Start_frame)

root.mainloop()