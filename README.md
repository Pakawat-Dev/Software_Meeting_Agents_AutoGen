# Software Meeting Agents

AI-powered meeting simulation for software development discussions using AutoGen and OpenAI.

## Features

- **4 Specialized Agents**: Management, Technical, Quality, and Minute-Taker
- **Structured Discussions**: Covers scope, technical design, testing, and risks
- **Meeting Summary**: Automatic generation of key decisions and action items

## Setup

1. Install dependencies:
```bash
pip install pyautogen python-dotenv
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

```bash
python software_meeting_agent.py
```

Enter your meeting agenda when prompted (e.g., "Design a login system with 2FA").

## Agents

- **Management_Agent**: Project goals, timelines, scope
- **Technical_Agent**: Architecture, implementation, tools
- **Quality_Agent**: Testing, security, reliability
- **Minute_Taker**: Meeting summary and action items

## Configuration

- Model: GPT-4.1-nano
- Max tokens: 1024 per response
- Language: English only
- Max rounds: 6
