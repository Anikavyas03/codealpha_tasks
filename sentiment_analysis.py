import pandas as pd

# Load the dataset from your CSV file
df = pd.read_csv("imdb_reviews.csv")

# Display first 5 rows
print(df.head())
import string
import nltk
from nltk.corpus import stopwords

# Download stopwords once
nltk.download('stopwords')

# Get English stopwords
stop_words = set(stopwords.words('english'))

# Function to clean review text
def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    words = text.split()  # Tokenize
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    return " ".join(words)

# Apply the preprocessing to the 'review' column
df['cleaned_review'] = df['review'].apply(preprocess_text)

# Show cleaned data
print(df[['review', 'cleaned_review', 'sentiment']])
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned_review'])

# Labels
y = df['sentiment']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy and report
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
# Function to predict sentiment
def predict_sentiment(text):
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    print(f"\nReview: {text}")
    print(f"Predicted Sentiment: {prediction}")

# Example predictions
predict_sentiment("I really enjoyed the movie!")
predict_sentiment("It was boring and a waste of time.")
