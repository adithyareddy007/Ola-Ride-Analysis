-- 1. Retrieve all successful bookings
SELECT *
FROM ola_rides
WHERE Booking_Status = 'Success';

-- 2. Find the average ride distance for each vehicle type
SELECT Vehicle_Type, 
       ROUND(AVG(Ride_Distance), 2) AS avg_distance
FROM ola_rides
WHERE Ride_Distance > 0
GROUP BY Vehicle_Type
ORDER BY avg_distance DESC;

-- 3. Get the total number of cancelled rides by customers
SELECT COUNT(*) AS total_cancelled_by_customers
FROM ola_rides
WHERE Booking_Status = 'Canceled by Customer';

-- 4. List the top 5 customers who booked the highest number of rides
SELECT Customer_ID, 
       COUNT(*) AS total_rides
FROM ola_rides
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues
SELECT COUNT(*) AS cancelled_by_driver_personal_car_issue
FROM ola_rides
WHERE Booking_Status = 'Canceled by Driver'
  AND Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings
SELECT MAX(Driver_Ratings) AS max_rating,
       MIN(Driver_Ratings) AS min_rating
FROM ola_rides
WHERE Vehicle_Type = 'Prime Sedan'
  AND Driver_Ratings IS NOT NULL;

-- 7. Retrieve all rides where payment was made using UPI
SELECT *
FROM ola_rides
WHERE Payment_Method = 'Upi';

-- 8. Find the average customer rating per vehicle type
SELECT Vehicle_Type, 
       ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
FROM ola_rides
WHERE Customer_Rating IS NOT NULL
GROUP BY Vehicle_Type
ORDER BY avg_customer_rating DESC;

-- 9. Calculate the total booking value of rides completed successfully
SELECT SUM(Booking_Value) AS total_success_booking_value
FROM ola_rides
WHERE Booking_Status = 'Success';

-- 10. List all incomplete rides along with the reason
SELECT Booking_ID, Customer_ID, Vehicle_Type, Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 'Yes';
