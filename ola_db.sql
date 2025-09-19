CREATE TABLE ola_rides (
    Booking_ID VARCHAR(50) PRIMARY KEY,
    Booking_Status VARCHAR(50),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(255),
    Drop_Location VARCHAR(255),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer TEXT,
    Canceled_Rides_by_Driver TEXT,
    Incomplete_Rides VARCHAR(10),
    Incomplete_Rides_Reason TEXT,
    Booking_Value INT,
    Payment_Method VARCHAR(50),
    Ride_Distance INT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    Datetime TIMESTAMP,
    Is_Success INT,
    Is_Canceled INT,
    Year INT,
    Month INT,
    Day INT,
    Hour INT
);

COPY ola_rides
FROM 'C:/OLA_DataSet_Cleaned.csv'
DELIMITER ','
CSV HEADER;

select * from ola_rides limit(10)

select * from ola_rides
where pickup_location<>'Tumkur Road' and vehicle_type='Mini'
limit(10)
