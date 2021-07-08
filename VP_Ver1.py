from tkinter import Tk, Frame, Label, Button
from tkinter.scrolledtext import ScrolledText
from tkinter import BOTTOM, TOP, LEFT, RIGHT, END
from tkinter.font import Font as tkfont
from tkinter.font import BOLD, ITALIC
from tkinter.filedialog import askopenfilenames
from pandas import read_csv, concat
from time import time, ctime
from numpy.random import seed, randint, shuffle
from os import listdir
from functools import partial
from re import sub

# tk window basic setting: title and size###############################################
bgcolor = "#F9F1F0"
choice_bgcolor = "#FACCC9"
window = Tk()
window.title("Vocabulary Practice")
window.geometry("400x320")
window.configure(bg=bgcolor)
#######################################################################################

class VP_GUI():
    def __init__(self, parent):
        global font_qn, font_vocab, font_choice, font_result, font_score, font_wrong, font_btn
        global bgcolor, choice_bgcolor

        # questions setting
        self.extract_rate = 0.5
        self.choice_num = 5

        # window = top + middle + bottom
        self.top_frame = Frame(parent, height=40, width=400, bg=bgcolor)
        self.middle_frame = Frame(parent, bg=bgcolor)
        self.botton_frame = Frame(parent, bg=bgcolor)

        # top frame: display the vocabulary
        self.counter_qn = 0
        self.txt_qn = Label(self.top_frame, text="Q" + str(self.counter_qn) + ".", font=font_qn, bg=bgcolor)
        self.txt_vocab = Label(self.top_frame, text="Vocabulary", font=font_vocab, bg=bgcolor)

        # middle frame: display the choices, display score at the end of the test
        self.btn_choice_list = []
        for i in range(self.choice_num):
            btn = Button(self.middle_frame, text="選項" + str(i + 1), command=partial(self.checkA, i),
                         width=40, font=font_choice, bg=choice_bgcolor, borderwidth=0)
            self.btn_choice_list.append(btn)
        self.btn_checkScore = Button(self.middle_frame, text="Check the score", command=self.testResult,
                                     font=font_btn, bg=choice_bgcolor, borderwidth=0)
        self.txt_score = Label(self.middle_frame, text="", font=font_score, bg=bgcolor)
        self.txt_wrong = Label(self.middle_frame, text="Practice these vocabularies again!\n", font=font_score, bg=bgcolor)
        self.txtbox_wrong = ScrolledText(self.middle_frame, height=4, width=20, font=font_wrong, bg="#F79489", fg="#FFFFFF")

        # bottom frame: display the result
        self.txt_result = Label(self.botton_frame, text="Correct/Incorrect, correct one is...", font=font_result,
                                bg=bgcolor)
        self.btn_nextRound = Button(self.botton_frame, text="Next round", command=self.newRound,
                                    font=font_btn, bg=choice_bgcolor, borderwidth=0)

        self.readCsv()
        self.newRound()

    def getCsvPath(self):
        files = askopenfilenames(filetypes=[("CSV Files", ".csv")])

    def readCsv(self):
        self.vocab_csv_dir = listdir("vocab")
        self.vocab_df_list = []
        for filename in self.vocab_csv_dir:
            self.vocab_df_list.append(read_csv("vocab\\" + filename))
        self.vocab_df = concat(self.vocab_df_list, ignore_index=True)

    def packUI(self):
        # window
        self.top_frame.pack(side=TOP, pady=5, padx=5)
        self.middle_frame.pack(side=TOP, pady=5, padx=5)
        self.botton_frame.pack(side=BOTTOM, pady=15, padx=5)

        # top frame
        self.txt_qn.pack(side=TOP, pady=5)
        self.txt_vocab.pack(side=TOP)

        # middle frame
        for btn in self.btn_choice_list:
            btn.pack(side=TOP, pady=2)

        # botttom frame
        self.txt_result.pack(side=TOP)

    def newRound(self):
        # unpack widgets
        self.txt_score.pack_forget()
        self.txt_wrong.pack_forget()
        self.txtbox_wrong.pack_forget()
        self.btn_nextRound.pack_forget()

        # pack widgets
        self.packUI()

        # random seed
        seed(int(time()))

        # answer statistics
        self.correct = 0
        self.incorrect = 0
        self.incorrect_list = []

        # generate questions
        df = self.vocab_df.copy()
        normal_df = df[df["weight"] == 0]
        important_df = df[df["weight"] == 1]

        self.question_list = set(important_df.index)
        self.question_num = int(self.extract_rate * len(df))
        while (len(self.question_list) < self.question_num):
            self.question_list.add(int(randint(0, len(df), 1)))
        self.question_list = list(self.question_list)
        shuffle(self.question_list)
        # print(self.question_list)

        # generate choices
        self.choice_dict = {}
        for qindex in self.question_list:
            answers_list = {"(" + df.iloc[qindex, 1] + ".) " + df.iloc[qindex, 2]}
            while (len(answers_list) < self.choice_num):
                rn = int(randint(0, len(df), 1))
                if (df.iloc[rn, 0] != df.iloc[qindex, 0]):
                    if (df.iloc[rn, 1] != df.iloc[qindex, 1] or (
                            df.iloc[rn, 2] not in df.iloc[qindex, 2] and df.iloc[qindex, 2] not in df.iloc[rn, 2])):
                        answers_list.add("(" + df.iloc[rn, 1] + ".) " + df.iloc[rn, 2])
            answers_list = list(answers_list)
            shuffle(answers_list)
            self.choice_dict[qindex] = answers_list
        # print(self.choice_dict)

        # UI modification
        self.counter_qn = 0
        self.txt_qn.config(text="Q" + str(self.counter_qn) + ".")
        self.btn_nextRound.pack_forget()

        # start the test
        self.txt_result.config(text="")
        self.nextQ()

    def nextQ(self):
        if (self.counter_qn == len(self.question_list)):
            # unpack widgets
            for btn in self.btn_choice_list:
                btn.pack_forget()
            self.btn_checkScore.pack(side=BOTTOM)
            return

        self.this_qn = self.vocab_df.iloc[self.question_list[self.counter_qn]]
        self.counter_qn += 1
        self.txt_qn.config(text="Q" + str(self.counter_qn) + ".")

        # display quesion
        self.txt_vocab.config(text=self.this_qn["vocab"])
        for i in range(self.choice_num):
            self.btn_choice_list[i].config(text=self.choice_dict[self.this_qn.name][i])

    def checkA(self, selected):
        # print(self.btn_choice_list[selected].cget("text"))
        if (self.btn_choice_list[selected].cget("text") == "(" + self.this_qn["type"] + ".) " + self.this_qn[
            "meaning"]):
            result = "Correct!"
            self.correct += 1
            textcolor = "#000000"
        else:
            result = "Incorrect!"
            self.incorrect += 1
            self.incorrect_list.append(self.this_qn["vocab"])
            textcolor = "#EE0000"
        result += str.format("\n\"%s\" means \"%s\"!" % (self.this_qn["vocab"], self.this_qn["meaning"]))
        # print(result)
        self.txt_result.config(text=result)
        self.txt_result.config(fg=textcolor)
        self.nextQ()

    def testResult(self):
        self.txt_qn.config(text="Test Result")
        score = str.format("Correct:%d\nIncorrect:%d\n" % (self.correct, self.incorrect))
        self.txt_score.config(text=score)

        # wrong vocab
        if self.incorrect > 0:
            time_format = ctime(time()).split(' ')
            time_format[4] = sub(':', '', time_format[4])
            filename = time_format[1] + time_format[3] + time_format[5] + "-" + time_format[4] + ".txt"
            wrong_record_file=open("history\\"+filename,"w",encoding='utf8')
            for vocab in self.incorrect_list:
                self.txtbox_wrong.insert(END, vocab+'\n')
                wrong_record_file.write(vocab+'\n')
            wrong_record_file.close()


        # unpack widgets
        self.txt_vocab.pack_forget()
        self.txt_result.pack_forget()
        self.btn_checkScore.pack_forget()

        # pack widgets
        self.txt_score.pack(side=TOP)
        if (self.incorrect > 0):
            self.txt_wrong.pack(side=TOP)
            self.txtbox_wrong.pack(side=TOP)
        self.btn_nextRound.pack(side=BOTTOM)


# font / credit########################################################################
##font
font_qn = tkfont(family="Times", size=10, slant=ITALIC)
font_vocab = tkfont(family="Times", size=20)
font_choice = tkfont(family="微軟正黑體", size=10)
font_result = tkfont(family="微軟正黑體", size=10)
font_score = tkfont(family="Ariel", size=10, slant=ITALIC, weight=BOLD)
font_wrong = tkfont(family="Times", size=12, slant=ITALIC, weight=BOLD)
font_btn = tkfont(family="Ariel", size=10, slant=ITALIC, weight=BOLD)
font_cr = tkfont(family="Times", size=8, slant=ITALIC)
##copyright
txt_copyright = Label(window, text="® KaielHsu 2021", font=font_cr, bg=bgcolor)
txt_copyright.pack(side=BOTTOM)
#######################################################################################

# window looping########################################################################
if __name__ == '__main__':
    vp = VP_GUI(window)
    window.mainloop()