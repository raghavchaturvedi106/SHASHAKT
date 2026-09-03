import os
import re
from typing import Optional, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ============================================================
# SHASHAKT
# AI-Powered Conversational Livelihood & Skill Recommendation
# ============================================================


app = FastAPI(
    title="SHASHAKT API",
    description="AI-powered conversational livelihood and skill recommendation platform",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# IN-MEMORY SESSION STORE
# ============================================================
#
# MVP ke liye Redis ki jagah simple memory use kar rahe hain.
# Production version mein Redis use kiya ja sakta hai.
# ============================================================

sessions: Dict[str, Dict] = {}


# ============================================================
# SAMPLE OPPORTUNITY DATA
# ============================================================
#
# Baad mein isko opportunities.json / database se replace
# kiya ja sakta hai.
# ============================================================

OPPORTUNITIES = [

    {
        "id": "OP001",
        "title": "Data Entry & Computer Operations",
        "type": "Training + Job",
        "location": "Mathura",
        "education": "10th/12th",
        "skills": [
            "computer",
            "typing",
            "ms office",
            "data entry"
        ],
        "interests": [
            "computer",
            "office work",
            "technology"
        ],
        "description":
            "Basic computer operations, typing, MS Office and data entry skills."
    },

    {
        "id": "OP002",
        "title": "Digital Marketing Training",
        "type": "Training",
        "location": "Mathura",
        "education": "12th",
        "skills": [
            "social media",
            "marketing",
            "communication",
            "computer"
        ],
        "interests": [
            "marketing",
            "social media",
            "business",
            "computer"
        ],
        "description":
            "Digital marketing, social media management and online business skills."
    },

    {
        "id": "OP003",
        "title": "Web Development Training",
        "type": "Training",
        "location": "Online",
        "education": "10th/12th",
        "skills": [
            "html",
            "css",
            "javascript",
            "programming"
        ],
        "interests": [
            "coding",
            "computer",
            "technology",
            "software"
        ],
        "description":
            "Learn HTML, CSS, JavaScript and fundamentals of web development."
    },

    {
        "id": "OP004",
        "title": "Cybersecurity Fundamentals",
        "type": "Training",
        "location": "Online",
        "education": "12th",
        "skills": [
            "networking",
            "linux",
            "cybersecurity",
            "security"
        ],
        "interests": [
            "cybersecurity",
            "ethical hacking",
            "technology",
            "computers"
        ],
        "description":
            "Beginner cybersecurity training covering networking, Linux and security fundamentals."
    },

    {
        "id": "OP005",
        "title": "Computer Hardware Technician",
        "type": "Training + Job",
        "location": "Mathura",
        "education": "10th",
        "skills": [
            "hardware",
            "computer",
            "troubleshooting",
            "repair"
        ],
        "interests": [
            "computer",
            "hardware",
            "technology",
            "repair"
        ],
        "description":
            "Computer hardware installation, troubleshooting and repair skills."
    }
]


# ============================================================
# NSQF-STYLE KNOWLEDGE DATA
# ============================================================

KNOWLEDGE_BASE = [

    {
        "topic": "computer",
        "text":
            "Computer-related entry-level careers include data entry, "
            "computer operations, hardware support and web development."
    },

    {
        "topic": "cybersecurity",
        "text":
            "Cybersecurity beginners should develop fundamentals of "
            "computer networks, Linux, operating systems and security concepts."
    },

    {
        "topic": "web development",
        "text":
            "Web development beginners can start with HTML, CSS and JavaScript "
            "before moving towards frameworks and backend development."
    },

    {
        "topic": "digital marketing",
        "text":
            "Digital marketing includes social media management, content, "
            "online advertising, analytics and digital business skills."
    }
]


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    language: str = "hinglish"


class ProfileRequest(BaseModel):
    session_id: str = "default"


# ============================================================
# BASIC TEXT UTILITIES
# ============================================================

def normalize(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower().strip()
    )


def contains_any(text: str, words: List[str]) -> bool:
    return any(word in text for word in words)


# ============================================================
# PROFILE EXTRACTION
# ============================================================

def extract_profile(message: str, profile: Dict) -> Dict:

    text = normalize(message)

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "12th",
            "12 pass",
            "inter pass",
            "intermediate"
        ]
    ):
        profile["education"] = "12th"

    elif contains_any(
        text,
        [
            "10th",
            "10 pass",
            "high school"
        ]
    ):
        profile["education"] = "10th"

    elif contains_any(
        text,
        [
            "graduation",
            "graduate",
            "btech",
            "b.tech",
            "degree"
        ]
    ):
        profile["education"] = "Graduate"

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    known_locations = [
        "mathura",
        "delhi",
        "noida",
        "ghaziabad",
        "agra",
        "lucknow",
        "jaipur",
        "gurgaon",
        "gurugram"
    ]

    for location in known_locations:

        if location in text:
            profile["location"] = location.title()
            break

    # --------------------------------------------------------
    # Interests
    # --------------------------------------------------------

    interest_map = {

        "computer": [
            "computer",
            "computers"
        ],

        "coding": [
            "coding",
            "programming",
            "developer",
            "development"
        ],

        "cybersecurity": [
            "cybersecurity",
            "cyber security",
            "ethical hacking",
            "hacking"
        ],

        "digital marketing": [
            "digital marketing",
            "marketing",
            "social media"
        ],

        "hardware": [
            "hardware",
            "repair",
            "computer repair"
        ]
    }

    interests = profile.get(
        "interests",
        []
    )

    for interest, keywords in interest_map.items():

        if contains_any(text, keywords):

            if interest not in interests:
                interests.append(interest)

    profile["interests"] = interests

    # --------------------------------------------------------
    # Career Goal
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "job",
            "naukri",
            "employment",
            "kamai",
            "work"
        ]
    ):
        profile["goal"] = "Job"

    elif contains_any(
        text,
        [
            "course",
            "training",
            "seekhna",
            "learn"
        ]
    ):
        profile["goal"] = "Training"

    return profile


# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(query: str) -> List[Dict]:

    text = normalize(query)

    results = []

    for item in KNOWLEDGE_BASE:

        if item["topic"] in text:

            results.append(item)

    return results


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def calculate_score(
    opportunity: Dict,
    profile: Dict
) -> int:

    score = 0

    education = profile.get(
        "education",
        ""
    ).lower()

    location = profile.get(
        "location",
        ""
    ).lower()

    interests = profile.get(
        "interests",
        []
    )

    interests = [
        str(x).lower()
        for x in interests
    ]

    # --------------------------------------------------------
    # Location match
    # --------------------------------------------------------

    if location:

        if (
            opportunity["location"].lower()
            == location
        ):
            score += 30

        elif opportunity["location"].lower() == "online":
            score += 20

    # --------------------------------------------------------
    # Education match
    # --------------------------------------------------------

    required_education = (
        opportunity["education"]
        .lower()
    )

    if education:

        if education in required_education:
            score += 25

        elif education == "graduate":
            score += 25

    # --------------------------------------------------------
    # Interest match
    # --------------------------------------------------------

    opportunity_interests = [
        x.lower()
        for x in opportunity["interests"]
    ]

    for interest in interests:

        if interest in opportunity_interests:
            score += 15

    # --------------------------------------------------------
    # Skill / interest semantic-style matching
    # --------------------------------------------------------

    opportunity_text = normalize(
        opportunity["title"]
        + " "
        + opportunity["description"]
        + " "
        + " ".join(opportunity["skills"])
    )

    for interest in interests:

        if interest in opportunity_text:
            score += 10

    return min(score, 100)


def recommend(
    profile: Dict,
    limit: int = 3
) -> List[Dict]:

    recommendations = []

    for opportunity in OPPORTUNITIES:

        score = calculate_score(
            opportunity,
            profile
        )

        item = opportunity.copy()

        item["score"] = score

        recommendations.append(item)

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:limit]


# ============================================================
# RESPONSE GENERATOR
# ============================================================

