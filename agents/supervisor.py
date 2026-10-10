import asyncio
from typing import List
from agents.hackathon_agent import HackathonAgent
from agents.job_marketing_agent import JobMarketingAgent
from agents.evaluator_agent import EvaluatorAgent
from models.schema import EvaluatedOpportunity, EvaluationVerdict, RawOpportunity, OpportunityType


class SupervisorAgent:
    """
    মূল সাপ্লাই (Supervisor Orchestrator):
    - স্বাধীন হ্যাকাথন এজেন্ট ও জব/মার্কেটিং এজেন্টের সমন্বয় করে।
    - ইভালুয়েটরের ফিডব্যাক লুপ পরিচালনা করে: যদি কোনো তথ্য অসম্পূর্ণ থাকে,
      তবে তা ড্রপ না করে সংশ্লিষ্ট এজেন্টের কাছে আবার পাঠিয়ে রি-স্ক্যান করায়।
    """
    def __init__(self):
        self.hackathon_agent = HackathonAgent()
        self.job_agent = JobMarketingAgent()
        self.evaluator = EvaluatorAgent(max_retries=3)

    async def _process_with_reflection_loop(self, raw_item: RawOpportunity) -> EvaluatedOpportunity:
        current_item = raw_item
        while True:
            evaluation = await self.evaluator.evaluate(current_item)
            
            # যদি ইভালুয়েটর পাস করে বা পুরোপুরি বাতিল করে, লুপ শেষ
            if evaluation.verdict != EvaluationVerdict.RETRY_REQUIRED:
                return evaluation

            print(f"  [⚠️ ইভালুয়েটর ফিডব্যাক]: '{current_item.title}' তে তথ্য ঘাটতি! রি-ট্রাই পাঠানো হচ্ছে...")
            
            # ঘাটতি পূরণের জন্য নির্দিষ্ট সাব-এজেন্টের কাছে ফেরত পাঠানো
            if current_item.type == OpportunityType.HACKATHON:
                current_item = await self.hackathon_agent.refine_opportunity(current_item, evaluation.missing_fields)
            else:
                current_item = await self.job_agent.refine_opportunity(current_item, evaluation.missing_fields)

    async def run_pipeline(self) -> List[EvaluatedOpportunity]:
        print("[মূল সাপ্লাই] পাইপলাইন চালু হচ্ছে: পৃথক সাব-এজেন্টদের অনুসন্ধানের নির্দেশ দেওয়া হলো...")
        
        # হ্যাকাথন ও জব হান্টাররা সমান্তরালে কাজ শুরু করল
        initial_hackathons, initial_jobs = await asyncio.gather(
            self.hackathon_agent.fetch_initial_hackathons(),
            self.job_agent.fetch_initial_jobs()
        )
        all_raw_items = initial_hackathons + initial_jobs
        print(f"[মূল সাপ্লাই] মোট {len(all_raw_items)}টি প্রাথমিক সুযোগ সংগৃহীত হয়েছে। ইভালুয়েশন শুরু হচ্ছে...")

        verified_results: List[EvaluatedOpportunity] = []

        for item in all_raw_items:
            final_eval = await self._process_with_reflection_loop(item)
            if final_eval.verdict == EvaluationVerdict.APPROVED:
                print(f"  [✓ সম্পূর্ণ ও অনুমোদিত - স্কোর {final_eval.score}%]: {final_eval.raw.title} (রি-ট্রাই: {final_eval.raw.retry_count} বার)")
                verified_results.append(final_eval)
            else:
                print(f"  [✗ বাতিল]: {final_eval.raw.title} - {final_eval.evaluation_notes}")

        print(f"[মূল সাপ্লাই] সফলভাবে যাচাই সম্পন্ন। ফাইনাল উত্তীর্ণ সুযোগ: {len(verified_results)}টি।")
        return verified_results
