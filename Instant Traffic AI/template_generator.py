import random
from datetime import datetime

def generate_campaign(niche, platform='all'):
    """Generate marketing campaign using smart templates"""
    
    niche_title = niche.title()
    niche_lower = niche.lower()
    year = datetime.now().year
    
    platform_names = {
        'facebook': 'Facebook', 'instagram': 'Instagram', 'twitter': 'Twitter',
        'linkedin': 'LinkedIn', 'youtube': 'YouTube', 'pinterest': 'Pinterest',
        'tiktok': 'TikTok', 'reddit': 'Reddit', 'all': 'All Platforms'
    }
    platform_name = platform_names.get(platform.lower(), 'All Platforms')
    
    numbers = ["5", "7", "10", "12", "15"]
    timeframes = ["30 Days", "60 Days", "90 Days", "6 Months"]
    actions = ["Strategies", "Techniques", "Methods", "Tactics", "Hacks"]
    
    blog_posts = []
    for i in range(10):
        num = random.choice(numbers)
        action = random.choice(actions)
        time = random.choice(timeframes)
        
        titles = [
            f"{num} Proven {niche_title} {action} for {platform_name} That Work in {year}",
            f"The Ultimate {niche_title} Guide for {platform_name} ({year} Edition)",
            f"How to Master {niche_title} in {time} (Step-by-Step)",
            f"{niche_title} Success Stories: Real Results from Real People",
            f"{num} {niche_title} Hacks That Will Transform Your Results",
            f"The Future of {niche_title}: Trends to Watch in {year + 1}",
            f"{niche_title} vs Traditional Methods: Which is Better?",
            f"Stop Wasting Money: The {niche_title} ROI Guide",
            f"From Zero to Hero: My {niche_title} Journey",
            f"The {niche_title} Checklist: Never Miss a Step Again"
        ]
        
        title = titles[i] if i < len(titles) else random.choice(titles)
        
        blog_posts.append({
            "title": title,
            "keywords": f"{niche_lower}, {niche_lower} tips, best {niche_lower}, {niche_lower} guide",
            "h2_sections": [
                f"Why {niche_title} Matters in {year}",
                f"Top {niche_title} Mistakes to Avoid",
                f"Advanced {niche_title} Techniques",
                f"Measuring Your {niche_title} Success"
            ]
        })
    
    # Generate social posts
    fb_posts = [
        f"Want to dominate {niche_lower}? Here is the secret... #{niche.replace(' ', '')}{year}",
        f"Just discovered a game-changing {niche_lower} strategy! #{niche.replace(' ', '')}Tips",
        f"Stop struggling with {niche_lower}. Try this simple hack! #{niche.replace(' ', '')}Hacks",
        f"Your {niche_lower} results not what you expected? Here is why... #{niche.replace(' ', '')}",
        f"The future of {niche_lower} is here and it is incredible! #{niche.replace(' ', '')}{year}",
        f"From beginner to expert: My {niche_lower} transformation #{niche.replace(' ', '')}Journey",
        f"These {niche_lower} mistakes cost me thousands. Learn from them! #{niche.replace(' ', '')}",
        f"The ultimate {niche_lower} guide is finally here! #{niche.replace(' ', '')}Guide",
        f"Unlock your {niche_lower} potential with these strategies #{niche.replace(' ', '')}Success",
        f"Real {niche_lower} results: See what is possible! #{niche.replace(' ', '')}Results"
    ]
    
    tw_posts = [
        f"{niche_title} tip: Focus on quality over quantity. #{niche.replace(' ', '')}",
        f"Your {niche_lower} strategy should adapt every quarter. #{niche.replace(' ', '')}Tips",
        f"Hot take: Most {niche_lower} advice is outdated. Here is what works in {year}",
        f"The 3 pillars of successful {niche_lower}: Strategy, Execution, Measurement",
        f"Stop copying competitors. Start innovating in {niche_lower}",
        f"Just analyzed 100 {niche_lower} campaigns. Here is what winners do",
        f"Your {niche_lower} ROI will thank you for this. Bookmark it",
        f"The {niche_lower} landscape changed. Here is how to adapt",
        f"Myth: {niche_title} is expensive. Reality: It pays off",
        f"New to {niche_lower}? Start here. This is the only roadmap you need"
    ]
    
    li_posts = [
        f"After 5 years in {niche_lower}, here are 5 lessons that transformed my approach",
        f"Companies investing in {niche_lower} see 3x better results. Here is the data",
        f"Industry insight: The {niche_lower} market is shifting. Are you prepared?",
        f"How we increased our {niche_lower} ROI by 200% in 6 months",
        f"The future of {niche_lower} is collaborative, not competitive",
        f"5 {niche_lower} metrics every executive should track in {year}",
        f"Lessons from leading {niche_lower} transformations at Fortune 500 companies",
        f"Why traditional {niche_lower} approaches are failing and what to do instead",
        f"The ROI conversation around {niche_lower} needs to change",
        f"Building a world-class {niche_lower} team: What we learned"
    ]
    
    all_social_posts = {
        "facebook": fb_posts,
        "twitter": tw_posts,
        "linkedin": li_posts
    }
    
    if platform.lower() in ['facebook', 'instagram', 'twitter', 'linkedin']:
        key = 'twitter' if platform.lower() in ['twitter', 'x'] else platform.lower()
        if key in all_social_posts:
            posts = all_social_posts[key] * 3
            social_posts = {key: posts[:30]}
        else:
            social_posts = all_social_posts
    else:
        social_posts = all_social_posts
    
    email_sequences = [
        {
            "name": "Lead Generation",
            "goal": "Convert visitors into qualified leads",
            "emails": [
                {"subject": f"The {niche_title} Secret Nobody Talks About", "preview": f"Discover the overlooked {niche_lower} strategy"},
                {"subject": f"Your Free {niche_title} Starter Kit is Ready", "preview": f"Everything you need to start with {niche_lower}"},
                {"subject": "Quick question about your goals", "preview": f"I would love to help with your {niche_lower} journey"},
                {"subject": f"[Case Study] How Sarah tripled her {niche_title} results", "preview": "Real results from someone like you"},
                {"subject": "Last chance to claim your spot", "preview": f"Limited seats for our {niche_lower} workshop"}
            ]
        },
        {
            "name": "Sales",
            "goal": "Convert leads into customers",
            "emails": [
                {"subject": f"Why {niche_title} is not working for you (yet)", "preview": f"The missing piece in your {niche_lower} strategy"},
                {"subject": f"Special offer: {niche_title} Mastery Program", "preview": "40% off for the next 48 hours only"},
                {"subject": "What our students are saying", "preview": f"Real {niche_lower} transformations"},
                {"subject": "Still on the fence? Read this", "preview": f"Your {niche_lower} questions answered"},
                {"subject": "Final call: Offer expires tonight", "preview": "Last chance to join"}
            ]
        }
    ]
    
    landing_pages = [
        {
            "name": "Lead Magnet",
            "headline": f"Get Your Free {niche_title} Toolkit",
            "subheadline": f"Everything you need to start succeeding with {niche_lower} today",
            "cta": "Download Free Toolkit"
        },
        {
            "name": "Sales Page",
            "headline": f"Master {niche_title} in 30 Days or Get Your Money Back",
            "subheadline": f"Join 10,000+ students who transformed their {niche_lower} results",
            "cta": "Enroll Now - Special Offer"
        },
        {
            "name": "Webinar",
            "headline": f"Free Workshop: The {niche_title} Blueprint for {year}",
            "subheadline": f"Learn the system to achieve {niche_lower} success",
            "cta": "Save My Spot (Free)"
        }
    ]
    
    keywords = [
        {"keyword": f"{niche_lower}", "volume": "10K-100K", "competition": "High", "trend": "Stable"},
        {"keyword": f"{niche_lower} tips", "volume": "5K-50K", "competition": "Medium", "trend": "Rising"},
        {"keyword": f"{niche_lower} for beginners", "volume": "1K-10K", "competition": "Low", "trend": "Rising"},
        {"keyword": f"best {niche_lower}", "volume": "5K-50K", "competition": "High", "trend": "Stable"},
        {"keyword": f"{niche_lower} guide", "volume": "1K-10K", "competition": "Medium", "trend": "Stable"},
        {"keyword": f"how to {niche_lower}", "volume": "10K-100K", "competition": "High", "trend": "Stable"},
        {"keyword": f"{niche_lower} strategies", "volume": "1K-10K", "competition": "Medium", "trend": "Rising"},
        {"keyword": f"{niche_lower} tutorial", "volume": "1K-10K", "competition": "Low", "trend": "Rising"},
        {"keyword": f"{niche_lower} course", "volume": "500-5K", "competition": "High", "trend": "Rising"},
        {"keyword": f"learn {niche_lower}", "volume": "5K-50K", "competition": "Medium", "trend": "Stable"}
    ]
    
    return {
        "blog_posts": blog_posts,
        "social_posts": social_posts,
        "email_sequences": email_sequences,
        "landing_pages": landing_pages,
        "keywords": keywords
    }


