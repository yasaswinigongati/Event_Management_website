from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "utsav_secret_2024"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utsav.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer)
    date = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

TRANSLATIONS = {
    "en": {
        "lang": "en",
        "h1": "Every Celebration", "h2": "Deserves to be", "h3": "Extraordinary",
        "badge": "Budget Friendly · No Hidden Costs",
        "hsub": "We craft unforgettable events rooted in Telugu values and traditions — weddings, birthdays, and family celebrations planned beautifully within your budget.",
        "hcta": "Start Planning", "hcta2": "See Our Work",
        "s1n": "1000+", "s1l": "Events Planned",
        "s2n": "95%",    "s2l": "Satisfaction",
        "s3n": "3+",     "s3l": "Years Experience",
        "s4n": "10+",    "s4l": "Cities Covered",
        "weye": "Why Us",
        "wtit": "Why Families Choose Us",
        "wsub": "We're not a faceless agency. We're your family's event partner.",
        "w1t": "Honest Pricing",     "w1d": "What you see is what you pay. Transparent packages from ₹15,000 — zero surprises.",
        "w2t": "End-to-End Care",    "w2d": "From first call to final decoration — we handle everything so you enjoy the moment.",
        "w3t": "Local & Trusted",    "w3d": "Rooted in Vijayawada, serving 10+ cities. We know local traditions, vendors, and venues deeply.",
        "w4t": "Your Vision First",  "w4d": "We listen before we plan. Your dream event, not a copy-paste template.",
        "seye": "Services", "stit": "What We Do", "ssub": "From intimate gatherings to grand celebrations, with an authentic Telugu cultural touch",
        "sv1t": "Weddings",           "sv1d": "Telugu weddings with pellikuthuru, pellikoduku, mangala vadyam, and tradition-rich decor handled with care.",
        "sv2t": "Birthdays",          "sv2d": "Joyful birthdays with traditional themes, family rituals, and memorable stage setups for every age.",
        "sv4t": "Cultural & Religious","sv4d": "Namakaranam, Aksharabhyasam, Upanayanam, Gruha Pravesham, Satyanarayana Vratham — organized with full sampradayam.",
        "sv5t": "Photography",        "sv5d": "Candid and cinematic coverage focused on Telugu rituals, emotions, and family moments you will cherish forever.",
        "sv6t": "Catering",           "sv6d": "Authentic vegetarian and non-vegetarian menus, plus modern options, curated to delight every guest.",
        "preye": "Pricing", "prtit": "Simple, Honest Pricing", "prsub": "Pick what fits. Upgrade anytime. No hidden fees — ever.",
        "p1n": "Starter",     "p1tag": "Intimate events · up to 50 guests",   "p1price": "₹15,000",
        "p2n": "Celebration", "p2tag": "Mid-size events · up to 200 guests",  "p2price": "₹50,000",
        "p3n": "Grand",       "p3tag": "Large events · up to 500 guests",     "p3price": "₹90,000",
        "pbadge": "✦ Most Loved", "pbtn": "Get This Plan",
        "feats": ["Event Coordinator","Decoration Setup","Catering Included","Photography","Videography","Custom Theme Design","Live Music / DJ","24/7 Support"],
        "p1off": [4,5,6], "p2off": [6], "p3off": [],
        "geye": "Gallery", "gtit": "Moments We've Created", "gsub": "Real tradition-first events across Vijayawada, Tirupati, Kurnool, Nandyal, Nellore, and Ongole.",
        "ceye": "Contact", "ctit": "Let's Plan Together",
        "csub": "Tell us about your dream event — we'll get back within 3 hours.",
        "clname": "Your Name", "clphone": "Phone", "clemail": "Email",
        "clevent": "What's the Occasion?", "clguests": "Expected Guests",
        "cldate": "Preferred Date", "clmsg": "Any special requests?",
        "o1": "Wedding", "o2": "Birthday", "o4": "Cultural / Religious", "o5": "Other",
        "cnote": "We respond within <strong>3 hours</strong> — always.",
        "csbtn": "Send Message →",
        "cok": "✓ Received! We'll call you within 3 hours.",
        "fcopy": "© 2024 Utsav Events · Vijayawada, Andhra Pradesh",
        "flsvc": "Services", "flpr": "Pricing", "flgal": "Gallery", "flct": "Contact",
        "nav_why": "Why Us", "nav_svc": "Services", "nav_pr": "Pricing",
        "nav_gal": "Gallery", "nav_ct": "Contact",
    },
    "hi": {
        "lang": "hi",
        "h1": "हर उत्सव", "h2": "बनना चाहिए", "h3": "असाधारण",
        "badge": "बजट फ्रेंडली · कोई छुपी लागत नहीं",
        "hsub": "तेलुगु परंपराओं के साथ शादी, जन्मदिन और पारिवारिक उत्सव — हर खास मौके को बजट में खूबसूरती से सजाते हैं।",
        "hcta": "योजना शुरू करें", "hcta2": "हमारा काम देखें",
        "s1n": "1000+", "s1l": "इवेंट",
        "s2n": "95%",    "s2l": "संतुष्टि",
        "s3n": "3+",     "s3l": "साल अनुभव",
        "s4n": "10+",    "s4l": "शहर",
        "weye": "क्यों हम",
        "wtit": "परिवार हमें क्यों चुनते हैं",
        "wsub": "हम एक एजेंसी नहीं, आपके परिवार के साथी हैं।",
        "w1t": "ईमानदार मूल्य",      "w1d": "जो दिखे वही दाम। ₹15,000 से शुरू — कोई छुपी फीस नहीं।",
        "w2t": "पूरी जिम्मेदारी",    "w2d": "पहली कॉल से आखिरी सजावट तक — सब हम संभालते हैं।",
        "w3t": "स्थानीय व भरोसेमंद", "w3d": "विजयवाड़ा में जड़ें, 10+ शहरों में सेवा।",
        "w4t": "आपकी कल्पना पहले",   "w4d": "पहले सुनते हैं, फिर योजना — आपका सपना, हमारी मेहनत।",
        "seye": "सेवाएं", "stit": "हम क्या करते हैं", "ssub": "छोटी सभाओं से भव्य समारोहों तक, तेलुगु सांस्कृतिक छाप के साथ",
        "sv1t": "शादी",          "sv1d": "तेलुगु शादी की पेल्लिकुथुरु, पेल्लिकोडुकु, मंगल वाद्य और पारंपरिक सजावट — हर विवरण स्नेह से संभालते हैं।",
        "sv2t": "जन्मदिन",       "sv2d": "पारंपरिक थीम, पारिवारिक रीति-रिवाज और शानदार स्टेज सजावट के साथ यादगार जन्मदिन।",
        "sv4t": "सांस्कृतिक",    "sv4d": "नामकरण, अक्षराभ्यास, उपनयन, गृह प्रवेश, सत्यनारायण व्रत — पूर्ण परंपरा और श्रद्धा के साथ आयोजन।",
        "sv5t": "फोटोग्राफी",    "sv5d": "कैंडिड और सिनेमैटिक कवरेज, जो तेलुगु रस्में, भावनाएं और पारिवारिक क्षण हमेशा के लिए सहेज ले।",
        "sv6t": "कैटरिंग",       "sv6d": "असली शाकाहारी और मांसाहारी व्यंजन, साथ में आधुनिक विकल्प — हर मेहमान के स्वाद के अनुसार।",
        "preye": "मूल्य", "prtit": "सरल, ईमानदार मूल्य", "prsub": "जो सही लगे वो चुनें। कोई छुपी फीस नहीं।",
        "p1n": "स्टार्टर", "p1tag": "50 मेहमान तक",  "p1price": "₹15,000",
        "p2n": "उत्सव",    "p2tag": "200 मेहमान तक", "p2price": "₹50,000",
        "p3n": "ग्रैंड",   "p3tag": "500 मेहमान तक", "p3price": "₹90,000",
        "pbadge": "✦ सबसे लोकप्रिय", "pbtn": "यह प्लान चुनें",
        "feats": ["इवेंट कोऑर्डिनेटर","सजावट","कैटरिंग शामिल","फोटोग्राफी","वीडियोग्राफी","कस्टम थीम","लाइव म्यूजिक / DJ","24/7 सहायता"],
        "p1off": [4,5,6], "p2off": [6], "p3off": [],
        "geye": "गैलरी", "gtit": "हमारे बनाए पल", "gsub": "विजयवाड़ा, तिरुपति, कुरनूल, नंद्याल, नेल्लोर और ओंगोल में तेलुगु-परंपरा आधारित वास्तविक आयोजन।",
        "ceye": "संपर्क", "ctit": "मिलकर योजना बनाएं",
        "csub": "अपने सपने के इवेंट के बारे में बताएं — 3 घंटे में संपर्क करेंगे।",
        "clname": "आपका नाम", "clphone": "फोन नंबर", "clemail": "ईमेल",
        "clevent": "क्या अवसर है?", "clguests": "अनुमानित मेहमान",
        "cldate": "पसंदीदा तारीख", "clmsg": "कोई विशेष अनुरोध?",
        "o1": "शादी", "o2": "जन्मदिन", "o4": "सांस्कृतिक", "o5": "अन्य",
        "cnote": "हम <strong>3 घंटे</strong> में हमेशा जवाब देते हैं।",
        "csbtn": "संदेश भेजें →",
        "cok": "✓ मिल गया! 3 घंटे में कॉल करेंगे।",
        "fcopy": "© 2024 उत्सव इवेंट्स · विजयवाड़ा, आंध्र प्रदेश",
        "flsvc": "सेवाएं", "flpr": "मूल्य", "flgal": "गैलरी", "flct": "संपर्क",
        "nav_why": "क्यों हम", "nav_svc": "सेवाएं", "nav_pr": "मूल्य",
        "nav_gal": "गैलरी", "nav_ct": "संपर्क",
    },
    "te": {
        "lang": "te",
        "h1": "ప్రతి వేడుక", "h2": "అద్భుతంగా", "h3": "ఉండాలి",
        "badge": "బడ్జెట్ అనుకూలం · దాచిన ఖర్చులు లేవు",
        "hsub": "తెలుగు సంప్రదాయంతో పెళ్లిళ్లు, పుట్టినరోజులు, కుటుంబ వేడుకలను మీ బడ్జెట్‌లో అందంగా నిర్వహిస్తాం.",
        "hcta": "ప్లానింగ్ ప్రారంభించండి", "hcta2": "మా పని చూడండి",
        "s1n": "1000+", "s1l": "ఈవెంట్లు",
        "s2n": "95%",    "s2l": "సంతృప్తి",
        "s3n": "3+",     "s3l": "సంవత్సరాల అనుభవం",
        "s4n": "10+",    "s4l": "నగరాలు",
        "weye": "ఎందుకు మేము",
        "wtit": "కుటుంబాలు మమ్మల్ని ఎందుకు ఎంచుకుంటాయి",
        "wsub": "మేము ఏజెన్సీ కాదు — మీ కుటుంబ సహచరులం.",
        "w1t": "నిజాయితీ ధరలు",      "w1d": "చూసినదే చెల్లించేది. ₹15,000 నుండి — ఆశ్చర్యపోయే బిల్లులు లేవు.",
        "w2t": "పూర్తి బాధ్యత",       "w2d": "మొదటి కాల్ నుండి చివరి అలంకరణ వరకు — మేము అన్నీ చూసుకుంటాం.",
        "w3t": "స్థానిక & విశ్వసనీయం","w3d": "విజయవాడలో పాతుకుపోయి, 10+ నగరాల్లో సేవలు.",
        "w4t": "మీ దృష్టి మొదట",      "w4d": "ముందు వింటాం, తరువాత ప్లాన్ — మీ కల, మా కష్టం.",
        "seye": "సేవలు", "stit": "మేము ఏమి చేస్తాం", "ssub": "చిన్న సమావేశాల నుండి భారీ వేడుకల వరకు, నిజమైన తెలుగు సంస్కృతి స్పర్శతో",
        "sv1t": "వివాహాలు",              "sv1d": "పెళ్లికూతురు, పెళ్లికొడుకు, మంగళ వాద్యాలు, సంప్రదాయ అలంకరణలతో తెలుగు పెళ్లిళ్లను శ్రద్ధగా నిర్వహిస్తాం.",
        "sv2t": "పుట్టినరోజులు",         "sv2d": "సంప్రదాయ థీమ్స్, కుటుంబ ఆచారాలు, అందమైన స్టేజ్ సెటప్‌లతో గుర్తుండిపోయే పుట్టినరోజులు.",
        "sv4t": "సాంస్కృతిక / మతపరమైన", "sv4d": "నామకరణం, అక్షరాభ్యాసం, ఉపనయనం, గృహ ప్రవేశం, సత్యనారాయణ వ్రతం — పూర్తి సంప్రదాయంతో నిర్వహణ.",
        "sv5t": "ఫోటోగ్రఫీ",             "sv5d": "తెలుగు ఆచారాలు, భావోద్వేగాలు, కుటుంబ క్షణాలను చిరస్థాయిగా నిలిపే క్యాండిడ్ & సినిమాటిక్ కవరేజ్.",
        "sv6t": "క్యాటరింగ్",            "sv6d": "అసలైన వెజ్, నాన్-వెజ్ వంటకాలతో పాటు ఆధునిక మెనూలు — ప్రతి అతిథి రుచికి సరిపోయేలా.",
        "preye": "ధరలు", "prtit": "సరళమైన, నిజాయితీ ధరలు", "prsub": "మీకు సరిపోయేది ఎంచుకోండి. దాచిన ఫీజులు లేవు.",
        "p1n": "స్టార్టర్", "p1tag": "50 అతిథుల వరకు",  "p1price": "₹15,000",
        "p2n": "వేడుక",     "p2tag": "200 అతిథుల వరకు", "p2price": "₹50,000",
        "p3n": "గ్రాండ్",   "p3tag": "500 అతిథుల వరకు", "p3price": "₹90,000",
        "pbadge": "✦ అత్యంత జనప్రియం", "pbtn": "ఈ ప్లాన్ తీసుకోండి",
        "feats": ["ఈవెంట్ కోఆర్డినేటర్","అలంకరణ","క్యాటరింగ్ చేర్చబడింది","ఫోటోగ్రఫీ","వీడియోగ్రఫీ","కస్టమ్ థీమ్","లైవ్ మ్యూజిక్ / DJ","24/7 మద్దతు"],
        "p1off": [4,5,6], "p2off": [6], "p3off": [],
        "geye": "గ్యాలరీ", "gtit": "మేము సృష్టించిన క్షణాలు", "gsub": "విజయవాడ, తిరుపతి, కర్నూలు, నంద్యాల, నెల్లూరు, ఒంగోలులో తెలుగు సంప్రదాయ ప్రధానమైన నిజమైన కార్యక్రమాలు.",
        "ceye": "సంప్రదించండి", "ctit": "కలిసి ప్లాన్ చేద్దాం",
        "csub": "మీ కలల ఈవెంట్ గురించి చెప్పండి — 3 గంటల్లో తిరిగి వస్తాం.",
        "clname": "మీ పేరు", "clphone": "ఫోన్ నంబర్", "clemail": "ఇమెయిల్",
        "clevent": "సందర్భం ఏమిటి?", "clguests": "అంచనా అతిథులు",
        "cldate": "ఇష్టమైన తేదీ", "clmsg": "ప్రత్యేక అభ్యర్థనలు?",
        "o1": "వివాహం", "o2": "పుట్టినరోజు", "o4": "సాంస్కృతిక / మతపరమైన", "o5": "ఇతర",
        "cnote": "మేము <strong>3 గంటల్లో</strong> స్పందిస్తాం — ఎల్లప్పుడూ.",
        "csbtn": "సందేశం పంపండి →",
        "cok": "✓ అందింది! 3 గంటల్లో కాల్ చేస్తాం.",
        "fcopy": "© 2024 ఉత్సవ్ ఈవెంట్స్ · విజయవాడ, ఆంధ్రప్రదేశ్",
        "flsvc": "సేవలు", "flpr": "ధరలు", "flgal": "గ్యాలరీ", "flct": "సంప్రదించండి",
        "nav_why": "ఎందుకు మేము", "nav_svc": "సేవలు", "nav_pr": "ధరలు",
        "nav_gal": "గ్యాలరీ", "nav_ct": "సంప్రదించండి",
    },
}

