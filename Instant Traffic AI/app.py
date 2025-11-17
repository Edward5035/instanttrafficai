from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os
# # import template_generator as groq_helper
from . import web_scraper

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traffic_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    campaigns = db.relationship('Campaign', backref='user', lazy=True, cascade='all, delete-orphan')
    traffic_sources = db.relationship('TrafficSource', backref='user', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrafficSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    source_name = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    potential_reach = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/login', methods=['POST'])
@csrf.exempt
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip().lower()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        name = username.capitalize()
        user = User(username=username, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        message = 'Account created and logged in successfully!'
    else:
        if not user.check_password(password):
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        message = 'Logged in successfully!'
    
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['username'] = user.username
    
    return jsonify({'success': True, 'message': message, 'user': {'name': user.name, 'username': user.username}})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    campaigns = Campaign.query.filter_by(user_id=session['user_id']).order_by(Campaign.created_at.desc()).all()
    
    return jsonify({'success': True, 'campaigns': [
        {
            'id': c.id,
            'name': c.name,
            'niche': c.niche,
            'platform': c.platform,
            'status': c.status,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        } for c in campaigns
    ]})

# @app.route('/api/campaigns/generate', methods=['POST'])
def generate_campaign_route():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    niche = data.get('niche', '').strip()
    platform = data.get('platform', 'all')
    
    if not niche:
        return jsonify({'success': False, 'message': 'Niche is required'}), 400
    
    campaign_name = f"{niche.title()} Campaign - {datetime.now().strftime('%b %d')}"
    
    campaign = Campaign(
        user_id=session['user_id'],
        name=campaign_name,
        niche=niche,
        platform=platform,
        status='active'
    )
    db.session.add(campaign)
    db.session.commit()
    
    try:
        campaign_data = web_scraper.generate_campaign(niche, platform)
        
        if campaign_data:
            return jsonify({
                'success': True,
                'campaign': {
                    'id': campaign.id,
                    'name': campaign.name,
                    'niche': campaign.niche,
                    'platform': campaign.platform,
                    'blog_posts': campaign_data.get('blog_posts', []),
                    'social_posts': campaign_data.get('social_posts', {}),
                    'email_sequences': campaign_data.get('email_sequences', []),
                    'landing_pages': campaign_data.get('landing_pages', []),
                    'keywords': campaign_data.get('keywords', [])
                }
            })
        else:
            return jsonify({'success': False, 'message': 'AI generated empty response. Please try again.'}), 500
    except Exception as e:
        error_msg = str(e)
        if '503' in error_msg or 'overloaded' in error_msg.lower():
            return jsonify({'success': False, 'message': 'AI service is busy right now. Please try again in a moment.'}), 503
        elif 'quota' in error_msg.lower() or '429' in error_msg:
            return jsonify({'success': False, 'message': 'Rate limit reached. Please wait a moment and try again.'}), 429
        else:
            return jsonify({'success': False, 'message': f'Error generating campaign. Please try again.'}), 500

# @app.route('/api/traffic-leaks/find', methods=['POST'])
def find_traffic_leaks():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    niche = data.get('niche', '').strip()
    competitor_url = data.get('competitor_url', '').strip()
    
    if not niche:
        return jsonify({'success': False, 'message': 'Niche is required'}), 400
    
    result = web_scraper.find_real_traffic_leaks(niche, competitor_url if competitor_url else None)
    leaks = result.get('leaks', [])
    
    for leak in leaks:
        source = TrafficSource(
            user_id=session['user_id'],
            platform=leak.get('platform', 'Unknown'),
            source_name=leak.get('source', 'Unknown'),
            niche=niche,
            potential_reach=leak.get('members', 'Unknown')
        )
        db.session.add(source)
    
    db.session.commit()
    
    return jsonify({'success': True, 'leaks': leaks})

@app.route('/api/analytics/heatmap', methods=['GET'])
def get_heatmap_data():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    analytics = Analytics.query.filter_by(user_id=session['user_id']).all()
    
    heatmap_data = {
        'Facebook': 0,
        'Reddit': 0,
        'YouTube': 0,
        'Pinterest': 0,
        'Quora': 0,
        'Instagram': 0,
        'Twitter': 0,
        'LinkedIn': 0
    }
    
    for record in analytics:
        if record.platform in heatmap_data:
            heatmap_data[record.platform] += record.clicks
    
    sources = TrafficSource.query.filter_by(user_id=session['user_id']).all()
    for source in sources:
        if source.platform in heatmap_data:
            heatmap_data[source.platform] += 50
    
    return jsonify({'success': True, 'heatmap': heatmap_data})


# --- New Feature API Endpoints ---

@app.route('/api/features/trend-caster', methods=['POST'])
def trend_caster():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.trend_caster_ai(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/niche-scanner', methods=['POST'])
def niche_scanner():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    hashtag = data.get('hashtag', '').strip()
    if not hashtag:
        return jsonify({'success': False, 'message': 'Hashtag is required'}), 400
    
    result = web_scraper.niche_scanner(hashtag)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/viral-vortex', methods=['POST'])
def viral_vortex():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.viral_vortex(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/competitor-cloner', methods=['POST'])
def competitor_cloner():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'}), 400
    
    result = web_scraper.competitor_cloner(username)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/hashtag-matrix', methods=['POST'])
def hashtag_matrix():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.hashtag_matrix(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/content-spark', methods=['POST'])
def content_spark():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.content_spark(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/authority-architect', methods=['POST'])
def authority_architect():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.authority_architect(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/influencer-radar', methods=['POST'])
def influencer_radar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.influencer_radar(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/traffic-loom', methods=['POST'])
def traffic_loom():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    if not keyword:
        return jsonify({'success': False, 'message': 'Keyword is required'}), 400
    
    result = web_scraper.traffic_loom(keyword)
    return jsonify({'success': True, 'data': result})

@app.route('/api/features/trend-trigger', methods=['GET'])
def trend_trigger():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    result = web_scraper.trend_trigger()
    return jsonify({'success': True, 'data': result})

@app.route('/api/analytics/stats', methods=['GET'])
def get_stats():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    campaigns_count = Campaign.query.filter_by(user_id=session['user_id']).count()
    sources_count = TrafficSource.query.filter_by(user_id=session['user_id']).count()
    total_clicks = db.session.query(db.func.sum(Analytics.clicks)).filter_by(user_id=session['user_id']).scalar() or 0
    
    return jsonify({
        'success': True,
        'stats': {
            'campaigns': campaigns_count,
            'traffic_sources': sources_count,
            'total_clicks': total_clicks,
            'conversion_rate': '3.5%'
        }
    })

# @app.route('/api/viral-content/find', methods=['POST'])
def find_viral_content():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    niche = data.get('niche', '').strip()
    
    if not niche:
        return jsonify({'success': False, 'message': 'Niche is required'}), 400
    
    result = web_scraper.find_viral_content(niche)
    trending = result.get('trending', [])
    
    return jsonify({'success': True, 'trending': trending})

# @app.route('/api/competitor/analyze', methods=['POST'])
def analyze_competitor():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    competitor_url = data.get('url', '').strip()
    niche = data.get('niche', '').strip()
    
    if not niche:
        return jsonify({'success': False, 'message': 'Niche is required'}), 400
    
    # URL is optional - we analyze the niche itself for strategic insights
    result = web_scraper.analyze_competitor(competitor_url or niche, niche)
    analysis = result.get('analysis', {})
    
    return jsonify({'success': True, 'analysis': analysis})

# @app.route('/api/email/generate', methods=['POST'])
def generate_email_sequence():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    goal = data.get('goal', '').strip()
    niche = data.get('niche', '').strip()
    num_emails = int(data.get('num_emails', 5))
    
    if not goal:
        return jsonify({'success': False, 'message': 'Campaign goal is required'}), 400
    
    result = web_scraper.generate_email_sequence(goal, niche, num_emails)
    sequence = result.get('sequence', {})
    
    return jsonify({'success': True, 'sequence': sequence})

# @app.route('/api/heatmap/generate', methods=['POST'])
def generate_heatmap():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    niche = data.get('niche', '').strip()
    
    if not niche:
        return jsonify({'success': False, 'message': 'Niche is required'}), 400
    
    result = web_scraper.get_traffic_heatmap_data(niche)
    heatmap = result.get('heatmap', {})
    
    return jsonify({'success': True, 'heatmap': heatmap})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
