import csv
from colorama import Fore, Style, init
from my_db_setup import create_connection, create_tables
from my_db_setup import add_driver, add_route, record_trip, daily_report as get_daily_report


init(autoreset=True)  # ensures color resets after each print


# ------------------- REGISTER DRIVER -------------------
def register_driver():
    conn = create_connection()
    cursor = conn.cursor()
    
    name = input("🚖 Enter driver's name: ")
    taxi_number = input("🆔 Enter taxi number: ")

    try:
        add_driver(cursor, name, taxi_number)
        conn.commit()
        print(Fore.GREEN + f"✅ Driver {name} with taxi number {taxi_number} registered successfully.")
    except Exception as e:
        print(Fore.RED + f"❌ Error registering driver: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- REGISTER ROUTE -------------------
def register_new_route():
    conn = create_connection()
    cursor = conn.cursor()

    origin = input("📍 Enter the origin: ")
    destination = input("📍 Enter the destination: ")
    fare = float(input("💰 Enter the fare: "))

    try:
        add_route(cursor, origin, destination, fare)
        conn.commit()
        print(Fore.GREEN + f"✅ Route from {origin} to {destination} with fare {fare} added successfully.")
    except Exception as e:
        print(Fore.RED + f"❌ Error adding route: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- LOG TRIP -------------------
def log_trip():
    conn = create_connection()
    cursor = conn.cursor()

    # Get driver ID
    while True:
        try:
            driver_id = int(input("🚖 Enter driver ID: "))
            cursor.execute("SELECT COUNT(*) FROM drivers WHERE id = %s", (driver_id,))
            if cursor.fetchone()[0] == 0:
                print(Fore.YELLOW + f"Driver ID {driver_id} does not exist.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

    # Get route ID
    while True:
        try:
            route_id = int(input("🛣️ Enter route ID: "))
            cursor.execute("SELECT COUNT(*) FROM drivers_routes WHERE id = %s", (route_id,))
            if cursor.fetchone()[0] == 0:
                print(Fore.YELLOW + f"Route ID {route_id} does not exist.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

    # Get passengers
    while True:
        try:
            passengers = int(input("👥 Enter number of passengers: "))
            if passengers < 0:
                print(Fore.YELLOW + "Number of passengers cannot be negative.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

    try:
        trip_record = record_trip(cursor, driver_id, route_id, passengers)
        conn.commit()
        print(Fore.GREEN + f"✅ Trip logged successfully: {trip_record}")
    except Exception as e:
        print(Fore.RED + f"❌ Error logging trip: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- DAILY REPORT -------------------
def daily_report():
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        report_data = get_daily_report(cursor)
        
        if not report_data:
            print(Fore.YELLOW + "No trips recorded today.")
            return
        
        print(Fore.CYAN + "📊 Daily Trip Report:")
        print(Fore.YELLOW + "Driver | Total Passengers | Total Earnings")
        for row in report_data:
            print(Fore.GREEN + f"{row[0]} | {row[1]} | {row[2]}")

        with open('daily_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Driver", "Total Passengers", "Total Earnings"])
            writer.writerows(report_data)

        print(Fore.GREEN + "✅ Report exported successfully to daily_report.csv")
    
    except Exception as e:
        print(Fore.RED + f"❌ Error generating report: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- SEARCH DRIVER -------------------
def search_driver():
    conn = create_connection()
    cursor = conn.cursor()
    
    keyword = input("🔍 Enter driver name or taxi number to search: ")
    
    try:
        cursor.execute("""
            SELECT id, name, taxi_number 
            FROM drivers 
            WHERE name ILIKE %s OR taxi_number ILIKE %s
        """, (f"%{keyword}%", f"%{keyword}%"))
        
        results = cursor.fetchall()
        if results:
            print(Fore.CYAN + "Search Results:")
            print(Fore.YELLOW + "ID | Name | Taxi Number")
            for row in results:
                print(Fore.GREEN + f"{row[0]} | {row[1]} | {row[2]}")
        else:
            print(Fore.YELLOW + "No drivers found matching your search.")
    except Exception as e:
        print(Fore.RED + f"❌ Error searching drivers: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- SEARCH ROUTE -------------------
def search_route():
    conn = create_connection()
    cursor = conn.cursor()
    
    keyword = input("🔍 Enter origin or destination to search: ")
    
    try:
        cursor.execute("""
            SELECT id, origin, destination, fare 
            FROM drivers_routes 
            WHERE origin ILIKE %s OR destination ILIKE %s
        """, (f"%{keyword}%", f"%{keyword}%"))
        
        results = cursor.fetchall()
        if results:
            print(Fore.CYAN + "Search Results:")
            print(Fore.YELLOW + "ID | Origin | Destination | Fare")
            for row in results:
                print(Fore.GREEN + f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        else:
            print(Fore.YELLOW + "No routes found matching your search.")
    except Exception as e:
        print(Fore.RED + f"❌ Error searching routes: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- TOP EARNING DRIVER -------------------
def top_earning_driver():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT d.name, SUM(t.total_amount) AS total_earnings
            FROM trips t
            JOIN drivers d ON t.driver_id = d.id
            WHERE t.trip_date >= CURRENT_DATE
            GROUP BY d.name
            ORDER BY total_earnings DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        if result:
            print(Fore.CYAN + f"🏆 Top-Earning Driver Today: {Fore.GREEN}{result[0]}{Fore.CYAN} with total earnings of R{result[1]:.2f}")
        else:
            print(Fore.YELLOW + "No trips recorded today.")
    except Exception as e:
        print(Fore.RED + f"❌ Error fetching top-earning driver: {e}")
    finally:
        cursor.close()
        conn.close()


# ------------------- MAIN MENU -------------------
def main():
    print(Fore.CYAN + "👋 Sawubona! Welcome to Kasi Transport Tracker!")
    create_tables()
    
menu = {
    "1": (Fore.CYAN + "🚖 Register Driver"),
    "2": (Fore.CYAN + "🛣️ Register New Route"),
    "3": (Fore.CYAN + "📝 Log Trip"),
    "4": (Fore.CYAN + "📊 Daily Report"),
    "5": (Fore.CYAN + "🔍 Search Driver"),
    "6": (Fore.CYAN + "🔍 Search Route"),
    "7": (Fore.CYAN + "🏆 Top-Earning Driver"),
    "8": (Fore.RED + "❌ Exit")
}

print(Fore.MAGENTA + "\n📋 Main Menu:")
for key, value in menu.items():
    print(f"{Fore.YELLOW}{key}. {value}")


    while True:
        print("\n📋 Menu:")
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
            search_driver()
        elif choice == '6':
            search_route()
        elif choice == '7':
            top_earning_driver()
        elif choice == '8':
            print(Fore.CYAN + "👋 Exiting the system.")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
