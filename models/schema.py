from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class OpportunityType(str, Enum):
    HACKATHON = "HACKATHON"
    REMOTE_JOB = "REMOTE_JOB"


class EvaluationVerdict(str, Enum):
    APPROVED = "APPROVED"                   # সম্পূর্ণ সঠিক ও অনুমোদিত
    RETRY_REQUIRED = "RETRY_REQUIRED"       # অসম্পূর্ণ তথ্য, সাব-এজেন্টের কাছে ফেরত পাঠানো হবে
    PERMANENT_REJECT = "PERMANENT_REJECT"   # স্প্যাম বা বাতিলযোগ্য


class ProposalTemplate(BaseModel):
    """৩ স্তরের ক্লায়েন্ট ও জব অ্যাপ্লিকেশন পিচ"""
    cold_email: str = Field(description="সংক্ষিপ্ত ও সরাসরি কোল্ড ইমেইল")
    case_study_pitch: str = Field(description="দক্ষতা ও প্রজেক্ট প্রমাণসহ বিশদ প্রপোজাল")
    linkedin_dm: str = Field(description="সোশ্যাল মিডিয়া/লিঙ্কডইন/মেসেঞ্জার ডিএম ফরম্যাট")


class RawOpportunity(BaseModel):
    """হান্টার সাব-এজেন্ট যে প্রাথমিক তথ্য খুঁজে পায়"""
    id: str = Field(description="অনন্য ট্র্যাকিং আইডি")
    title: str = Field(description="ইভেন্ট বা জবের নাম")
    type: OpportunityType = Field(description="হ্যাকাথন নাকি রিমোট জব")
    source_url: str = Field(description="প্রাথমিক তথ্যের ইউআরএল")
    organizer_or_company: str = Field(description="আয়োজক প্রতিষ্ঠান বা কোম্পানির নাম")
    raw_description: str = Field(description="বিবরণ বা পোস্টের লেখা")
    location: str = Field(default="Bangladesh", description="লোকেশন বা রিমোট স্ট্যাটাস")
    extracted_deadline: Optional[str] = Field(default=None, description="আবেদনের শেষ তারিখ")
    tags: List[str] = Field(default_factory=list, description="ট্যাগসমূহ যেমন AI, Web, App")
    retry_count: int = Field(default=0, description="কতবার রি-ট্রাই করা হয়েছে")


class EvaluatedOpportunity(BaseModel):
    """ইভালুয়েটরের মান যাচাই ও ভেরিফিকেশনের পর প্রস্তুতকৃত তথ্য"""
    raw: RawOpportunity
    verdict: EvaluationVerdict = Field(description="ইভালুয়েটরের রায়")
    score: int = Field(ge=0, le=100, description="প্রাসঙ্গিকতা ও নির্ভরযোগ্যতার স্কোর (০-১০০)")
    evaluation_notes: str = Field(description="যাচাইকরণ নোট বা রিজেকশনের কারণ")
    missing_fields: List[str] = Field(default_factory=list, description="যেসব তথ্য অনুপস্থিত")
    actionable_summary: str = Field(default="", description="ইউজারের পড়ার জন্য সাজানো পরিষ্কার বাংলা সারাংশ")
    official_apply_url: str = Field(default="", description="আবেদনের আসল ও নিশ্চিত ইউআরএল")
    deadline: str = Field(default="", description="নিশ্চিত ডেডলাইন")
    proposal_bundle: Optional[ProposalTemplate] = Field(default=None, description="প্রস্তুতকৃত ৩ স্তরের প্রপোজাল বান্ডিল")
