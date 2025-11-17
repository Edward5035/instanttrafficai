import groq_helper
import json

def test_campaign_generator():
    print("\n" + "="*60)
    print("TEST 1: Campaign Generator")
    print("="*60)
    
    niche = "fitness"
    print(f"Testing campaign generation for niche: {niche}")
    
    result = groq_helper.generate_campaign(niche, "all")
    
    if result:
        print("✓ Campaign generated successfully!")
        print(f"  - Blog posts: {len(result.get('blog_posts', []))} found")
        print(f"  - Social posts (Facebook): {len(result.get('social_posts', {}).get('facebook', []))} found")
        print(f"  - Social posts (Twitter): {len(result.get('social_posts', {}).get('twitter', []))} found")
        print(f"  - Social posts (LinkedIn): {len(result.get('social_posts', {}).get('linkedin', []))} found")
        print(f"  - Email sequences: {len(result.get('email_sequences', []))} found")
        print(f"  - Landing pages: {len(result.get('landing_pages', []))} found")
        print(f"  - Keywords: {len(result.get('keywords', []))} found")
        
        if result.get('blog_posts'):
            print(f"\n  Sample Blog Post:")
            print(f"    Title: {result['blog_posts'][0].get('title', 'N/A')}")
            print(f"    Keywords: {result['blog_posts'][0].get('keywords', 'N/A')}")
        
        if result.get('keywords'):
            print(f"\n  Sample Keywords:")
            for i, kw in enumerate(result['keywords'][:3], 1):
                print(f"    {i}. {kw.get('keyword', 'N/A')} - Volume: {kw.get('volume', 'N/A')}, Competition: {kw.get('competition', 'N/A')}")
        
        return True
    else:
        print("✗ Campaign generation FAILED")
        return False

def test_traffic_leaks():
    print("\n" + "="*60)
    print("TEST 2: Traffic Leak Finder")
    print("="*60)
    
    niche = "affiliate marketing"
    print(f"Testing traffic leak finder for niche: {niche}")
    
    result = groq_helper.find_traffic_leaks(niche)
    
    if result and result.get('leaks'):
        print(f"✓ Found {len(result['leaks'])} traffic sources!")
        
        for i, leak in enumerate(result['leaks'][:5], 1):
            print(f"\n  {i}. {leak.get('platform', 'N/A')}")
            print(f"     Source: {leak.get('source', 'N/A')}")
            print(f"     Members: {leak.get('members', 'N/A')}")
            print(f"     Engagement: {leak.get('engagement', 'N/A')}")
        
        return True
    else:
        print("✗ Traffic leak finder FAILED")
        return False

def test_viral_content():
    print("\n" + "="*60)
    print("TEST 3: Viral Content Finder")
    print("="*60)
    
    niche = "productivity"
    print(f"Testing viral content finder for niche: {niche}")
    
    result = groq_helper.find_viral_content(niche)
    
    if result and result.get('trending'):
        print(f"✓ Found {len(result['trending'])} trending pieces!")
        
        for i, content in enumerate(result['trending'][:3], 1):
            print(f"\n  {i}. {content.get('title', 'N/A')}")
            print(f"     Platform: {content.get('platform', 'N/A')}")
            print(f"     Engagement: {content.get('engagement', 'N/A')}")
            print(f"     URL: {content.get('url', 'N/A')}")
        
        return True
    else:
        print("✗ Viral content finder FAILED")
        return False

def test_competitor_analysis():
    print("\n" + "="*60)
    print("TEST 4: Competitor Analyzer")
    print("="*60)
    
    competitor_url = "https://neilpatel.com"
    niche = "digital marketing"
    print(f"Testing competitor analysis for: {competitor_url}")
    
    result = groq_helper.analyze_competitor(competitor_url, niche)
    
    if result and result.get('analysis'):
        analysis = result['analysis']
        print("✓ Competitor analysis completed!")
        print(f"  - Top content topics: {len(analysis.get('top_content', []))} found")
        print(f"  - Keywords: {len(analysis.get('keywords', []))} found")
        print(f"  - Social platforms: {len(analysis.get('social_platforms', []))} found")
        print(f"  - Opportunities: {len(analysis.get('opportunities', []))} found")
        
        if analysis.get('top_content'):
            print(f"\n  Top Content Topics:")
            for topic in analysis['top_content'][:3]:
                print(f"    - {topic}")
        
        if analysis.get('opportunities'):
            print(f"\n  Opportunities:")
            for opp in analysis['opportunities'][:2]:
                print(f"    - {opp}")
        
        return True
    else:
        print("✗ Competitor analysis FAILED")
        return False

def test_email_sequence():
    print("\n" + "="*60)
    print("TEST 5: Email Sequence Generator")
    print("="*60)
    
    goal = "product launch"
    niche = "software"
    num_emails = 5
    print(f"Testing email sequence generation for: {goal}")
    
    result = groq_helper.generate_email_sequence(goal, niche, num_emails)
    
    if result and result.get('sequence'):
        sequence = result['sequence']
        emails = sequence.get('emails', [])
        print(f"✓ Generated {len(emails)} emails!")
        print(f"  Sequence Name: {sequence.get('name', 'N/A')}")
        
        for i, email in enumerate(emails[:3], 1):
            print(f"\n  Email {i}:")
            print(f"    Subject: {email.get('subject', 'N/A')}")
            print(f"    Preview: {email.get('preview', 'N/A')}")
        
        return True
    else:
        print("✗ Email sequence generation FAILED")
        return False

def test_heatmap():
    print("\n" + "="*60)
    print("TEST 6: Traffic Heatmap Generator")
    print("="*60)
    
    niche = "ecommerce"
    print(f"Testing heatmap generation for niche: {niche}")
    
    result = groq_helper.get_traffic_heatmap_data(niche)
    
    if result and result.get('heatmap'):
        heatmap = result['heatmap']
        print(f"✓ Heatmap data generated!")
        
        sorted_platforms = sorted(heatmap.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n  Platform Opportunity Scores:")
        for platform, score in sorted_platforms:
            bar = "█" * (score // 10)
            print(f"    {platform:12} [{score:3}] {bar}")
        
        return True
    else:
        print("✗ Heatmap generation FAILED")
        return False

def main():
    print("\n" + "="*60)
    print("INSTANT TRAFFIC AI - FEATURE TESTING SUITE")
    print("="*60)
    print("\nTesting all Groq AI-powered features...\n")
    
    results = {
        "Campaign Generator": test_campaign_generator(),
        "Traffic Leak Finder": test_traffic_leaks(),
        "Viral Content Finder": test_viral_content(),
        "Competitor Analyzer": test_competitor_analysis(),
        "Email Sequence Generator": test_email_sequence(),
        "Traffic Heatmap": test_heatmap()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for feature, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{feature:30} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL FEATURES WORKING PERFECTLY!")
    else:
        print(f"\n⚠️  {total - passed} feature(s) need attention")

if __name__ == "__main__":
    main()
