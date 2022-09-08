CREATE TABLE kijiji_elements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    image VARCHAR(255),
    date DATE,
    beds INTEGER,
    currency VARCHAR(63),
    price VARCHAR(255)

)