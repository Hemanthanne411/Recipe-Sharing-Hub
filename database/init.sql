-- init.sql

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the recipes table with a foreign key
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    ingredients TEXT,
    instructions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert a sample user for initial testing
INSERT INTO users (username, password) VALUES ('instructor', 'instructor123') ON CONFLICT (username) DO NOTHING;

-- Insert some sample recipes for the instructor to see
INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES
(1, 'Spaghetti Bolognese', 'Spaghetti, ground beef, tomato sauce, onion', '1. Cook spaghetti. 2. Brown beef. 3. Mix ingredients with sauce. 4. Serve.') ON CONFLICT DO NOTHING;

INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES
(1, 'Simple Caesar Salad', 'Lettuce, croutons, Caesar dressing, parmesan cheese', '1. Tear lettuce. 2. Add dressing, croutons, and cheese. 3. Toss well.') ON CONFLICT DO NOTHING;

INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES
(1, 'Quick Chicken Curry', 'Chicken breast, curry powder, coconut milk, vegetables', '1. Sauté chicken. 2. Add vegetables and curry powder. 3. Stir in coconut milk. 4. Simmer until cooked.') ON CONFLICT DO NOTHING;