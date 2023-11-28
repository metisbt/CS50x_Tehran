-- Keep a log of any SQL queries you execute as you solve the mystery.

-- check data in crime_scene_reports
SELECT description FROM crime_scene_reports WHERE year = "2021" AND month = "7" AND day = "28" AND street = "Humphrey Street";

-- check the transcript of each people that were in the bakery
SELECT name, transcript FROM interviews WHERE year = "2021" AND month = "7" AND day = "28";

-- According to the "Ruth" report, we will check the security report of the bakery at the 10:25am.
SELECT activity, license_plate FROM bakery_security_logs WHERE year = "2021" AND month = "7" AND day = "28" AND hour = "10" AND minute LIKE "2%";

-- According to the "Eugene" report, check the people that receiving money from atm that day on that street and Join people and bank_accounts and atm_transactions to get closer to finding thif name.
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE year = "2021" AND month = "7" AND day = "28" AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- Find the name of fiftyville airport
SELECT abbreviation, full_name, city FROM airports WHERE city = 'Fiftyville';

-- Find first fly on july 29 from Fiftyville Regional Airport
SELECT city, hour, minute FROM airports JOIN flights ON airports.id = flights.destination_airport_id WHERE flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND flights.year = 2021 AND flights.month = 7 AND flights.day = 29 ORDER BY flights.hour, flights.minute;

-- By connecting tables people and passengers and flights and phone_calls and bakery_security_logs and command INTERSECT, we find the name of the person who called less than 1 minute and left the parking in the time period and went to destination Fiftyville.
SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number JOIN flights ON passengers.flight_id = flights.id WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20 INTERSECT SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60 INTERSECT SELECT name FROM people JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate WHERE bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 AND bakery_security_logs.activity = 'exit' AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 LIMIT 1;

-- Find ACCOMPLICE name from poeple join with phone_calls where Bruce call it
SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver WHERE phone_calls.id IN (SELECT phone_calls.id FROM phone_calls JOIN people ON phone_calls.caller = people.phone_number WHERE name = 'Bruce' AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60);