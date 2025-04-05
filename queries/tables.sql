-- ATM Locations (основа для клиентов и транзакций)
CREATE TABLE IF NOT EXISTS atm_location (
    location_id VARCHAR,  -- LocationID
    location_name VARCHAR,  -- Location Name
    atm_count INTEGER,  -- No of ATMs
    city VARCHAR,  -- City
    state VARCHAR,  -- State
    country VARCHAR,  -- Country
    PRIMARY KEY(location_id)
);

-- Transaction Types (основа для transactions)
CREATE TABLE IF NOT EXISTS transaction_type (
    transaction_type_id INTEGER,  -- TransactionTypeID
    transaction_desc VARCHAR,  -- TransactionTypeName
    PRIMARY KEY(transaction_type_id)
);

-- Customers (ссылается на atm_location)
CREATE TABLE IF NOT EXISTS customers (
    cardholder_id VARCHAR,  -- CardholderID
    first_name VARCHAR,  -- First Name
    last_name VARCHAR,  -- Last Name
    gender CHAR(1),  -- Gender
    atm_id VARCHAR,  -- ATMID
    birth_date DATE,  -- Birth Date
    occupation VARCHAR,  -- Occupation
    account_type VARCHAR,  -- AccountType
    is_wisabi BOOLEAN,  -- IsWisabi
    PRIMARY KEY(cardholder_id),
    FOREIGN KEY(atm_id) REFERENCES atm_location(location_id)
);

-- Таблица транзакций (ссылается на customers, atm_location и transaction_type)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR,  -- TransactionID
    start_time TIMESTAMP,  -- TransactionStartDateTime
    end_time TIMESTAMP,  -- TransactionEndDateTime
    cardholder_id VARCHAR,  -- CardholderID
    location_id VARCHAR,  -- LocationID
    transaction_type_id INTEGER,  -- TransactionTypeID
    amount INTEGER,  -- TransactionAmount
    region VARCHAR,  -- Регион
    PRIMARY KEY(transaction_id),
    FOREIGN KEY(cardholder_id) REFERENCES customers(cardholder_id),
    FOREIGN KEY(location_id) REFERENCES atm_location(location_id),
    FOREIGN KEY(transaction_type_id) REFERENCES transaction_type(transaction_type_id)
);

-- Calendar
CREATE TABLE IF NOT EXISTS calendar (
    date DATE,  -- Date
    year INTEGER,  -- Year
    month_name VARCHAR,  -- Month Name
    month INTEGER,  -- Month
    quarter VARCHAR,  -- Quarter
    week_of_year INTEGER,  -- Week of Year
    end_of_week DATE,  -- End of Week
    day_of_week INTEGER,  -- Day of Week
    day_name VARCHAR,  -- Day Name
    is_holiday BOOLEAN,  -- IsHoliday
    PRIMARY KEY(date)
);

-- Hour Lookup
CREATE TABLE IF NOT EXISTS hour_lookup (
    hour_key VARCHAR,  -- Hour_Key
    hour_start VARCHAR,  -- Hour_Start_Time
    hour_end VARCHAR,  -- Hour_End_Time
    PRIMARY KEY(hour_key)
);
