import psycopg2
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
# Function to establish a connection to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="demo_db",
        user="postgres",
        password="123"
    )
    return conn
# Streamlit app
def main():
    conn = connect_to_db()
    cursor = conn.cursor()
    st.header("FLEMS AIRLINES DATABASE")
    new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Functions</p>'
    st.sidebar.markdown(new_title, unsafe_allow_html=True)
    st.header('INSERT')
    st.sidebar.markdown('[Go to INSERT](#insert)')
    ######INSERT
    # Insert a record into the customer table
    st.subheader("Insert a record into the customers table")
    id = st.text_input("Enter the id:")
    gender = st.text_input("Enter gender:")
    age = st.text_input("Enter age:")
    type = st.text_input("Enter type:")
    purpose = st.text_input("Enter purpose:")
    if st.button("Insert"):
        cursor.execute(
            "INSERT INTO flems.customer (id,gender,age,type,purpose) VALUES (%s, %s, %s,%s,%s)",
            (id, gender, age,type,purpose)
        )
        conn.commit()
        st.success("Record inserted successfully!")
    # Delete a record from the customer table
    st.header('DELETE')
    st.sidebar.markdown('[Go to DELETE](#delete)')
    st.subheader("Delete a record from the customers table")
    id = st.text_input("Enter customer id to be deleted:")
    if st.button("Delete"):
        cursor.execute(
            "DELETE FROM flems.customer WHERE id = %s",
            (id,)
        )
        conn.commit()
        st.success("Record deleted successfully!")
    #display the record inserted
    # st.subheader("Display the record inserted")
    # cursor.execute("SELECT * FROM flems.customer WHERE id = %s", (id,))
    # rows = cursor.fetchall()
    # for row in rows:
    #     st.write(row)
    # Perform a query on the customer table
    st.subheader("Display 10 rows of the customer table")
    cursor.execute("SELECT * FROM flems.customer limit 10")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)   
    #search
    st.header('SEARCH')
    st.sidebar.markdown('[Go to SEARCH](#search)')
    st.subheader("Search the flights")
    search_value = st.text_input("Enter the flight id to be searched:")
    if st.button("Search"):
        cursor.execute(
            "SELECT * FROM flems.flights WHERE flight_id = %s",
            (search_value,)
        )
        rows = cursor.fetchall()
        for row in rows:
            st.write(row)
    st.header('UPDATE')
    st.sidebar.markdown('[Go to UPDATE](#update)')
    # Update arrival time (arr_time), departure time (de_time) and destination airport (dest_airport) of a flight
    st.subheader("Update the flights schedule")
    flight_id = st.text_input("Enter the flight id to be updated:")
    arr_time = st.text_input("Enter the arrival time:")
    dep_time = st.text_input("Enter the departure time:")
    dest_airport = st.text_input("Enter the destination airport:")
    schedule_id=st.text_input("Enter the schedule id:")
    if st.button("Update"):
        cursor.execute(
            "UPDATE flems.schedule SET arr_time = %s, dep_time = %s, dest_airport = %s WHERE flight_id = %s and schedule_id = %s",
            (arr_time, dep_time, dest_airport, flight_id,schedule_id)
        )
        conn.commit()
        st.success("Record updated successfully!")
    #####top 5 busiest airports
    st.header('TOP 5 BUSIEST AIRPORTS')
    st.sidebar.markdown('[Go to TOP 5 BUSIEST AIRPORTS](#top5)')
    # Top 5 busiest airports
    st.subheader("TOP5")
    #if st.button("Top 5 busiest airports"):
    cursor.execute("SELECT a.airport_code FROM flems.schedule as s, flems.airport as a WHERE a.airport_code = s.dest_airport GROUP BY a.airport_code ORDER BY (COUNT(schedule_id)) DESC LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)
    ## airlines and number of flights  leaving  between certain times and airports on a particular day
    st.header('AIRLINES AND NUMBER OF FLIGHTS FROM ATL')
    st.sidebar.markdown('[Go to AIRLINES AND NUMBER OF FLIGHTS](#airlines)')
    st.subheader("AIRLINES")
    #enter origin and destination
    #origin_airport = st.text_input("Enter the origin:")
    #dest_airport = st.text_input("Enter the destination:")
    #enter time
    dep_time1 = st.text_input("Enter the departure time of flight:")
    arr_time1 = st.text_input("Enter the arrival time of flight:")
    #enter day
    flight_date = st.text_input("Enter the date of the flight:")
    if st.button("Airlines and number of flights"):
        cursor.execute("SELECT a.name, COUNT(*) as count FROM flems.schedule as s, flems.flights as f, flems.airlines as a WHERE s.flight_id=f.flight_id AND f.opr_airline_code = a.airline_code AND s.dep_time> %s AND s.arr_time< %s AND s.flight_date = %s AND s.origin_airport='ATL' GROUP BY(a.name) ORDER BY COUNT(*) DESC", (dep_time1,arr_time1,flight_date))
        rows = cursor.fetchall()
        for row in rows:
            st.write(row)
    #display top 5 route of the flight where the number of dissatisfied sentiments are the maximum
    st.header('TOP 5 ROUTES')
    st.sidebar.markdown('[Go to TOP 5 ROUTES](#routes)')
    st.subheader("ROUTES")
    cursor.execute("SELECT origin_airport, dest_airport, count(s.id) FROM flems.sentiment as s, flems.airlines as air, flems.flights as f, flems.schedule as sch  WHERE s.airline_code = air.airline_code AND air.airline_code=f.opr_airline_code AND f.flight_id = sch.flight_id AND s.sentiment='Dissatisfied' GROUP BY (origin_airport,dest_airport) ORDER BY (COUNT(s.id)) DESC LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)
    ##airline which has provided the cheapest price ticket on a particular route as per historical data
    st.header('CHEAPEST AIRLINE')
    st.sidebar.markdown('[Go to CHEAPEST AIRLINE](#cheapest)')
    st.subheader("CHEAPEST")
    #enter origin and destination
    origin_airport = st.text_input("Enter the origin:")
    dest_airport = st.text_input("Enter the destination:")
    if st.button("Cheapest airline"):
        cursor.execute("select   distinct f.opr_airline_code, min(b.price_tkt) as p from flems.booking as b join flems.flights as f on  f.flight_id=b.flight_id where origin_airport=%s and dest_airport = %s group by f.opr_airline_code order by p asc limit 1", (origin_airport,dest_airport))
        rows = cursor.fetchall()
        for row in rows:
            st.write(row)
    ##### AVERAGE TICKET PRICE
    st.header('AVERAGE TICKET PRICE')
    st.sidebar.markdown('[Go to AVERAGE TICKET PRICE](#calculate)')
    # Average ticket price of a flight
    st.subheader("CALCULATE")
    #enter origin and destination
    origin_airport2 = st.text_input("Enter the origin2:")
    dest_airport2 = st.text_input("Enter the destination2:")
    #enter class
    #class_id = st.text_input("Enter the class:")
    if st.button("Calculate average ticket price"):
        cursor.execute("SELECT   AVG(flems.booking.price_tkt) as avg_price FROM flems.booking  WHERE flems.booking.origin_airport = %s AND flems.booking.dest_airport = %s ",(origin_airport2, dest_airport2))
    #    )
        rows = cursor.fetchall()
        for row in rows:
            st.write(row)
   # Close the database connection
### LINEAR REGRESSION to predict the ticket price using a data from a query
#use table bs as a dataframe
#     st.header('REGRESSION')
#     st.sidebar.markdown('[Go toREGRESSION](#regression)')
#     st.subheader("regression")
#     ## convert table bs to a dataframe
#     #
#     cursor.execute("SELECT DISTINCT origin_airport FROM flems.booking")
#     origin_airport11 = [row[0] for row in cursor.fetchall()]
#     cursor.execute("SELECT DISTINCT dest_airport FROM flems.booking")
#     dest_airport11 = [row[0] for row in cursor.fetchall()]
#     origin_airport1 = st.selectbox('Origin Airport', sorted(origin_airport11))
#     dest_airport1= st.selectbox('Destination Airport', sorted(dest_airport11))
#     future_date = st.date_input('Future Date')
#     input_data = pd.DataFrame({'origin_airport1': [origin_airport1],
#                                'dest_airport1': [dest_airport1],
#                                'Future Date': [future_date]})
#     df=pd.read_sql_query("select b.booking_id,b.customer_id, b.flight_id, b.origin_airport,b.dest_airport,b.num_tkt, b.price_tkt, s.schedule_id, s.delay_time from flems.booking as b join flems.schedule as s on b.flight_id=s.flight_id where b.origin_airport=%s and b.dest_airport=%s", conn, params=(origin_airport1,dest_airport1))
#     input_data = pd.merge(input_data, df, left_on=['origin_airport1', 'dest_airport1'], right_on=['origin_airport', 'dest_airport'])
#     #input_data['Future Date'] = (input_data['Future Date'] - pd.Timestamp.now()) / pd.Timedelta(days=1)
#     #input_data = input_data[['Future Date', 'Departure Time',  'Flight Duration']]
#     reg = RandomForestRegressor()
#     #fit the model input data drop price on x axis and price on y axis
#     reg.fit(input_data.drop('price_tkt', axis=1), input_data['price_tkt'])
#     prediction = reg.predict(input_data)  
# #display the predicted price
#     st.write(prediction)
    # if st.button('Predict'):
    # price = prediction[0]
    # st.write(f'The predicted price for a ticket from {origin} to {destination} on {future_date} is ${price:.2f}')
    cursor.close()
    conn.close()
if __name__ == '__main__':
    main()

