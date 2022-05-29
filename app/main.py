# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen

story_genre = ''


def genre_text_generation(genre):
    
    if genre == 'horror':
        file_dest = 'model/horror_files'
        
    if genre == 'drama':
        file_dest = 'model/drama_files'
        
    if genre == 'thriller':
        file_dest = 'model/thriller_files'
        
    if genre == 'scifi':
        file_dest = 'model/scifi_files'
        
    if genre == 'superhero':
        file_dest = 'model/superhero_files'
        
    if genre == 'action':
        file_dest = 'model/action_files'
        
    return file_dest

# load up a model from memory. Note you may not need all of these options.

#ai = aitextgen(model_folder = 'model/action_files', to_gpu=False)
# ai = aitextgen(model_folder="model/", tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)
#ai = aitextgen(model="distilgpt2", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver


@app.route(f'{base_url}')
def home():
    return render_template('writer_home.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('Write-your-story-with-AI.html', generated=data)
    else:
        return render_template('Write-your-story-with-AI.html', generated=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    print(prompt)
    genre_type = request.form['genre']
    print('genre type is: ', genre_type)
    story_genre = genre_text_generation(genre_type)
    print('file destination is: ', story_genre)
    ai = aitextgen(model_folder = story_genre, to_gpu=False)
    
    if prompt is not None:
        generated = ai.generate(
            n=1,
            batch_size=10,
            prompt=str(prompt),
            max_length=100,
            temperature=1.0,
            return_as_list=True
        )

    data = {'generated_ls': generated}
    session['data'] = generated[0]
    return redirect(url_for('results'))

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc8.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
