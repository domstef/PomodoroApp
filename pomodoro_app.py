from tkinter import *
from PIL import Image, ImageTk

PINK = "#FFE5E5"
RED = "#FFBFBF"
GREEN = "#A8DF8E"
LIGHT_GREEN = "#F3FDE8"
YELLOW = "#f7f5dd"

BACKGROUND_COLOR = YELLOW

TICK = "✔"

FONT = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

WIDTH = 200
HEIGHT = 150


class Pomodoro:

    def __init__(self):
        self.window = Tk()
        self.window.title("Pomodoro App")
        self.window.minsize(400, 300)
        self.window.config(padx=10, pady=20, bg=BACKGROUND_COLOR)

        self.label = Label(text="Pomodoro Timer", fg=GREEN, font=(FONT, 25, "bold"), bg=BACKGROUND_COLOR,
                           width=20, height=1)
        self.label.grid(row=0, column=1)

        self.canvas = Canvas(width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
        image = Image.open("bg.png")
        image = image.resize((200, 150))
        self.background_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(WIDTH / 2, HEIGHT / 2, image=self.background_image)
        self.timer_text = self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="00:00", fill=PINK,
                                                  font=(FONT, 30, "bold"))
        self.canvas.grid(row=1, column=1)

        self.start_button = Button(text="Let's go!", font=(FONT, 12, "bold"),
                                   height=1, width=17, bg=GREEN, command=self.pomodoro_timer)
        self.start_button.grid(row=2, column=1, sticky="w")

        self.reset_button = Button(text="Stop the session", font=(FONT, 12, "bold"), height=1, width=17,
                                   bg=GREEN, command=self.restart_session)
        self.reset_button.grid(row=2, column=1, sticky="e")

        self.checkmarks = Label(text="", bg=BACKGROUND_COLOR, fg=GREEN, font=("bold", 24))
        self.checkmarks.grid(row=3, column=1)


        self.pomodoro_mode = True
        self.working_mode = True
        self.num_of_sessions = 0
        self.working_session = 0

        self.window.mainloop()




    def pomodoro_timer(self):
        if self.num_of_sessions > 0:
            print("You already pressed the button!")
        else:
            self.working_time()


    def restart_session(self):
        print("Restarting...")
        self.label.config(text="Pomodoro Timer", width=20)
        self.checkmarks.config(text="")

        self.num_of_sessions = 0
        self.working_session = 0
        self.canvas.itemconfig(self.timer_text, text="00:00")

        self.working_mode = False

    def working_time(self):
        global BACKGROUND_COLOR
        self.label.config(text="Keep working!", width=20)
        self.num_of_sessions += 1
        if self.num_of_sessions % 8 == 0 or self.num_of_sessions % 2 == 0:
            self.break_time()
        else:
            self.working_session += 1
            print("Entering the working time in working session {}...".format(self.working_session))
            BACKGROUND_COLOR = RED
            self.change_background_color()
            time = WORK_MIN * 60
            self.count_down(time)

    def change_background_color(self):
        self.canvas.config(bg=BACKGROUND_COLOR)
        self.window.config(bg=BACKGROUND_COLOR)
        self.label.config(bg=BACKGROUND_COLOR)
        self.checkmarks.config(bg=BACKGROUND_COLOR)

    def break_time(self):
        global BACKGROUND_COLOR
        self.checkmarks.config(text=TICK * self.working_session)

        if self.num_of_sessions % 8 == 0:
            self.label.config(text="Long break!", width=20, font=(FONT, 25, "bold"))
            BACKGROUND_COLOR = PINK
            self.change_background_color()
            self.count_down(LONG_BREAK_MIN * 60)

        else:
            BACKGROUND_COLOR = LIGHT_GREEN
            self.change_background_color()
            self.label.config(text="Short break!", width=20, font=(FONT, 25, "bold"))
            self.count_down(SHORT_BREAK_MIN * 60)


    def count_down(self, count):
        global BACKGROUND_COLOR
        minutes = count // 60
        seconds = count % 60
        self.canvas.itemconfig(self.timer_text, text="{:02d}:{:02d}".format(minutes, seconds))

        if count > 0 and self.working_mode:
            self.window.after(100, self.count_down, count - 1)
        elif count == 0:
            self.canvas.itemconfig(self.timer_text, text="00:00")
            self.working_time()
        else:
            self.working_mode = not self.working_mode
            self.canvas.itemconfig(self.timer_text, text="00:00")
            BACKGROUND_COLOR = YELLOW
            self.change_background_color()


Pomodoro()
