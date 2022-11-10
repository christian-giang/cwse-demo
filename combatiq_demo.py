import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from datetime import datetime
import time
import base64
import os
from natsort import natsorted

try:
    import pickle5 as pickle
except ImportError:
    import pickle

# *********** DISABLE HAMBURGER MENU **************

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# *********** DEFINITION OF FUNCTIONS **************


# ***********************************************


# ********** PASSWORD CHECK *******************
if 'unlocked' not in st.session_state:
    st.session_state['unlocked'] = False

correct_pass = "CWS3-2022"

if st.session_state['unlocked'] == False:
	text_input_container1 = st.empty()
	text_input_container2 = st.empty()
	text_input_container3 = st.empty()


	text_input_container1.image("redciq-copy.png", width=175)
	text_input_container2.markdown("Please enter the access code to enter your private area.", unsafe_allow_html=True)	
	password = text_input_container3.text_input("Access code", type="password")

	if password == correct_pass:
		st.session_state['unlocked'] = True
		text_input_container1.empty()
		text_input_container2.empty()
		text_input_container3.empty()
	elif password =='':
		text_input_container4 = st.empty()
	else:
		st.error('The password you entered is wrong.')



if st.session_state['unlocked'] == True:

	# ********** SIDEBAR ELEMENTS *******************

	st.sidebar.image("redciq-copy.png", width=175)


	st.sidebar.markdown("###### The fight summary provides an overview with the most important metrics for the selected fight. The action logs allow to trace and visualize all main actions of the fight in chronological order. The last option provides a detailed overview of the metrics by round.")

	list_fights = []

	for file in os.listdir():
		if file.startswith("CWSE"):
			list_fights.append(file)

	list_fights = natsorted(list_fights)

	choice_fight = st.sidebar.selectbox(label="Please select a fight:", options=list_fights)

	choice_subpage = st.sidebar.radio(label=' ', options=('Fight summary', 'Striking logs', 'Striking by round'))


	if choice_subpage == 'Fight summary':
		subpage = 'summary'
	elif choice_subpage == 'Striking logs':
		subpage = 'logs'
	elif choice_subpage == 'Striking by round':
		subpage = 'byround'



	#*************************************************




	#*************** MAIN PAGE ELEMENTS **************

	col1, col2 = st.columns(2)	
	col1.image("cwase.png", width=250)
	col2.markdown("<h4 style='text-align: right; color:white;'> User profile: CWSE</h4>", unsafe_allow_html=True)

	st.markdown("""---""") 
	st.markdown("<h4 style='text-align: center; color:white;'> CWSE29: Charter Hall Colchester (October 08, 2022)</h4>", unsafe_allow_html=True)
	#st.markdown("""---""") 

	col1, col2, col3, col4, col5 = st.columns([2,3,3,3,2])

	fight =  choice_fight + '/'

	df_summary = pd.read_excel(fight + 'summary.xlsx')

	if df_summary['Winner'][0] == df_summary['Fighter_0'][0]:
		name_0 = df_summary["Fighter_0"][0].upper() + ' (W)'
		name_1 = df_summary["Fighter_1"][0].upper() + ' (L)'
	else: 
		name_1 = df_summary["Fighter_1"][0].upper() + ' (W)'
		name_0 = df_summary["Fighter_0"][0].upper() + ' (L)'

	with col2:
		st.markdown("<h5 style='text-align: center; color:white;'>" + name_0 + "</h4>", unsafe_allow_html=True)

	with col3:
		st.markdown("<h5 style='text-align: center; color:white;'> vs. </h4>", unsafe_allow_html=True)

	with col4:
		st.markdown("<h5 style='text-align: center; color:white;'>" + name_1 + "</h4>", unsafe_allow_html=True)



	if subpage== 'summary':

		with col2:
			st.image(fight + '/fighter_0.png', width=150)

		with col4:
			st.image(fight + '/fighter_1.png', width=150)

		st.markdown("""---""") 


		col1, col2, col3 = st.columns([1,20,1])
		with col2:
			st.markdown("<h5 style='text-align: center; color:crimson;'> FIGHT SITUATIONS OVER TIME</h4>", unsafe_allow_html=True)
			st.image(fight + '/dist-sit.png')


		st.markdown("""---""") 

		col1a, col2a, col3a, col4a, col5a, col6a, col7a = st.columns([2,2,2,3,2,2,2])

		col1a.metric("Attempts", df_summary["Attempts_0"][0])
		col2a.metric("Landed", df_summary["Landed_0"][0])
		col3a.metric("Accuracy",  str(df_summary["Accuracy_0"][0])+"%")
		col4a.markdown("<h5 style='text-align: center; color:crimson;'> STRIKES </h4>", unsafe_allow_html=True)
		col5a.metric("Attempts", df_summary["Attempts_1"][0])
		col6a.metric("Landed", df_summary["Landed_1"][0])
		col7a.metric("Accuracy", str(df_summary["Accuracy_1"][0])+"%")

		st.markdown("""---""") 

		col1, col2, col3, col4, col5 = st.columns([1,8,4,8,1])

		with col2:
			st.image(fight + "body-sil_0.png", width=250)

		with col3:
			st.markdown("<h5 style='text-align: center; color:crimson;'> TARGET </h4>", unsafe_allow_html=True)

		with col4:
			st.image(fight + "body-sil_1.png", width=250)

		st.markdown("""---""") 


		col1, col2, col3, col4, col5 = st.columns([1,8,4,8,1])

		

		with col2:
			st.image(fight + "Fighter_0_oct.png", width=250)

		with col3:
			st.markdown("<h5 style='text-align: center; color:crimson;'> CAGE AREA </h4>", unsafe_allow_html=True)

		with col4:
			st.image(fight + "Fighter_1_oct.png", width=250)



			
	elif subpage == 'logs':


		st.markdown("""---""") 

		st.markdown("<h5 style='text-align: left; color:crimson;'> STRIKING LOGS </h5>", unsafe_allow_html=True)

		st.markdown("<p	style='text-align: justify; color:white;'> Below you find all the relevant striking actions of the fight as identified by Combat IQ's AI models. "+ 
		" As of now, striking actions are only analyzed for distance fight situations. " +
		"To visualize the scene associated with an action, select the corresponding ID in the dropdown menu below. </p>", unsafe_allow_html=True)

		st.markdown("""---""") 

		df_logs = pd.read_excel(fight + 'logs_all_cleaned.xlsx')
		st.dataframe(df_logs, height=200, use_container_width=True)

		list_actions = ['']
		list_actions = list_actions + df_logs['ID'].tolist()

		col1, col2 = st.columns([1,3])
		with col1:	
			selected_action = st.selectbox("Select an action ID:", list_actions)
		with col2:
			if selected_action !='': 
				file_ = open(fight + "selected_frames/"+str(selected_action)+".gif", "rb")
				contents = file_.read()
				data_url = base64.b64encode(contents).decode("utf-8")
				file_.close()

				st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True)




	elif subpage == 'byround':

		st.markdown("""---""") 

		st.markdown("<h5 style='text-align: left; color:crimson;'> TOTAL </h5>", unsafe_allow_html=True)

		df_strikes = pd.read_excel(fight + 'stats-strikes-all.xlsx')
		st.dataframe(df_strikes)

		df_targets = pd.read_excel(fight + 'stats-targets-all.xlsx')
		st.dataframe(df_targets)


		# Find number of rounds:
		rounds = 0
		
		for file in os.listdir(fight):
			if file.startswith("stats-strikes-R"):
				rounds = rounds + 1

		for round_i in range(1,rounds+1):
			
			st.markdown("""---""") 

			st.markdown("<h5 style='text-align: left; color:crimson;'> ROUND "+ str(round_i) + " </h5>", unsafe_allow_html=True)

			df_strikes = pd.read_excel(fight + 'stats-strikes-R' + str(round_i) + '.xlsx')
			st.dataframe(df_strikes)

			df_targets = pd.read_excel(fight + 'stats-targets-R'+ str(round_i) +'.xlsx')
			st.dataframe(df_targets)
	
