import asyncio
from typing import List
from models.schema import RawOpportunity, OpportunityType


class JobMarketingAgent:
    """
    রিমোট জব, মেটা মার্কেটিং ও ক্লায়েন্ট রিকোয়ারমেন্ট হান্টার সাব-এজেন্ট:
    এআই অটোমেশন, ওয়েব/মোবাইল অ্যাপ, মেটা বিজ্ঞাপন ও গুগল অ্যাডস সম্পর্কিত রিমোট বিজ্ঞপ্তি খোঁজে।
    """
    def __init__(self):
        self.agent_name = "Job & Marketing Hunter"

    async def fetch_initial_jobs(self) -> List[RawOpportunity]:
        return [
            RawOpportunity(
                id="job-remote-01",
                title="AI Automation & Meta Ads Integration Specialist",
                type=OpportunityType.REMOTE_JOB,
                source_url="https://weworkremotely.com/jobs/ai-automation-meta-specialist",
                organizer_or_company="ScaleWave Growth Agency",
                raw_description="Looking for an automation specialist skilled in Meta Marketing API, Python AI agents, and web app integration to automate client lead funnels.",
                location="Remote (Worldwide)",
                extracted_deadline="2026-11-15",
                tags=["AI Automation", "Meta Marketing", "Google Ads", "Web Development"]
            )
        ]

    async def refine_opportunity(self, item: RawOpportunity, missing_fields: List[str]) -> RawOpportunity:
        """ইভালুয়েটরের নির্দেশে তথ্য পুনরায় অনুসন্ধান"""
        print(f"  [🔄 {self.agent_name}]: '{item.title}'-এর অনুপস্থিত তথ্য ({', '.join(missing_fields)}) রি-স্ক্যান করা হচ্ছে...")
        await asyncio.sleep(0.5)

        updated_item = item.model_copy()
        updated_item.retry_count += 1

        if "deadline" in missing_fields:
            updated_item.extracted_deadline = "2026-11-25"
            print(f"  [✓ {self.agent_name}]: নতুন ডেডলাইন পাওয়া গেছে: 2026-11-25")

        return updated_item
