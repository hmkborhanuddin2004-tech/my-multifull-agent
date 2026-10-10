import unittest
import asyncio
from models.schema import RawOpportunity, OpportunityType, EvaluationVerdict
from agents.evaluator_agent import EvaluatorAgent


class TestEvaluatorReflection(unittest.TestCase):
    def setUp(self):
        self.evaluator = EvaluatorAgent(max_retries=3)

    def test_missing_deadline_triggers_retry_required(self):
        """ডেডলাইন না থাকলে ড্রপ না করে RETRY_REQUIRED ট্রিগার হয় কি না"""
        raw = RawOpportunity(
            id="test-1",
            title="Incomplete Hackathon",
            type=OpportunityType.HACKATHON,
            source_url="https://example.com/hackathon",
            organizer_or_company="Test Org",
            raw_description="A hackathon without deadline specified initially",
            location="Dhaka",
            extracted_deadline=None,
            tags=["AI"],
            retry_count=0
        )
        res = asyncio.run(self.evaluator.evaluate(raw))
        self.assertEqual(res.verdict, EvaluationVerdict.RETRY_REQUIRED)
        self.assertIn("deadline", res.missing_fields)

    def test_proposals_generated_for_remote_job(self):
        """অনুমোদিত রিমোট জবের জন্য ৩ স্তরের প্রপোজাল তৈরি হয় কি না"""
        raw = RawOpportunity(
            id="test-2",
            title="Automation & Meta Ads Engineer",
            type=OpportunityType.REMOTE_JOB,
            source_url="https://example.com/job",
            organizer_or_company="Growth Agency",
            raw_description="Looking for an engineer to build pipelines",
            location="Remote",
            extracted_deadline="2026-11-20",
            tags=["AI Automation", "Meta Marketing"],
            retry_count=0
        )
        res = asyncio.run(self.evaluator.evaluate(raw))
        self.assertEqual(res.verdict, EvaluationVerdict.APPROVED)
        self.assertIsNotNone(res.proposal_bundle)
        self.assertIn("Subject:", res.proposal_bundle.cold_email)
        self.assertIn("Growth Agency", res.proposal_bundle.cold_email)


if __name__ == "__main__":
    unittest.main()
