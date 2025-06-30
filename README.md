# 🌿 ReflectAI – Mental Health Chatbot & Mood Tracker

> *“Sometimes the best thing you can do is simply check in with yourself.”*  
> ReflectAI helps you do just that — with the power of AI.

ReflectAI is a Streamlit-based AI mental wellness companion that lets users share their feelings, detects emotional tone using NLP, suggests personalized self-care tips, and visualizes mood trends over time. Built for awareness, empathy, and educational exploration.

---

##  Key Features

-  **Emotion-Aware Chat Interface** – Talk to the chatbot and receive real-time emotional feedback.
-  **AI-Powered Emotion Detection** – BERT-based classification (GoEmotions dataset).
-  **Personalized Self-Care Tips** – Based on detected emotions (quotes, music, breathing links).
-  **Mood Trend Graphs** – Visualize emotions over time using Plotly and Matplotlib.
-  **Chat History Logging** – SQLite-based message + emotion + timestamp log.
-  **Filter by Emotion** – View only “sad”, “happy”, or other emotion categories.
---

##  Tech Stack

| Layer        | Technology                                                          |
|--------------|---------------------------------------------------------------------|
| Frontend     | Streamlit (or React, optional)                                      |
| Backend      | Flask / FastAPI                                                     |
| NLP Model    | BERT (`bert-base-go-emotion`)                                       |
| Data Storage | SQLite (or MySQL)                                                   |
| Visuals      | Plotly, Matplotlib                                                  |
| Libraries    | `transformers`, `pandas`, `requests`, `TextBlob`, `VaderSentiment`  |

##  How It Works

1. User types a thought or message.
2. BERT-based model analyzes the emotion.
3. Emotion, confidence, and timestamp are stored in DB.
4. App suggests mood-specific resources (music, breathing tips).
5. Charts show emotional trends over time.

---

##  Use Cases

-  Students journaling and tracking mental health
-  Anyone wanting to reflect on their emotional patterns
-  Developers exploring NLP & sentiment analysis
-  Counselors interested in anonymized emotional data trends

---

##  Customization Ideas
|-------------|----------------------------------------------------|
| Feature     | Customization                                      |
|-------------|----------------------------------------------------|
| NLP Model   | Swap to RoBERTa, DistilBERT, or local LLM          |
| Frontend    | Convert to React Native / mobile app               |
| Charts      | Add weekly/monthly breakdown                       |
| Voice Input | Use `speech_recognition` or Whisper                |
| Cloud       | Deploy with Render, Heroku, or Hugging Face Spaces |
|-------------|----------------------------------------------------|

---

##  Disclaimer

> This project is for **educational and awareness** purposes only. It is **not a substitute** for professional mental health care.

---

##  Author

**Gopikashree PR**  
Aspiring AI & Data Science Final Year Student 
GitHub: [@gopikashreepr](https://github.com/gopikashreepr)

---

##  Want to contribute?

Feel free to fork, suggest enhancements, or open an issue!

---

