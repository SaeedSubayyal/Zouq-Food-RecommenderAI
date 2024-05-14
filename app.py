from flask import Flask, render_template, request, jsonify, url_for
import json
import model_output  # Ensure this module is correctly implemented and debugged

app = Flask(__name__, static_folder='assets', template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        if not data or 'preferences' not in data:
            return jsonify({"error": "Missing 'preferences' in request"}), 400

        search_term = data['preferences'].strip()
        if not search_term:
            return jsonify([])

        print(f"Search term: {search_term}")  # Log the search term

        recipes = model_output.get_recommendations(search_term)
        
        for recipe in recipes:
            if 'image_url' in recipe and recipe['image_url']:
                recipe['image_url'] = recipe['image_url']
        
        return jsonify(recipes)

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
