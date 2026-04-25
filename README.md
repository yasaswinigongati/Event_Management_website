# Utsav — Event Management Website (Flask)

A unique, handcrafted-aesthetic event management website built with Python Flask.
Supports **English**, **Hindi (हिन्दी)**, and **Telugu (తెలుగు)**.

## Project Structure

```
utsav/
├── app.py                  ← Flask app + all translations
├── requirements.txt
├── templates/
│   └── index.html          ← Full single-page template
└── static/                 ← (add images/custom assets here)
```

## Quick Start

```bash
# 1. Unzip and enter folder
cd utsav

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install Flask
pip install -r requirements.txt

# 4. Run
python app.py

# 5. Open browser
#    http://localhost:5000
```

## Features

| Feature | Details |
|---|---|
| Languages | English / हिन्दी / తెలుగు — switch instantly |
| Sections | Hero · Why Us · Services · Pricing · Gallery · Contact |
| Pricing | ₹15,000 / ₹50,000 / ₹90,000 — fully transparent |
| Contact Form | AJAX submit — no page reload |
| Design | Cormorant Garamond serif + saffron palette |
| Animations | Scroll reveal, floating lanterns, hover effects |
| Responsive | Mobile, tablet, desktop |

## Language Switching

Click **EN / हि / తె** in the navbar. Language is saved in the Flask session.
Routes: `/lang/en`, `/lang/hi`, `/lang/te`

## Customise

- **Brand name**: Search `Utsav` in `app.py` and `index.html`
- **Colors**: Edit CSS variables in `index.html` (`:root` block)
- **Pricing**: Update `p1price`, `p2price`, `p3price` in `TRANSLATIONS`
- **Contact form**: Add DB/email logic in the `/contact` route in `app.py`
- **Gallery**: Replace emoji + labels in the Gallery section of `index.html`
