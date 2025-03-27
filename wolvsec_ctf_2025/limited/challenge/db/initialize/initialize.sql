USE ctf;

-- This password is 13 characters and can be found in rockyou.
-- It is the flag for one of the challenges using this source
-- BUT it needs to be wrapped by wctf{} before submitting.
create user 'flag' identified by 'maricrissarah';

grant select on mysql.user to ctf;

-- The actual name of this table in the host challenge starts with Flag_ but is unguessable.
CREATE TABLE Flag_843423739
(
    value VARCHAR(255) NOT NULL
);

INSERT INTO Flag_843423739 (value) VALUES ('wctf{r34d1n6_07h3r_74bl35_15_fun_96427235634}');


CREATE TABLE Menu
(
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL
);

INSERT INTO Menu (id, name, description, price, category)
VALUES
    (1, 'Classic Cheeseburger', 'Juicy beef patty with melted cheddar cheese, lettuce, and tomato on a sesame seed bun', 9.99, 'Burgers'),
    (2, 'Margherita Pizza', 'Classic pizza with tomato sauce, fresh mozzarella, and basil leaves', 12.99, 'Pizza'),
    (3, 'Chicken Alfredo Pasta', 'Creamy Alfredo sauce with grilled chicken breast served over fettuccine pasta', 14.99, 'Pasta'),
    (4, 'Vegetarian Sushi Roll', 'Avocado, cucumber, and carrot rolled in seasoned rice and seaweed', 10.99, 'Sushi'),
    (5, 'Caesar Salad', 'Crisp romaine lettuce, garlic croutons, parmesan cheese, and Caesar dressing', 8.99, 'Salads'),
    (6, 'Grilled Salmon', 'Freshly grilled salmon fillet with lemon butter sauce', 16.99, 'Seafood'),
    (7, 'Mushroom Risotto', 'Creamy risotto with sautéed mushrooms and parmesan cheese', 13.99, 'Risotto'),
    (8, 'BBQ Pulled Pork Sandwich', 'Slow-cooked pulled pork with barbecue sauce on a toasted bun', 11.99, 'Sandwiches'),
    (9, 'Spinach and Feta Stuffed Chicken', 'Chicken breast stuffed with spinach and feta cheese, served with a side of roasted vegetables', 15.99, 'Entrees'),
    (10, 'Shrimp Scampi', 'Sautéed shrimp in a garlic and white wine butter sauce, served over linguine', 17.99, 'Seafood'),
    (11, 'Caprese Panini', 'Fresh mozzarella, tomato, and basil pesto on ciabatta bread', 9.99, 'Panini'),
    (12, 'Vegan Buddha Bowl', 'Quinoa, roasted vegetables, avocado, and tahini dressing', 12.99, 'Bowls'),
    (13, 'Hawaiian Poke Bowl', 'Ahi tuna, avocado, mango, and sesame seeds over sushi rice', 14.99, 'Bowls'),
    (14, 'Classic Tiramisu', 'Layered coffee-soaked ladyfingers and mascarpone cream, dusted with cocoa powder', 7.99, 'Desserts'),
    (15, 'Key Lime Pie', 'Tangy key lime filling in a graham cracker crust, topped with whipped cream', 6.99, 'Desserts'),
    (16, 'Mango Tango Smoothie', 'Fresh mango, banana, and orange juice blended into a refreshing smoothie', 4.99, 'Beverages'),
    (17, 'Pho Ga', 'Vietnamese chicken noodle soup with rice noodles, bean sprouts, and herbs', 10.99, 'Soups'),
    (18, 'Gourmet Mac and Cheese', 'Creamy macaroni and cheese with a blend of artisanal cheeses', 11.99, 'Comfort Food'),
    (19, 'Cajun Shrimp Tacos', 'Spicy Cajun-seasoned shrimp, coleslaw, and avocado in soft corn tortillas', 13.99, 'Tacos'),
    (20, 'Classic French Onion Soup', 'Caramelized onions in a savory broth, topped with melted Gruyère cheese', 8.99, 'Soups'),
    (21, 'Quinoa Salad', 'Mixed greens, quinoa, cherry tomatoes, cucumber, and balsamic vinaigrette', 9.99, 'Salads'),
    (22, 'Chicken Teriyaki Bowl', 'Grilled chicken, broccoli, and carrots in teriyaki sauce over rice', 12.99, 'Bowls'),
    (23, 'Stuffed Portobello Mushrooms', 'Portobello mushrooms stuffed with spinach, feta, and breadcrumbs', 10.99, 'Appetizers'),
    (24, 'Margarita Cocktail', 'Classic margarita with tequila, triple sec, lime juice, and a salted rim', 8.99, 'Cocktails'),
    (25, 'Vegetable Spring Rolls', 'Crispy spring rolls filled with assorted vegetables, served with sweet chili sauce', 6.99, 'Appetizers'),
    (26, 'Lemon Herb Grilled Chicken', 'Grilled chicken breast marinated in lemon, garlic, and herbs', 13.99, 'Entrees'),
    (27, 'Vegetable Lasagna', 'Layered lasagna with marinara sauce, ricotta, mozzarella, and assorted vegetables', 14.99, 'Pasta'),
    (28, 'Crispy Calamari', 'Lightly breaded and fried calamari served with marinara sauce', 11.99, 'Appetizers'),
    (29, 'Southwest Chicken Salad', 'Grilled chicken, black beans, corn, avocado, and chipotle ranch dressing', 12.99, 'Salads'),
    (30, 'Classic Vanilla Milkshake', 'Creamy vanilla ice cream blended into a thick and delicious milkshake', 5.99, 'Desserts'),
    (31, 'BBQ Ribs', 'Slow-cooked barbecue ribs with a tangy BBQ glaze, served with coleslaw', 16.99, 'Entrees'),
    (32, 'Pesto Caprese Flatbread', 'Flatbread topped with pesto, fresh mozzarella, cherry tomatoes, and balsamic glaze', 10.99, 'Appetizers'),
    (33, 'Spicy Tuna Roll', 'Spicy tuna, cucumber, and avocado rolled in seaweed and rice', 11.99, 'Sushi'),
    (34, 'Cherry Almond Tart', 'Almond tart filled with cherry compote and topped with sliced almonds', 7.99, 'Desserts'),
    (35, 'Teriyaki Salmon', 'Grilled salmon glazed with teriyaki sauce, served with steamed rice and vegetables', 15.99, 'Seafood'),
    (36, 'Mushroom Truffle Risotto', 'Creamy truffle-infused risotto with assorted mushrooms', 16.99, 'Risotto'),
    (37, 'Classic Eggs Benedict', 'Poached eggs and Canadian bacon on an English muffin, topped with hollandaise sauce', 11.99, 'Breakfast'),
    (38, 'Fettuccine Carbonara', 'Creamy carbonara sauce with pancetta and parmesan cheese over fettuccine pasta', 13.99, 'Pasta'),
    (39, 'Greek Gyro Wrap', 'Grilled lamb, tzatziki sauce, tomatoes, and onions wrapped in warm pita bread', 9.99, 'Wraps'),
    (40, 'Chocolate Lava Cake', 'Warm and gooey chocolate cake with a molten chocolate center, served with vanilla ice cream', 8.99, 'Desserts'),
    (41, 'Chicken Quesadilla', 'Grilled chicken, melted cheese, and sautéed peppers in a crispy tortilla', 10.99, 'Appetizers'),
    (42, 'Crispy Brussels Sprouts', 'Roasted Brussels sprouts tossed in balsamic glaze and topped with parmesan cheese', 7.99, 'Appetizers'),
    (43, 'Pineapple Fried Rice', 'Stir-fried rice with pineapple, shrimp, chicken, and vegetables', 12.99, 'Rice Dishes'),
    (44, 'Classic Club Sandwich', 'Turkey, ham, bacon, lettuce, tomato, and mayo on toasted bread', 11.99, 'Sandwiches'),
    (45, 'Shrimp and Grits', 'Sautéed shrimp in a creamy garlic sauce served over cheesy grits', 14.99, 'Southern Cuisine'),
    (46, 'Mint Chocolate Chip Shake', 'Refreshing mint chocolate chip ice cream blended into a delightful shake', 6.99, 'Beverages'),
    (47, 'Thai Green Curry', 'Green curry with chicken, coconut milk, bamboo shoots, and bell peppers', 15.99, 'Curry'),
    (48, 'Lemon Poppy Seed Pancakes', 'Fluffy pancakes with lemon zest and poppy seeds, served with maple syrup', 9.99, 'Breakfast'),
    (49, 'Crispy Duck Confit', 'Crispy duck leg confit served with mashed potatoes and red wine reduction', 18.99, 'Entrees'),
    (50, 'Blueberry Cheesecake', 'Creamy cheesecake with a blueberry compote topping', 8.99, 'Desserts');
