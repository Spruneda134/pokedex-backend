# Pokédex Web App

Developed a mobile-first full-stack Pokédex web app that lets users explore and interact with Pokémon data through an AI-powered interface. The frontend, hosted on Vercel and developed with Next.js, TypeScript, and Tailwind CSS, provides a responsive and dynamic Pokédex-like experience.

The backend, built with Flask, integrates OpenAI’s API to generate natural Pokémon responses and uses pandas for structured data handling from a CSV-based Pokédex dataset. Hosted on Render, the backend communicates securely with the Vercel-hosted frontend via configured CORS to handle cross-origin requests.

---

## Features
- **Search & Explore:** Browse Pokémon by name, type, or ability  
- **AI-Powered Responses:** Get natural language insights about Pokémon  
- **Data Handling:** Structured Pokémon data managed with pandas from a CSV dataset  
- **Responsive Design:** Mobile-first frontend for seamless user experience  
- **Secure Frontend-Backend Communication:** Configured CORS between Vercel frontend and Render backend  

---

## Tech Stack
- **Frontend:** Next.js, TypeScript, Tailwind CSS (hosted on Vercel)  
- **Backend:** Flask, OpenAI API, pandas (hosted on Render)  
- **Deployment:** Vercel (frontend), Render (backend)  

---

## Note
The backend is hosted on Render’s free tier, which may go into “sleep mode” when not in use. If the server has been idle, the first request may take 10–30 seconds to wake up before responding. After that, performance is normal.

---

**Frontend Github:** https://github.com/Spruneda134/pokedex-frontend
