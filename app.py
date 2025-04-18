from flask import Flask, render_template, request
import re
import random
from datetime import datetime

app = Flask(__name__)

# One Piece character feedback
CREW_FEEDBACK = {
    "luffy": ["👑 GOMU GOMU NO PASSWORD KING!", "THIS PASSWORD WILL MAKE ME PIRATE KING!"],
    "zoro": ["🗡️ Three-sword style secure!", "Could slice through Marine HQ!"],
    "nami": ["💰 Beli-proof security!", "Even Big Mom couldn't crack this!"],
    "sanji": ["👨‍🍳 Flambé-grade encryption!", "Hotter than Diable Jambe!"],
    "chopper": ["🩺 Medical-grade protection!", "This would make Doctorine proud!"],
    "robin": ["📚 Poneglyph-level security!", "Ohara would approve!"]
}

def generate_recommendations(base_password):
    """Generate 3 secure password variations based on user's input"""
    recommendations = []
    
    # Skip recommendations if password is too weak or common
    if len(base_password) < 4 or base_password.lower() in ['123456', 'password', 'qwerty']:
        base_password = "StrawHat"  # Fallback base
    
    # Common transformation patterns
    patterns = [
        # Pattern 1: Capitalize + numbers + symbol
        lambda p: f"{p.capitalize()}{random.randint(100,999)}{random.choice('!@#$%^&*')}",
        
        # Pattern 2: Symbol + partial + uppercase + numbers
        lambda p: f"{random.choice('@$#*')}{p[:4]}{random.choice('ABCDEFGH')}{random.randint(10,99)}",
        
        # Pattern 3: First 3 uppercase + separator + last 3 lowercase + numbers
        lambda p: f"{p[:3].upper()}{random.choice('_-!@')}{p[-3:].lower()}{random.randint(1000,9999)}",
        
        # Pattern 4: Mixed case with special chars
        lambda p: f"{p[:2].lower()}{random.choice('!@#')}{p[2:].capitalize()}{random.choice('€¥£')}"
    ]
    
    # Generate 3 unique recommendations
    while len(recommendations) < 3:
        # Select random pattern
        pattern_func = random.choice(patterns)
        new_pass = pattern_func(base_password)
        
        # Ensure complexity requirements
        if not re.search(r'\d', new_pass):
            new_pass += str(random.randint(1,9))
        if not re.search(r'[A-Z]', new_pass):
            new_pass = new_pass[0].upper() + new_pass[1:]
        if not re.search(r'[^A-Za-z0-9]', new_pass):
            new_pass += random.choice('!@#$%^&*')
        
        # Ensure minimum length and uniqueness
        if len(new_pass) >= 8 and new_pass not in recommendations:
            recommendations.append(new_pass)
    
    return recommendations[:3]

def analyze_password(password):
    score = 0
    feedback = []
    warnings = []
    
    # Length check
    length = len(password)
    if length >= 16:
        score += 3
        feedback.append("🔥 YONKO-LEVEL LENGTH! (16+ chars)")
    elif length >= 12:
        score += 2
        feedback.append("⭐ NEW WORLD READY! (12+ chars)")
    elif length >= 8:
        score += 1
        feedback.append("🌊 GRAND LINE WORTHY (8+ chars)")
    else:
        score -= 1
        warnings.append("💀 EAST BLUE WEAK! (Too short)")

    # Character variety checks
    checks = [
        (r'[a-z]', "lowercase letter"),
        (r'[A-Z]', "uppercase letter"),
        (r'\d', "number"),
        (r'[^A-Za-z0-9]', "special character")
    ]
    
    for pattern, description in checks:
        if re.search(pattern, password):
            score += 1
        else:
            warnings.append(f"Missing {description}")

    # Common password check
    common_passwords = ['123456', 'password', 'qwerty', 'luffy', 'onepiece']
    if password.lower() in common_passwords:
        score = max(0, score - 2)
        warnings.append("☠️ MARINE-GRADE WEAK! (Common password)")

    # Calculate verdict
    if score >= 7:
        verdict = "🏴‍☠️ PIRATE KING TIER"
        char = random.choice(list(CREW_FEEDBACK.keys()))
        feedback.extend(CREW_FEEDBACK[char])
    elif score >= 5:
        verdict = "⭐ SUPER ROOKIE"
    elif score >= 3:
        verdict = "🌊 GRAND LINE READY"
    else:
        verdict = "💀 DAVY BACK FAILURE"
        feedback.append("Even a Sea King could crack this!")

    return {
        "score": score,
        "max_score": 10,
        "verdict": verdict,
        "feedback": feedback,
        "warnings": warnings,
        "length": length,
        "password": password,
        "recommendations": generate_recommendations(password),
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        password = request.form['password']
        result = analyze_password(password)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
