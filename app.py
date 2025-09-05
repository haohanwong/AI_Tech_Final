from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Configure Google AI Studio API
genai.configure(api_key="API_KEY") 
model = genai.GenerativeModel("gemini-1.5-flash")

# Chat history (simple save)
chat_history = []

# FAQ (rule-based answers)
faq = {
    "dorm condition": "The dorms are 2-person rooms, equipped with air conditioning and a private bathroom.",
    "library hours": "The library is open from 8:00 AM to 10:00 PM.",
    "canteen": "The canteen has 3 floors, and meals cost between RM8 to RM15.",
    "course selection time": "The course selection system opens one week before the semester starts. Prepare in advance.",
    "student clubs": "There are over 50 student clubs, covering arts, sports, and technology.",
    "exam schedule": "Final exams are usually held in December and June. Please check the schedule one week in advance."
}

# Rule-based answer with strict + fuzzy matching
def rule_based_answer(user_input: str):
    user_input = user_input.strip().lower()
    
    if user_input in faq:
        return faq[user_input]
    
    for key, value in faq.items():
        key_words = key.split()
        if all(word in user_input for word in key_words):
            return value
    
    return None

# AI answer (Google Gemini)
def ai_answer(user_input):
    prompt = f"You are a campus Q&A chatbot. Please answer concisely: {user_input}"
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, AI did not return a response."

# Combined logic
def get_answer(user_input):
    answer = rule_based_answer(user_input)
    if answer:
        return answer
    return ai_answer(user_input)

html_page = """
<!DOCTYPE html>
<html>
<head>
  <title>🎓 Campus Q&A Bot</title>
  <style>
    body { font-family: Arial; margin: 40px; }
    .chat-box { width: 500px; margin: auto; }
    .msg { padding: 8px; border-radius: 6px; margin: 5px 0; }
    .user { background: #d1e7dd; text-align: right; }
    .bot { background: #f8d7da; text-align: left; }
  </style>
</head>
<body>
  <div class="chat-box">
    <h2>🎓 Campus Q&A Bot</h2>
    <div id="chat"></div>
    <input type="text" id="msg" placeholder="Type your question..." style="width:80%">
    <button onclick="sendMsg()">Send</button>
  </div>
 <script>
  const chat = document.getElementById("chat");
  const msgInput = document.getElementById("msg");

  msgInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") sendMsg();
  });

  async function loadHistory() {
    let res = await fetch("/history");
    let data = await res.json();
    data.forEach(item => {
      addMessage(item.Q, "user");
      addMessage(item.A, "bot");
    });
    chat.scrollTop = chat.scrollHeight;
  }

  async function sendMsg() {
    let msg = msgInput.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    msgInput.value = "";
    chat.scrollTop = chat.scrollHeight;

    let res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "question": msg })
    });
    let data = await res.json();
    addMessage(data.answer, "bot");
    chat.scrollTop = chat.scrollHeight;
  }

  function addMessage(text, sender){
    let msgDiv = document.createElement("div");
    msgDiv.className = "msg " + sender;
    msgDiv.textContent = text;
    chat.appendChild(msgDiv);
  }

  loadHistory();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_page)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")
    answer = get_answer(user_input)
    chat_history.append({"Q": user_input, "A": answer})
    return jsonify({"answer": answer})

@app.route("/history")
def history():
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(debug=True)