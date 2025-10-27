import psycopg2
from db_setup import create_connection, create_tables
from db_setup import add_driver
from db_setup import add_route
from db_setup import record_trip
from db_setup import daily_report





def register_driver(name, taxi_number):
    conn= create_connection()
    cursor = conn.cursor()
    
    name = input("Enter driver's name: ")
    taxi_number = input("Enter taxi number: ")

    add_driver(cursor, name, taxi_number)
    
    
    try:
        print(f"Driver {name} with taxi number {taxi_number} registered successfully.")
    except Exception as e:
        print(f"Error registering driver: {e}")
        
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        
        
def register_new_route():
    conn= create_connection()
    cursor = conn.cursor()


    origin = input("Enter the origin: ")
    destination = input("Enter the destination: ")
    fare = float(input("Enter the fare: "))

    add_route(cursor, origin, destination, fare)

    try:
            print(f"Route from {origin} to {destination} with fare {fare} added successfully.")
    except Exception as e:
        print(f"Error adding route: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


        
def log_trip():
    conn= create_connection()
    cursor = conn.cursor()

    driver_id = int(input("Enter driver ID: "))
    route_id = int(input("Enter route ID: "))
    passengers = int(input("Enter number of passengers: "))

    trip_record = record_trip(cursor, driver_id, route_id, passengers)
    
    try:
        print(f"Trip logged successfully: {trip_record}")
    except Exception as e:
        print(f"Error logging trip: {e}")
        
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        
        
def daily_report(): 
    conn= create_connection()
    cursor = conn.cursor()

    trips = cursor.fetchall()

    print("Daily Trip Report:")
    for trip in trips:
        name, origin, destination, passengers, total_amount = trip
        print(f"Driver: {name}, Route: {origin} to {destination}, Passengers: {passengers}, Total Amount: {total_amount}")

    cursor.close()
    conn.close()
    
    

    
        

def main():
        print(" Sawubona! Welcome to Kasi Transport Tracker!")
create_tables()
menu = {

        "1": "Register Driver",
        "2": "Register New Route",
        "3": "Log Trip",
        "4": "Daily Report",
        "5": "Exit"
    }

while True:
        print("\nMenu:")
        for key, value in menu.items():
            print(f"{key}. {value}")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_driver()
        elif choice == '2':
            register_new_route()
        elif choice == '3':
            log_trip()
        elif choice == '4':
            daily_report()
        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
            
            main()
if __name__ == "__main__":
    main()

        
