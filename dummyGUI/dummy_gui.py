#!/usr/bin/env python3
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *
import subprocess
import webbrowser


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Instantiate a central widget object
		self.centralWidget = CentralWidget()
		# Set the central widget object as the central widget of the main window
		self.setCentralWidget(self.centralWidget)
		# Set the title for the GUI
		self.setWindowTitle("Neural Network Playground")

		# Instantiate a menu bar object
		self.menubar = self.menuBar()
		# Create a menu option and add it to the menu bar
		self.database = self.menubar.addMenu("Database")
		# Add an action to the database menu option
		self.databaseAction = QAction("Display Database", self)
		# Create the action for the above added action
		self.database.addAction(self.databaseAction)
		# Connect the action to the database view method in the central widget class
		self.database.triggered[QAction].connect(self.centralWidget.databaseView.exec)

		# Create a menu option and add it to the menu bar
		self.help = self.menubar.addMenu("Help")
		# Add an action to the help menu option
		self.helpAction = QAction("Display Help", self)
		# Create the action for the above added action
		self.help.addAction(self.helpAction)
		# Connect the action to the launch help method in the central widget class
		self.help.triggered[QAction].connect(self.centralWidget.launchHelp)


class CentralWidget(QWidget):
	def __init__(self):
		super().__init__()

		# Instantiate a database viewer object in the central widget class to be called in the menu
		self.databaseView = databaseViewer()
		# Create the main layout for the central widget
		self.realmainLayout = QVBoxLayout(self)
		# Create the layout for the game images
		self.mainLayout = QHBoxLayout()
		# Create the layout for the Play buttons
		self.buttonLayout = QHBoxLayout()

		# Instantiate a dialog box object for flappy bird
		self.flappyDialog = flappyOptionSelection()
		# Instantiate a dialog box object for snake
		self.snakeDialog = snakeOptionSelection()
		# Instantiate a dialog box object for breakout
		self.breakoutDialog = breakoutOptionSelection()

		# Retrieve the list of options from the dialog object
		self.flappyOptions = self.flappyDialog.allOptions
		# Retrieve the list of options from the dialog object
		self.snakeOptions = self.snakeDialog.allOptions
		# Retrieve the list of options from the dialog object
		self.breakoutOptions = self.breakoutDialog.allOptions

		# Create a Button to play flappy bird
		self.flappyButton = QPushButton("Play Flappy Bird")
		# Connect it to the get tubes method
		self.flappyButton.clicked.connect(self.getTubes)

		# Create a button to play breakout
		self.breakoutButton = QPushButton("Play Breakout")
		# Connect it to the get breaks method
		self.breakoutButton.clicked.connect(self.getBreaks)

		# Create a button to play snake
		self.snakeButton = QPushButton("Play Snake")
		# Connect it to the get snakes method
		self.snakeButton.clicked.connect(self.getSnakes)

		# Instantiate a QLabel object
		self.flappyLabel = QLabel()
		# Add the flappy bird image to the QLabel object
		self.flappyLabel.setPixmap(QPixmap("flappy.png"))

		# Instantiate a QLabel object
		self.breakoutLabel = QLabel()
		# Add the breakout game image to the QLabel object
		self.breakoutLabel.setPixmap(QPixmap("breakout.png"))

		# Instantiate a QLabel object
		self.snakeLabel = QLabel()
		# Add the snake game image to the QLabel object
		self.snakeLabel.setPixmap(QPixmap("snake.png"))

		# Add the flappy bird image to the game image layout
		self.mainLayout.addWidget(self.flappyLabel)
		# Add stretch between the images
		self.mainLayout.addStretch()
		# Add the snake game image to the game image layout
		self.mainLayout.addWidget(self.snakeLabel)
		# Add stretch between the images
		self.mainLayout.addStretch()
		# Add the breakout game image to the game image layout
		self.mainLayout.addWidget(self.breakoutLabel)
		# Add stretch between the images
		self.mainLayout.addStretch()

		# Add the play flappy bird button to the button layout
		self.buttonLayout.addWidget(self.flappyButton)
		# Add the play snake button to the button layout
		self.buttonLayout.addWidget(self.snakeButton)
		# Add the play breakout button to the button layout
		self.buttonLayout.addWidget(self.breakoutButton)

		# Add the game image layout to the main layout
		self.realmainLayout.addLayout(self.mainLayout)
		# Add the button layout to the main layout
		self.realmainLayout.addLayout(self.buttonLayout)

	def getTubes(self):
		"""This method gets the user selected options from the flappy bird dialog box
		and passes it to the launch method to execute the neural network.
		"""
		# Reset the options list everytime the dialog is called so the user can call
		# multiple windows with different options
		self.flappyDialog.allOptions = []
		# Launch the flappy bird dialog box so the user can select NN options
		self.flappyDialog.exec()
		# If the user presses OK on the dialog box launch the NN with their options
		if self.flappyDialog.termination is True:
			# Launch the NN with the options
			self.launchFlappy(self.flappyDialog.allOptions)
		# Reset the flag to false so that the user can open multiple windows at once
		self.flappyDialog.termination = False

	def getBreaks(self):
		"""This method gets the user selected options from the breakout dialog box
		and passes it to the launch method to execute the neural network.
		"""
		# Reset the options list everytime the dialog is called so the user can call
		# multiple windows with different options
		self.breakoutDialog.allOptions = []
		# Launch the breakout dialog box so the user can select NN options
		self.breakoutDialog.exec()
		# If the user presses OK on the dialog box launch the NN with their options
		if self.breakoutDialog.termination is True:
			# Launch the NN with the options
			self.launchBreakout(self.breakoutDialog.allOptions)
		# Reset the flag to false so that the user can open multiple windows at once
		self.flappyDialog.termination = False

	def getSnakes(self):
		"""This method gets the user selected options from the flappy bird dialog box
		and passes it to the launch method to execute the neural network.
		"""
		# Reset the options list everytime the dialog is called so the user can call
		# multiple windows with different options
		self.snakeDialog.allOptions = []
		# Launch the snake dialog box so the user can select NN options
		self.snakeDialog.exec()
		# If the user presses OK on the dialog box launch the NN with their options
		if self.snakeDialog.termination is True:
			# Launch the NN with the options
			self.launchSnake(self.snakeDialog.allOptions)
		# Reset the flag to false so that the user can open multiple windows at once
		self.flappyDialog.termination = False

	def temp(self):
		print(self.flappyOptions)

	def launchBreakout(self, optionsList):
		""" This method takes the user options and launches the Neural Network using subprocess

			Input: list of strings [options <str>]
			Output: launches NN via subprocess
		"""
		# Create a dictionary to convert the string of readable user options into integers
		# because I'm too lazy to parse the full string
		parameterdict = {"Normal Settings": 0, "Increase Ball Speed": 1, "Increase Bat Speed": 2, "Increase Both": 3}
		# Start a for loop to check for the game option the user selected
		for key, value in parameterdict.items():
			# If the key matches the user selected option
			if key == optionsList[0]:
				# Then set option one to be that key
				option1 = str(parameterdict[key])
		# Set the option variables to user selected NN options
		option2 = optionsList[1]
		option3 = optionsList[2]
		# Create a string for the subprocess call that includes the options the user selected
		string = "python3 breakout_driver.py -i 4 -o 1 -h " + option2 + " -l " + option3 + " -p " + option1
		# Call subprocess in the shell with a new session each time so the user can open multiple runs at once
		subprocess.Popen([string], shell=True, start_new_session=True)

	def launchFlappy(self, optionsList):
		""" This method takes the user options and launches the Neural Network using subprocess

			Input: list of strings [options <str>]
			Output: launches NN via subprocess
		"""
		# Create a dictionary to convert the string of readable user options into integers
		# because I'm too lazy to parse the full string
		parameterdict = {"Unvariable Tubes": 0, "Random Tubes": 1, "Shift Tubes Up": 2, "Shift Tubes Down": 3}
		# Start a for loop to check for the game option the user selected
		for key, value in parameterdict.items():
			# If the key matches the user selected option
			if key == optionsList[0]:
				# Then set option one to be that key
				option1 = str(parameterdict[key])
		# Set the option variables to user selected NN options
		option2 = optionsList[1]
		option3 = optionsList[2]
		# Create a string for the subprocess call that includes the options the user selected
		string = "python3 flappy_driver.py -i 10 -o 1 -h " + option2 + " -l " + option3 + " -p " + option1
		# Call subprocess in the shell with a new session each time so the user can open multiple runs at once
		sp = subprocess.Popen([string], shell=True, start_new_session=True, stdout=subprocess.PIPE)
		out = sp.communicate()
		print(out)

	def launchSnake(self, optionsList):
		""" This method takes the user options and launches the Neural Network using subprocess

			Input: list of strings [options <str>]
			Output: launches NN via subprocess
		"""
		# Create a dictionary to convert the string of readable user options into integers
		# because I'm too lazy to parse the full string
		parameterdict = {"Normal Settings": 0, "Increase Speed": 1, "Add Barricade Blocks": 2}
		# Start a for loop to check for the game option the user selected
		for key, value in parameterdict.items():
			# If the key matches the user selected option
			if key == optionsList[0]:
				# Then set option one to be that key
				option1 = str(parameterdict[key])
		# Set the option variables to user selected NN options
		option2 = optionsList[1]
		option3 = optionsList[2]
		# Create a string for the subprocess call that includes the options the user selected
		string = "python3 snakeio_driver.py -i 4 -o 1 -h " + option2 + " -l " + option3 + " -p " + option1
		# Call subprocess in the shell with a new session each time so the user can open multiple runs at once
		subprocess.Popen([string], shell=True, start_new_session=True)

	def launchHelp(self):
		""" This method has no inputs or outputs but when called it launches the webHelp.py script which
			boots up the help website and then the website is opened up in the users default browser
		"""
		webbrowser.open_new("http://127.0.0.1:5000")


