import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load the existing dataset
df = pd.read_csv("intents.csv")

# Add more diverse queries to the dataset
additional_data = [
    # Greetings
    ("hi there", "greeting"),
    ("hello there", "greeting"),
    ("hey buddy", "greeting"),
    ("good day", "greeting"),
    ("what's going on", "greeting"),
    # Price Inquiries
    ("can you show me the price", "price_inquiry"),
    ("tell me the cost", "price_inquiry"),
    ("what's the price for this", "price_inquiry"),
    ("how expensive is this", "price_inquiry"),
    ("give me a price comparison", "price_inquiry"),
    # Order Tracking
    ("has my package arrived", "order_tracking"),
    ("is the order delivered", "order_tracking"),
    ("what's the delivery status", "order_tracking"),
    ("can you update me on my order", "order_tracking"),
    ("how long will it take for my order", "order_tracking"),
    # Order Cancellation
    ("can I cancel my order", "order_cancellation"),
    ("is it possible to cancel", "order_cancellation"),
    ("help me reverse my order", "order_cancellation"),
    ("how do I cancel this order", "order_cancellation"),
    ("I made a mistake, cancel my order", "order_cancellation"),
    # Help Requests
    ("please assist me", "help_request"),
    ("I need guidance", "help_request"),
    ("help me out", "help_request"),
    ("can I get support", "help_request"),
    ("I'm stuck, help me", "help_request"),
    # Product Recommendations
    ("what's a good option", "product_recommendation"),
    ("which one do you suggest", "product_recommendation"),
    ("what's the top choice", "product_recommendation"),
    ("what product do you recommend", "product_recommendation"),
    ("help me choose the best product", "product_recommendation"),
    # Farewells
    ("see you", "farewell"),
    ("catch you later", "farewell"),
    ("have a good day", "farewell"),
    ("later", "farewell"),
    ("peace out", "farewell"),
]

# Append the additional data to the DataFrame
df_additional = pd.DataFrame(additional_data, columns=["query", "intent"])
df = pd.concat([df, df_additional], ignore_index=True)

# Save the updated dataset for future use
df.to_csv("intents.csv", index=False)
  
# Split into features and labels
X = df["query"]
y = df["intent"]

# Vectorize the text data
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_vectorized, y)

# Save the model and vectorizer
with open("intent_model.pkl", "wb") as model_file:
    pickle.dump((vectorizer, classifier), model_file)

print("Model retrained with expanded dataset and saved!")