def generate_response(
    message: str,
    profile: Dict,
    recommendations: List[Dict],
    language: str
) -> str:

    text = normalize(message)

    # --------------------------------------------------------
    # Greeting
    # --------------------------------------------------------

    if contains_any(
        text,
        [
            "hello",
            "hi",
            "hii",
            "namaste",
            "hey"
        ]
    ) and len(text.split()) <= 3:

        return (
            "Namaste! Main SHASHAKT hoon. "
            "Aap apni education, location, skills ya career goal batao. "
            "Main aapke liye suitable training aur opportunities find karunga."
        )

    # --------------------------------------------------------
    # Missing profile information
    # --------------------------------------------------------

    missing = []

    if not profile.get("education"):
        missing.append("education")

    if not profile.get("location"):
        missing.append("location")

    if not profile.get("interests"):
        missing.append("interest/skill")

    if missing:

        readable = ", ".join(missing)

        return (
            f"Main aapke liye personalized recommendation bana sakta hoon. "
            f"Bas mujhe aapki {readable} ke baare mein thoda bata do."
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    if not recommendations:

        return (
            "Abhi exact match nahi mila. "
            "Aap apni skills ya career goal thoda aur detail mein batao."
        )

    response = (
        f"Aapki profile ke basis par mujhe "
        f"{len(recommendations)} suitable options mile hain:\n\n"
    )

    for index, item in enumerate(
        recommendations,
        start=1
    ):

        response += (
            f"{index}. {item['title']}\n"
            f"   Type: {item['type']}\n"
            f"   Location: {item['location']}\n"
            f"   Match Score: {item['score']}%\n\n"
        )

    response += (
        "Meri recommendation: pehle highest-match option ko "
        "consider karo. Agar aap chaho to main iska "
        "learning path aur next steps bhi bata sakta hoon."
    )

    return response


# ============================================================
# ORCHESTRATOR
# ============================================================

def orchestrate(
    request: ChatRequest
) -> Dict:

    session_id = request.session_id

    # Create session
    if session_id not in sessions:

        sessions[session_id] = {
            "profile": {},
            "history": []
        }

    session = sessions[session_id]

    profile = session["profile"]

    # --------------------------------------------------------
    # 1. Understand user message
    # --------------------------------------------------------

    message = request.message.strip()

    # --------------------------------------------------------
    # 2. Extract / update profile
    # --------------------------------------------------------

    profile = extract_profile(
        message,
        profile
    )

    session["profile"] = profile

    # --------------------------------------------------------
    # 3. Save conversation state
    # --------------------------------------------------------

    session["history"].append(
        {
            "role": "user",
            "content": message
        }
    )

    # Keep MVP memory small
    session["history"] = (
        session["history"][-10:]
    )

    # --------------------------------------------------------
    # 4. Retrieve relevant knowledge
    # --------------------------------------------------------

    knowledge = retrieve_knowledge(
        message
    )

    # --------------------------------------------------------
    # 5. Recommendation engine
    # --------------------------------------------------------

    recommendations = recommend(
        profile
    )

    # --------------------------------------------------------
    # 6. Generate explanation
    # --------------------------------------------------------

    answer = generate_response(
        message,
        profile,
        recommendations,
        request.language
    )

    # --------------------------------------------------------
    # 7. Save assistant response
    # --------------------------------------------------------

    session["history"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return {

        "success": True,

        "session_id": session_id,

        "answer": answer,

        "profile": profile,

        "recommendations": recommendations,

        "knowledge_context": knowledge,

        "orchestrator": {
            "profile_updated": True,
            "knowledge_retrieved": len(knowledge),
            "recommendations_generated": len(
                recommendations
            )
        }
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "name": "SHASHAKT",
        "description":
            "AI-powered conversational livelihood and skill recommendation platform",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "SHASHAKT",

        "knowledge_items":
            len(KNOWLEDGE_BASE),

        "opportunities":
            len(OPPORTUNITIES),

        "sessions":
            len(sessions)
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    return orchestrate(request)


# ============================================================
# PROFILE
# ============================================================

@app.post("/profile")
def get_profile(
    request: ProfileRequest
):

    session = sessions.get(
        request.session_id
    )

    if not session:

        return {
            "success": False,
            "message": "Session not found."
        }

    return {

        "success": True,

        "session_id":
            request.session_id,

        "profile":
            session["profile"]
    }


# ============================================================
# OPPORTUNITIES
# ============================================================

@app.get("/opportunities")
def opportunities():

    return {

        "success": True,

        "count":
            len(OPPORTUNITIES),

        "opportunities":
            OPPORTUNITIES
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

@app.get("/recommend")
def recommendations(
    session_id: str = "default"
):

    session = sessions.get(
        session_id
    )

    if not session:

        return {

            "success": False,

            "message":
                "Session not found."
        }

    profile = session["profile"]

    results = recommend(
        profile
    )

    return {

        "success": True,

        "profile":
            profile,

        "recommendations":
            results
    }


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    import uvicorn

    port = int(
        os.environ.get(
            "PORT",
            8000
        )
    )

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )
