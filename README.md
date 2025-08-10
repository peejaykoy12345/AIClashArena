# AIClashArena

**AIClashArena** is an innovative platform that simulates debates between two AI agents presenting opposing viewpoints on any chosen topic. One AI takes on the role of the defender, while the other acts as the attacker, engaging in dynamic, insightful, and balanced discussions.

This project serves as a research and exploration platform for AI-driven argumentative reasoning and natural language dialogue generation. By leveraging state-of-the-art language models, AIClashArena aims to foster critical thinking and provide users with diverse perspectives on a wide range of subjects.

---

## Features

- **Dual AI Debates:** Simultaneously simulate two AI agents arguing for and against a given topic.
- **Role-based Arguments:** Each AI assumes a clear role — *Defense* or *Attack* — to ensure structured and coherent discussions.
- **Dynamic Topic Selection:** Users can input any topic, enabling debates across technology, culture, ethics, and more.
- **Rate Limiting & Security:** Built-in API token authorization and request limiting to ensure fair and secure access.
- **Clean & Responsive UI:** Modern web interface that facilitates easy navigation and engaging user experience.

---

## Technologies Used

- **Flask** – Backend web framework for routing and API development.
- **Bootstrap 5** – Responsive, mobile-first UI design.
- **Requests** – Python HTTP client for interacting with AI APIs.
- **External AI APIs** – Utilizes advanced language models for generating debate responses.
- **Flask-Limiter** – Rate limiting middleware to protect API endpoints.
- **Dotenv** – Environment variable management for secure API key handling.

---

## Getting Started

### Prerequisites

- Python 3.8+
- A valid API key for the AI language model provider
- Virtual environment recommended

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AIClashArena.git
   cd AIClashArena
   ```
2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file in the root directory and add your API key:
    GROQ_API_KEY=your_api_key_here

Run the application:
```bash
gunicorn run:app
```

### License
This project is for research purposes. Please contact the maintainers for licensing inquiries.
