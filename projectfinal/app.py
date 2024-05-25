from flask import Flask, render_template, request, redirect
#used requests to ask the api for data, redirect to take anyone who uses this to dif pages of the website request to handle the data the user inputs 
import requests
import random

app = Flask(__name__)

API_KEY = "live_PgSuXlgv56UnYklxqfDY13Du6cuVK1lTEwDKkkWRZy1erhwPuRGpYr9SeIe9nkYc"

#this is the key to the api i used its important its here or the api will not give any info
@app.route('/')
#gives a url fto the homepage
def index():
    response = requests.get("https://api.thedogapi.com/v1/images/search?has_breeds=true&limit=1", headers={"x-api-key": API_KEY})
    #makes a request to the api for an img and breed info
    data = response.json()[0]
    #converts that into a disctonary 
    image_url = data['url']
    #grabs url of the image of the dog
    breed = data['breeds'][0]['name']
    #gets dog breed name
    return render_template('index.html', image_url=image_url, breed=breed)

@app.route('/check_guess', methods=['POST'])
#names the url thatll check the guess post requests only
#this function checks user's guess
def check_guess():
    user_guess = request.form['guess'].lower()
    #grabs the users guess 
    breed = request.form['breed'].lower()
    image_url = request.form['image_url']
    #grabs breed and its image and bottom if statement evals if their right or wrong
    if user_guess == breed:
        result = "correct! the breed is " + breed.capitalize() + "."
        color = 'green'
    else:
        result = "wrong lol. try again!"
        color = 'red'
    return render_template('result.html', result=result, color=color, image_url=image_url)

#gives name to url if user tryna play again
@app.route('/play_again', methods=['POST'])
def play_again():
    return redirect('/')

#if he is hes taken back to the home page
@app.route('/guess_attributes')
#this grabs the info that the user has to guess on from the json
def guess_attributes():
    response = requests.get("https://api.thedogapi.com/v1/breeds", headers={"x-api-key": API_KEY})
    breeds = response.json()
    dog = random.choice(breeds)
    attributes = {
        'name': dog['name'],
        'life_span': dog['life_span'],
        'temperament': dog['temperament'],
        'origin': dog.get('origin', 'Unknown')
    }
    return render_template('attributes.html', attributes=attributes)

#checks if their right using if statement but firstly grabbing their guess and formatting it
@app.route('/check_attributes_guess', methods=['POST'])
def check_attributes_guess():
    user_guess = request.form['guess'].lower()
    breed_name = request.form['breed_name'].lower()
    if user_guess == breed_name:
        result = "WRONGGGG! jk. the breed is " + breed_name.capitalize() + "."
        color = 'green'
    else:
        result = "WRONGGGGGGG. try again!"
        color = 'red'
    attributes = {
        'name': request.form['breed_name'],
        'life_span': request.form['life_span'],
        'temperament': request.form['temperament'],
        'origin': request.form['origin']
    }
    return render_template('attributes_result.html', result=result, color=color, attributes=attributes)

@app.route('/guess_attributes_again', methods=['POST'])
def guess_attributes_again():
    return redirect('/guess_attributes')
#handles request to play again if user chooses

@app.route('/breed_lookup')
def breed_lookup():
    return render_template('breed_lookup.html')
#just grabs the html that has the breed look up

@app.route('/lookup_result', methods=['POST'])
#grabs the info and formats it 
def lookup_result():
    breed_name = request.form['breed_name'].lower()
    response = requests.get(f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}", headers={"x-api-key": API_KEY})
    breed_info = response.json()
    if breed_info:
        breed = breed_info[0]
        image_response = requests.get(f"https://api.thedogapi.com/v1/images/{breed['reference_image_id']}", headers={"x-api-key": API_KEY})
        image_url = image_response.json()['url']
        attributes = {
            'name': breed['name'],
            'life_span': breed['life_span'],
            'temperament': breed['temperament'],
            'origin': breed.get('origin', 'Unknown'),
            'image_url': image_url
        }
        return render_template('lookup_result.html', attributes=attributes)
    else:
        #handles invalid choices
        result = "Breed not found. Try again!"
        return render_template('breed_lookup.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

