
# For GCI 2019-20 task
# task link : https://codein.withgoogle.com/dashboard/task-instances/6634846919589888/

# Author: Basil labib
# Date: 21-01-2020

# references:
# there are too many to list! 
# those blogs on tkinter etc...
# 2. Tkinter by Example - David Love (good book)

#imports
import random as rd # for random number generation
import sys # for sys.exit()
import csv
from PIL import Image, ImageTk
# GUI modules 
import tkinter as tk
import tkinter.messagebox as msg



# # TODO : 
# 	use better fonts 
# 	use Good borders and colors
# 	use better layout 
# 	properly comment the source code...

# Game class inherits Tk class of tkinter module..
class Game(tk.Tk):

	def __init__(self):
		super().__init__()

		# the instance variables below 
		self.incorrect = 0
		self.correct = 0

		self.atomic_no = None

		self.ptable = []
		with open('elementlist.csv','r') as list_of_elems:
			reader = csv.reader(list_of_elems)

			for row in reader:
				self.ptable.append(row)
		self.no_of_elems = len(self.ptable)
		self.atomic_no = self.get_rand_atomic_no()


		# the GUI Stuff ------------------------------------------------------------------
		self.title('Periodic Table Guessing Game.')
		self.geometry('500x500')   			# may change 

		# -------------------------- the periodic table image -------------------------------------------------
		# Attempt 1 : Not resizable 
		# load = Image.open("periodic_table_img.png")
		# render = ImageTk.PhotoImage(load)
		# img = tk.Label(self, image=render)
		# img.image = render
		# img.place(x=0, y=0)

		# TODO : render a image of the periodic table image
		canvas = tk.Canvas(self, width = 500, height = 100)  
		img = ImageTk.PhotoImage(Image.open("periodic_table_img.png"))  
		canvas.create_image(30, 30, image=img) 
		canvas.pack()  

		self.labels = tk.Frame(self)
		self.labels.pack(side = tk.TOP, padx = 5, pady = 5)

		self.label0 = tk.Label(self.labels, text = 'WELCOME TO PERIODIC TABLE GUESSING GAME!!',
													font='courier',
														fg='#ff0000',bg='#e0d8c3',
															padx = 10, pady = 10)
		self.label0.pack(side = tk.TOP, fill = tk.X)

		self.label1 = tk.Label(self.labels, text='What is the atomic symbol for...', 
													font='helvetica',
														fg='#000000', bg='#ffffcc',
															padx = 10, pady = 10)
		self.label1.pack(side = tk.TOP, fill = tk.X)

		self.label2 = tk.Label(self.labels, text=str(self.atomic_no),
													font='consolas',
														fg='#000000',bg='#e0d8c3',
															padx = 10, pady = 10)
		self.label2.pack(side = tk.TOP, fill = tk.X)

		self.statuslabel = tk.Label(self.labels, text='I am the status label!', 
													font='consolas',
														fg = '#000000',bg='#ffffcc',
															padx = 10, pady = 10)
		self.statuslabel.pack(side = tk.BOTTOM, fill = tk.X)

		self.text_frame = tk.Frame(self)
		self.text_frame.pack(side = tk.BOTTOM)
		self.input_field = tk.Text(self.text_frame, 
								height = 3,
									fg = 'black',
										bg = 'white')

		self.input_field.pack(fill = tk.X)
		self.input_field.bind("<Return>",self.process_input)
		self.input_field.focus_set()


		self.button_frame = tk.Frame(self)
		self.button_frame.pack(side=tk.BOTTOM, pady = 25)

		self.new_button = tk.Button(self.button_frame, text='New',fg='brown',padx = 5,pady = 5,command=self.clicked_new)
		self.answer_button = tk.Button(self.button_frame, text='Show Answer', fg='blue', padx = 5,pady = 5, command=self.clicked_answer)
		self.quit_button = tk.Button(self.button_frame, text='Quit', fg='red',padx = 5,pady = 5,command=self.clicked_quit)
		self.submit_button = tk.Button(self.button_frame, text='Submit',fg= 'green', padx = 5,pady = 5,command=self.clicked_submit)
		
		self.quit_button.pack(side=tk.LEFT, fill = tk.X,padx=10)
		self.new_button.pack(side=tk.LEFT, fill=tk.X,padx=10)
		self.answer_button.pack(side=tk.LEFT, fill = tk.X,padx=10)
		self.submit_button.pack(side=tk.LEFT, fill = tk.X,padx=10)


	def show_popup(self, status, text=None):
		if status == 'correct':
			# msg. blah blah 
			msg.showinfo('Correct Answer!', 'Congratulations! That\'s a correct answer!') #+ str(self.correct))
		elif status == 'incorrect':
			# msg.. show hint...
			msg.showinfo('Incorrect Answer!', 'Oops, that\'s a wrong answer!') #+ str(self.incorrect))
		elif status == 'over':
			# show bad ,sg with score 
			msg.showinfo('GAME OVER!', 'You ran out of chances..Game Over! Score : ' + str(self.correct))
		elif status == 'invalid char':
			msg.showwarning('Warning','Enter only valid characters! There is no '+str(text)+' in the periodic table')
			# warn and say to be careful

	def show_hint(self, text, ans):
		
		for elem in self.ptable:
			if elem[1] == text: idx = elem[0]

		if int(idx) > int(ans): 
			msg.showinfo('Hint!','You are thinking too big! The answer is smaller than you think!')
		elif int(idx) < int(ans):
			msg.showinfo('Hint!','You are thinking too small! Think BIG!') 

	#   ====================== EVENT HANDLING ==========================================

	def clicked_new(self, event = None):
		self.change_status('You pressed New Button!')
		self.clear_infield()
		self.update_game()

	def clicked_submit(self, event = None):
		self.process_input()

	def clicked_quit(self, event = None):
		if msg.askyesno('Really Quit?','Do you really want to quit?'):
			msg.showinfo('Good-Bye!', 'Your score : ' + str(self.correct))
			sys.exit(0)

	def clicked_answer(self, event = None):
		msg.showwarning('Element Symbol.','The symbol of element '+ str(self.atomic_no) + " is "
												+ self.ptable[self.atomic_no-1][1]+
													" ( "+self.ptable[self.atomic_no-1][2]+" )")
		self.change_status('You chose to see the answer :P')
		self.clear_infield()   		# clear everything 
		self.update_game()

	# ====================================================================================

	def process_input(self, event = None):

		text = self.input_field.get(1.0,tk.END).strip()

		if self.is_valid(text):
			if self.is_correct(text, self.atomic_no):
				self.correct += 1
				self.show_popup('correct')
				self.clear_infield()
				self.update_game()
			else:
				self.incorrect += 1
				self.show_popup('incorrect')
				self.show_hint(text, self.atomic_no)
		else:
			self.show_popup('invalid char',text=text)

		# game over, pal...
		if self.incorrect >= 5:
			self.show_popup('over')
			sys.exit(0)

		# clear the field everytime...
		self.clear_infield()



	def clear_infield(self):
		self.input_field.delete(1.0,tk.END)	

	def change_status(self, string):
		self.statuslabel.configure(text=string)

	# ========== THE LOGICAL PART =====================

	def update_game(self):
		self.atomic_no = self.get_rand_atomic_no()
		# update the atomic number question label accordingly...
		self.label2.configure(text=str(self.atomic_no), font='consolas')


	def get_rand_atomic_no(self):
		rint = rd.randint(0,self.no_of_elems - 1)
		return (rint+1) 			# since hydrogen is atomic no 1, not 0 

	def is_valid(self, text):
		is_valid = False
		for elem in self.ptable:
			if text == elem[1]:
				is_valid = True
		return is_valid

	def is_correct(self, text, atomic_no):
		for elem in self.ptable:
			if str(atomic_no) == elem[0] and text == elem[1]:
				return True
		return False

	# start showing...
	def _run(self):
		self.mainloop()

def main():
	game = Game()
	game._run()

if __name__ == "__main__":
	main()