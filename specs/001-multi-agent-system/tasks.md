# Tasks: Hierarchical Multi-Agent Radar & Automation System

**Feature Identifier**: `001-multi-agent-system`  
**Status**: READY FOR IMPLEMENTATION  

---

## Phase 1: Setup & Data Modeling
- [x] **T001**: Setup project virtual environment and core dependencies (`requirements.txt`).
- [ ] **T002**: Refactor `models/schema.py` to support `EvaluationVerdict` (`APPROVED`, `RETRY_REQUIRED`, `PERMANENT_REJECT`) and structured `ProposalTemplate`.

---

## Phase 2: Decoupled Specialist Agents (P1)
- [ ] **T003**: Create `agents/hackathon_agent.py` — স্বতন্ত্র হ্যাকাথন হান্টার (Bangladesh & Global AI/Web/App).
- [ ] **T004**: Create `agents/job_marketing_agent.py` — রিমোট জব ও মেটা মার্কেটিং/অটোমেশন হান্টার।
- [ ] **T005**: Add retry handling capability to both hunter agents when receiving feedback from Evaluator.

---

## Phase 3: Evaluator Reflection & Feedback Loop (P1 - Core Quality Gate)
- [ ] **T006**: Upgrade `agents/evaluator_agent.py` with the Critique/Reflection Loop.
  - তথ্য অসম্পূর্ণ থাকলে ডেটা ড্রপ না করে `RETRY_REQUIRED` সহ মিসিং ফিল্ড নির্দেশিকা হান্টারের কাছে ফেরত পাঠানো।
  - সর্বোচ্চ ৩ বার রি-ট্রাই লুপ পরিচালনা।
- [ ] **T007**: Add 3-Tier Proposal & Cover Letter generator to Evaluator for remote jobs.

---

## Phase 4: Supervisor Orchestration & Telegram Bot Commands (P2)
- [ ] **T008**: Update `agents/supervisor.py` to coordinate the new decoupled agents and the evaluation feedback loop.
- [ ] **T009**: Upgrade `bot/telegram_service.py` to handle slash commands:
  - `/hunt_hackathon`
  - `/hunt_jobs`
  - `/test_agents`
  - `/run_now`
- [ ] **T010**: Connect real-time Telegram alert delivery with interactive buttons.

---

## Phase 5: Verification & End-to-End Testing (P3)
- [ ] **T011**: Update unit tests in `tests/test_evaluator.py` to verify the new Retry/Reflection loop.
- [ ] **T012**: Execute full integration test across all 4 agents and log trace.
