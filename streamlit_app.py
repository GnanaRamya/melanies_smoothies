import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


import streamlit as st
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe,max_selections =5
)


# If ingredients are selected, generate SQL
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (name_on_order, ingredients)
    VALUES ("""+ ingredients_string + ""","""+ name_on_order + """);"""
    
     #st.write("Generated SQL:", my_insert_stmt)
    time_to_insert= st.button('Submit Order')
        
