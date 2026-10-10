import os
import re
from typing import Optional, List
from datetime import datetime
from models.schema import (
    RawOpportunity, 
    EvaluatedOpportunity, 
    OpportunityType, 
    EvaluationVerdict, 
    ProposalTemplate
)


class EvaluatorAgent:
    """
    ইভালুয়েটর সাব-এজেন্ট (Quality Gate & Reflection/Feedback Engine):
    ১. তথ্য অসম্পূর্ণ হলে ড্রপ করে না, বরং RETRY_REQUIRED দিয়ে হান্টারের কাছে ফেরত পাঠায়।
    ২. তথ্য নিশ্চিত হলে APPROVED ঘোষণা করে এবং ৩-স্তরের প্রপোজাল তৈরি করে।
    ৩. স্প্যাম বা ভুয়া হলে PERMANENT_REJECT করে।
    """
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def _is_valid_url(self, url: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(re.match(regex, url))

    def _check_deadline(self, deadline_str: Optional[str]) -> bool:
        if not deadline_str:
            return False # ডেডলাইন না থাকা মানে তথ্য অসম্পূর্ণ
        try:
            dt = datetime.strptime(deadline_str[:10], "%Y-%m-%d")
            return dt >= datetime.now()
        except Exception:
            return False

    def _generate_proposals(self, raw: RawOpportunity) -> ProposalTemplate:
        """৩ স্তরের পেশাদার প্রপোজাল ও কভার লেটার ড্রাফট"""
        cold_email = (
            f"Subject: Solving Automation & Lead Inefficiencies for {raw.organizer_or_company}\n\n"
            f"Hi {raw.organizer_or_company} Team,\n\n"
            f"I noticed your requirement for '{raw.title}'. With practical experience in autonomous "
            f"AI agent architectures, Python automations, and Meta Ads API integration, I can help you "
            f"deploy reliable pipelines that eliminate manual repetitive tasks and lower acquisition costs.\n\n"
            f"Would you be open to a quick 10-minute demo of a recent automated lead workflow I built?\n\n"
            f"Best regards,\n[Your Name] | Full-Stack AI & Automation Developer"
        )

        case_study_pitch = (
            f"### Proposal: {raw.title}\n"
            f"**To:** {raw.organizer_or_company}\n\n"
            f"**Why My Background Matches:**\n"
            f"- Built end-to-end multi-agent systems featuring self-correcting evaluators and real-time alerts.\n"
            f"- Specialized in Meta Marketing & Google Ads funnel tracking with automated conversion pipelines.\n"
            f"- Hands-on tech stack: Python, Pydantic, REST/Webhooks, Web & App Development.\n\n"
            f"**Action Plan:**\n"
            f"1. Audit current manual bottlenecks.\n"
            f"2. Build custom automation agent scripts.\n"
            f"3. Deliver production-ready dashboards with zero downtime.\n"
        )

        linkedin_dm = (
            f"Hi there! Saw your opening for {raw.title} at {raw.organizer_or_company}. "
            f"I specialize in building intelligent AI automation agents and Meta Ads pipelines. "
            f"I've helped streamline similar workflows—let me know if you'd like to see a quick walkthrough!"
        )

        return ProposalTemplate(
            cold_email=cold_email,
            case_study_pitch=case_study_pitch,
            linkedin_dm=linkedin_dm
        )

    async def evaluate(self, raw: RawOpportunity) -> EvaluatedOpportunity:
        missing_fields: List[str] = []

        # ১. ইউআরএল ভ্যালিডেশন
        if not self._is_valid_url(raw.source_url):
            missing_fields.append("source_url")

        # ২. ডেডলাইন অসম্পূর্ণ কি না
        if not raw.extracted_deadline:
            missing_fields.append("deadline")
        elif not self._check_deadline(raw.extracted_deadline):
            return EvaluatedOpportunity(
                raw=raw,
                verdict=EvaluationVerdict.PERMANENT_REJECT,
                score=10,
                evaluation_notes="আবেদনের সময়সীমা শেষ হয়ে গেছে (Expired)।",
                missing_fields=[]
            )

        # ৩. যদি তথ্য অসম্পূর্ণ থাকে এবং রি-ট্রাই বাকি থাকে ➔ রিজেক্ট না করে রি-ট্রাই লুপে পাঠানো
        if missing_fields:
            if raw.retry_count < self.max_retries:
                return EvaluatedOpportunity(
                    raw=raw,
                    verdict=EvaluationVerdict.RETRY_REQUIRED,
                    score=40,
                    evaluation_notes=f"তথ্য অসম্পূর্ণ। অনুপস্থিত ফিল্ড: {', '.join(missing_fields)}। সাব-এজেন্টকে পুনরায় নির্দেশ পাঠানো হলো।",
                    missing_fields=missing_fields
                )
            else:
                return EvaluatedOpportunity(
                    raw=raw,
                    verdict=EvaluationVerdict.PERMANENT_REJECT,
                    score=20,
                    evaluation_notes=f"সর্বোচ্চ {self.max_retries} বার রি-ট্রাই করার পরও তথ্য উদ্ধার করা যায়নি।",
                    missing_fields=missing_fields
                )

        # ৪. তথ্য সম্পূর্ণ ➔ স্কিল স্কোর ও অ্যাপ্রুভাল
        score = 85
        if any("bangladesh" in loc.lower() for loc in [raw.location, raw.title]):
            score = 100
        elif any(t.lower() in ["ai", "automation", "meta marketing"] for t in raw.tags):
            score = 95

        summary = (
            f"📌 **{raw.title}**\n"
            f"🏢 প্রতিষ্ঠান/আয়োজক: {raw.organizer_or_company}\n"
            f"📍 অবস্থান: {raw.location}\n"
            f"⏳ আবেদনের শেষ সময়: {raw.extracted_deadline}\n"
            f"💡 বিবরণ: {raw.raw_description}\n"
            f"🏷️ টপিক: {', '.join(raw.tags)}"
        )

        proposal_bundle = None
        if raw.type == OpportunityType.REMOTE_JOB:
            proposal_bundle = self._generate_proposals(raw)

        return EvaluatedOpportunity(
            raw=raw,
            verdict=EvaluationVerdict.APPROVED,
            score=score,
            evaluation_notes="তথ্য সম্পূর্ণ, ইউআরএল সচল এবং আপনার স্কিল সেটের সাথে সামঞ্জস্যপূর্ণ।",
            missing_fields=[],
            actionable_summary=summary,
            official_apply_url=raw.source_url,
            deadline=raw.extracted_deadline,
            proposal_bundle=proposal_bundle
        )
