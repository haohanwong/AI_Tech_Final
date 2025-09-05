# AI_Tech_Final
# 🎓 Campus Q&A Chatbot

A simple AI-powered chatbot for answering questions about university life. It combines **rule-based FAQ responses** with **Google Gemini AI** to provide concise answers.

---

## Features

- **Simple Web UI**: Input box, “Send” button, and chat display area.
- **Rule-based answers**: Predefined FAQs for common campus questions.
- **AI-powered answers**: Google Gemini API handles queries not covered by FAQs.
- **Chat history (session)**: Displays conversation history during the session.
- **UI Enhancements**: Automatic scrolling, enter-to-send, distinct user/robot chat bubbles.

---

## Example FAQ Responses

- **Dorm condition**: "The dorms are 4-person rooms, equipped with air conditioning and a private bathroom."
- **Library hours**: "The library is open from 8:00 AM to 10:00 PM."
- **Canteen**: "The canteen has 3 floors, and meals cost between 8 to 15 RMB."
- **Course selection time**: "The course selection system opens one week before the semester starts. Prepare in advance."
- **Student clubs**: "There are over 50 student clubs, covering arts, sports, and technology."
- **Exam schedule**: "Final exams are usually held in December and June. Please check the schedule one week in advance."

---

## Requirements

- Python 3.8+
- Flask
- Google Generative AI Python SDK (`google-generativeai`)

Install dependencies:

```bash
pip install flask google-generativeai
