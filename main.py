import tkinter
import tkinter as tk
import time
import random
import math

#Initializing Tkinter window to have a 1400 pixel width and 400 pixel height along with a title.
screen = tk.Tk()
screen.geometry("1400x400")
screen.title("Fast Fingers")

#Instructions for how to use this application to be displayed at the top of the screen.
instructions = tk.Label(text="Type the blue highlighted example text as fast as you can into the text box.")
instructions.grid(row=0, column=1)

#Frame object to house the typing prompt.
text_frame = tk.Frame(screen, bg=("#7aa9f5"))
text_frame.grid(row = 1, column=1)

class TextFunctions:
    def __init__(self):
        self.error_count = 0
        self.start_time = 0
        self.result_display = tk.Label(screen, font='Helvetica 18 bold', anchor="center")
        self.prompt_text = "The quick fox jumped over the lazy brown dog."
        self.prompt_display = tk.Label(text_frame, text= self.prompt_text, bg=("#7aa9f5"), font='Helvetica 18 bold', anchor="center")

        #Create a list of prompts from the file with the typing prompts in it
        self.prompt_list = []
        prompt_file = open("typing_prompts.txt", "r")
        #Loop adds one line of the text file to the prompt list at a time.
        for line in prompt_file:
            self.prompt_list.append(line)
        #Button for requesting a new typing prompt to start the challenge/game again.
        self.next_prompt_button = tk.Button(screen, text="New Prompt", command=self.new_prompt)

        #Input box Tkinter widget where the user types
        self.input_box = tk.Text(screen, height=5, width=70)

        # Creating a correct tag to color the correct text green
        self.input_box.tag_config("correct", foreground="green")
        self.input_box.tag_config("wrong", foreground="red")

        #Whenever a key is released, the checkInput function is ran to evaluate if they have made any errors yet and to check if they are finished.
        self.input_box.bind("<KeyRelease>", lambda e: self.checkInput())


    def calcWPM(self, seconds):
        #Gross WPM = (Typed Characters / 5) / Minutes elapsed
        #Net WPM = GWPM - Number of Errors / Time in Minutes.


        #characters in the example text/how many characters were typed
        typed_chars = len(self.prompt_text)
        minutes = seconds / 60
        GWPM = (typed_chars / 5) / minutes


        WPM = GWPM - self.error_count / minutes
        #Returning GWPM now but program calculates Net WPM with error count factored in if desired to change the results. I prefer to know GWPM
        return GWPM

    #Function checks if the typed input equates to the goal prompt. Also colors the text green if matching and red if input includes a mistake.
    def checkInput(self):
        input = self.input_box.get(1.0, "end-1c")
        if len(input) == 1:

            self.start_time = time.time()
            #Hiding the display text if the user starts the challenge over
            self.result_display.config(text="")
            #set error count to zero if the user is just starting to type the prompt again
            self.error_count = 0


        if input == self.prompt_text[:len(input)]:

            self.input_box.tag_add("correct", "1.0", "2.0")
            self.input_box.tag_remove("wrong", "1.0", "end")
        else:

            self.input_box.tag_remove("correct", "1.0", "end")
            self.input_box.tag_add("wrong", "1.0", "end")
            #keep track of mistakes made for Net WPM calculation
            self.error_count += 1



        if input == self.prompt_text:

            finish_time = time.time() - self.start_time

            WPM = text.calcWPM(finish_time)

            #Formatting finish_time to include fewer decimals after calculation
            finish_time = math.ceil(finish_time*100)/100

            self.result_display.config(text="WPM: "+str(WPM)+"\nCharacters typed: "+str(len(self.prompt_text))+"\nTime elapsed: "+str(finish_time)+" seconds")
            screen.update()

    #Function chooses a random string from the list to be the new prompt for typing.
    def new_prompt(self):

        #Set error count to zero when there is a new prompt to type
        self.error_count = 0


        new_prompt = random.choice(self.prompt_list)[:-1]
        #Substring to last character to omit the new line "\n"
        self.prompt_display.config(text=new_prompt)

        #Change the prompt class variable to be the new prompt
        self.prompt_text = new_prompt

        # Hiding the display/results text if the user starts the challenge over
        self.result_display.config(text="")

        #Clears text input to make way for the next prompt to be typed
        self.input_box.delete("1.0","end")

        screen.update()
#Instantiating TextFunction object and displaying the class widgets to the Tkinter window
text = TextFunctions()
text.result_display.grid(row=3,column=1)
text.prompt_display.pack(expand=True, fill='both')
text.next_prompt_button.grid(row= 4, column=1)
text.input_box.grid(row=2, column=1, padx=10, pady=10)


screen.mainloop()
