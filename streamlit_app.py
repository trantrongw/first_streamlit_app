import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title('my parrents new healthy dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_show)

#create funtion
def get_fruit_data(this_fruit_choise):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choise)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


#New Sector
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit!!")
  else:
      back_from_funtion = get_fruit_data(fruit_choice)
      streamlit.dataframe(back_from_funtion)
except URLError as e:
  streamlit.error()
  
streamlit.header("the fruit_load_list contain:")
#snow funtion
def get_fruit_load_list():
  with my_cnx.cursor() as mycursor:
       mycursor.execute("select * from fruit_load_list")
       return mycursor.fetchall()

#Add a button
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_datarow = get_fruit_load_list()
  streamlit.dataframe(my_datarow)
  
#dont run any past
streamlit.stop()

#allow end user enter text
var01 = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thank for adding ', var01)

#Test
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
