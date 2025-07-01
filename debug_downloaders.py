#!/usr/bin/env python
"""
Debug script for Dailymotion and Shutterstock downloaders
"""
import os
import sys
import django
import yt_dlp

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_tools.settings')
django.setup()

def test_dailymotion():
    print("\n=== Testing Dailymotion ===")
    test_urls = [
        'https://www.dailymotion.com/video/x7tgad0',  # Popular video
        'https://www.dailymotion.com/video/x2btuie',  # Another test
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            ydl_opts = {
                'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
                'quiet': False,  # Enable output to see what's happening
                'no_warnings': False,
                'extract_flat': False,
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                print(f"✓ Successfully extracted info")
                print(f"  Title: {info.get('title', 'N/A')}")
                print(f"  Duration: {info.get('duration', 'N/A')}")
                print(f"  Formats available: {len(info.get('formats', []))}")
                
                if 'formats' in info:
                    for i, fmt in enumerate(info['formats'][:3]):  # Show first 3 formats
                        print(f"    Format {i+1}: {fmt.get('format_id')} - {fmt.get('ext')} - {fmt.get('height', 'N/A')}p")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")

def test_shutterstock():
    print("\n=== Testing Shutterstock ===")
    test_urls = [
        'https://www.shutterstock.com/video/clip-1017380344-happy-young-multiethnic-millennial-couples-dancing-laughing',
        'https://www.shutterstock.com/video/clip-1008893906-closeup-portrait-young-beautiful-girl-bright',
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            ydl_opts = {
                'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
                'quiet': False,  # Enable output to see what's happening
                'no_warnings': False,
                'extract_flat': False,
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                print(f"✓ Successfully extracted info")
                print(f"  Title: {info.get('title', 'N/A')}")
                print(f"  Duration: {info.get('duration', 'N/A')}")
                print(f"  Formats available: {len(info.get('formats', []))}")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")

def check_yt_dlp_version():
    print("=== yt-dlp Information ===")
    print(f"yt-dlp version: {yt_dlp.version.__version__}")
    
    # Check if these extractors are available
    extractors = ['dailymotion', 'shutterstock']
    from yt_dlp.extractor import get_info_extractor
    
    for extractor_name in extractors:
        try:
            extractor = get_info_extractor(extractor_name)
            print(f"✓ {extractor_name} extractor: Available")
        except Exception as e:
            print(f"✗ {extractor_name} extractor: Not available - {e}")

def main():
    print("Debugging Dailymotion and Shutterstock downloaders...")
    
    check_yt_dlp_version()
    test_dailymotion()
    test_shutterstock()
    
    print("\n=== Debug Complete ===")

if __name__ == '__main__':
    main() 