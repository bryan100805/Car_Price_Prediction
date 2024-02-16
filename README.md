# README
This project aim to develop a AI Machine Learning Web application (https://car-guru.onrender.com/login)
that is able to predict the price of cars based on the 
following parameters:
 
1. Aspiration (std, turbo)
2. Carbody (convertible, hatchback, sedan, wagon, hardtop) 
3. Drivewheel (rwd, fwd, 4wd)
4. Enginetype (dohc, ohcv, ohc, l, rotor, ohcf) 
5. Cylindernumber (two, four, five, six, eight) 
6. Fueleconomy = (citympg x 0.55) + (highwaympg x 0.45) 
    - Citympg: Mileage in city
    - Highwaympg: Mileage on highway
7. Carlength - Measured in inches
8. Carwidth - Measured in inches
9. Curbweight - Weight of a car without occupants or baggage, Measured in pounds
10. Enginesize - Size of engine, measured in Cubic Inches (CID)
11. Boreratio - Represents how many times the bore diameter is in relation to the stroke length within the engine cylinder
12. Horsepower - Power of car engine, measured in HP
13. Wheelbase - Distance between front and rear wheel, measured in inches
14. CarName - Company of the car 
    - Example: ['alfa-romeo' 'audi' 'bmw' 'chevrolet' 'dodge' 'honda' 'isuzu' 'jaguar' 
    'mazda' 'buick' 'mercury' 'mitsubishi' 'nissan' 'peugeot' 'plymouth' 'porsche'
    'renault' 'saab' 'subaru' 'toyota' 'volkswagen' 'volvo']
15. CarPrice Range - The price range classifier based on the average prices of the cars of each car company
    - Example: ['Budget Price' 'Medium Price' 'Highend Price']
