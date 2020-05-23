import gspread
from oauth2client.service_account import ServiceAccountCredentials
import webbrowser
import requests
import urllib, json
import math

import kivy
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button 
from kivy.uix.widget import Widget 
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.clock import Clock


class MainWindow(Screen):
	location = ObjectProperty(None)
	time = ObjectProperty(None)
	date = ObjectProperty(None)
	air = ObjectProperty(None)
	tank_type = ObjectProperty(None)
	total_volume = ObjectProperty(None)
	current_volume = ObjectProperty(None)
	air_gap = ''


	def get_cumberland(self):

		try:

			#response = requests.get('https://s12.remoteaware.com/api/v1.0/CurrentAssetReading', auth=('tankscan_username', 'tankscan_password'))
			#null = 0
			#true = 1
			#data = response.text

			#y = json.loads(data) 

			#air_gap_raw = (y[1]['ReadingText'])
			asset_name = 'Cumberland'#(y[1]['AssetName'])
			self.air_gap = '1.5'#air_gap_raw[0:5]
			#ReadingDateUTC = (y[1]['ReadingDateUTC'])
			date_recorded = 'cumb date'#ReadingDateUTC[0:10]
			time_recorded = 'cumb time'#ReadingDateUTC[11:19]
			tank_type = 'Horizontal Elliptical'

			self.location.text = asset_name
			self.date.text = date_recorded
			self.time.text = time_recorded
			self.air.text = self.air_gap
			self.tank_type.text = tank_type

		except:

			P_tankscan.show_error_popup()

	def get_shrewsbury(self):

		try:

			#response = requests.get('https://s12.remoteaware.com/api/v1.0/CurrentAssetReading', auth=('tankscan_username', 'tankscan_password'))
			#null = 0
			#true = 1
			#data = response.text

			#y = json.loads(data) 

			#air_gap_raw = (y[1]['ReadingText'])
			asset_name = 'Shrewsbury'#(y[1]['AssetName'])
			self.air_gap = '60'#air_gap_raw[0:5]
			#ReadingDateUTC = (y[1]['ReadingDateUTC'])
			date_recorded = 'shrews date'#ReadingDateUTC[0:10]
			time_recorded = 'shrews time'#ReadingDateUTC[11:19]
			tank_type = 'Horizontal Elliptical'

			self.location.text = asset_name
			self.date.text = date_recorded
			self.time.text = time_recorded
			self.air.text = self.air_gap
			self.tank_type.text = tank_type

		except:

			P_tankscan.show_error_popup()


	

	def get_merimack(self):

		try:

			#response = requests.get('https://s12.remoteaware.com/api/v1.0/CurrentAssetReading', auth=('tankscan_username', 'tankscan_password'))
			#null = 0
			#true = 1
			#data = response.text

			#y = json.loads(data) 

			#air_gap_raw = (y[1]['ReadingText'])
			asset_name = 'Merimack'#(y[1]['AssetName'])
			self.air_gap = '36'#air_gap_raw[0:5]
			#ReadingDateUTC = (y[1]['ReadingDateUTC'])
			date_recorded = 'meri date'#ReadingDateUTC[0:10]
			time_recorded = 'meri time'#ReadingDateUTC[11:19]
			tank_type = 'Vertical Cylinder'

			self.location.text = asset_name
			self.date.text = date_recorded
			self.time.text = time_recorded
			self.air.text = self.air_gap
			self.tank_type.text = tank_type

		except:

			P_tankscan.show_error_popup()

	def get_portsmouth(self):

		try:

			#response = requests.get('https://s12.remoteaware.com/api/v1.0/CurrentAssetReading', auth=('tankscan_username', 'tankscan_password'))
			#null = 0
			#true = 1
			#data = response.text

			#y = json.loads(data) 

			#air_gap_raw = (y[1]['ReadingText'])
			asset_name = 'Portsmouth'#(y[1]['AssetName'])
			self.air_gap = '25'#air_gap_raw[0:5]
			#ReadingDateUTC = (y[1]['ReadingDateUTC'])
			date_recorded = 'ports date'#ReadingDateUTC[0:10]
			time_recorded = 'ports time'#ReadingDateUTC[11:19]
			tank_type = 'Horizontal Cylinder'

			self.location.text = asset_name
			self.date.text = date_recorded
			self.time.text = time_recorded
			self.air.text = self.air_gap
			self.tank_type.text = tank_type

		except:

			P_tankscan.show_error_popup()

	def calc_vol(self):

		air_gap_measured = float(self.air_gap)
		tank_type = self.tank_type.text

		if tank_type == 'Horizontal Elliptical': # decide which tank calculator function to call
			self.calc_vol_horizontal_elliptical(air_gap_measured)

		elif tank_type == 'Horizontal Cylinder':
			self.calc_vol_horizontal_cylinder(air_gap_measured)

		elif tank_type == 'Vertical Cylinder':
			self.calc_vol_vertical_cylinder(air_gap_measured)

		else:  
			P_tankscan.show_error_popup()


	def calc_vol_horizontal_elliptical(self, air_gap_measured):

		try:


			pi = math.pi 

			cm_measure = (air_gap_measured) * 2.54 #-3 is for the added air gap programmed by tankscan  
			cm_liquid_level = 152.4 - cm_measure #inverse air gap to find liquid level

			h = cm_liquid_level#depth of fluid
			a = 226.02 #major axid
			b = 152.4 #minor axis
			l = 1239.52 #length of tank

			a = abs(a/2) #split the tank in half by axis
			b = abs(b/2) #split the tank in half by axis
			l = abs(l/2)

			spvol = (l*pi*a*b)#Total Volume Calc
			total_volume =	((spvol/1000)*2)
			total_volume_gallons = int(total_volume * .264172)
			self.total_volume.text = str(total_volume_gallons)

			self.heavy_func_horizontal_elliptical(h, a, b, l)

		except:

			P_tankscan.show_error_popup()


	def heavy_func_horizontal_elliptical(self, h, a, b, l):

		try:

			pi = math.pi 

			if (h < b):
				spvol = (l*pi*a*b)
				hb = (1-(h/b))
				hb2 = hb * hb 
				hb2 = math.sqrt(1-hb2)
				hb2 = a * (b-h) * hb2
				hb = a * b * math.acos(hb)
				spvol = ((hb - hb2) * l)
				spvov = spvol / 1000

				current_volume_liters = spvov*2
				current_volume_gallons = current_volume_liters * .264172# liters to gallons

				self.current_volume.text = str(round(current_volume_gallons))

			elif h == b or h == (b*2):
				spvol = (l*pi*a*b)
				total_volume = ((spvol/1000)*2)
				total_volume_gallons = int(total_volume * .264172)

				if h == b:
					self.current_volume.text = str(round(total_volume_gallons/2))

				else:
					self.current_volume.text = str(round(total_volume_gallons))

			else:
				spvol = (l*pi*a*b)
				h = b + b -h 
				hb = (1-(h/b))
				hb2 = hb * hb 
				hb2 = math.sqrt(abs(1-hb2))
				hb2 = a * (b-h) * hb2
				hb = a * b * math.acos(hb)
				spvol = spvol - ((hb - hb2) * l)
				spvov = spvol / 1000 #cm3 to liter

				current_volume_liters = spvov*2
				current_volume_gallons = current_volume_liters * .264172# liters to gallons

				self.current_volume.text = str(round(current_volume_gallons))

		except:

			P_tankscan.show_error_popup()




	def calc_vol_horizontal_cylinder(self, air_gap_measured):

		try:

			pi = math.pi

			liquid_height =  60 - air_gap_measured #find liquid level (tank height - air gap = liquid level)

			h = liquid_height / 12 #convert to feet
			tank_diameter = 6 #tank height in feet
			tank_length = 40 #tank length in feet	

			r = tank_diameter/2 #radius

			area = math.acos((r-h)/r)*r**2 - (r-h)*math.sqrt(2*r*h-(h**2))

			liquid_volume = area * tank_length # get liquid volume level cubic feet
			self.current_volume.text = str(round(liquid_volume * 7.481)) # get liquid volume gallons

			tank_length_cm = tank_length * 30.48
			r_cm = r * 30.48

			total_volume = round(pi * (r_cm**2) * tank_length_cm / 1000)
			self.total_volume.text = str(round(total_volume / 3.785))

		except:

			P_tankscan.show_error_popup()



	def calc_vol_vertical_cylinder(self, air_gap_measured):

		try:
		
			pi = math.pi 

			liquid_height = 480 - air_gap_measured

			h = liquid_height / 12
			tank_length = 40
			tank_diameter = 6

			r = tank_diameter / 2

			self.total_volume.text = str(round((pi * ( r**2 ) * tank_length) * 7.481))

			self.current_volume.text = str(round((pi * ( r**2 ) * h) * 7.481))

		except:

			P_tankscan.show_error_popup()


