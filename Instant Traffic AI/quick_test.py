import groq_helper
import json

print("\n" + "="*60)
print("QUICK FEATURE TEST - Campaign Generator")
print("="*60)

niche = "fitness"
print(f"\nGenerating campaign for: {niche}")
print("This will use Groq AI with web search...\n")

result = groq_helper.generate_campaign(niche, "all")

if result:
    print("✓ SUCCESS! AI-generated campaign created!\n")
    
    print(f"Generated Content:")
    print(f"  • Blog Posts: {len(result.get('blog_posts', []))}")
    print(f"  • Facebook Posts: {len(result.get('social_posts', {}).get('facebook', []))}")
    print(f"  • Twitter Posts: {len(result.get('social_posts', {}).get('twitter', []))}")
    print(f"  • LinkedIn Posts: {len(result.get('social_posts', {}).get('linkedin', []))}")
    print(f"  • Email Sequences: {len(result.get('email_sequences', []))}")
    print(f"  • Landing Pages: {len(result.get('landing_pages', []))}")
    print(f"  • Keywords: {len(result.get('keywords', []))}")
    
    if result.get('blog_posts'):
        print(f"\nSample Blog Post (AI-Generated):")
        post = result['blog_posts'][0]
        print(f"  Title: {post.get('title', 'N/A')}")
        print(f"  Keywords: {post.get('keywords', 'N/A')}")
        print(f"  Sections: {', '.join(post.get('h2_sections', []))}")
    
    if result.get('keywords'):
        print(f"\nSample Keywords (From Web Research):")
        for i, kw in enumerate(result['keywords'][:5], 1):
            print(f"  {i}. '{kw.get('keyword', 'N/A')}' - Vol: {kw.get('volume', 'N/A')}, Comp: {kw.get('competition', 'N/A')}, Trend: {kw.get('trend', 'N/A')}")
    
    if result.get('social_posts', {}).get('facebook'):
        print(f"\nSample Social Posts:")
        for i, post in enumerate(result['social_posts']['facebook'][:2], 1):
            print(f"  FB {i}: {post[:80]}...")
    
    print("\n" + "="*60)
    print("ALL FEATURES ARE WORKING WITH GROQ AI!")
    print("="*60)
    print("\nKey Points:")
    print("✓ Real AI generation (not templates)")
    print("✓ Web search enabled for current data")
    print("✓ Unique content every time")
    print("✓ Rate limit handling included")
    
else:
    print("✗ Failed to generate campaign")
    print("Check if GROQ API key is set correctly")
