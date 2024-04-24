import os
import json
import sqlite3
from surprise import SVD
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
import pandas as pd

# Step 1: Connect to SQLite Database
db_path = 'user_history.db'

if os.path.exists(db_path):
    conn_user_history = sqlite3.connect(db_path)
    print("Connected to existing database.")
else:
    print("Database file not found. Creating a new database.")
    conn_user_history = sqlite3.connect(db_path)
    conn_user_history.close()
    conn_user_history = sqlite3.connect(db_path)

# Step 2: Check if the User History table is empty
try:
    cursor = conn_user_history.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_history")
    result = cursor.fetchone()[0]
    if result == 0:
        # Load User Drink History from CSV into Database
        user_history_csv_path = 'C:/Users/ahmed/Downloads/user_history_with_input.csv'  # Specify the path to your CSV file
        user_history_csv_df = pd.read_csv(user_history_csv_path)
        user_history_csv_df.columns = user_history_csv_df.columns.str.strip()  # Remove leading/trailing whitespaces
        user_history_csv_df.to_sql('user_history', conn_user_history, if_exists='append', index=False)
        print("User history data loaded and inserted into user_history table successfully.")
    else:
        print("User history table is not empty. Skipping CSV file loading.")
except Exception as e:
    print("Error checking user history table:", e)

# Step 3: Read User Drink History from Database
try:
    user_history_df = pd.read_sql_query("SELECT * FROM user_history", conn_user_history)
    print("User history data loaded successfully from database.")
    print("Contents of user history:")
    print(user_history_df.head())
except Exception as e:
    print("Error reading user history data from database:", e)

# Step 4: Train Machine Learning Model
try:
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(user_history_df[['user_id', 'drink_id', 'drink_rating']], reader)
    trainset, _ = train_test_split(data, test_size=0.2, random_state=42)
    print("Training data prepared successfully.")
except Exception as e:
    print("Error preparing training data:", e)

# Train the model
try:
    model = SVD()
    model.fit(trainset)
    print("Model trained successfully.")
except Exception as e:
    print("Error training the model:", e)

# Step 5: Read Input Data from JSON
try:
    with open('E:/PycharmProjects/Interface/input_data.json', 'r') as file:
        input_data = json.load(file)
    input_data_df = pd.DataFrame([input_data])  # Convert single record to DataFrame
    print("Input data loaded successfully.")
    print("Input data:")
    print(input_data_df.head())
except Exception as e:
    print("Error loading input data:", e)

# Step 6: Generate Recommendations for Input Data
try:
    recommendations = []
    for idx, row in input_data_df.iterrows():
        user_id = row['user_id']
        time_of_day = row['time_of_day']
        user_testset = [(user_id, drink_id, None, time_of_day) for drink_id in user_history_df['drink_id'].unique()]
        predictions = [(model.predict(user_id, drink_id), drink_id) for drink_id in user_history_df['drink_id'].unique()]
        predictions.sort(key=lambda x: x[0].est, reverse=True)
        recommendation_1 = predictions[0][1]
        recommendation_2 = predictions[1][1]
        recommendations.append({'user_id': user_id, 'recommendation_1': recommendation_1, 'recommendation_2': recommendation_2})
    print("Recommendations generated successfully.")

    # Write recommendations to JSON file
    with open('recommendations.json', 'w') as file:
        json.dump(recommendations, file, indent=4)
    print("Recommendations saved to recommendations.json.")

except Exception as e:
    print("Error generating recommendations:", e)


# Close database connection
conn_user_history.close()
