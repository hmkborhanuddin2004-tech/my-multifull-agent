import asyncio
import os
import sys

# Windows কনসোলে বাংলা ও ইমোজি প্রিন্ট সাপোর্ট
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from agents.supervisor import SupervisorAgent
from bot.telegram_service import TelegramDeliveryService

# .env লোড
load_dotenv()


async def main():
    print("=" * 60)
    print("🚀 মাল্টি-এজেন্ট সিস্টেম (ফেজ ১: হ্যাকাথন ও জব ট্র্যাকার) চালু হচ্ছে...")
    print("=" * 60)

    # ১. মূল সাপ্লাই (Supervisor) এজেন্ট ইনিশিয়ালাইজেশন
    supervisor = SupervisorAgent()
    telegram_service = TelegramDeliveryService()

    # ২. পাইপলাইন রান
    verified_opportunities = await supervisor.run_pipeline()

    # ৩. টেলিগ্রাম বাটন ডেলিভারি
    print(f"\n[টেলিগ্রাম ডেলিভারি] ব্যবহারকারীর কাছে {len(verified_opportunities)}টি কার্ড পাঠানো হচ্ছে...")
    await telegram_service.broadcast_opportunities(verified_opportunities)

    print("\n✅ পুরো পাইপলাইন সফলভাবে সম্পন্ন হয়েছে।")


if __name__ == "__main__":
    asyncio.run(main())