class flappyOptionSelection(QDialog):
	def __init__(self):
		super().__init__()

		# Create an empty list that will contain the user selected options
		self.allOptions = []
		# Create a flag to know if the user hit OK or not
		self.termination = False
		# Set the main layout for the dialog box
		self.mainLayout = QVBoxLayout(self)
		# Set the layout for the buttons
		self.ButtonLayout = QHBoxLayout()

		# Create the OK button
		self.ok = QPushButton("OK")
		# When the OK button is clicked it will call the OK event method
		self.ok.clicked.connect(self.okEvent)

		# Create the CANCEL button
		self.cancel = QPushButton("CANCEL")
		# When the CANCEL button is clicked it will call the cancel event method
		self.cancel.clicked.connect(self.cancelEvent)

		# Instantiate a combo box object for the game modification option
		self.tubeOptions = QComboBox(self)
		# Add the items to the tube options combo box
		self.tubeOptions.addItems(["Unvariable Tubes", "Random Tubes", "Shift Tubes Up", "Shift Tubes Down"])

		# Instantiate a combo box object for the hidden layer option
		self.hiddenLayerOptions = QComboBox(self)
		# Add the items to the hidden layer option combo box
		self.hiddenLayerOptions.addItems(["0", "1", "2"])

		# Instantiate a combo box object for the hidden neurons option
		self.hiddenNeurons = QComboBox(self)
		# Add the items to the hidden neuron options to the combo box
		self.hiddenNeurons.addItems(["2", "3", "4"])

		# Create a label for the hidden layer option
		self.layerlabel = QLabel("Select Number of Hidden Layers")
		# Create a label for the game modification option
		self.tubelabel = QLabel("Select Tube Parameter")
		# Create a label for the hidden neuron option
		self.neuronlabel = QLabel("Select Number of Hidden Neurons")

		# Add the OK button to the button layout
		self.ButtonLayout.addWidget(self.ok)
		# Add the CANCEL button to the button layout
		self.ButtonLayout.addWidget(self.cancel)

		# Add the label for the game modification option to the main layout
		self.mainLayout.addWidget(self.tubelabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the game modification combo box to the main layout
		self.mainLayout.addWidget(self.tubeOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the label for the hidden layer option to the main layout
		self.mainLayout.addWidget(self.layerlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden layer combo box to the main layout
		self.mainLayout.addWidget(self.hiddenLayerOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron option label to the main layout
		self.mainLayout.addWidget(self.neuronlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron combo box
		self.mainLayout.addWidget(self.hiddenNeurons)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the button layout to the main layout
		self.mainLayout.addLayout(self.ButtonLayout)

	def okEvent(self):
		""" This method has no inputs or outputs but when called it updates the options list
			with the ones the user selected and sets the exit flag to true
		"""
		# Append the in game options to the option list
		self.allOptions.append(self.tubeOptions.currentText())
		# Append the hidden layer options to the option list
		self.allOptions.append(self.hiddenLayerOptions.currentText())
		# Append the hidden neuron options to the option list
		self.allOptions.append(self.hiddenNeurons.currentText())
		# Set the flag to true
		self.termination = True
		# Close the dialog box
		self.close()

	def cancelEvent(self):
		""" This method has no inputs or outputs but when called it clears the options list
			and closes the dialog box"""
		self.allOptions = []
		self.close()


class snakeOptionSelection(QDialog):
	def __init__(self):
		super().__init__()

		# Create an empty list that will contain the user selected options
		self.allOptions = []
		# Create a flag to know if the user hit OK or not
		self.termination = False
		# Set the main layout for the dialog box
		self.mainLayout = QVBoxLayout(self)
		# Set the layout for the buttons
		self.ButtonLayout = QHBoxLayout()

		# Create an OK button
		self.ok = QPushButton("OK")
		# When the OK button is clicked it will call the OK event method
		self.ok.clicked.connect(self.okEvent)

		# Create a CANCEL button
		self.cancel = QPushButton("CANCEL")
		# Whent the CANCEL button is clicked it will call the cancel event method
		self.cancel.clicked.connect(self.cancelEvent)

		# Instantiate a Combo box object for the game options
		self.gameOptions = QComboBox(self)
		# Add the options to the above combo box
		self.gameOptions.addItems(["Normal Settings", "Increase Speed", "Add Barricade Blocks"])

		# Instantiate a combo box object for the hidden layer options
		self.hiddenLayerOptions = QComboBox(self)
		# Add the hidden layer options to the above combo box
		self.hiddenLayerOptions.addItems(["0", "1", "2"])

		# Instantiate a combo box object for the hidden neuron options
		self.hiddenNeurons = QComboBox(self)
		# Add the hidden neuron options to the above combo box
		self.hiddenNeurons.addItems(["2", "3", "4"])

		# Create a label for the hidden layer options
		self.layerlabel = QLabel("Select Number of Hidden Layers")
		# Create a label for the game options
		self.gamelabel = QLabel("Select Game Parameter")
		# Create a label for the hidden neuron options
		self.neuronlabel = QLabel("Select Number of Hidden Neurons")

		# Add the OK button to the button layout
		self.ButtonLayout.addWidget(self.ok)
		# Add the CANCEL button to the button layout
		self.ButtonLayout.addWidget(self.cancel)

		# Add the game options label to the main layout
		self.mainLayout.addWidget(self.gamelabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the game options combo box to the main layout
		self.mainLayout.addWidget(self.gameOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden layer options label to the main layout
		self.mainLayout.addWidget(self.layerlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden layer options combo box to the main layout
		self.mainLayout.addWidget(self.hiddenLayerOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron options label to the main layout
		self.mainLayout.addWidget(self.neuronlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron combo box to the main layout
		self.mainLayout.addWidget(self.hiddenNeurons)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the button layout to the main layout
		self.mainLayout.addLayout(self.ButtonLayout)

	def okEvent(self):
		""" This method has no inputs or outputs but when called it updates the options list
			with the ones the user selected and sets the exit flag to true
		"""
		# Append the in game options to the option list
		self.allOptions.append(self.gameOptions.currentText())
		# Append the hidden layer options to the option list
		self.allOptions.append(self.hiddenLayerOptions.currentText())
		# Append the hidden neuron options to the option list
		self.allOptions.append(self.hiddenNeurons.currentText())
		# Set the flag to true
		self.termination = True
		# Close the dialog box
		self.close()

	def cancelEvent(self):
		""" This method has no inputs or outputs but when called it clears the options list
			and closes the dialog box"""
		self.allOptions = []
		self.close()


class breakoutOptionSelection(QDialog):
	def __init__(self):
		super().__init__()

		# Create an empty list that will contain the user selected options
		self.allOptions = []
		# Create a flag to know if the user hit OK or not
		self.termination = False
		# Set the main layout for the dialog box
		self.mainLayout = QVBoxLayout(self)
		# Set the layout for the buttons
		self.ButtonLayout = QHBoxLayout()

		# Create an OK button
		self.ok = QPushButton("OK")
		# When the OK button is clicked it will call the OK event method
		self.ok.clicked.connect(self.okEvent)

		# Create a CANCEL button
		self.cancel = QPushButton("CANCEL")
		# Whent the CANCEL button is clicked it will call the cancel event method
		self.cancel.clicked.connect(self.cancelEvent)

		# Create a combo box for the in game options
		self.gameOptions = QComboBox(self)
		# Add the options to the above combo box
		self.gameOptions.addItems(["Normal Settings", "Increase Ball Speed", "Increase Bat Speed", "Increase Both"])

		# Instantiate a combo box object for the hidden layer options
		self.hiddenLayerOptions = QComboBox(self)
		# Add the hidden layer options to the above combo box
		self.hiddenLayerOptions.addItems(["0", "1", "2"])

		# Instantiate a combo box object for the hidden neuron options
		self.hiddenNeurons = QComboBox(self)
		# Add the hidden neuron options to the above combo box
		self.hiddenNeurons.addItems(["2", "3", "4"])

		# Create a label for the hidden layer options
		self.layerlabel = QLabel("Select Number of Hidden Layers")
		# Create a label for the game options
		self.gamelabel = QLabel("Select Game Parameter")
		# Create a label for the hidden neuron options
		self.neuronlabel = QLabel("Select Number of Hidden Neurons")

		# Add the OK button to the button layout
		self.ButtonLayout.addWidget(self.ok)
		# Add the CANCEL button to the button layout
		self.ButtonLayout.addWidget(self.cancel)

		# Add the game options label to the main layout
		self.mainLayout.addWidget(self.gamelabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the game options combo box to the main layout
		self.mainLayout.addWidget(self.gameOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden layer options label to the main layout
		self.mainLayout.addWidget(self.layerlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden layer options combo box to the main layout
		self.mainLayout.addWidget(self.hiddenLayerOptions)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron options label to the main layout
		self.mainLayout.addWidget(self.neuronlabel)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the hidden neuron combo box to the main layout
		self.mainLayout.addWidget(self.hiddenNeurons)
		# Add stretch
		self.mainLayout.addStretch()
		# Add the button layout to the main layout
		self.mainLayout.addLayout(self.ButtonLayout)

	def okEvent(self):
		""" This method has no inputs or outputs but when called it updates the options list
			with the ones the user selected and sets the exit flag to true
		"""
		# Append the in game options to the option list
		self.allOptions.append(self.gameOptions.currentText())
		# Append the hidden layer options to the option list
		self.allOptions.append(self.hiddenLayerOptions.currentText())
		# Append the hidden neuron options to the option list
		self.allOptions.append(self.hiddenNeurons.currentText())
		# Set the flag to true
		self.termination = True
		# Close the dialog box
		self.close()

	def cancelEvent(self):
		""" This method has no inputs or outputs but when called it clears the options list
			and closes the dialog box"""
		self.allOptions = []
		self.close()


class databaseViewer(QDialog):
	def __init__(self):
		super().__init__()

		# Create a sqlite database
		self.db = QSqlDatabase.addDatabase('QSQLITE')
		# Set the name of the database
		self.db.setDatabaseName("sports.db")
		# Open the database so that it can accept queries
		self.db.open()
		# Instantiate a query object
		self.query = QSqlQuery()
		# Create a table within the database
		self.query.exec_("create table sportsmen( id int primary key"
		                 ", firstname varchar(20), lastname varchar(20))")
		# Insert into the table
		self.query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")

		# Instantiate a model object
		self.model = QSqlTableModel()
		# Create a variable to delete the rows
		self.delrow = -1
		# Initialize the model object
		self.initializeModel(self.model)
		# Create a view of the model object
		self.view1 = self.createView("Table Model (View 1)", self.model)

		# Create the layout for the table dialog box
		self.dlgLayout = QVBoxLayout()
		# Add the model view to the dialog box layout
		self.dlgLayout.addWidget(self.view1)
		# self.button = QPushButton("Add a row")
		# self.button.clicked.connect(self.addrow)
		# self.dlgLayout.addWidget(self.button)
		# self.btn1 = QPushButton("Delete a row")
		# self.btn1.clicked.connect(lambda: self.model.removeRow(self.view1.currentIndex().row()))
		# self.dlgLayout.addWidget(self.btn1)
		self.setLayout(self.dlgLayout)
		self.setWindowTitle("Database Viewer")

	def initializeModel(self, model):
		""" This method creates a model that allows the database to be viewed
			in a readable way for the user. It takes in a model object as input

			Input: SQL Table Model object

		"""
		# Set the table that the model will display
		model.setTable("sportsmen")
		# Set it so that the model will update evertime something is added to the database
		model.setEditStrategy(QSqlTableModel.OnFieldChange)
		# Select the model to edit the headers
		model.select()
		# Set the first header title
		model.setHeaderData(0, Qt.Horizontal, "ID")
		# Set the second header title
		model.setHeaderData(1, Qt.Horizontal, "First Name")
		# Set the third header title
		model.setHeaderData(2, Qt.Horizontal, "Last Name")

	def createView(self, title, model):
		""" This method takes in a title for the view and a model object
			and outputs a view for the database

			Input: string, model object
			Output: table view object
		"""
		# Instantiate a view object
		view = QTableView()
		# Create a view of the model object
		view.setModel(model)
		# Set the window title
		view.setWindowTitle(title)
		# Output the view object
		return (view)

	# def addrow(self):
	# 	ret = self.model.insertRows(self.model.rowCount(), 1)
	#
	# def findrow(self, i):
	# 	delrow = i.row()


def main():
	# Instantiate a QApplication object
	app = QApplication([])
	# Instantiate a main window object
	mw = MainWindow()
	# Show the main window
	mw.show()
	# Instantiate a QProcess object
	webProcess = QProcess()
	# Spin up the website
	webProcess.start("python3 webHelp.py")
	# Exit when the app is done being executed
	exit(app.exec())
	# Terminate the web server after the app is terminated
	webProcess.terminate()


if __name__ == '__main__':
	main()