##################################
#### Tank Scan General Error #####
##################################


class P_tankscan(GridLayout):

	def show_error_popup():

		show = P()

		layout = GridLayout(cols = 1, padding = 10)

		popupLabel = Label(text = "Sorry we've encounted an error, please try again", size_hint = (.5, .9))
		closeButton = Button(text = 'Return to Main Page', size_hint = (.5, .1))

		layout.add_widget(popupLabel)
		layout.add_widget(closeButton)

		popup = Popup(title = 'Error Message', content=layout, auto_dismiss=False)
		closeButton.bind(on_press= popup.dismiss)

		popup.open()

##################################
####Restaurant Main Window #######
##################################


class SecondWindow(Screen):
	restaurant_search = ObjectProperty(None)
	restaurant_status = ObjectProperty(None)
	nbd_accounts_len = ''
	lower_user_input = ''


	def current_account(self):

		try:

			scope =  ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('insert_secret_json_key_here', scope)
			client = gspread.authorize(creds)
			sheet = client.open("testing")
			worksheet = sheet.get_worksheet(1)

			nbd_accounts = worksheet.col_values(2)
			competitor_accounts = worksheet.col_values(3)
			open_accounts = worksheet.col_values(4)


			lower_nbd_accounts = list(map(lambda x: x.lower(), nbd_accounts))
			lower_competitor_accounts = list(map(lambda x: x.lower(), competitor_accounts))
			self.lower_user_input = self.restaurant_search.text
			self.lower_user_input1 = self.lower_user_input.lower()

			self.nbd_accounts_len = len(lower_nbd_accounts)
			self.competitor_accounts_len = len(lower_competitor_accounts)
			self.open_accounts_len = len(worksheet.col_values(4))

			self.is_nbd_account = 0
			self.is_competitor_account = 0 
			self.known_account = 0

			for i in lower_nbd_accounts:

				if i == self.lower_user_input1:
					self.is_nbd_account += 1
					self.known_account += 1

			for i in lower_competitor_accounts:

				if i == self.lower_user_input1:
					self.is_competitor_account += 1
					self.known_account +=1

			if self.is_nbd_account == True:
				self.restaurant_status.text = 'Status: NBD Account'

			elif self.is_competitor_account == True:
				self.restaurant_status.text = 'Status: Competitor Account'
				
			else:
				self.restaurant_status.text = 'Status: Open Account'

		except:

			P.show_error_popup()

	def clear_status(self):

		self.restaurant_status.text = ''#clear

	def open_google(self):

		url = "https://www.google.com.tr/search?q={}".format(self.restaurant_search.text)
		webbrowser.open_new_tab(url)

	def open_upload(self):

		nbd_accounts_len_upload = self.nbd_accounts_len + 1
		competitor_accounts_len_upload = self.competitor_accounts_len + 1
		open_accounts_len_upload = self.open_accounts_len + 1
		lower_user_input_upload = self.lower_user_input

		P_upload.send_to_master(self, nbd_accounts_len_upload, competitor_accounts_len_upload, open_accounts_len_upload, lower_user_input_upload, self.is_nbd_account, self.is_competitor_account)


