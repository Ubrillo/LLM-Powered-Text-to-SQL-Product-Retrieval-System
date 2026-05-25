# LLM-Powered Text-to-SQL Product Retrieval System

An AI-powered application that converts natural language product requests into SQL queries and retrieves relevant information from a relational database using Large Language Models (LLMs), semantic embeddings, vector similarity search, and voice input.

---

# Project Overview

This project demonstrates the integration of Large Language Models with relational databases to enable intelligent database querying through natural language.

Instead of manually writing SQL statements, users can interact with the system conversationally — by speaking or typing requests such as:

```text
Show me all black t-shirts under £30
```

The system processes the request, generates SQL queries, executes them against a MySQL database, and returns the relevant product information through a web interface.

The project combines:
- Natural Language Processing (NLP)
- Text-to-SQL generation
- Semantic similarity search
- Prompt engineering
- Vector embeddings
- Relational database querying
- AI-assisted retrieval systems
- Voice-to-text transcription (Whisper)

---

# Core Concepts Demonstrated

- Large Language Model (LLM) Integration
- Text-to-SQL Systems
- Prompt Engineering
- Few-Shot Learning
- Semantic Similarity Search
- Vector Databases
- Embedding Models
- Retrieval-Augmented Generation (RAG)
- Relational Database Querying
- AI-Powered Data Retrieval
- Full-Stack AI Application Development
- Voice Query Integration (Speech-to-Text)

---

# Project Structure

```bash
├── main.py
├── langchain_helper.py
├── few_shots.py
├── requirement.txt
├── db_creating_afriq_tshirts.sql
├── .env
└── README.md
```

---

# Project Components

## `main.py`

Contains the frontend application responsible for:
- Accepting user queries via **voice (microphone)** or text input
- Transcribing spoken queries using **OpenAI Whisper**
- Sending requests to the processing pipeline
- Displaying generated SQL queries
- Rendering retrieved database results

---

## `langchain_helper.py`

Core backend processing layer responsible for:
- SQL query generation
- Prompt construction
- Semantic retrieval
- Query execution pipeline
- Embedding integration
- Vector similarity matching
- Database interaction

---

## `few_shots.py`

Contains few-shot examples used to guide the language model toward generating more accurate and context-aware SQL queries.

This improves:
- Query consistency
- SQL syntax accuracy
- Product filtering precision
- Database schema understanding

---

## `db_creating_afriq_tshirts.sql`

Contains the relational database schema and SQL table definitions used for product storage and retrieval.

---

## `.env`

Stores API keys and environment configurations securely.

---

# System Architecture

```text
+----------------------------------+
|   User Input                     |
|   Voice (Microphone) or Text     |
+----------+-----------------------+
           |
           v
+----------------------------------+
|   Voice Transcription (Whisper)  |
|   Speech-to-Text via OpenAI      |
|   Whisper "base" model           |
+----------+-----------------------+
           |
           v
+------------------------------+
|   Frontend UI                |
|   (main.py / Streamlit)      |
+----------+-------------------+
           |
           v
+------------------------------+
| Processing Layer             |
| (langchain_helper.py)        |
+----------+-------------------+
           |
           v
+------------------------------+
| Few-Shot Prompt Engineering  |
| (few_shots.py)               |
+----------+-------------------+
           |
           v
+------------------------------+
| Semantic Similarity Search   |
| Vector Embeddings            |
+----------+-------------------+
           |
           v
+------------------------------+
| LLM SQL Generation           |
+----------+-------------------+
           |
           v
+------------------------------+
| MySQL Database Execution     |
+----------+-------------------+
           |
           v
+------------------------------+
| Product Retrieval Results    |
+------------------------------+
```

---

# Voice Integration

Users can now query the database entirely by voice using the built-in microphone recorder.

## How It Works

1. The user clicks the **"🎤 Click to record"** button in the Streamlit UI
2. The recorded audio is saved as a temporary `.wav` file
3. **OpenAI Whisper** (`base` model) transcribes the audio to text
4. The transcribed text is displayed back to the user for confirmation
5. The query is passed through the LangChain pipeline as normal
6. A **text input fallback** is also available for users who prefer typing

## Technologies Used

- `openai-whisper` — local speech-to-text transcription
- `streamlit-mic-recorder` — in-browser microphone capture
- `soundfile` — audio file handling
- `tempfile` — secure temporary file management

## Example Voice Query

> 🎤 *"Show me all red t-shirts in medium size below 40 pounds"*

Transcribed and converted to SQL:

```sql
SELECT *
FROM t_shirts
WHERE color = 'red'
AND size = 'M'
AND price < 40;
```

---

# Example Query

## User Input (Text or Voice)

```text
Show me all red t-shirts in medium size below 40 pounds
```

## AI-Generated SQL

```sql
SELECT *
FROM t_shirts
WHERE color = 'red'
AND size = 'M'
AND price < 40;
```

---

# Skills Demonstrated

- Prompt Engineering
- LLM Application Development with Langchain
- Semantic Search Systems
- Database Integration
- Backend Development
- Vector Embedding Systems
- Retrieval-Augmented Generation (RAG)
- SQL Query Automation
- Full-Stack AI Development
- Voice Query Integration (Speech-to-Text with Whisper)

---

# Future Improvements

- Conversational memory support
- Multi-database compatibility
- SQL validation and query safety
- Authentication and access control
- Containerization and cloud deployment
- Real-time analytics dashboard
- Improved voice model accuracy with Whisper `medium` or `large` variants
- Multi-language voice support