def find_traffic_leaks(niche, competitor_url=None):
    platforms = ["Facebook", "Reddit", "LinkedIn", "YouTube", "Pinterest", "Twitter", "Quora", "Instagram"]
    random.shuffle(platforms)
    
    leaks = []
    for platform in platforms[:8]:
        engagement = random.choice(["High", "Medium", "Low"])
        members = random.choice(["500K+", "100K-500K", "10K-100K", "50K-100K"])
        
        source = f"{niche.title()} {platform} Community" if platform != "Reddit" else f"r/{niche.replace(' ', '')}"
        
        leaks.append({
            "platform": platform,
            "source": source,
            "members": members,
            "engagement": engagement,
            "opportunity": f"Active {niche.lower()} discussions with {engagement.lower()} engagement rate"
        })
    
    return {"leaks": leaks}


def find_viral_content(niche):
    content_types = ["Blog Post", "Video", "Infographic", "Social Post", "Podcast"]
    
    trending = []
    for i in range(10):
        content_type = random.choice(content_types)
        engagement = random.randint(1000, 50000)
        
        trending.append({
            "title": f"{random.choice(['How to', 'The Ultimate Guide to', '10 Ways to'])} {niche.title()}",
            "platform": random.choice(["LinkedIn", "Medium", "YouTube", "Twitter", "Facebook"]),
            "engagement": f"{engagement:,} {random.choice(['views', 'shares'])}",
            "url": f"https://example.com/{niche.replace(' ', '-')}-{i+1}",
            "insight": f"Viral {content_type.lower()} focusing on {niche.lower()} best practices"
        })
    
    return {"trending": trending}


