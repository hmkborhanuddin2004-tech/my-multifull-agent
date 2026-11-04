# Multi-Agent Automation Architecture

An autonomous multi-agent cooperative framework written in Python, implementing supervisor-worker agent design patterns for business workflow execution, marketing automation, data aggregation, and structured evaluation.

---

## Architecture Components

- **Supervisor Agent (`supervisor.py`):** Central coordinator responsible for task decomposition, priority scheduling, and dispatching tasks to specialized subagents.
- **Job Marketing Agent (`job_marketing_agent.py`):** Autonomous lead generation, outreach drafting, and marketing pipeline automation.
- **Hunter Agent (`hunter_agent.py`):** Web scraper and data aggregator identifying market opportunities and business requirements.
- **Evaluator Agent (`evaluator_agent.py`):** Quality assurance and grading agent reviewing outputs before final delivery.
- **Hackathon Agent (`hackathon_agent.py`):** Rapid research, prototyping, and technical synthesis assistant.

---

## Technical Stack

- **Language:** Python 3.10+
- **Architecture:** Supervisor-Worker Multi-Agent Pattern
- **Libraries:** Requests, Pydantic, Dotenv, Asyncio
- **Integration:** REST APIs & Webhooks

---

## Getting Started

```bash
git clone https://github.com/hmkborhanuddin2004-tech/my-multifull-agent.git
cd my-multifull-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

## License

This project is licensed under the MIT License.
