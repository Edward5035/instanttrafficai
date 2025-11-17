let csrfToken = null;

async function getCSRFToken() {
    if (csrfToken) return csrfToken;
    try {
        const response = await fetch('/api/csrf-token');
        const data = await response.json();
        csrfToken = data.csrf_token;
        return csrfToken;
    } catch (error) {
        console.error('Error getting CSRF token:', error);
        return null;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await getCSRFToken();
    loadStats();
    setupNavigation();
    setupMobileMenu();
    setupProfileDropdown();
    loadRecentCampaigns();
    setUserName();
});

function setUserName() {
    const userName = sessionStorage.getItem('user_name') || 'User';
    const username = sessionStorage.getItem('username') || 'user';
    
    const profileName = document.getElementById('profileName');
    const profileMenuName = document.getElementById('profileMenuName');
    const profileMenuUsername = document.getElementById('profileMenuUsername');
    
    if (profileName) profileName.textContent = userName;
    if (profileMenuName) profileMenuName.textContent = userName;
    if (profileMenuUsername) profileMenuUsername.textContent = '@' + username;
}

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const pageNames = {
        'dashboard': 'Dashboard',
        'campaign': 'Campaign Generator',
        'leaks': 'Traffic Leak Finder',
        'heatmap': 'Traffic Heatmap',
        'viral': 'Viral Content Finder',
        'email': 'Email Sequences',
        'calendar': 'Content Calendar',
        'library': 'Content Library',
        'competitors': 'Competitor Tracker',
        'tips': 'Pro Tips'
    };
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = item.getAttribute('data-page');
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            const pages = document.querySelectorAll('.page');
            pages.forEach(page => page.classList.remove('active'));
            
            const targetPage = document.getElementById(pageName + 'Page');
            if (targetPage) {
                targetPage.classList.add('active');
            }
            
            const breadcrumb = document.getElementById('currentPageName');
            if (breadcrumb && pageNames[pageName]) {
                breadcrumb.textContent = pageNames[pageName];
            }
            
            if (window.innerWidth <= 1024) {
                document.getElementById('sidebar').classList.remove('active');
            }
            
            if (pageName === 'dashboard') {
                loadStats();
                loadRecentCampaigns();
            } else if (pageName === 'heatmap') {
                loadHeatmap();
            }
        });
    });
}

function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
    
    closeSidebar.addEventListener('click', () => {
        sidebar.classList.remove('active');
    });
}

function setupProfileDropdown() {
    const profileBtn = document.getElementById('profileBtn');
    const profileMenu = document.getElementById('profileMenu');
    
    profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileMenu.classList.toggle('active');
    });
    
    document.addEventListener('click', (e) => {
        if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
            profileMenu.classList.remove('active');
        }
    });
}

function showSettings(e) {
    e.preventDefault();
    alert('Settings functionality coming soon! This will allow you to update your profile information and change your password.');
    document.getElementById('profileMenu').classList.remove('active');
}