# Make Python enumerate available in Jinja2
app.jinja_env.filters["enumerate"] = enumerate

@app.route("/")
def index():
    lang = session.get("lang", "en")
    t = TRANSLATIONS[lang]
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    return render_template("index.html", t=t, current_user=user)

@app.route("/lang/<code>")
def set_lang(code):
    if code in TRANSLATIONS:
        session["lang"] = code
    return redirect(url_for("index"))

@app.route("/contact", methods=["POST"])
def contact():
    # Public inquiry (not a booking)
    return jsonify({"ok": True, "message": "Inquiry received."})

@app.route("/book", methods=["POST"])
def book():
    if 'user_id' not in session:
        return jsonify({"ok": False, "error": "Please login to book an event."}), 401
    
    data = request.form
    new_booking = Booking(
        user_id=session['user_id'],
        event_type=data.get("event"),
        guests=int(data.get("guests")) if data.get("guests") else None,
        date=data.get("date"),
        message=data.get("message")
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"ok": True, "message": "Booking successful!"})

@app.route("/register", methods=["GET", "POST"])
def register():
    lang = session.get("lang", "en")
    t = TRANSLATIONS[lang]
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("register"))
            
        user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("index"))
        
    return render_template("register.html", t=t)

@app.route("/login", methods=["GET", "POST"])
def login():
    lang = session.get("lang", "en")
    t = TRANSLATIONS[lang]
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))
            
    return render_template("login.html", t=t)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route("/my_bookings")
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    lang = session.get("lang", "en")
    t = TRANSLATIONS[lang]
    user = User.query.get(session['user_id'])
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.created_at.desc()).all()
    return render_template("bookings.html", t=t, current_user=user, bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
