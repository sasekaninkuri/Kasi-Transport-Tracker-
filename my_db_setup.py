import psycopg2

def create_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="kasi_transport",
        user="postgres",
        password="mypassword"
    )
    print("Connection successfully created")
    return conn


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    create_drivers_table = """
    CREATE TABLE IF NOT EXISTS drivers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        taxi_number VARCHAR(50) UNIQUE NOT NULL
    );
    """

    create_drivers_routes_table = """
    CREATE TABLE IF NOT EXISTS drivers_routes (
        id SERIAL PRIMARY KEY,
        origin VARCHAR(100) NOT NULL,
        destination VARCHAR(100) NOT NULL,
        fare DECIMAL(10, 2) NOT NULL
    );
    """

    create_trips_table = """
    CREATE TABLE IF NOT EXISTS trips (
        id SERIAL PRIMARY KEY,
        driver_id INTEGER REFERENCES drivers(id),
        route_id INTEGER REFERENCES drivers_routes(id),
        passengers INTEGER NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL,
        trip_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    
    cursor.execute(create_drivers_table)
    cursor.execute(create_drivers_routes_table)
    cursor.execute(create_trips_table)
    
    conn.commit()
    print("Tables created successfully")
    cursor.close()
    conn.close()    
    
    # ------------------- DAILY REPORT -------------------
def daily_report(cursor):
    cursor.execute("""
        SELECT d.name, SUM(t.passengers) AS total_passengers, SUM(t.total_amount) AS total_earnings
        FROM trips t
        JOIN drivers d ON t.driver_id = d.id
        WHERE t.trip_date >= CURRENT_DATE
        GROUP BY d.name;
    """)
    return cursor.fetchall()

# ------------------- SEARCH DRIVER -------------------
def search_driver(cursor, keyword):
    cursor.execute("""
        SELECT id, name, taxi_number
        FROM drivers
        WHERE name ILIKE %s OR taxi_number ILIKE %s
    """, (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()

# ------------------- SEARCH ROUTE -------------------
def search_route(cursor, keyword):
    cursor.execute("""
        SELECT id, origin, destination, fare
        FROM drivers_routes
        WHERE origin ILIKE %s OR destination ILIKE %s
    """, (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()

# ------------------- TOP EARNING DRIVER -------------------
def top_earning_driver(cursor):
    cursor.execute("""
        SELECT d.name, SUM(t.total_amount) AS total_earnings
        FROM trips t
        JOIN drivers d ON t.driver_id = d.id
        WHERE t.trip_date >= CURRENT_DATE
        GROUP BY d.name
        ORDER BY total_earnings DESC
        LIMIT 1;
    """)
    return cursor.fetchone()


    cursor.execute(create_drivers_table)
    cursor.execute(create_drivers_routes_table)
    cursor.execute(create_trips_table)

    conn.commit()
    print("Tables created successfully")
    cursor.close()
    conn.close()


create_tables()


def add_driver(cursor,name, taxi_number):
    cursor.execute( """
        insert into drivers (name, taxi_number) values
        (%s, %s)""",
            (name, taxi_number)
    )

def add_route(cursor, origin, destination, fare):
    cursor.execute( """
        insert into drivers_routes (origin, destination, fare) values
        (%s, %s, %s)""",
        (origin, destination, fare)
    )
        
        

def record_trip(cursor, driver_id, route_id, passengers):  
    cursor.execute("SELECT fare FROM drivers_routes WHERE id = %s", (route_id,))
    fare = cursor.fetchone()
    
    if fare is None:
        raise ValueError("Route ID does not exist.")
    
    fare = fare[0]  
    total_amount = fare * passengers  

    cursor.execute( """
        INSERT INTO trips (driver_id, route_id, passengers, total_amount) VALUES
        (%s, %s, %s, %s)""",
        (driver_id, route_id, passengers, total_amount)
    )

    trip_record = {
        "driver_id": driver_id,
        "route_id": route_id,
        "passengers": passengers,
        "total_amount": total_amount
    }
    return trip_record


def daily_report(cursor):
    cursor.execute("""
        SELECT d.name, SUM(t.passengers) AS total_passengers, SUM(t.total_amount) AS total_earnings
        FROM trips t
        JOIN drivers d ON t.driver_id = d.id
        WHERE t.trip_date >= CURRENT_DATE
        GROUP BY d.name;
    """)
    return cursor.fetchall()
    

                

            

