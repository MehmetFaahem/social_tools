# Social Media Tools

A Django web application providing various social media tools including Instagram and Facebook content downloaders, and an AI image generator.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following variables:
```bash
# Cloudflare API Configuration for AI Image Generator
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here
CLOUDFLARE_API_KEY=your_cloudflare_api_key_here

# Django Settings
SECRET_KEY=django-insecure-wg*1hlx0l^91vqp*-n44wo5==!$iaq21z%76+r+r(5%b6mrulj
DEBUG=False
```

3. Get your Cloudflare API credentials:
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
   - Create an API token with AI permissions
   - Get your Account ID from the dashboard

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Features

- Instagram Reel Download
- Instagram Photo Download  
- Instagram Story Download
- Instagram Hashtag Generator
- Instagram to MP3 Converter
- Facebook Reel Download
- AI Image Generator (requires Cloudflare API)

## Note

The AI Image Generator feature requires valid Cloudflare API credentials. If you see "API configuration is missing" error, make sure to set the `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_KEY` environment variables in your `.env` file.