async function loadStats() {
    try {
        const response = await fetch('/api/analytics/stats');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('statCampaigns').textContent = data.stats.campaigns;
            document.getElementById('statSources').textContent = data.stats.traffic_sources;
            document.getElementById('statClicks').textContent = data.stats.total_clicks;
            document.getElementById('statConversion').textContent = data.stats.conversion_rate;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadRecentCampaigns() {
    const resultBox = document.getElementById('recentCampaigns');
    resultBox.innerHTML = '<div class="loading">Loading recent campaigns...</div>';
    resultBox.classList.add('show');
    
    try {
        const response = await fetch('/api/campaigns');
        const data = await response.json();
        
        if (data.success) {
            if (data.campaigns.length === 0) {
                resultBox.innerHTML = '<p style="text-align: center; color: #666;">No campaigns yet. Create your first one!</p>';
            } else {
                const recentCampaigns = data.campaigns.slice(0, 3);
                let html = '';
                
                recentCampaigns.forEach(campaign => {
                    html += `
                        <div class="campaign-item">
                            <h4>${campaign.name}</h4>
                            <div class="campaign-meta">
                                <span>Niche: ${campaign.niche}</span> | 
                                <span>Platform: ${campaign.platform}</span> | 
                                <span>Created: ${campaign.created_at}</span>
                            </div>
                        </div>
                    `;
                });
                
                resultBox.innerHTML = html;
            }
        } else {
            resultBox.innerHTML = `<div class="message error">${data.message}</div>`;
        }
    } catch (error) {
        resultBox.innerHTML = '<div class="message error">An error occurred. Please try again.</div>';
    }
}

document.getElementById('campaignForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const niche = document.getElementById('campaignNiche').value;
    const platform = document.getElementById('campaignPlatform').value;
    const resultBox = document.getElementById('campaignResult');
    
    resultBox.innerHTML = '<div class="loading">Generating your campaign...</div>';
    resultBox.classList.add('show');
    
    try {
        const token = await getCSRFToken();
        const response = await fetch('/api/campaigns/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({ niche, platform })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const campaign = data.campaign;
            let html = `
                <h3 style="color: var(--success); margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                    <i class="ph ph-check-circle"></i> Campaign Generated in 60 Seconds: ${campaign.name}
                </h3>
                
                <div style="background: linear-gradient(135deg, rgba(39, 174, 96, 0.1), rgba(34, 153, 84, 0.1)); padding: 20px; border-radius: 12px; margin-bottom: 24px; border: 2px solid var(--success);">
                    <h4 style="color: var(--success); margin-bottom: 12px;"><i class="ph ph-sparkle"></i> Complete Asset Inventory Generated:</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                        <div><i class="ph ph-article"></i> <strong>10</strong> Blog Post Outlines</div>
                        <div><i class="ph ph-share-network"></i> <strong>30</strong> Social Media Posts</div>
                        <div><i class="ph ph-envelope"></i> <strong>5</strong> Email Sequences</div>
                        <div><i class="ph ph-browsers"></i> <strong>3</strong> Landing Pages</div>
                        <div><i class="ph ph-key"></i> <strong>20</strong> Keywords</div>
                    </div>
                </div>
                
                <h4 style="color: var(--primary); margin: 24px 0 12px;"><i class="ph ph-article"></i> 10 SEO-Optimized Blog Posts</h4>
                <div style="display: grid; gap: 12px;">
            `;
            
            campaign.blog_posts.forEach((post, i) => {
                html += `
                    <div style="background: white; padding: 16px; border-radius: 10px; border-left: 4px solid var(--primary); box-shadow: var(--shadow-sm);">
                        <strong>${i + 1}. ${post.title}</strong>
                        <div style="margin-top: 8px; color: var(--text-muted); font-size: 0.9rem;">
                            <div><strong>Keywords:</strong> ${post.keywords}</div>
                            <div><strong>H2 Sections:</strong> ${post.h2_sections.join(' • ')}</div>
                        </div>
                    </div>
                `;
            });
            
            html += `
                </div>
                
                <h4 style="color: var(--primary); margin: 24px 0 12px;"><i class="ph ph-share-network"></i> 30 Social Media Posts</h4>
                
                <div style="margin-bottom: 16px;">
                    <h5 style="color: var(--secondary);">Facebook (10 posts)</h5>
                    <div style="display: grid; gap: 8px; margin-top: 8px;">
            `;
            
            campaign.social_posts.facebook.forEach(post => {
                html += `<div style="background: #f0f2f5; padding: 12px; border-radius: 8px; font-size: 0.95rem;">${post}</div>`;
            });
            
            html += `
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <h5 style="color: var(--secondary);">Twitter (10 posts)</h5>
                    <div style="display: grid; gap: 8px; margin-top: 8px;">
            `;
            
            campaign.social_posts.twitter.forEach(post => {
                html += `<div style="background: #e8f5fe; padding: 12px; border-radius: 8px; font-size: 0.95rem;">${post}</div>`;
            });
            
            html += `
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <h5 style="color: var(--secondary);">LinkedIn (10 posts)</h5>
                    <div style="display: grid; gap: 8px; margin-top: 8px;">
            `;
            
            campaign.social_posts.linkedin.forEach(post => {
                html += `<div style="background: #e7f3ff; padding: 12px; border-radius: 8px; font-size: 0.95rem;">${post}</div>`;
            });
            
            html += `
                    </div>
                </div>
                
                <h4 style="color: var(--primary); margin: 24px 0 12px;"><i class="ph ph-envelope"></i> 5 Email Sequences (25 Total Emails)</h4>
                <div style="display: grid; gap: 12px;">
            `;
            
            campaign.email_sequences.forEach((seq, i) => {
                html += `
                    <div style="background: white; padding: 16px; border-radius: 10px; border-left: 4px solid var(--secondary); box-shadow: var(--shadow-sm);">
                        <strong>${i + 1}. ${seq.name}</strong> (${seq.emails.length} emails)
                        <div style="margin-top: 8px; color: var(--text-muted); font-size: 0.9rem;">
                            <div><strong>Goal:</strong> ${seq.goal}</div>
                            <div style="margin-top: 8px;"><strong>Emails:</strong></div>
                            <ul style="margin: 8px 0 0 20px;">
                `;
                seq.emails.forEach(email => {
                    html += `<li>${email.subject} - ${email.preview}</li>`;
                });
                html += `
                            </ul>
                        </div>
                    </div>
                `;
            });
            
            html += `
                </div>
                
                <h4 style="color: var(--primary); margin: 24px 0 12px;"><i class="ph ph-browsers"></i> 3 Landing Page Variations</h4>
                <div style="display: grid; gap: 12px;">
            `;
            
            campaign.landing_pages.forEach((page, i) => {
                html += `
                    <div style="background: white; padding: 16px; border-radius: 10px; border-left: 4px solid var(--accent); box-shadow: var(--shadow-sm);">
                        <strong>${i + 1}. ${page.name}</strong>
                        <div style="margin-top: 8px; color: var(--text-muted); font-size: 0.9rem;">
                            <div><strong>Headline:</strong> ${page.headline}</div>
                            <div><strong>Subheadline:</strong> ${page.subheadline}</div>
                            <div><strong>CTA:</strong> ${page.cta}</div>
                        </div>
                    </div>
                `;
            });
            
            html += `
                </div>
                
                <h4 style="color: var(--primary); margin: 24px 0 12px;"><i class="ph ph-key"></i> 20 Profitable Keywords</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px;">
            `;
            
            campaign.keywords.forEach(kw => {
                const color = kw.competition === 'Low' ? 'var(--success)' : kw.competition === 'Medium' ? 'var(--accent)' : 'var(--error)';
                html += `
                    <div style="background: white; padding: 12px; border-radius: 8px; box-shadow: var(--shadow-sm);">
                        <div style="font-weight: 600; color: var(--dark); margin-bottom: 6px;">${kw.keyword}</div>
                        <div style="display: flex; gap: 8px; font-size: 0.85rem; color: var(--text-muted);">
                            <span>📊 ${kw.volume}</span>
                            <span style="color: ${color};">⚡ ${kw.competition}</span>
                            <span>📈 ${kw.trend}</span>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
            resultBox.innerHTML = html;
            loadStats();
        } else {
            resultBox.innerHTML = `<div class="message error">${data.message}</div>`;
        }
    } catch (error) {
        resultBox.innerHTML = '<div class="message error">An error occurred. Please try again.</div>';
    }
});

document.getElementById('leaksForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const niche = document.getElementById('leaksNiche').value;
    const resultBox = document.getElementById('leaksResult');
    
    resultBox.innerHTML = '<div class="loading">Finding traffic leaks...</div>';
    resultBox.classList.add('show');
    
    try {
        const token = await getCSRFToken();
        const response = await fetch('/api/traffic-leaks/find', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({ niche })
        });
        
        const data = await response.json();
        
        if (data.success) {
            let html = '<h3 style="color: var(--primary); margin-bottom: 15px;">🎯 Traffic Leaks Found</h3>';
            
            data.leaks.forEach(leak => {
                html += `
                    <div class="leak-item">
                        <h4>${leak.platform}</h4>
                        <p><strong>Source:</strong> ${leak.source}</p>
                        <p><strong>Audience:</strong> ${leak.members}</p>
                        <p><strong>Engagement:</strong> ${leak.engagement}</p>
                        <p><strong>Opportunity:</strong> ${leak.opportunity}</p>
                    </div>
                `;
            });
            
            resultBox.innerHTML = html;
            loadStats();
        } else {
            resultBox.innerHTML = `<div class="message error">${data.message}</div>`;
        }
    } catch (error) {
        resultBox.innerHTML = '<div class="message error">An error occurred. Please try again.</div>';
    }
});

async function loadHeatmap() {
    const resultBox = document.getElementById('heatmapResult');
    resultBox.innerHTML = '<div class="loading">Loading heatmap data...</div>';
    
    try {
        const response = await fetch('/api/analytics/heatmap');
        const data = await response.json();
        
        if (data.success) {
            const maxValue = Math.max(...Object.values(data.heatmap), 1);
            let html = '<h3 style="color: var(--primary); margin-bottom: 20px;">Traffic Distribution</h3>';
            
            Object.entries(data.heatmap).forEach(([platform, value]) => {
                const percentage = (value / maxValue) * 100;
                html += `
                    <div class="heatmap-bar">
                        <div class="heatmap-label">
                            <span>${platform}</span>
                            <span>${value} visits</span>
                        </div>
                        <div class="heatmap-progress">
                            <div class="heatmap-fill" style="width: ${percentage}%;">
                                ${percentage > 20 ? Math.round(percentage) + '%' : ''}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            resultBox.innerHTML = html;
        } else {
            resultBox.innerHTML = `<div class="message error">${data.message}</div>`;
        }
    } catch (error) {
        resultBox.innerHTML = '<div class="message error">An error occurred. Please try again.</div>';
    }
}

document.getElementById('viralForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const niche = document.getElementById('viralNiche').value;
    const resultBox = document.getElementById('viralResult');
    
    resultBox.innerHTML = '<div class="loading">Finding viral content...</div>';
    resultBox.classList.add('show');
    
    const viralContent = [
        {
            title: `Top 10 ${niche} Tips That Go Viral`,
            platform: 'TikTok',
            engagement: '500K+ views',
            type: 'Video'
        },
        {
            title: `${niche} Transformation Story`,
            platform: 'Instagram',
            engagement: '100K+ likes',
            type: 'Carousel'
        },
        {
            title: `Ultimate ${niche} Guide 2025`,
            platform: 'Pinterest',
            engagement: '50K+ saves',
            type: 'Infographic'
        },
        {
            title: `${niche} Myths Debunked`,
            platform: 'YouTube',
            engagement: '250K+ views',
            type: 'Video'
        }
    ];
    
    let html = '<h3 style="color: var(--primary); margin-bottom: 15px;">💫 Viral Content Examples</h3>';
    
    viralContent.forEach(content => {
        html += `
            <div class="leak-item">
                <h4>${content.title}</h4>
                <p><strong>Platform:</strong> ${content.platform}</p>
                <p><strong>Type:</strong> ${content.type}</p>
                <p><strong>Engagement:</strong> ${content.engagement}</p>
            </div>
        `;
    });
    
    resultBox.innerHTML = html;
});

document.getElementById('emailForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const goal = document.getElementById('emailGoal').value;
    const count = document.getElementById('emailCount').value;
    const resultBox = document.getElementById('emailResult');
    
    resultBox.innerHTML = '<div class="loading">Generating email sequence...</div>';
    resultBox.classList.add('show');
    
    let html = `<h3 style="color: var(--primary); margin-bottom: 15px;">✉️ ${count}-Email Sequence for: ${goal}</h3>`;
    
    const emailTitles = [
        `Email 1: Introduction & Hook`,
        `Email 2: Problem Identification`,
        `Email 3: Solution Preview`,
        `Email 4: Social Proof & Testimonials`,
        `Email 5: Call to Action`,
        `Email 6: Urgency & Scarcity`,
        `Email 7: Final Push & Bonuses`
    ];
    
    for (let i = 0; i < count; i++) {
        html += `
            <div class="campaign-item">
                <h4>${emailTitles[i]}</h4>
                <p style="color: #666; margin-top: 8px;">Subject: ${goal} - ${emailTitles[i].split(': ')[1]}</p>
            </div>
        `;
    }
    
    resultBox.innerHTML = html;
});

document.getElementById('calendarForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const niche = document.getElementById('calendarNiche').value;
    const postsPerWeek = document.getElementById('postsPerWeek').value;
    const resultBox = document.getElementById('calendarResult');
    
    resultBox.innerHTML = '<div class="loading">Generating content calendar...</div>';
    resultBox.classList.add('show');
    
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const contentTypes = ['Blog Post', 'Video', 'Infographic', 'Social Media Post', 'Email'];
    
    let html = `<h3 style="color: var(--primary); margin-bottom: 15px;">📅 Content Calendar - ${postsPerWeek} posts/week</h3>`;
    
    const daysToPost = days.slice(0, parseInt(postsPerWeek));
    
    daysToPost.forEach((day, index) => {
        const contentType = contentTypes[index % contentTypes.length];
        html += `
            <div class="campaign-item">
                <h4>${day}</h4>
                <p><strong>Type:</strong> ${contentType}</p>
                <p><strong>Topic:</strong> ${niche} - ${contentType} content</p>
            </div>
        `;
    });
    
    resultBox.innerHTML = html;
});

function loadLibrary() {
    const resultBox = document.getElementById('libraryResult');
    resultBox.innerHTML = '<p style="text-align: center; padding: 40px; color: #666;">Your content library is empty. Start creating campaigns to automatically save your best content here!</p>';
}

document.getElementById('competitorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const competitor = document.getElementById('competitorName').value;
    const resultBox = document.getElementById('competitorResult');
    
    resultBox.innerHTML = '<div class="loading">Analyzing competitor...</div>';
    resultBox.classList.add('show');
    
    const analysis = {
        traffic_sources: ['Facebook (35%)', 'YouTube (30%)', 'SEO (20%)', 'Email (15%)'],
        top_content: [`${competitor} Guide`, `${competitor} Tips`, `${competitor} Reviews`],
        posting_frequency: '5 posts/week',
        engagement_rate: '4.2%'
    };
    
    let html = `<h3 style="color: var(--primary); margin-bottom: 15px;">🎪 Competitor Analysis: ${competitor}</h3>`;
    
    html += `
        <div class="leak-item">
            <h4>Traffic Sources</h4>
            ${analysis.traffic_sources.map(source => `<p>• ${source}</p>`).join('')}
        </div>
        
        <div class="leak-item">
            <h4>Top Performing Content</h4>
            ${analysis.top_content.map(content => `<p>• ${content}</p>`).join('')}
        </div>
        
        <div class="leak-item">
            <h4>Key Metrics</h4>
            <p><strong>Posting Frequency:</strong> ${analysis.posting_frequency}</p>
            <p><strong>Engagement Rate:</strong> ${analysis.engagement_rate}</p>
        </div>
    `;
    
    resultBox.innerHTML = html;
});

async function logout() {
    try {
        const token = await getCSRFToken();
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'X-CSRFToken': token
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}
