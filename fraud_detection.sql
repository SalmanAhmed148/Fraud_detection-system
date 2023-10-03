-- Use the database
USE fraud_detection;

/*-- Create a table to store transactions
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store fraud alerts
CREATE TABLE fraud_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    transaction_id INT,
    reason VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE transactions
ADD COLUMN user_id INT,
ADD FOREIGN KEY (user_id) REFERENCES users(id);
*/

select * from ;