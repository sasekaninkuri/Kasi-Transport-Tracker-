import psycopg2
from db_setup import create_connection, create_tables
from db_setup import add_driver, add_route, record_trip

def register_driver():
    conn = create_connection()
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
    conn = create_connection()
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
    conn = create_connection()
    cursor = conn.cursor()

    # Get driver ID
    while True:
        try:
            driver_id = int(input("Enter driver ID: "))
            if driver_id <= 0:
                print("Driver ID must be positive.")
                continue

            # Check if driver exists
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE id = %s", (driver_id,))
            if cursor.fetchone()[0] == 0:
                print(f"Driver ID {driver_id} does not exist. Please enter a valid driver ID.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for driver ID.")

    # Get route ID
    while True:
        try:
            route_id = int(input("Enter route ID: "))
            if route_id <= 0:
                print("Route ID must be positive.")
                continue

            # Check if route exists in drivers_routes table
            cursor.execute("SELECT COUNT(*) FROM drivers_routes WHERE id = %s", (route_id,))
            if cursor.fetchone()[0] == 0:
                print(f"Route ID {route_id} does not exist. Please enter a valid route ID.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for route ID.")

    # Get number of passengers
    while True:
        try:
            passengers = int(input("Enter number of passengers: "))
            if passengers < 0:
                print("Number of passengers cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for passengers.")

    # Record the trip
    try:
        trip_record = record_trip(cursor, driver_id, route_id, passengers)
        print(f"Trip logged successfully: {trip_record}")
    except Exception as e:
        print(f"Error logging trip: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def daily_report():
    print("Daily Trip Report: This feature is currently unavailable.")


def main():
    print("Sawubona! Welcome to Kasi Transport Tracker!")
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


if __name__ == "__main__":
    main()
