from flask import Flask, redirect
from flask import render_template
from datetime import datetime
import json
import os
from markupsafe import escape

app = Flask(__name__)
drinks = {
    201: 'drink1',
    202: 'drink2',
    203: 'drink3',
    204: 'drink4',
}
# Dictionary to store drink details by ID
drinks_details = {
    201: {'name': 'Sweet Dream', 'details': 'A delightfully sweet concoction perfect for dessert.'},
    202: {'name': 'Caffeine Boost', 'details': 'A robust caffeinated drink to jump-start your day.'},
    203: {'name': 'Bitter Leaf', 'details': 'A refined bitter beverage for the acquired palate.'},
    204: {'name': 'Sour Punch', 'details': 'A tangy and sour drink that refreshes and excites.'},
}



def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 16:
        return 'afternoon'
    elif 16 <= hour < 19:
        return 'evening'
    else:
        return 'night'


user_id_map = {
    'Aashiq': 1, 'Abhi': 2, 'Prasanna': 3, 'Neha': 4, 'Viki': 5, 'Ajith': 6, 'Brian': 7, 'Ashwin': 8, 'Shar': 9,
    'Yadu': 10
}


@app.route('/')
def index():
    greeting = "Hello there, Need a Drink ?"
    return render_template('index.html', greet=greeting)


@app.route('/loading')
def loading():
    return render_template('loading.html')


@app.route('/checkUser')
def checkUser():
    f = open("user.txt", "r")
    username = f.readline()
    f.close()
    if username:
        print(username)
        num_user = user_id_map[username]
        time_now = get_time_of_day()
        input_data = {
            "user_id": num_user,
            "time_of_day": time_now
        }
        with open('input_data.json', 'w') as json_file:
            json.dump(input_data, json_file, indent=4)

        address = '/user/' + username
        return redirect(address)
    else:
        return render_template('newuser.html')


@app.route('/user/<username>')
def new_user(username):
    os.system("python Model.py")
    return render_template('user.html', username=username)


def load_recommendations():
    with open('recommendation.json', 'r') as file:
        data = json.load(file)
    rec1 = drinks.get(data['recommendation_1'])
    rec2 = drinks.get(data['recommendation_2'])
    return rec1, rec2

@app.route('/drink1')
def drink1():
    drink = drinks_details[201]
    return render_template('drink.html', drink=drink)

@app.route('/drink2')
def drink2():
    drink = drinks_details[202]
    return render_template('drink.html', drink=drink)

@app.route('/drink3')
def drink3():
    drink = drinks_details[203]
    return render_template('drink.html', drink=drink)

@app.route('/drink4')
def drink4():
    drink = drinks_details[204]
    return render_template('drink.html', drink=drink)


@app.route('/recommendations/<rec1>')
def recommendations():
    return render_template('drink.html')


if __name__ == '__main__':
    app.run(debug=1)
