# 🎓 CampusTrade: A Student Marketplace

**CampusTrade** is a full-stack peer-to-peer (P2P) marketplace built exclusively for college students.  
It enables authenticated users from a specific college to **buy, sell, and trade** items within their campus community.  
The platform includes a built-in **messaging system** for seamless communication between buyers and sellers.

---

## ✨ Features

### 🔐 Secure Authentication
- Only users with a valid college email domain (e.g., `@iiitkottayam.ac.in`) can register.
- JWT-based token authentication for secure API access.

### 🛍️ Item Marketplace
- Authenticated users can **post**, **view**, and **search** for items.
- Each listing includes item details, trade preferences, and user information.

### 🔎 Search Functionality
- Find items by **title**, **description**, or **trade interests**.

### 📦 Personal Item Management
- A **“My Items”** page to view and delete your own listings.

### 💬 Conversation System
- Initiate conversations directly from an item's detail page.
- **“Conversations”** page groups all chats by item and user.
- **“Chat Thread”** page shows the entire message history and allows real-time replies.

---

## 🛠️ Tech Stack

### Backend
- **Python**
- **Django**
- **Django REST Framework (DRF)** — for RESTful APIs
- **Simple JWT** — for secure token authentication

### Frontend
- **Streamlit** — for building the interactive UI
- **Requests** — for API communication with the Django backend

### Database
- **Neon** — Serverless Cloud PostgreSQL (high-performance and free-tier friendly)

---

## 🚀 How to Run This Project

This project has two main parts:  
1. **Backend** – Django REST API  
2. **Frontend** – Streamlit UI  

You’ll need to run both in **separate terminals**.

---

### ✅ Prerequisites

Before you begin, make sure you have:
- **Python 3.10+**
- A **Neon account** for your PostgreSQL database
- Installed **Git** (optional, for version control)

---
