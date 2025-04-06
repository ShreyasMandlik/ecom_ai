# 🛍️ AI-Powered Product Recommendation System

## Overview

This project implements a multi-agent, AI-driven recommendation engine designed to deliver high-quality, personalized product suggestions based on customer behavior and preferences. Built using Python, Django, and LLMs like TinyLlama and LLaMA 3.2 (via Ollama), the system is modular, scalable, and cost-efficient.

---

## 🚀 Key Features

- **Customer Behavior Analysis**  
  Leverages AI to analyze demographics, browsing patterns, and purchase history to identify customer preferences.

- **Product Filtering & Scoring**  
  Narrows down product catalog based on inferred categories and affinity scores like price match, seasonality, and sentiment.

- **Personalized Recommendation**  
  Uses deep context reasoning to recommend top products that match the customer's needs.

---

## 🧠 Agents' Interaction Design

- **CustomerAgent**  
  Analyzes customer data (demographics, behavior, history) and infers relevant product categories.

- **ProductAgent**  
  Filters the product catalog using AI-inferred categories and scores them based on multiple affinity metrics. Selects the top 100.

- **RecommendationAgent**  
  Chunks filtered products into batches, then selects the top 3 from each using deep customer context and AI reasoning.

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Framework:** Django  
- **Data Analysis:** Pandas  
- **IDE:** Visual Studio Code  
- **LLMs (via Ollama):** TinyLlama, LLaMA 3.2

---

## 💾 Data Handling & Optimization

- Filters products based on average order pricing to better match customer intent.
- Caches AI outputs and stores analysis in a database to avoid redundant LLM calls, reducing cost.
- Includes a feedback loop: if customer preferences shift, stored analysis is updated automatically.

---

## 📈 Future Enhancements

- Real-time integration with user interaction data.
- Dashboard for visualizing agent performance and product trends.
- A/B testing to evaluate recommendation quality.
- Caches AI-generated insights to reduce repeated LLM calls and save computation cost.

---
## Demo 
- https://drive.google.com/file/d/1RqCyYmmOepg5Dys5RgClsubY8ZtcCKho/view?usp=drive_link

## ✅ Conclusion

This solution effectively addresses the need for intelligent, adaptive product recommendations. Through the use of specialized agents and powerful LLMs, it ensures personalized results while minimizing system load and cost. The feedback-driven design guarantees relevance even as customer behavior evolves.

---
