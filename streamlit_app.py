# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import avg
pip install snowflake-snowpark-python
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!.
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be;', name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options") . select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )


if ingredients_list:    
    ingredients_string= ''
   
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

   
    time_to_insert = st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        success_message = f"Your Smoothie is ordered, {name_on_order}! ✅"
        st.success(success_message)





