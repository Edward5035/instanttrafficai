# Instant Traffic AI

A modern SaaS Flask-based web application that helps users generate traffic campaigns, find traffic sources, and analyze their marketing performance.

## Overview

Instant Traffic AI is a comprehensive marketing automation tool with a modern SaaS interface featuring:
- Dashboard Overview with Real-time Stats
- One-Click Campaign Generator
- Traffic Leak Finder
- Traffic Heatmap Dashboard
- Viral Content Finder
- Email Sequence Builder
- Content Calendar
- Content Library
- Competitor Tracker
- Traffic Tips & Best Practices

## Recent Changes (November 17, 2025)

### Latest Updates (November 17, 2025 - Web Scraping Enhancement)
- **Real Data Scraping Module**: Added `web_scraper.py` for pulling real data instead of templates
  - Reddit API integration to find real communities with actual member counts
  - Web scraping for trending content from multiple platforms
  - Competitor website analysis extracting real SEO data, keywords, and meta information
  - DuckDuckGo search integration for finding Facebook groups and articles
  - Replaces template-based fake data with authentic information
- **Caching System**: Added `cache_helper.py` for performance optimization
  - 1-hour cache expiry for scraped data
  - Prevents repeated API calls and reduces load times
  - Automatic cache invalidation after expiry
- **Enhanced Dependencies**: Added BeautifulSoup4 and lxml for web scraping
- **Integration Complete**: Connected web scraper to all relevant endpoints
  - Traffic Leak Finder now uses real Reddit communities and platform searches
  - Viral Content Finder scrapes actual trending posts and articles
  - Competitor Tracker analyzes real websites for SEO insights

### Previous Updates
- **Gemini API Integration**: Configured GEMINI_API_KEY securely in environment secrets
- **Upgraded to Gemini 2.5 Flash**: Updated from gemini-2.0-flash to the latest stable gemini-2.5-flash model
  - Better reasoning capabilities
  - Improved token efficiency (20-30% fewer tokens)
  - Enhanced response quality
- Added google-genai library to dependencies

### Initial Setup
- Initial project setup with Flask and SQLAlchemy
- Implemented secure auto-registration login system with password authentication
  - Password requirement: minimum 6 characters
  - Passwords hashed using Werkzeug's secure password hashing
  - Auto-creates account if email doesn't exist, verifies password if it does
- Added CSRF protection for all state-changing endpoints using Flask-WTF
  - CSRF tokens fetched and included in all POST requests
  - SameSite=Lax and HttpOnly cookies for session security
- **Redesigned entire UI as modern SaaS application**
  - Sidebar navigation with all 10 features
  - Top navbar with user info
  - Responsive mobile toggle menu
  - Modern card-based layouts
  - Warm color scheme (orange, yellow, coral tones)
- Built AJAX-based features to avoid full page reloads
- Added 4 database models: User (with password_hash), Campaign, TrafficSource, Analytics
- Implemented all 10 features:
  - Dashboard with real-time analytics
  - Campaign Generator
  - Traffic Leak Finder
  - Traffic Heatmap
  - Viral Content Finder
  - Email Sequence Builder
  - Content Calendar
  - Content Library
  - Competitor Tracker
  - Traffic Tips & Best Practices

## User Preferences

- Modern SaaS design with sidebar navigation
- Warm colors throughout the application (orange, yellow, coral)
- AJAX for all interactions (no full page reloads)
- Auto-registration with password for seamless and secure onboarding
- Responsive design with mobile toggle menu
- Clean, intuitive interface with icon-based navigation

## Project Architecture

### Tech Stack
- **Backend**: Python 3.11, Flask, Flask-SQLAlchemy, Flask-WTF (CSRF protection)
- **AI/ML**: Google Gemini 2.5 Flash (latest stable model)
- **Web Scraping**: BeautifulSoup4, lxml, requests (real data extraction from Reddit, web search)
- **Frontend**: HTML, CSS, Vanilla JavaScript (AJAX)
- **Database**: SQLite
- **Security**: 
  - Password hashing with Werkzeug
  - CSRF protection on all POST endpoints
  - Secure session cookies (SameSite=Lax, HttpOnly)
  - Session management with secure secret key

### File Structure
```
.
├── app.py                 # Main Flask application with models and routes
├── web_scraper.py         # Web scraping module for real data extraction
├── cache_helper.py        # Caching system for performance optimization
├── template_generator.py  # Fallback template generator
├── templates/
│   ├── login.html        # Login page with secure auto-registration
│   └── dashboard.html    # Modern SaaS dashboard with sidebar & 10 features
├── static/
│   ├── style.css         # Modern SaaS styling with warm colors
│   └── script.js         # AJAX functionality & navigation
├── cache/                # Cache directory for scraped data (auto-created)
├── instance/
│   └── traffic_ai.db     # SQLite database (auto-created)
└── replit.md             # This file
```

### Database Schema

**User**
- id, email (unique), name, password_hash, created_at
- Password methods: set_password(), check_password()
- Relationships: campaigns, traffic_sources, analytics

**Campaign**
- id, user_id, name, niche, platform, status, created_at

**TrafficSource**
- id, user_id, platform, source_name, niche, potential_reach, created_at

**Analytics**
- id, user_id, platform, clicks, date, created_at

### Key Features

1. **Secure Auto-Registration Login**: Users enter email and password (min 6 chars)
   - New users: automatically creates account with hashed password
   - Existing users: verifies password before granting access
   - All passwords securely hashed using Werkzeug
2. **Campaign Generator**: AI-powered campaign creation with niche and platform targeting
3. **Traffic Leak Finder**: Discovers untapped traffic sources across platforms
4. **Traffic Heatmap**: Visual analytics showing traffic distribution
5. **Stats Dashboard**: Real-time metrics (campaigns, sources, clicks, conversion rate)

## Development

The application runs on port 5000 in debug mode. All features use AJAX to provide a smooth, no-reload user experience.

### Environment Variables
- `SESSION_SECRET`: Flask session secret (auto-generated if not provided)

## Security Features

- **Password Authentication**: All accounts require passwords (minimum 6 characters)
- **Password Hashing**: Werkzeug's secure password hashing (never stores plain text)
- **CSRF Protection**: All POST endpoints protected with CSRF tokens
- **Secure Sessions**: HttpOnly and SameSite cookies prevent XSS and CSRF attacks
- **Input Validation**: Email and password validation on both client and server side

## Notes

- All user interactions use AJAX for seamless experience
- Warm color palette: #FF6B35 (primary), #F7931E (secondary), #FDC830 (accent)
- Auto-registration with password eliminates signup friction while maintaining security
- Responsive design for mobile and desktop
- CSRF tokens automatically fetched and included in all state-changing requests
