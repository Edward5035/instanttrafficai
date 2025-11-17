import os
from groq import Groq
import json
import time

api_key = os.environ.get('app_api') or os.environ.get('GROQ_API_KEY')
client = None

def get_client():
    """Get or create Groq client"""
    global client
    if client is None:
        if not api_key:
            raise Exception("GROQ_API_KEY not set. Please add your API key in Secrets.")
        client = Groq(api_key=api_key)
    return client

def call_groq_with_retry(model, messages, temperature, max_tokens, max_retries=3):
    """Call Groq API with retry logic for rate limits"""
    groq_client = get_client()
    for attempt in range(max_retries):
        try:
            response = groq_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"Rate limit hit, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise e
    return None

def generate_campaign(niche, platform='all'):
    """Generate a complete marketing campaign using Groq AI with web search"""
    
    prompt = f"""You are a marketing expert. Generate a comprehensive traffic campaign for the niche: {niche}.

Use web search to find:
1. Current trends in the {niche} industry
2. Popular keywords people are searching for
3. What content is performing well
4. Active communities and platforms

Then create:

1. 10 SEO-optimized blog post titles with:
   - Compelling title
   - 3-5 relevant keywords (use real search data)
   - 4 H2 section suggestions

2. 30 social media posts (10 for Facebook, 10 for Twitter, 10 for LinkedIn):
   - Each must be unique and engaging
   - Include relevant hashtags
   - Use current trends from your search

3. 5 email sequences (Lead Generation, Sales, Nurture, Webinar, Re-engagement):
   - Each sequence has 5 emails
   - Include subject lines with high open rate potential
   - Brief email preview text

4. 3 landing page variations:
   - Compelling headline
   - Subheadline
   - Call-to-action

5. 20 profitable keywords with:
   - Keyword phrase
   - Estimated search volume range
   - Competition level (Low/Medium/High)
   - Trend (Rising/Stable/Declining)

Return ONLY valid JSON in this exact format:
{{
    "blog_posts": [
        {{"title": "", "keywords": "", "h2_sections": ["", "", "", ""]}}
    ],
    "social_posts": {{
        "facebook": ["post1", "post2", ...],
        "twitter": ["post1", "post2", ...],
        "linkedin": ["post1", "post2", ...]
    }},
    "email_sequences": [
        {{
            "name": "",
            "goal": "",
            "emails": [
                {{"subject": "", "preview": ""}}
            ]
        }}
    ],
    "landing_pages": [
        {{"name": "", "headline": "", "subheadline": "", "cta": ""}}
    ],
    "keywords": [
        {{"keyword": "", "volume": "", "competition": "", "trend": ""}}
    ]
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=4000
        )
        
        if not response:
            return None
            
        content = response.choices[0].message.content
        
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return None
            
    except Exception as e:
        print(f"Error generating campaign: {str(e)}")
        return None


def find_traffic_leaks(niche, competitor_url=None):
    """Find traffic sources and opportunities using web search"""
    
    if competitor_url:
        prompt = f"""Analyze the competitor URL: {competitor_url} in the {niche} niche.

Use web search and browser automation to:
1. Visit their website and analyze their content strategy
2. Find where they're getting traffic from
3. Discover communities they're active in
4. Identify their backlink sources

Return real, actionable traffic sources in JSON format:
{{
    "leaks": [
        {{
            "platform": "",
            "source": "",
            "members": "",
            "engagement": "High/Medium/Low",
            "opportunity": ""
        }}
    ]
}}"""
    else:
        prompt = f"""Search the web for the best traffic sources in the {niche} niche.

Find:
1. Active forums and communities
2. Popular Facebook groups
3. Relevant subreddits
4. YouTube channels accepting collaborations
5. Guest post opportunities

Return at least 8 real traffic sources in JSON format:
{{
    "leaks": [
        {{
            "platform": "",
            "source": "",
            "members": "",
            "engagement": "High/Medium/Low",
            "opportunity": ""
        }}
    ]
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return {"leaks": []}
            
    except Exception as e:
        print(f"Error finding traffic leaks: {str(e)}")
        return {"leaks": []}


def find_viral_content(niche):
    """Find trending/viral content in a niche using web search"""
    
    prompt = f"""Search the web for the top trending and viral content in the {niche} niche RIGHT NOW.

Find:
1. Viral blog posts with high engagement
2. Trending social media posts
3. Popular YouTube videos
4. Hot Reddit discussions
5. Trending topics on Twitter/X

For each piece of content, include:
- Title/headline
- Platform
- Engagement metrics (likes, shares, comments, views)
- URL
- Why it's performing well

Return at least 10 trending pieces in JSON format:
{{
    "trending": [
        {{
            "title": "",
            "platform": "",
            "engagement": "",
            "url": "",
            "insight": ""
        }}
    ]
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return {"trending": []}
            
    except Exception as e:
        print(f"Error finding viral content: {str(e)}")
        return {"trending": []}


def analyze_competitor(competitor_url, niche):
    """Analyze competitor website and strategy"""
    
    prompt = f"""Use browser automation to visit and analyze: {competitor_url}

This is a {niche} website. Analyze:
1. Their content strategy and topics
2. Their top performing pages
3. Keywords they're ranking for
4. Their social media presence
5. Their traffic sources
6. Content gaps and opportunities

Return detailed analysis in JSON format:
{{
    "analysis": {{
        "top_content": ["topic1", "topic2", ...],
        "keywords": ["keyword1", "keyword2", ...],
        "social_platforms": ["platform1", "platform2", ...],
        "content_types": ["type1", "type2", ...],
        "opportunities": ["opp1", "opp2", ...],
        "traffic_estimate": "",
        "strengths": ["strength1", "strength2", ...],
        "weaknesses": ["weakness1", "weakness2", ...]
    }}
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return {"analysis": {}}
            
    except Exception as e:
        print(f"Error analyzing competitor: {str(e)}")
        return {"analysis": {}}


def generate_email_sequence(goal, niche, num_emails=5):
    """Generate personalized email sequence"""
    
    prompt = f"""Create a {num_emails}-email sequence for {goal} in the {niche} niche.

Each email should have:
- Compelling subject line (optimized for high open rates)
- Preview text
- Brief outline of email body

Make it unique and tailored to the {niche} audience.

Return JSON format:
{{
    "sequence": {{
        "name": "{goal}",
        "emails": [
            {{
                "number": 1,
                "subject": "",
                "preview": "",
                "outline": ""
            }}
        ]
    }}
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return {"sequence": {"emails": []}}
            
    except Exception as e:
        print(f"Error generating email sequence: {str(e)}")
        return {"sequence": {"emails": []}}


def get_traffic_heatmap_data(niche):
    """Get traffic opportunity data for heatmap visualization"""
    
    prompt = f"""Search the web for traffic opportunity data in the {niche} niche.

Analyze the following platforms and rate their opportunity level (0-100 score):
- Facebook
- Instagram
- Twitter/X
- LinkedIn
- Reddit
- YouTube
- Pinterest
- TikTok
- Quora
- Medium

Consider:
- Audience size in this niche
- Engagement levels
- Competition level (lower competition = higher opportunity)
- Current trends

Return JSON:
{{
    "heatmap": {{
        "Facebook": 0-100,
        "Instagram": 0-100,
        ...
    }}
}}"""

    try:
        response = call_groq_with_retry(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_content = content[start_idx:end_idx]
            return json.loads(json_content)
        else:
            return {"heatmap": {}}
            
    except Exception as e:
        print(f"Error getting heatmap data: {str(e)}")
        return {"heatmap": {}}
