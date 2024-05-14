import pandas as pd
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import html
import ast

# Load the model and the recipe data
model_path = 'D:\\Users\\Subayyal Saeed\\Desktop\\Deski\\AI project\\MealRec-main\\CCMR\\checkpoints\\model_epoch_10'
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

recipes_df = pd.read_csv('D:\\Users\\Subayyal Saeed\\Desktop\\Deski\\AI project\\dataset\\recipe.csv')


# Function to preprocess and clean text
def preprocess_text(text):
    if isinstance(text, str):
        text = html.unescape(text)
        try:
            text = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            pass
        if isinstance(text, dict) and 'directions' in text:
            text = text['directions']
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'\^', ', ', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[\{\}\[\]]', '', text)
    return text

# Main function to get recommendations based on user preferences
def get_recommendations(user_preferences):
    results = []  # Initialize the results list
    vectorizer = TfidfVectorizer(stop_words='english')
    user_tfidf = vectorizer.fit_transform([user_preferences])

    # Step 2: Combine categories and ingredients into one text to vectorize
    recipes_df['combined_features'] = recipes_df['category'].fillna('') + ", " + recipes_df['ingredients'].fillna('')

    # Step 3: Vectorize recipes' combined features
    recipe_tfidf = vectorizer.transform(recipes_df['combined_features'])

    # Step 4: Compute similarity scores between user preferences and recipes
    similarity_scores = cosine_similarity(user_tfidf, recipe_tfidf).flatten()

    # Step 5: Predict interest scores using the model (simulating with random scores here)
    predicted_scores = torch.rand(len(recipes_df))

    # Combine model prediction with similarity scores
    combined_scores = predicted_scores.numpy() + similarity_scores

    # Step 6: Get top 5 recommended recipes
    top_indices = combined_scores.argsort()[-5:][::-1]
    recommended_recipes = recipes_df.iloc[top_indices]

    # Print the recommended recipes with cleaned ingredients and cooking directions
    for idx in top_indices:
        row = recipes_df.iloc[idx]
        results.append({
            "name": row['recipe_name'],
            "description": "", 
            "image_url": row['image_url'],
            "ingredients": preprocess_text(row['ingredients']),
            "directions": preprocess_text(row['cooking_directions']),
            "score": combined_scores[idx]
        })
    return results
