# SHASHAKT

## AI-Powered Conversational Livelihood & Skill Recommendation Platform

SHASHAKT is an AI-powered, multilingual conversational platform designed to help users discover suitable skills, training programs, and local livelihood opportunities based on their personal profile, interests, education, location, and goals.

The system is designed as an omnichannel assistant that can eventually work through Web, WhatsApp, and Phone/IVR interfaces.

---

## 🎯 Problem

Many students and job seekers struggle to identify:

- Which skills they should learn
- Which training programs match their background
- Which career path is suitable for them
- Which opportunities are available locally
- What eligibility requirements they need to fulfil
- What steps they should take next

SHASHAKT solves this through a conversational AI-based recommendation system.

---

## 💡 Solution

Instead of forcing users to fill complicated forms, SHASHAKT allows them to simply talk to an AI assistant.

Example:

> "Main 12th pass hoon, Mathura mein rehta hoon aur mujhe computer field mein jaana hai."

SHASHAKT can understand the user's information, build a profile, retrieve relevant knowledge and opportunities, rank suitable options, and explain the recommended path in simple language.

---

## 🧠 Core Architecture

```text
                    USER
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        WEB        WHATSAPP     PHONE/IVR
          │           │           │
          └───────────┼───────────┘
                      ↓
             VOICE / MESSAGE GATEWAY
                      ↓
          CONVERSATION ORCHESTRATOR
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
     PROFILE /     NSQF RAG     LOCAL
       MEMORY                    DATA
          │           │           │
          └───────────┼───────────┘
                      ↓
           RECOMMENDATION ENGINE
                      ↓
          SCORING + SEMANTIC MATCH
                      ↓
             EXPLANATION / PLAN
                      ↓
                     USER
