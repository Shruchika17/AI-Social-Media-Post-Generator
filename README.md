# AI Social Media Post Generator

An AI-powered tool to generate and schedule LinkedIn + Instagram posts using **LangChain** and **Google Gemini**.

## Features

- 🤖 **AI Content Generation** — LangChain + Gemini generates platform-optimized posts
- 🎨 **AI Image Generation** — HuggingFace (SDXL) or Pollinations.ai (no key needed)
- 🔥 **Smart Hashtags** — RapidAPI trending hashtags + LLM fallback
- 💼 **LinkedIn Publishing** — Direct post via LinkedIn UGC API
- 📸 **Instagram Publishing** — Instagram Graph API integration
- 📅 **Post Scheduling** — APScheduler for future-dated posts
- 🖥️ **Beautiful UI** — Streamlit frontend with live preview

## Setup

### 1. Clone & Install
```bash
git clone <repo>
cd ai-social-poster
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Fill in your API keys in .env
```

**Required API Keys:**
| Service | Cost | Link |
|---------|------|------|
| Google Gemini | Free | [aistudio.google.com](https://aistudio.google.com) |
| HuggingFace | Free | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| LinkedIn API | Free | [linkedin.com/developers](https://www.linkedin.com/developers/) |
| Instagram Graph API | Free | [developers.facebook.com](https://developers.facebook.com) |
| RapidAPI | Free tier | [rapidapi.com](https://rapidapi.com) |
| ImgBB (Instagram images) | Free | [imgbb.com](https://imgbb.com) |

### 3. Run

**Option A: Full Stack (API + UI)**
```bash
python run.py
```
Then open http://localhost:8501 for the UI and http://localhost:8000/docs for the API.

**Option B: API only**
```bash
uvicorn app.main:app --reload --port 8000
```

**Option C: UI only (offline mode)**
```bash
streamlit run ui/streamlit_app.py
```

## Project Structure

```
ai-social-poster/
├── app/
│   ├── main.py                  # FastAPI backend
│   ├── agents/
│   │   ├── content_agent.py     # LangChain + Gemini content generation
│   │   ├── image_agent.py       # HuggingFace / Pollinations image generation
│   │   └── hashtag_agent.py     # RapidAPI + LLM hashtag generation
│   ├── platforms/
│   │   ├── linkedin.py          # LinkedIn API integration
│   │   └── instagram.py         # Instagram Graph API integration
│   ├── scheduler/
│   │   └── post_scheduler.py    # APScheduler for scheduled posts
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   └── utils/
│       └── helpers.py           # Utility functions
├── ui/
│   └── streamlit_app.py         # Streamlit frontend
├── generated_images/            # AI-generated images saved here
├── .env.example                 # Environment variable template
├── requirements.txt
└── run.py                       # Entry point (runs both API + UI)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate` | Generate post content + image + hashtags |
| POST | `/publish/{post_id}` | Immediately publish to platforms |
| POST | `/schedule` | Schedule a post for later |
| GET | `/scheduled` | List all scheduled posts |
| DELETE | `/scheduled/{job_id}` | Cancel a scheduled post |
| GET | `/health` | Check API key configuration status |
| GET | `/docs` | Swagger UI for interactive API docs |

## How It Works

```
User Input (topic, platform, tone)
         ↓
  [Hashtag Agent] ──→ RapidAPI trending hashtags
         ↓              (falls back to Gemini LLM)
  [Content Agent] ──→ LangChain + Gemini
         ↓              generates LinkedIn + Instagram content
  [Image Agent]  ──→ HuggingFace SDXL
         ↓              (falls back to Pollinations.ai)
  [Post Scheduler] ─→ Immediate publish or APScheduler
         ↓
  LinkedIn API + Instagram Graph API
```

## Tech Stack

- **LangChain** — Agent orchestration and LLM chains
- **Google Gemini 1.5 Flash** — Content and hashtag generation (free)
- **HuggingFace SDXL** — Image generation (free tier)
- **Pollinations.ai** — Free fallback image generation (no key needed)
- **FastAPI** — REST API backend
- **Streamlit** — Frontend UI
- **APScheduler** — Background job scheduling
- **LinkedIn UGC API** — Post publishing
- **Instagram Graph API** — Post publishing

## License

MIT
