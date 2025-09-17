# Scout 🔍

A lightweight website auditing and outreach helper. No API keys, no cost — just scrape, score, and pitch.

## What is Scout?

Scout analyzes small business websites and generates actionable insights for web development outreach. It crawls target sites, scores them on business-critical metrics, and prepares fact-based data for personalized pitch emails.

Perfect for:
- **Web developers** looking for clients
- **Digital agencies** prospecting local businesses
- **Freelancers** identifying improvement opportunities
- **Business consultants** auditing client websites

## Features

✅ **Zero-cost auditing** - No APIs or paid services required
✅ **Business-focused scoring** - Prioritizes metrics small businesses care about
✅ **Outreach-ready output** - Generates structured facts for pitch emails
✅ **Multi-format reports** - JSON, Markdown, and facts files
✅ **Batch processing** - Audit multiple sites from CSV

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Add target websites to `targets.csv`:**
```csv
url
https://localrestaurant.com
https://plumbingcompany.net
https://dentistoffice.org
```

3. **Run Scout:**
```bash
python scout.py
```

4. **Check results in `out/` folder**

## Scoring System (0-100)

Scout evaluates websites on business-critical factors:

| Factor | Points | Why It Matters |
|--------|--------|----------------|
| HTTPS Security | 10 | Customer trust & SEO |
| Mobile Viewport | 10 | Mobile user experience |
| Phone Number | 10 | Local business discoverability |
| Email Contact | 10 | Lead generation |
| Booking CTA | 15 | Revenue conversion |
| Page Speed | 15 | User experience & SEO |
| Content Quality | 10 | SEO & engagement |
| Meta Description | 10 | Search visibility |
| Analytics Setup | 5 | Data-driven decisions |

## Output Files

For each domain, Scout generates:

- **`domain.json`** - Complete audit data and score
- **`domain.md`** - Human-readable report
- **`domain.facts.txt`** - Structured facts for outreach

## Sample Outreach Workflow

1. **Scout identifies issues:** Site lacks HTTPS, no mobile viewport, slow loading
2. **Generate pitch email:** Use `pitch_prompt.txt` with the facts file
3. **Personalized outreach:** "I noticed your site loads in 3.2 seconds and isn't mobile-optimized..."

## What Scout Detects

- **Technical Issues:** Missing HTTPS, viewport tags, slow response times
- **Contact Problems:** No phone/email, hard to find contact info
- **Conversion Gaps:** Missing booking buttons, unclear CTAs
- **SEO Basics:** Missing meta descriptions, poor content structure
- **Platform Detection:** WordPress, Wix, Squarespace, Shopify hints

## Requirements

- Python 3.7+
- No API keys required
- Works with any website

## Contributing

Scout is designed to be simple and focused. If you have ideas for business-relevant metrics or better scoring algorithms, PRs welcome!