def analyze_competitor(competitor_url, niche):
    analysis = {
        "top_content": [
            f"{niche.title()} How-To Guides",
            f"{niche.title()} Case Studies",
            f"{niche.title()} Templates",
            f"{niche.title()} Best Practices",
            f"{niche.title()} Industry News"
        ],
        "keywords": [f"{niche.lower()}", f"{niche.lower()} guide", f"best {niche.lower()}"],
        "social_platforms": ["Facebook", "Twitter", "LinkedIn", "Instagram", "YouTube"],
        "content_types": ["Blog posts", "Videos", "Infographics", "Ebooks"],
        "opportunities": [
            f"Create more video content about {niche.lower()}",
            f"Target long-tail {niche.lower()} keywords",
            f"Build interactive {niche.lower()} tools"
        ],
        "traffic_estimate": "100K-500K monthly visits",
        "strengths": ["Consistent publishing", "Strong social presence", "Good SEO"],
        "weaknesses": ["Limited video content", "Slow site speed"]
    }
    
    return {"analysis": analysis}


def generate_email_sequence(goal, niche, num_emails=5):
    emails = []
    for i in range(num_emails):
        emails.append({
            "number": i + 1,
            "subject": f"Day {i+1}: {niche.title()} Strategy #{i+1}",
            "preview": f"Today: How to improve your {niche.lower()} results",
            "outline": f"Introduction | Main strategy | Examples | Call to action"
        })
    
    return {"sequence": {"name": goal, "emails": emails}}


def get_traffic_heatmap_data(niche):
    platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "Reddit", "YouTube", "Pinterest", "TikTok", "Quora", "Medium"]
    
    heatmap = {}
    for platform in platforms:
        heatmap[platform] = random.randint(35, 95)
    
    return {"heatmap": heatmap}
