# Scout

A lightweight website auditing and outreach helper. No API keys, no cost: just scrape, score, and pitch.

## What is Scout?

Scout analyzes small business websites and generates useful insights for web development outreach. It crawls target sites, scores them on business-critical metrics, and prepares fact-based data for personalized pitch emails.

Useful for:
- Web developers looking for clients
- Digital agencies prospecting local businesses
- Freelancers identifying improvement opportunities
- Business consultants auditing client websites

## Features

- Zero-cost auditing with no APIs or paid services required
- Business-focused scoring that prioritizes metrics small businesses care about
- Outreach-ready output with structured facts for pitch emails
- Multi-format reports: JSON, Markdown, and facts files
- Batch processing to audit multiple sites from CSV

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add target websites to `targets.csv`:
```csv
url
https://localrestaurant.com
https://plumbingcompany.net
https://dentistoffice.org
```

3. Run Scout:
```bash
python scout.py
```

4. Check results in the `out/` folder.

## Scoring System (0-100)

Scout evaluates websites on business-critical factors:

| Factor | Points | Why It Matters |
|--------|--------|----------------|
| HTTPS Security | 10 | Customer trust and SEO |
| Mobile Viewport | 10 | Mobile user experience |
| Phone Number | 10 | Local business discoverability |
| Email Contact | 10 | Lead generation |
| Booking CTA | 15 | Revenue conversion |
| Page Speed | 15 | User experience and SEO |
| Content Quality | 10 | SEO and engagement |
| Meta Description | 10 | Search visibility |
| Analytics Setup | 5 | Data-driven decisions |

## Output Files

For each domain, Scout generates:

- `domain.json`: Complete audit data and score
- `domain.md`: Human-readable report
- `domain.facts.txt`: Structured facts for outreach

## Sample Outreach Workflow

1. Scout identifies issues: site lacks HTTPS, no mobile viewport, slow loading.
2. Generate a pitch email: use `pitch_prompt.txt` with the facts file.
3. Send personalized outreach: "I noticed your site loads in 3.2 seconds and isn't mobile-optimized..."

## What Scout Detects

- Technical issues: missing HTTPS, viewport tags, slow response times
- Contact problems: no phone/email, hard to find contact info
- Conversion gaps: missing booking buttons, unclear CTAs
- SEO basics: missing meta descriptions, poor content structure
- Platform detection: WordPress, Wix, Squarespace, Shopify hints

## Requirements

- Python 3.7+
- No API keys required
- Works with any website

## Contributing

Scout is designed to be simple and focused. If you have ideas for business-relevant metrics or better scoring algorithms, PRs welcome.
