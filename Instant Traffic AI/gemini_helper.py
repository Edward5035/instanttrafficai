import os
from google import genai
from google.genai import types
import json
import time
import re

# IMPORTANT: Using python_gemini blueprint for Google Gemini integration
# Using gemini-2.5-flash model (latest stable version) for fast, reliable responses

api_key = os.environ.get('GEMINI_API_KEY')
client = None

def clean_and_parse_json(content):
    """Clean and parse JSON from Gemini response, handling common issues"""
    if not content:
        return None
    
    # Try direct JSON parsing first
    try:
        return json.loads(content)
    except:
        pass
    
    # Extract JSON from markdown code blocks
    json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except:
            pass
    
    # Find JSON object boundaries
    start_idx = content.find('{')
    end_idx = content.rfind('}') + 1
    if start_idx != -1 and end_idx != 0:
        json_str = content[start_idx:end_idx]
        
        # Try parsing cleaned string
        try:
            return json.loads(json_str)
        except:
            pass
        
        # Fix common JSON issues: trailing commas
        try:
            # Remove trailing commas before closing braces/brackets
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            return json.loads(json_str)
        except:
            pass
    
    return None

def get_client():
    """Get or create Gemini client"""
    global client
    if client is None:
        if not api_key:
            raise Exception("GEMINI_API_KEY not set. Please add your API key in Secrets.")
        client = genai.Client(api_key=api_key)
    return client

def call_gemini_with_retry(prompt, temperature=0.8, max_tokens=4000, max_retries=3):
    """Call Gemini API with retry logic and fallback models"""
    gemini_client = get_client()
    
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        for attempt in range(max_retries):
            try:
                response = gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                        response_mime_type="application/json"
                    )
                )
                if attempt > 0 or model_name != "gemini-2.5-flash":
                    print(f"✓ Successfully used {model_name} (attempt {attempt + 1})")
                return response
            except Exception as e:
                error_msg = str(e)
                is_retryable = any(keyword in error_msg.lower() for keyword in 
                                  ["quota", "rate", "503", "overloaded", "unavailable", "429"])
                
                if is_retryable and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"⚠ {model_name} error (attempt {attempt + 1}/{max_retries}): {error_msg[:100]}...")
                    print(f"   Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                elif model_name == models_to_try[-1]:
                    print(f"✗ All models failed. Last error: {error_msg}")
                    raise e
                else:
                    print(f"✗ {model_name} failed after {attempt + 1} attempts, trying fallback model...")
                    break
    
    return None

def generate_campaign(niche, platform='all'):
    """Generate a complete marketing campaign using Gemini AI with web search"""
    
    prompt = f"""You are a marketing expert. Generate a comprehensive traffic campaign for the niche: {niche}.

Search the web and find:
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
        response = call_gemini_with_retry(prompt, temperature=0.8, max_tokens=4000)
        
        if not response or not response.text:
            return None
        
        return clean_and_parse_json(response.text)
            
    except Exception as e:
        print(f"Error generating campaign: {str(e)}")
        return None


def find_traffic_leaks(niche, competitor_url=None):
    """Find traffic sources and opportunities using web search"""
    
    if competitor_url:
        prompt = f"""Analyze the competitor URL: {competitor_url} in the {niche} niche.

Search the web to:
1. Find information about their content strategy
2. Discover where they're getting traffic from
3. Identify communities they're active in
4. Find their backlink sources

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
        response = call_gemini_with_retry(prompt, temperature=0.7, max_tokens=2000)
        
        if not response or not response.text:
            return {"leaks": []}
            
        result = clean_and_parse_json(response.text)
        return result if result else {"leaks": []}
            
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
        response = call_gemini_with_retry(prompt, temperature=0.7, max_tokens=2500)
        
        if not response or not response.text:
            return {"trending": []}
            
        result = clean_and_parse_json(response.text)
        return result if result else {"trending": []}
            
    except Exception as e:
        print(f"Error finding viral content: {str(e)}")
        return {"trending": []}


def analyze_competitor(competitor_url, niche):
    """Analyze competitor website and strategy"""
    
    prompt = f"""Search the web for information about: {competitor_url}

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
        response = call_gemini_with_retry(prompt, temperature=0.7, max_tokens=2000)
        
        if not response or not response.text:
            return {"analysis": {}}
            
        result = clean_and_parse_json(response.text)
        return result if result else {"analysis": {}}
            
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
        response = call_gemini_with_retry(prompt, temperature=0.8, max_tokens=1500)
        
        if not response or not response.text:
            return {"sequence": {"emails": []}}
            
        result = clean_and_parse_json(response.text)
        return result if result else {"sequence": {"emails": []}}
            
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
        "Twitter": 0-100,
        "LinkedIn": 0-100,
        "Reddit": 0-100,
        "YouTube": 0-100,
        "Pinterest": 0-100,
        "TikTok": 0-100,
        "Quora": 0-100,
        "Medium": 0-100
    }}
}}"""

    try:
        response = call_gemini_with_retry(prompt, temperature=0.7, max_tokens=1000)
        
        if not response or not response.text:
            return {"heatmap": {}}
            
        result = clean_and_parse_json(response.text)
        return result if result else {"heatmap": {}}
            
    except Exception as e:
        print(f"Error getting heatmap data: {str(e)}")
        return {"heatmap": {}}