##################################
#####   Main Popup Error  ########
##################################


class P(GridLayout):

	def show_error_popup():

		show = P()

		layout = GridLayout(cols = 1, padding = 10)

		popupLabel = Label(text = "Sorry we've encounted an error, please try again", size_hint = (.5, .9))
		closeButton = Button(text = 'Return to Main Page', size_hint = (.5, .1))

		layout.add_widget(popupLabel)
		layout.add_widget(closeButton)

		popup = Popup(title = 'Error Message', content=layout, auto_dismiss=False)
		closeButton.bind(on_press= popup.dismiss)

		popup.open()

##################################
####    Upload Parameter  ########
##################################

class P_upload(GridLayout):

	def send_to_master(self, nbd_accounts_len_upload, competitor_accounts_len_upload, open_accounts_len_upload, lower_user_input_upload, is_nbd_account, is_competitor_account):

		next_open_cell = ''

		#set initial values in upload screen

		if is_nbd_account == True:
			next_open_cell = str(nbd_accounts_len_upload)


		elif is_competitor_account == True: 
			next_open_cell = str(competitor_accounts_len_upload)


		else:
			next_open_cell = str(open_accounts_len_upload)

		show = P_upload()
		dropdown = DropDown()

		layout = GridLayout(cols = 2, padding = 15)

		recentSearchLabel = Label(text = "Restaurant Entry: ", size_hint = (.2, .2))
		restaurantTextInput = TextInput(text= lower_user_input_upload, size_hint = (.2, .2))

		columnLabel = Label(text = "Upload Column: ", size_hint = (.2, .2))
		columnHeaderLabel = Label(text = "", size_hint = (.2, .2))

		nextOpenCellLabel = Label(text = "Next Open Cell: ", size_hint = (.2, .2))
		openCellTextInput = TextInput(text = next_open_cell, size_hint = (.2, .2))

		uploadButton = Button(text = 'Send to Google Sheets', size_hint = (.2, .2))
		closeButton = Button(text = 'Return to Main Page', size_hint = (.2, .2))

		spacerLabel1 = Label(text = '', size_hint = (.2, .2))#blank space for dropdown list
		spacerLabel2 = Label(text = '', size_hint = (.2, .2))#blank space for dropdown list
		spacerLabel3 = Label(text = '', size_hint = (.2, .2))#blank space for dropdown list
		spacerLabel4 = Label(text = '', size_hint = (.2, .2))#blank space for dropdown list

		#Create Drop Down List

		dropdown_list = ['NBD Accounts', 'Competitor Accounts', 'Unkown Accounts']

		for i in dropdown_list:

			btn = Button(text=i, size_hint_y = None, height = 40,#create button for each Column Header 
						on_release = lambda btn: set_len(self, btn.text))#call set_len and send column header text per button

			btn.bind(on_release=lambda btn: dropdown.select(btn.text))

			dropdown.add_widget(btn)

		def set_len(self, btn_text):

			column_select = btn_text

			if column_select == 'NBD Accounts':
				next_open_cell = str(nbd_accounts_len_upload)
				openCellTextInput.text = next_open_cell#update next open cell textinput
				columnHeaderLabel.text = 'NBD Accounts'

			elif column_select == 'Competitor Accounts':
				next_open_cell = str(competitor_accounts_len_upload)
				openCellTextInput.text = next_open_cell#update next open cell textinput
				columnHeaderLabel.text = 'Competitor Accounts'

			elif column_select == 'Unkown Accounts':
				next_open_cell = str(open_accounts_len_upload)
				openCellTextInput.text = next_open_cell#update next open cell textinput
				columnHeaderLabel.text = 'Unkown Accounts'

			else:
				openCellTextInput.text = 'Error finding next available cell'
			

		mainbutton = Button(text='Column Header', size_hint=(.2, .2))

		layout.add_widget(recentSearchLabel)
		layout.add_widget(restaurantTextInput)

		layout.add_widget(nextOpenCellLabel)
		layout.add_widget(openCellTextInput)

		layout.add_widget(columnLabel)
		layout.add_widget(mainbutton)

		layout.add_widget(spacerLabel1)
		layout.add_widget(spacerLabel2)
		layout.add_widget(spacerLabel3)
		layout.add_widget(spacerLabel4)

		layout.add_widget(uploadButton)
		layout.add_widget(closeButton)

		upload_popup = Popup(title = 'Upload to Google Sheets', title_size = 20, size_hint = (None, None), size=(600, 500), content=layout, auto_dismiss=False)
		uploadButton.bind(on_press = lambda x:P_upload_warning.show_warning(self, openCellTextInput.text, columnHeaderLabel.text, restaurantTextInput.text))
		closeButton.bind(on_press= upload_popup.dismiss)

		mainbutton.bind(on_release= dropdown.open)
		dropdown.bind(on_select=lambda instance, x:setattr(mainbutton, 'text', x))

		upload_popup.open()


