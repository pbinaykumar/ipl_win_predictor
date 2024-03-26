import streamlit as st
import pickle
import pandas as pd

teams = ['Gujarat Titans', 'Mumbai Indians', 'Chennai Super Kings',
       'Sunrisers Hyderabad', 'Royal Challengers Bangalore',
       'Lucknow Super Giants', 'Delhi Capitals','Kolkata Knight Riders', 'Rajasthan Royals', 'Kings XI Punjab']

cities = ['Mumbai', 'Dharamsala', 'Delhi', 'Jaipur', 'Abu Dhabi', 'Chennai',
       'Bengaluru', 'Kolkata', 'Visakhapatnam', 'Hyderabad', 'Chandigarh',
       'Centurion', 'Bangalore', 'Raipur', 'Ahmedabad', 'Nagpur',
       'Indore', 'Port Elizabeth', 'Johannesburg', 'Lucknow', 'Pune',
       'Sharjah', 'Navi Mumbai', 'Durban', 'Ranchi', 'Cape Town',
       'Cuttack', 'Bloemfontein', 'Kimberley', 'East London', 'Dubai',
       'Guwahati']

pipe = pickle.load(open('pipe_new.pkl','rb'))
st.title('IPL Win Predictor 2024')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

selected_city = st.selectbox('Select host city',sorted(cities))

target = int(st.number_input('Target'))

col3,col4,col5 = st.columns(3)

with col3:
    score = int(st.number_input('Score'))
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = int(st.number_input('Wickets out'))
if st.button('Predict Probability'):
    if target and score and overs and wickets and (batting_team != bowling_team):
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10 - wickets
        crr = score/overs
        rrr = (runs_left*6)/balls_left

        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'run_left':[runs_left],'ball_left':[balls_left],'wicket_left':[wickets],'total_run_req':[target],'crr':[crr],'rrr':[rrr]})
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win*100)) + "%")
        st.header(bowling_team + "- " + str(round(loss*100)) + "%")