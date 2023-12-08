from flask import Flask, render_template, request, session
import openai

app = Flask(__name__)


@app.route('/')
def index():
    if 'api_key' in session:
        api_key = session['api_key']
        return render_template('index.html', api_key='existing')

    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_api():
    api_key = request.form['api-key']
    session['api_key'] = api_key
    return render_template('index.html', api_key='existing')


@app.route('/generate', methods=['POST'])
def generate_lyrics():
    # Get user input from the form
    length = request.form['length']
    rhyme = request.form['rhyme']
    topic = request.form['topic']
    genre = request.form['genre']
    api_key = session['api_key']

    system_prompt = (f"You are a songwriter. Your only job is to write the lyrics to a song. Your response should only "
                     f"include the lyrics of the song.")

    # Generate prompt based on user input
    prompt = f"Generate music lyrics {length} words long"
    if rhyme.lower() == 'yes':
        prompt += " that rhyme"
    if topic:
        prompt += f" on the topic of {topic}"
    if genre:
        prompt += f" in the genre of {genre}"

    # Set OpenAI API key
    client = openai.Client(api_key=api_key)

    # Generate lyrics
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Get generated lyrics
    generated_lyrics = response.choices[0].message.content

    return render_template('index.html', generated_lyrics=generated_lyrics, api_key='existing')


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
