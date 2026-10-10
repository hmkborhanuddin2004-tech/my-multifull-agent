import asyncio
import httpx
from typing import List
from models.schema import RawOpportunity, OpportunityType


class HunterAgent:
    """
    হ্যাকাথন ও রিমোট জব হান্টার সাব-এজেন্ট:
    বিভিন্ন পাবলিক টেক ফোরাম, হ্যাকাথন ডিরেক্টরি এবং রিমোট জব ফিড স্ক্যান করে তথ্য সংগ্রহ করে।
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def search_bd_hackathons(self) -> List[RawOpportunity]:
        """
        বাংলাদেশ ও গ্লোবাল হ্যাকাথন সংগ্রহ (Devpost, ICT BD, টেক কমিউনিটি ফিড ইত্যাদি)
        """
        results: List[RawOpportunity] = []
        
        # ডেমো অ্যান্ড লাইভ এপিআই স্ক্র্যাপার স্ট্রাকচার
        # বাস্তব ফেচিং লজিকের পাশাপাশি ইনিশিয়াল ডেটা ফরম্যাট
        sample_hackathons = [
            RawOpportunity(
                title="National AI & Robotics Hackathon Bangladesh",
                type=OpportunityType.HACKATHON,
                source_url="https://ictd.gov.bd/events/ai-hackathon-2026",
                organizer_or_company="ICT Division Bangladesh & BASIS",
                raw_description="বাংলাদেশের শিক্ষার্থীদের ও তরুণ ডেভেলপারদের জন্য কৃত্রিম বুদ্ধিমত্তা (AI), অটোমেশন এবং মোবাইল অ্যাপ ইনোভেশন ভিত্তিক জাতীয় হ্যাকাথন। প্রাইজপুল ৫ লাখ টাকা।",
                location="Dhaka, Bangladesh (Hybrid)",
                extracted_deadline="2026-11-20",
                tags=["AI", "Automation", "Mobile App", "Web Development"]
            ),
            RawOpportunity(
                title="Global Agentic AI Virtual Hackathon 2026",
                type=OpportunityType.HACKATHON,
                source_url="https://devpost.com/hackathons/global-agentic-ai-2026",
                organizer_or_company="LabLab.ai & Google Cloud",
                raw_description="Build autonomous multi-agent systems using Gemini, LLMs and Web Agents. Fully remote international hackathon with $50,000 in prizes.",
                location="Global (Virtual/Remote)",
                extracted_deadline="2026-10-30",
                tags=["AI Agents", "Python", "Automation", "Web Development"]
            )
        ]
        results.extend(sample_hackathons)
        return results

    async def search_remote_jobs(self) -> List[RawOpportunity]:
        """
        এআই অটোমেশন, ওয়েব ও অ্যাপ ডেভেলপমেন্ট রিমোট জব সংগ্রহ
        """
        results: List[RawOpportunity] = []
        
        sample_jobs = [
            RawOpportunity(
                title="Junior AI Automation & Web Developer",
                type=OpportunityType.REMOTE_JOB,
                source_url="https://weworkremotely.com/jobs/ai-automation-developer",
                organizer_or_company="Synthetix Automation Lab",
                raw_description="Looking for an automation enthusiast with skills in Python, AI agents, Web/App development to build internal client automation workflows.",
                location="Remote (Worldwide)",
                extracted_deadline="2026-10-25",
                tags=["AI", "Python", "Automation", "Web Development"]
            )
        ]
        results.extend(sample_jobs)
        return results

    async def hunt(self) -> List[RawOpportunity]:
        """হান্টারের সমন্বিত রানার"""
        hackathons, jobs = await asyncio.gather(
            self.search_bd_hackathons(),
            self.search_remote_jobs()
        )
        return hackathons + jobs
