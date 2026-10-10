import os
import httpx
from typing import List, Optional
from models.schema import EvaluatedOpportunity, OpportunityType


class TelegramDeliveryService:
    """
    টেলিগ্রাম ডেলিভারি ও স্ল্যাশ কমান্ড সার্ভিস:
    - ইন্টারেক্টিভ বাটনসহ হ্যাকাথন ও জবের কার্ড পাঠায়।
    - ৩ স্তরের প্রপোজাল (Cold Email, Case Study, DM) আলাদা বাটনে দেখায়।
    """
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_opportunity_card(self, item: EvaluatedOpportunity) -> bool:
        if not self.bot_token or not self.chat_id or self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            # কনসোল ইন্টারেক্টিভ প্রিভিউ
            print("\n" + "=" * 50)
            print(f"📱 [টেলিগ্রাম কার্ড প্রিভিউ] (চ্যাট আইডি: {self.chat_id or 'Demo'})")
            print(item.actionable_summary)
            print(f"🔘 বাটন ১: [🌐 সরাসরি আবেদন করুন -> {item.official_apply_url}]")
            if item.proposal_bundle:
                print("🔘 বাটন ২: [📄 ৩-স্তরের প্রপোজাল দেখুন (Cold Email / Case Study / DM)]")
            print(f"🔍 ইভালুয়েটর রিপোর্ট: {item.evaluation_notes} (রি-ট্রাই: {item.raw.retry_count} বার)")
            print("=" * 50)
            return True

        inline_keyboard = [
            [{"text": "🌐 সরাসরি আবেদন করুন", "url": item.official_apply_url}]
        ]

        text = (
            f"🎯 *নতুন ভেরিফায়েড সুযোগ ({'হ্যাকাথন' if item.raw.type == OpportunityType.HACKATHON else 'রিমোট জব'})*\n"
            f"⭐ বিশ্বস্ততা স্কোর: {item.score}%\n\n"
            f"{item.actionable_summary}\n\n"
            f"🔍 *ইভালুয়েটরের মন্তব্য:* {item.evaluation_notes}"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "reply_markup": {"inline_keyboard": inline_keyboard}
        }

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{self.base_url}/sendMessage", json=payload, timeout=10.0)
                if res.status_code == 200:
                    if item.proposal_bundle:
                        # প্রপোজাল বান্ডিল সেন্ড
                        proposal_text = (
                            f"💼 *{item.raw.title} এর জন্য ৩-স্তরের প্রপোজাল পিচ:*\n\n"
                            f"*১. শর্ট কোল্ড ইমেইল:*\n```\n{item.proposal_bundle.cold_email}\n```\n\n"
                            f"*২. লিঙ্কডইন / মেসেঞ্জার ডিএম:*\n```\n{item.proposal_bundle.linkedin_dm}\n```"
                        )
                        await client.post(f"{self.base_url}/sendMessage", json={
                            "chat_id": self.chat_id,
                            "text": proposal_text,
                            "parse_mode": "Markdown"
                        }, timeout=10.0)
                    return True
                else:
                    print(f"[টেলিগ্রাম এরর] {res.status_code}: {res.text}")
                    return False
        except Exception as e:
            print(f"[টেলিগ্রাম এক্সেপশন]: {str(e)}")
            return False

    async def broadcast_opportunities(self, items: List[EvaluatedOpportunity]):
        for item in items:
            await self.send_opportunity_card(item)
