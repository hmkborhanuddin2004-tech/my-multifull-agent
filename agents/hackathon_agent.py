import asyncio
from typing import List, Dict, Any
from models.schema import RawOpportunity, OpportunityType


class HackathonAgent:
    """
    স্বতন্ত্র হ্যাকাথন হান্টার সাব-এজেন্ট:
    বাংলাদেশ (ICT Division, BASIS, Devpost, BD Tech Community) ও আন্তর্জাতিক এআই/ওয়েব হ্যাকাথন সংগ্রহ করে।
    ইভালুয়েটরের কাছ থেকে কোনো ফিডব্যাক বা অসম্পূর্ণ ফিল্ডের নোটিশ পেলে তা রি-স্ক্যান করে পূর্ণ করে।
    """
    def __init__(self):
        self.agent_name = "Hackathon Hunter"

    async def fetch_initial_hackathons(self) -> List[RawOpportunity]:
        """প্রথম পর্যায়ের হ্যাকাথন খোঁজা"""
        return [
            RawOpportunity(
                id="hack-bd-01",
                title="National AI & Robotics Hackathon Bangladesh",
                type=OpportunityType.HACKATHON,
                source_url="https://ictd.gov.bd/events/ai-hackathon-2026",
                organizer_or_company="ICT Division Bangladesh & BASIS",
                raw_description="বাংলাদেশের শিক্ষার্থীদের ও তরুণ ডেভেলপারদের জন্য কৃত্রিম বুদ্ধিমত্তা (AI), অটোমেশন এবং মোবাইল অ্যাপ ইনোভেশন ভিত্তিক জাতীয় হ্যাকাথন।",
                location="Dhaka, Bangladesh (Hybrid)",
                extracted_deadline="2026-11-20",
                tags=["AI", "Automation", "Mobile App", "Web Development"]
            ),
            RawOpportunity(
                id="hack-global-02",
                title="Global Agentic AI Virtual Hackathon 2026",
                type=OpportunityType.HACKATHON,
                source_url="https://devpost.com/hackathons/global-agentic-ai-2026",
                organizer_or_company="LabLab.ai & Google Cloud",
                raw_description="Build autonomous multi-agent systems using Gemini and Python. Fully remote international hackathon with $50,000 in prizes.",
                location="Global (Virtual/Remote)",
                extracted_deadline=None, # ডেমো টেস্ট: ইনিশিয়ালি ডেডলাইন মিসিং থাকবে যাতে ইভালুয়েটর রি-ট্রাই পাঠায়
                tags=["AI Agents", "Python", "Automation", "Web Development"]
            )
        ]

    async def refine_opportunity(self, item: RawOpportunity, missing_fields: List[str]) -> RawOpportunity:
        """ইভালুয়েটরের নির্দেশে তথ্য পুনরায় অনুসন্ধান ও সংশোধন করা"""
        print(f"  [🔄 {self.agent_name}]: '{item.title}'-এর অনুপস্থিত তথ্য ({', '.join(missing_fields)}) রি-স্ক্যান করা হচ্ছে...")
        await asyncio.sleep(0.5) # ডিপ সার্চ সিমুলেশন

        updated_item = item.model_copy()
        updated_item.retry_count += 1

        if "deadline" in missing_fields:
            updated_item.extracted_deadline = "2026-11-05"
            print(f"  [✓ {self.agent_name}]: ডেডলাইন উদ্ধার করা হয়েছে: 2026-11-05")

        if "source_url" in missing_fields or not updated_item.source_url.startswith("http"):
            updated_item.source_url = "https://devpost.com/hackathons/global-agentic-ai-2026"

        return updated_item
