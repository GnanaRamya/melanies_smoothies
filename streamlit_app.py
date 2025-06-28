# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothies!"""
)
#import streamlit as st
name_on_order= st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be:", name_on_order)
from snowflake.snowpark.functions import col
connection_params= Session.builder.configs({
    "account": st.secrets["HOXXSYJ-GWB61229"],
    "user": st.secrets["GNIMMAGADDA1"],
    "password": st.secrets["Sariyu671@1234"],
    "warehouse": st.secrets["COMPUTE_WH"],
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
})
session = Session.builder.configs(connection_params).create()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))  # Check exact column name
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,max_selections=5
)

if ingredients_list:
   
   ingredients_string=''

   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
   #st.write(ingredients_list)     

 
   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

   #st.write(my_insert_stmt)
   #st.stop()
   time_to_insert = st.button('Submit Order')
   if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