##################################
#### Final Upload Warning ########
##################################


class P_upload_warning(GridLayout):

	def show_warning(self, next_open_cell, selected_list, restaurantTextInput):    #Graphical Warning Popup

		next_open_cell = next_open_cell
		upload_column = selected_list
		restaurantTextInput = restaurantTextInput

		show = P_upload_warning()

		layout = GridLayout(cols = 1, padding = 10)
		label = Label(text = 'Warning!\n Changing the "Next Open Cell" to a\n cell with existing data, will cause your\n upload to replace existing data!!!', 
				size_hint = (.2, .2), 
				halign = 'center',
				valign = 'middle',)

		closeButton = closeButton = Button(text = 'Return to Upload', size_hint = (.2, .2))
		uploadButton = Button(text = 'Send to Google Sheets', size_hint = (.2, .2))

		layout.add_widget(label)
		layout.add_widget(closeButton)
		layout.add_widget(uploadButton)

		warning_popup = Popup(title= "Warning!!!", title_size = 20, size_hint = (None, None), size = (300, 400), content = layout, auto_dismiss = False)
		closeButton.bind(on_press = warning_popup.dismiss)
		uploadButton.bind(on_press = lambda x:P_upload_warning.upload(self, next_open_cell, selected_list, restaurantTextInput))

		warning_popup.open()

