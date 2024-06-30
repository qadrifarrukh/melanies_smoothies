# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on Smoothie will be: ',name_on_order)

#
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", 'Peaches'))
# st.write("You selected:", option)
#




# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert snowpark dataframe to pandas dataframe so we can use the loc function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose upto 5 ingridients'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
        
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""
    # st.write(my_insert_stmt)
    # st.stop


    
    # if ingredients_string:
    #     session.sql(my_insert_stmt).collect()
    #     st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert = st.button('Submit Form')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered: {name_on_order}!', icon="✅")

# new section to display fruityvice nutrition information
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
# fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

