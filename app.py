from flask import Flask, request, jsonify, render_template
import sqlite3
import pickle
from nltk.tokenize import word_tokenize
import re  # For regular expressions

app = Flask(__name__)

# Path to the Django SQLite3 database
DB_PATH = "C:/Users/mtiro/Desktop/django_chatbot/ecommerce/db.sqlite3"

# Load the trained intent detection model
with open("intent_model.pkl", "rb") as model_file:
    vectorizer, classifier = pickle.load(model_file)

# Detect user intent
def detect_intent(user_input):
    X_test = vectorizer.transform([user_input])
    return classifier.predict(X_test)[0]

# Fetch product price from the database
def get_product_price(product_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM products_product WHERE name LIKE ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    return f"${result[0]}" if result else "Product not found."

# Fetch order status from the database
def get_order_status(order_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders_order WHERE id = ?", (order_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return f"Order Status: {result[0]}."
        else:
            return "Order ID not found. Please check and try again."
    except sqlite3.Error as e:
        return f"Database error: {e}"

# Generate chatbot responses
def respond_to_query(user_input):
    intent = detect_intent(user_input)
    if intent == "price_inquiry":
        tokens = word_tokenize(user_input)
        product_name = tokens[-1]  # Assume product name is the last word
        return f"The price of {product_name} is {get_product_price(product_name)}."
    elif intent == "order_tracking":
        # Use regex to extract the order ID
        order_id_match = re.search(r'\b\d+\b', user_input)
        if order_id_match:
            order_id = int(order_id_match.group())
            return get_order_status(order_id)
        else:
            return "Invalid order ID format. Please provide a numeric ID."
    elif intent == "order_cancellation":
        return "Your order cancellation request has been noted. Please wait for confirmation."
    elif intent == "help_request":
        return "How can I assist you? Please provide more details."
    elif intent == "product_recommendation":
        return "I recommend checking out our latest smartphones and laptops for great value!"
    elif intent == "greeting":
        return "Hello! How can I assist you today?"
    elif intent == "farewell":
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I didn’t understand that."

# Debugging endpoint: List all routes
@app.route("/routes", methods=["GET"])
def list_routes():
    return jsonify({rule.rule: list(rule.methods) for rule in app.url_map.iter_rules()})

# Serve the chatbot frontend
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")



# Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        bot_response = respond_to_query(user_input)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