###########################################
########## Upload Function ################
###########################################	

	def upload(self, next_open_cell, selected_list, restaurantTextInput): 


		if selected_list == 'NBD Accounts':
			column = 2

		elif selected_list == 'Competitor Accounts':
			column = 3

		else:
			column = 4


		try:

			scope =  ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
			creds = ServiceAccountCredentials.from_json_keyfile_name('insert_secret_json_key_here', scope)
			client = gspread.authorize(creds)
			sheet = client.open("testing")
			worksheet = sheet.get_worksheet(1)

			worksheet.update_cell(int(next_open_cell), column, restaurantTextInput)

			P_success.show_success_popup(self)

		except:

			P.show_error_popup()


 
###########################################
#### Successfull Google Sheets Upload #####
###########################################	


class P_success(GridLayout): 

	def show_success_popup(self):

		show = P()

		layout = GridLayout(cols = 1, padding = 10)

		popupLabel = Label(text = "Successfully Uploaded to Google Sheets!", font_size = 20, size_hint = (.5, .9))
		closeButton = Button(text = 'Close', size_hint = (.5, .2))

		layout.add_widget(popupLabel)
		layout.add_widget(closeButton)

		popup = Popup(title = 'Success!',  title_size = 20, size_hint = (None, None), size=(300, 350), content=layout, auto_dismiss=False)
		closeButton.bind(on_press= popup.dismiss)

		popup.open()
		


class ThirdWindow(Screen):
	pass

class WindowManager(ScreenManager):
	pass

kv = Builder.load_file('accounts.kv')

class accountsMainApp(App):
	def build(self):
		return kv


if __name__ == '__main__':
	accountsMainApp().run()