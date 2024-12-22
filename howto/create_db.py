import duckdb

# Use the exact same default_schema from app.py
default_schema = """CREATE TABLE rideshare(
    hvfhs_license_num VARCHAR,
    dispatching_base_num VARCHAR,
    originating_base_num VARCHAR,
    request_datetime TIMESTAMP,
    on_scene_datetime TIMESTAMP,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    PULocationID BIGINT,
    DOLocationID BIGINT,
    trip_miles DOUBLE,
    trip_time BIGINT,
    base_passenger_fare DOUBLE,
    tolls DOUBLE,
    bcf DOUBLE,
    sales_tax DOUBLE,
    congestion_surcharge DOUBLE,
    airport_fee DOUBLE,
    tips DOUBLE,
    driver_pay DOUBLE,
    shared_request_flag VARCHAR,
    shared_match_flag VARCHAR,
    access_a_ride_flag VARCHAR,
    wav_request_flag VARCHAR,
    wav_match_flag VARCHAR
);

CREATE TABLE service_requests(
    unique_key BIGINT,
    created_date TIMESTAMP,
    closed_date TIMESTAMP,
    agency VARCHAR,
    agency_name VARCHAR,
    complaint_type VARCHAR,
    descriptor VARCHAR,
    location_type VARCHAR,
    incident_zip VARCHAR,
    incident_address VARCHAR,
    street_name VARCHAR,
    cross_street_1 VARCHAR,
    cross_street_2 VARCHAR,
    intersection_street_1 VARCHAR,
    intersection_street_2 VARCHAR,
    address_type VARCHAR,
    city VARCHAR,
    landmark VARCHAR,
    facility_type VARCHAR,
    status VARCHAR,
    due_date TIMESTAMP,
    resolution_description VARCHAR,
    resolution_action_updated_date TIMESTAMP,
    community_board VARCHAR,
    bbl VARCHAR,
    borough VARCHAR,
    x_coordinate_state_plane VARCHAR,
    y_coordinate_state_plane VARCHAR,
    open_data_channel_type VARCHAR,
    park_facility_name VARCHAR,
    park_borough VARCHAR,
    vehicle_type VARCHAR,
    taxi_company_borough VARCHAR,
    taxi_pick_up_location VARCHAR,
    bridge_highway_name VARCHAR,
    bridge_highway_direction VARCHAR,
    road_ramp VARCHAR,
    bridge_highway_segment VARCHAR,
    latitude DOUBLE,
    longitude DOUBLE
);

CREATE TABLE taxi(
    VendorID BIGINT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count DOUBLE,
    trip_distance DOUBLE,
    RatecodeID DOUBLE,
    store_and_fwd_flag VARCHAR,
    PULocationID BIGINT,
    DOLocationID BIGINT,
    payment_type BIGINT,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    congestion_surcharge DOUBLE,
    airport_fee DOUBLE,
    drivers VARCHAR[],
    speeding_tickets STRUCT(date TIMESTAMP, speed VARCHAR)[],
    other_violations JSON
);"""

def create_database(schema):
    # Create a new DuckDB database
    conn = duckdb.connect('demo.duckdb')
    
    # Create tables using the schema
    for create_statement in schema.split(';'):
        if create_statement.strip():
            conn.execute(create_statement)

    # Insert sample data
    conn.execute("""
    INSERT INTO taxi VALUES (
        1, 
        '2023-01-01 12:00:00',
        '2023-01-01 12:30:00',
        2,
        5.2,
        1,
        'N',
        100,
        101,
        1,
        20.5,
        1.0,
        0.5,
        4.0,
        0.0,
        0.3,
        26.3,
        2.5,
        0.0,
        ['John Doe', 'Jane Smith'],
        [{date: '2023-01-01 10:00:00', speed: '75mph'}],
        '{"parking_violations": 2}'
    )
    """)

    # Verify the tables were created
    print("\nTables in database:")
    print(conn.execute("SHOW TABLES").fetchall())

    # Verify sample data
    print("\nSample taxi data:")
    print(conn.execute("SELECT * FROM taxi").fetchall())

    conn.close()

if __name__ == "__main__":
    create_database(default_schema)