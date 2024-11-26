from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# List of products
products = [
    {"name": "Laptop", "description": "A high-performance laptop", "price": 1000, "availability": True},
    {"name": "Smartphone", "description": "A latest model smartphone", "price": 800, "availability": True},
    {"name": "Headphones", "description": "Noise-cancelling over-ear headphones", "price": 150, "availability": True},
    {"name": "Smartwatch", "description": "A smartwatch with fitness tracking", "price": 200, "availability": False},
    {"name": "Tablet", "description": "A powerful tablet for all your needs", "price": 500, "availability": True}
]

# Chatbot logic functions
def greet():
    return "Welcome to the Virtual Store! How can I assist you today?"

def list_products():
    available_products = [product for product in products if product['availability']]
    if available_products:
        response = "We have the following products available:\n"
        for product in available_products:
            response += f"- {product['name']}: {product['description']} (Price: ${product['price']})\n"
        return response
    else:
        return "Sorry, we currently have no products available."

def product_info(product_name):
    for product in products:
        if product['name'].lower() == product_name.lower():
            availability = "In stock" if product['availability'] else "Out of stock"
            return (f"Product: {product['name']}\nDescription: {product['description']}\n"
                    f"Price: ${product['price']}\nAvailability: {availability}")
    return "Sorry, we don't have that product."

def recommend_product(preference):
    for product in products:
        if preference.lower() in product['description'].lower() and product['availability']:
            return (f"How about this?\n{product['name']}: {product['description']} (Price: ${product['price']})")
    return "Sorry, we don't have a product that matches your preference."

def add_to_cart(cart, product_name):
    for product in products:
        if product['name'].lower() == product_name.lower() and product['availability']:
            cart.append(product)
            return f"{product['name']} has been added to your cart."
    return "Sorry, that product is not available."

def show_cart(cart):
    if cart:
        response = "Your cart contains the following products:\n"
        for item in cart:
            response += f"- {item['name']}: ${item['price']}\n"
        return response
    else:
        return "Your cart is empty."

def complete_purchase(cart):
    if cart:
        total = sum(item['price'] for item in cart)
        cart.clear()
        return f"Purchase complete! Your total is ${total}. Thank you for shopping with us."
    else:
        return "Your cart is empty. Add some products before checking out."

def store_hours():
    return "Our store is open from 9 AM to 9 PM every day."

def return_policy():
    return "You can return any product within 30 days of purchase. Please keep the receipt and ensure the product is in original condition."

def contact_info():
    return "You can contact us at support@virtualstore.com or call us at +1-234-567-890."

# Flask routes
@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Virtual Store Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1e1e1e;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 20px;
            animation: fadeIn 2s ease-in-out;
        }
        #chatbox {
            background-color: #2c2c2c;
            padding: 20px;
            max-width: 600px;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            animation: fadeIn 1s ease-in-out 0.5s;
        }
        #chatlog {
            height: 300px;
            overflow-y: auto;
            margin-bottom: 10px;
            border: 1px solid #444;
            padding: 10px;
            background-color: #333;
            border-radius: 8px;
        }
        #user-input {
            width: calc(100% - 80px);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #444;
            background-color: #444;
            color: #fff;
        }
        button {
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-left: 10px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<h1>Hi, I'm VISA, the Virtual Sales Assistant</h1>

<div id="chatbox">
    <div id="chatlog">
        <p><strong>Bot:</strong> Welcome to the Virtual Store! How can I assist you today?</p>
    </div>
    <div style="display: flex;">
        <input type="text" id="user-input" placeholder="Type your message..." onkeypress="handleKeyPress(event)" />
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
    function sendMessage() {
        const userInput = document.getElementById('user-input').value;
        if (userInput.trim() === '') return;

        // Display user message in the chat log
        const chatlog = document.getElementById('chatlog');
        chatlog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
        document.getElementById('user-input').value = ''; // Clear the input field

        // Send user input to the Flask backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            chatlog.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
            chatlog.scrollTop = chatlog.scrollHeight; // Scroll to the bottom
        });
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }
</script>

</body>
</html>
    """)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get('user_input', '').strip().lower()
    response = ""

    if user_input in ["quit", "exit"]:
        response = "Thank you for visiting the Virtual Store. Have a great day!"
    elif user_input in ["what products do you have?", "list products", "show products"]:
        response = list_products()
    elif user_input.startswith("tell me about "):
        product_name = user_input.replace("tell me about ", "").strip()
        response = product_info(product_name)
    elif user_input.startswith("recommend a product for "):
        preference = user_input.replace("recommend a product for ", "").strip()
        response = recommend_product(preference)
    elif user_input.startswith("add "):
        product_name = user_input.replace("add ", "").strip()
        response = add_to_cart([], product_name)  # Empty cart for simplicity
    elif user_input in ["show me my cart", "show cart", "my cart"]:
        response = show_cart([])
    elif user_input in ["complete purchase", "checkout"]:
        response = complete_purchase([])  # Empty cart for simplicity
    elif user_input in ["store hours", "what are your store hours"]:
        response = store_hours()
    elif user_input in ["return policy", "what is your return policy"]:
        response = return_policy()
    elif user_input in ["contact info", "contact information", "how can i contact you"]:
        response = contact_info()
    else:
        response = "I'm sorry, I didn't understand that. Can you please rephrase?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
