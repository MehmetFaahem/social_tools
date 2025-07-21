import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import yt_dlp
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import os
import base64
import json
import re
from urllib.parse import urlparse, parse_qs

def homepage(request):
    return render(request, "tools/homepage.html")

def goto_homepage(request):
    return redirect('homepage')

def instagram_reel_download(request):
    if request.method == 'POST':
        try:
            reel_url = request.POST.get('url')
            url = "https://instagram-reels-downloader-api.p.rapidapi.com/download"
            headers = {
                "x-rapidapi-key": "cc092825dfmsha262f7b60dca253p158431jsne06852111435",
                "x-rapidapi-host": "instagram-reels-downloader-api.p.rapidapi.com"
            }
            params = {"url": reel_url}

            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if response.status_code == 200 and data.get('success'):
                # Get the video URL from the first media item
                if data['data']['medias'] and len(data['data']['medias']) > 0:
                    download_link = data['data']['medias'][0]['url']
                    return render(request, 'tools/instagram_reel_download.html', 
                                {'download_link': download_link})
            
            return render(request, 'tools/instagram_reel_download.html', 
                        {'error': 'Failed to retrieve reel link.'})
                        
        except Exception as e:
            return render(request, 'tools/instagram_reel_download.html', 
                        {'error': f'An error occurred: {str(e)}'})
            
    return render(request, 'tools/instagram_reel_download.html')

def instagram_hashtag_generator(request):
    if request.method == 'POST':
        keyword = request.POST.get('post_title', '')
        try:
            url = f"https://tags-generator.p.rapidapi.com/tiktokTags/{keyword}"
            headers = {
                "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
                "x-rapidapi-host": "tags-generator.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers)
  
            if response.status_code == 200:
                data = response.json()
                hashtags = data['data']['tags']
                return render(request, 'tools/instagram_hashtag_generator.html', 
                            {'hashtags': hashtags})
            else:
                return render(request, 'tools/instagram_hashtag_generator.html', 
                            {'error': 'Failed to generate hashtags.'})
                            
        except Exception as e:
            return render(request, 'tools/instagram_hashtag_generator.html', 
                        {'error': f'An error occurred: {str(e)}'})
            
    return render(request, 'tools/instagram_hashtag_generator.html')

def instagram_story_download(request):
    if request.method == 'POST':
        username = request.POST.get('url')
        url = f"https://instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com/{username}"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "instagram-scrapper-posts-reels-stories-downloader.p.rapidapi.com"
        }
        params = {"id": username}

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if response.status_code == 200 and data.get('data') and len(data['data']) > 0:
                # Get the first story URL (you might want to handle multiple stories differently)
                download_link = data['data'][0].get('url')
                if download_link:
                    return render(request, 'tools/instagram_story_download.html', {
                        'download_link': download_link
                    })
            
            return render(request, 'tools/instagram_story_download.html', {
                'error': 'No stories found for this user.'
            })
            
        except Exception as e:
            return render(request, 'tools/instagram_story_download.html', {
                'error': 'Failed to retrieve story. Please try again.'
            })
            
    return render(request, 'tools/instagram_story_download.html')

def instagram_to_mp3(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Create a temporary directory that will be automatically cleaned up
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download video using yt-dlp
                temp_video = os.path.join(temp_dir, 'temp_video.mp4')
                temp_audio = os.path.join(temp_dir, 'temp_audio.mp3')
                
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': temp_video,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                try:
                    # Extract audio and convert to MP3
                    video = VideoFileClip(temp_video)
                    video.audio.write_audiofile(temp_audio)
                    
                    # Read the audio file and create response
                    with open(temp_audio, 'rb') as audio_file:
                        audio_data = audio_file.read()
                    
                    # Create streaming response
                    response = HttpResponse(audio_data, content_type='audio/mpeg')
                    response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
                    
                    return response
                    
                finally:
                    # Ensure proper cleanup of resources
                    if video is not None:
                        video.close()
                        if video.audio is not None:
                            video.audio.close()
                
        except Exception as e:
            return render(request, 'tools/instagram_to_mp3.html', {'error': f'Failed to convert to MP3: {str(e)}'})
            
    return render(request, 'tools/instagram_to_mp3.html')

def instagram_photo_download(request):
    if request.method == 'POST':
        try:
            photo_url = request.POST.get('url')
            url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
            headers = {
                "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
                "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            payload = {"url": photo_url}

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200 and not data.get('error'):
                context = {
                    'photos': data['medias'],  # This contains the array of photo objects
                    'title': data.get('title', ''),
                    'author': data.get('author', '')
                }
                return render(request, 'tools/instagram_photo_download.html', context)
            
            return render(request, 'tools/instagram_photo_download.html', 
                        {'error': 'Failed to retrieve photos.'})
            
        except Exception as e:
            return render(request, 'tools/instagram_photo_download.html', 
                        {'error': f'An error occurred: {str(e)}'})
            
    return render(request, 'tools/instagram_photo_download.html')

def facebook_reel_download(request):
    if request.method == 'POST':
        try:
            reel_url = request.POST.get('url')
            url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"
            headers = {
                "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
                "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            payload = {"url": reel_url}

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200 and not data.get('error'):
                # Get HD quality video URL first, if available
                video_url = next((media['url'] for media in data['medias'] 
                                if media['type'] == 'video' and media['quality'] == 'HD'), None)
                
                # If HD not available, get SD quality
                if not video_url:
                    video_url = next((media['url'] for media in data['medias'] 
                                    if media['type'] == 'video' and media['quality'] == 'SD'), None)
                
                if video_url:
                    return render(request, 'tools/facebook_reel_download.html', 
                                {'download_link': video_url})
                                
            return render(request, 'tools/facebook_reel_download.html', 
                        {'error': 'Failed to retrieve Facebook reel link.'})
                        
        except Exception as e:
            return render(request, 'tools/facebook_reel_download.html', 
                        {'error': f'An error occurred: {str(e)}'})
            
    return render(request, 'tools/facebook_reel_download.html')

def ai_image_generator(request):
    if request.method == 'POST':
        try:
            prompt = request.POST.get('prompt')
            
            # Get configuration from Django settings
            from django.conf import settings
            cloudflare_account_id = getattr(settings, 'CLOUDFLARE_ACCOUNT_ID', None)
            cloudflare_api_key = getattr(settings, 'CLOUDFLARE_API_KEY', None)
            
            if not cloudflare_account_id or not cloudflare_api_key:
                return render(request, 'tools/ai_image_generator.html', 
                            {'error': 'Cloudflare API configuration is missing. Please set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_KEY environment variables.'})
            
            # Make request to Cloudflare Workers AI API
            url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {
                "Authorization": f"Bearer {cloudflare_api_key}",
                "Content-Type": "application/json"
            }
            payload = {"prompt": prompt}
            
            response = requests.post(url, headers=headers, json=payload)
            
            # Check if the response is an image
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                # Convert the image to base64
                image_data = base64.b64encode(response.content).decode('utf-8')
                base64_image = f"data:image/png;base64,{image_data}"
                
                return render(request, 'tools/ai_image_generator.html', 
                            {'image_data': base64_image})
            else:
                # Handle error response
                error_message = "Failed to generate image."
                try:
                    error_data = response.json()
                    if 'errors' in error_data and error_data['errors']:
                        error_message = error_data['errors'][0].get('message', error_message)
                except:
                    pass
                
                return render(request, 'tools/ai_image_generator.html', 
                            {'error': error_message})
                
        except Exception as e:
            return render(request, 'tools/ai_image_generator.html', 
                        {'error': f'An error occurred: {str(e)}'})
            
    return render(request, 'tools/ai_image_generator.html')

def extract_youtube_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/.*[?&]v=([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/user\/.*#.*\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/.*\/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def youtube_reel_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url', '').strip()
            
            if not video_url:
                return render(request, 'tools/youtube_reel_download.html', 
                            {'error': 'Please provide a valid YouTube URL.'})
            
            # Extract video ID for validation
            video_id = extract_youtube_video_id(video_url)
            if not video_id:
                return render(request, 'tools/youtube_reel_download.html', 
                            {'error': 'Invalid YouTube URL format. Please check the URL and try again.'})
            
            # Try multiple configurations for better success rate
            configurations = [
                # Configuration 1: Most compatible
                {
                    'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web'],
                            'player_skip': ['webpage'],
                            'skip': ['hls', 'dash']
                        }
                    }
                },
                # Configuration 2: Alternative with different client
                {
                    'format': 'best[height<=480][ext=mp4]/best[ext=mp4]/best',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android_embedded', 'android'],
                            'player_skip': ['webpage', 'dash'],
                        }
                    }
                },
                # Configuration 3: Basic fallback
                {
                    'format': 'worst[ext=mp4]/worst',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web'],
                        }
                    }
                }
            ]
            
            base_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,
                'socket_timeout': 60,
                'retries': 5,
                'fragment_retries': 5,
                'extractor_retries': 5,
                'file_access_retries': 5,
                'sleep_interval_requests': 2.0,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
                'http_headers': {
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
                }
            }
            
            info = None
            last_error = None
            
            # Try each configuration
            for i, config in enumerate(configurations):
                try:
                    ydl_opts = {**base_opts, **config}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        if info:
                            break
                except Exception as e:
                    last_error = e
                    continue
            
            if not info:
                if last_error:
                    raise last_error
                else:
                    raise Exception("Unable to extract video information after trying multiple configurations")
            
            # Get the best available download URL
            download_url = info.get('url')
            
            # If no direct URL, try to get from formats
            if not download_url and 'formats' in info:
                formats = info['formats']
                
                # Filter valid formats with URLs
                valid_formats = [f for f in formats if f.get('url') and f.get('vcodec') != 'none']
                
                if valid_formats:
                    # Prioritize formats with both video and audio
                    combined_formats = [f for f in valid_formats if f.get('acodec') != 'none']
                    
                    if combined_formats:
                        # Sort by quality and prefer mp4
                        combined_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4',
                            x.get('quality', 0)
                        ), reverse=True)
                        download_url = combined_formats[0]['url']
                    else:
                        # Fall back to video-only formats
                        valid_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4'
                        ), reverse=True)
                        download_url = valid_formats[0]['url']
            
            if not download_url:
                raise Exception("No downloadable format found for this video")
            
            # Format duration for display
            duration = info.get('duration', 0)
            duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
            
            # Format view count
            view_count = info.get('view_count', 0)
            if view_count >= 1000000:
                view_count_str = f"{view_count / 1000000:.1f}M views"
            elif view_count >= 1000:
                view_count_str = f"{view_count / 1000:.1f}K views"
            else:
                view_count_str = f"{view_count} views" if view_count else "Unknown views"
            
            context = {
                'download_link': download_url,
                'title': info.get('title', 'YouTube Video'),
                'duration': duration_str,
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': view_count_str,
                'upload_date': info.get('upload_date', ''),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                'video_id': video_id
            }
            
            return render(request, 'tools/youtube_reel_download.html', context)
            
        except yt_dlp.DownloadError as e:
            error_message = str(e)
            if 'Private video' in error_message or 'Sign in to confirm your age' in error_message:
                error_message = "This video is private or age-restricted and cannot be downloaded."
            elif 'Video unavailable' in error_message or 'This video is not available' in error_message:
                error_message = "This video is unavailable or has been removed."
            elif 'This video is only available for Music Premium members' in error_message:
                error_message = "This video requires YouTube Music Premium to access."
            elif 'Failed to extract any player response' in error_message:
                error_message = "YouTube has updated their systems. Please try again later or contact support."
            elif 'please report this issue' in error_message:
                error_message = "YouTube extraction is currently experiencing issues. Please try again in a few minutes."
            else:
                error_message = "YouTube download is temporarily unavailable. This is likely due to recent changes on YouTube's end. Please try again later."
                
            return render(request, 'tools/youtube_reel_download.html', {'error': error_message})
            
        except Exception as e:
            error_message = str(e)
            
            # Enhanced error handling
            if 'timeout' in error_message.lower():
                error_message = "Connection timeout. YouTube servers may be slow. Please try again in a few moments."
            elif 'connection' in error_message.lower() and ('reset' in error_message.lower() or 'aborted' in error_message.lower()):
                error_message = "Connection was reset by YouTube. This is common during high traffic. Please try again."
            elif 'network' in error_message.lower() or 'connection' in error_message.lower():
                error_message = "Network connection error. Please check your internet connection and try again."
            elif '429' in error_message:
                error_message = "Too many requests to YouTube. Please wait 5-10 minutes before trying again."
            elif '403' in error_message:
                error_message = "Access forbidden by YouTube. This video may be geo-blocked or temporarily restricted."
            elif 'regex' in error_message.lower() or 'unable to extract' in error_message.lower():
                error_message = "Unable to process this YouTube URL. YouTube may have changed their format. Please try again later."
            elif 'player response' in error_message.lower():
                error_message = "YouTube has updated their player. This is a temporary issue - please try again in a few minutes."
            elif not error_message or error_message == "":
                error_message = "YouTube download failed. This is likely due to recent changes on YouTube's platform. Please try again later."
            else:
                error_message = "YouTube download is currently experiencing issues. Please try again in a few minutes."
                
            return render(request, 'tools/youtube_reel_download.html', {'error': error_message})
            
    return render(request, 'tools/youtube_reel_download.html')

def extract_dailymotion_video_id(url):
    """Extract video ID from Dailymotion URL"""
    patterns = [
        r'dailymotion\.com/video/([a-zA-Z0-9]+)',
        r'dai\.ly/([a-zA-Z0-9]+)',
        r'dailymotion\.com/.*video/([a-zA-Z0-9]+)',
        r'dailymotion\.com/embed/video/([a-zA-Z0-9]+)',
        r'dailymotion\.com/player/x([a-zA-Z0-9]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def dailymotion_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url', '').strip()
            
            if not video_url:
                return render(request, 'tools/dailymotion_download.html', 
                            {'error': 'Please provide a valid Dailymotion URL.'})
            
            # Extract video ID for validation
            video_id = extract_dailymotion_video_id(video_url)
            if not video_id:
                return render(request, 'tools/dailymotion_download.html', 
                            {'error': 'Invalid Dailymotion URL format. Please check the URL and try again.'})
            
            # Try multiple configurations for better success rate
            configurations = [
                # Configuration 1: Standard with French geo-bypass
                {
                    'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
                    'geo_bypass': True,
                    'geo_bypass_country': 'FR',
                    'extractor_args': {
                        'dailymotion': {
                            'force_json_metadata': True,
                            'include_hls_manifests': False
                        }
                    }
                },
                # Configuration 2: Without geo-bypass
                {
                    'format': 'best[height<=480][ext=mp4]/best[ext=mp4]/best',
                    'extractor_args': {
                        'dailymotion': {
                            'force_json_metadata': False,
                            'include_hls_manifests': True
                        }
                    }
                },
                # Configuration 3: Basic fallback
                {
                    'format': 'worst[ext=mp4]/worst',
                    'extractor_args': {
                        'dailymotion': {}
                    }
                }
            ]
            
            base_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,
                'socket_timeout': 60,
                'retries': 5,
                'fragment_retries': 5,
                'extractor_retries': 5,
                'file_access_retries': 5,
                'sleep_interval_requests': 2.0,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            }
            
            info = None
            last_error = None
            
            # Try each configuration
            for i, config in enumerate(configurations):
                try:
                    ydl_opts = {**base_opts, **config}
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        if info:
                            break
                except Exception as e:
                    last_error = e
                    continue
            
            if not info:
                if last_error:
                    raise last_error
                else:
                    raise Exception("Unable to extract video information after trying multiple configurations")
            
            # Get the best available download URL
            download_url = info.get('url')
            
            # If no direct URL, try to get from formats
            if not download_url and 'formats' in info:
                formats = info['formats']
                
                # Filter valid formats with URLs and video codec
                valid_formats = [f for f in formats if f.get('url') and f.get('vcodec') != 'none']
                
                if valid_formats:
                    # Prioritize combined video+audio formats
                    combined_formats = [f for f in valid_formats if f.get('acodec') != 'none']
                    
                    if combined_formats:
                        # Sort by quality and prefer mp4
                        combined_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4',
                            x.get('quality', 0),
                            x.get('filesize', 0)
                        ), reverse=True)
                        download_url = combined_formats[0]['url']
                    else:
                        # Fall back to video-only formats
                        valid_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4',
                            x.get('quality', 0)
                        ), reverse=True)
                        download_url = valid_formats[0]['url']
            
            if not download_url:
                raise Exception("No downloadable format found for this video. The video may be geo-restricted, private, or require authentication.")
            
            # Format duration for display
            duration = info.get('duration', 0)
            duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
            
            # Format view count
            view_count = info.get('view_count', 0)
            if view_count >= 1000000:
                view_count_str = f"{view_count / 1000000:.1f}M views"
            elif view_count >= 1000:
                view_count_str = f"{view_count / 1000:.1f}K views"
            else:
                view_count_str = f"{view_count} views" if view_count else "Unknown views"
            
            # Format upload date
            upload_date = info.get('upload_date', '')
            if upload_date and len(upload_date) == 8:  # Format: YYYYMMDD
                try:
                    year, month, day = upload_date[:4], upload_date[4:6], upload_date[6:8]
                    upload_date_formatted = f"{day}/{month}/{year}"
                except:
                    upload_date_formatted = upload_date
            else:
                upload_date_formatted = upload_date
            
            context = {
                'download_link': download_url,
                'title': info.get('title', 'Dailymotion Video'),
                'duration': duration_str,
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': view_count_str,
                'upload_date': upload_date_formatted,
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                'video_id': video_id,
                'age_limit': info.get('age_limit', 0)
            }
            
            return render(request, 'tools/dailymotion_download.html', context)
            
        except yt_dlp.DownloadError as e:
            error_message = str(e)
            if 'Private video' in error_message or 'This video is private' in error_message:
                error_message = "This video is private and cannot be downloaded."
            elif 'Video unavailable' in error_message or 'This video is not available' in error_message:
                error_message = "This video is unavailable or has been removed from Dailymotion."
            elif 'Geoblocked' in error_message or 'geo-blocked' in error_message:
                error_message = "This video is geo-blocked in your region. Try using a VPN."
            elif 'Access denied' in error_message or '403' in error_message:
                error_message = "Access denied. This video may be restricted in your region."
            elif 'Age verification' in error_message or 'age-restricted' in error_message:
                error_message = "This video is age-restricted and requires verification."
            elif 'Unable to download JSON metadata' in error_message:
                error_message = "Dailymotion servers are currently having issues. Please try again in a few minutes."
            elif 'Connection aborted' in error_message or 'Connection reset' in error_message:
                error_message = "Connection was interrupted by Dailymotion servers. This is temporary - please try again."
            else:
                error_message = "Dailymotion download is temporarily unavailable. Please try again later."
                
            return render(request, 'tools/dailymotion_download.html', {'error': error_message})
            
        except Exception as e:
            error_message = str(e)
            
            # Enhanced error handling for Dailymotion-specific issues
            if 'connection aborted' in error_message.lower() or 'connection reset' in error_message.lower():
                error_message = "Connection was reset by Dailymotion servers. This is common during high traffic. Please try again in a few minutes."
            elif 'timeout' in error_message.lower() or 'read timed out' in error_message.lower():
                error_message = "Connection timeout with Dailymotion servers. Please try again in a few moments."
            elif 'network' in error_message.lower() or 'connection' in error_message.lower():
                error_message = "Network connection error. Please check your internet connection and try again."
            elif '10054' in error_message:
                error_message = "Dailymotion forcibly closed the connection. This is a temporary server issue - please try again in a few minutes."
            elif '429' in error_message or 'too many requests' in error_message.lower():
                error_message = "Too many requests to Dailymotion. Please wait 5-10 minutes before trying again."
            elif '404' in error_message or 'not found' in error_message.lower():
                error_message = "Video not found. Please check the URL and try again."
            elif '403' in error_message or 'forbidden' in error_message.lower():
                error_message = "Access denied by Dailymotion. This video may be geo-restricted or private."
            elif 'authentication' in error_message.lower() or 'login' in error_message.lower():
                error_message = "This video requires authentication to download."
            elif 'geo' in error_message.lower() and ('block' in error_message.lower() or 'restrict' in error_message.lower()):
                error_message = "This video is geo-blocked in your region. Try using a VPN with a French location."
            elif 'json metadata' in error_message.lower():
                error_message = "Dailymotion metadata servers are experiencing issues. Please try again in a few minutes."
            elif 'regex' in error_message.lower() or 'unable to extract' in error_message.lower():
                error_message = "Unable to process this Dailymotion URL. Dailymotion may have changed their format. Please try again later."
            elif 'transporterror' in error_message.lower():
                error_message = "Transport error occurred while connecting to Dailymotion. This is a temporary network issue - please try again."
            elif not error_message or error_message == "":
                error_message = "Dailymotion download failed. This is likely due to temporary server issues. Please try again later."
            else:
                error_message = "Dailymotion download is currently experiencing issues. Please try again in a few minutes."
                
            return render(request, 'tools/dailymotion_download.html', {'error': error_message})
            
    return render(request, 'tools/dailymotion_download.html')

def shutterstock_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Shutterstock heavily protects their content, so we need a more sophisticated approach
            ydl_opts = {
                'format': 'best[height<=720]/best[height<=480]/best',  # Lower quality for better success rate
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
                'socket_timeout': 45,
                'retries': 3,
                'fragment_retries': 3,
                'sleep_interval_requests': 1,  # Longer delay to avoid rate limiting
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                },
                # Try to extract preview/watermarked versions which are more accessible
                'extractor_args': {
                    'generic': {
                        'check_formats': True
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info with better error handling for Shutterstock
                info = ydl.extract_info(video_url, download=False)
                
                download_url = None
                
                if 'url' in info:
                    download_url = info['url']
                elif 'formats' in info and info['formats']:
                    formats = info['formats']
                    
                    # Filter for valid formats (Shutterstock often has preview videos)
                    valid_formats = [f for f in formats if f.get('url') and 'preview' not in f.get('format_id', '').lower()]
                    
                    # If no non-preview formats, accept preview formats
                    if not valid_formats:
                        valid_formats = [f for f in formats if f.get('url')]
                    
                    if valid_formats:
                        # Sort by quality and format preference
                        valid_formats.sort(key=lambda x: (
                            'preview' not in x.get('format_id', '').lower(),  # Prefer non-preview
                            x.get('height', 0),                              # Then by quality
                            x.get('ext') == 'mp4',                           # Prefer mp4
                        ), reverse=True)
                        download_url = valid_formats[0]['url']
                
                if not download_url:
                    # Try alternative approach - look for embedded video or preview
                    raise Exception("Shutterstock content is heavily protected. Only preview/watermarked versions may be available for download.")
                
                # Check if this is a watermarked/preview version
                is_preview = any('preview' in f.get('format_id', '').lower() for f in info.get('formats', []))
                preview_warning = " (Note: This may be a watermarked preview version)" if is_preview else ""
                
                context = {
                    'download_link': download_url,
                    'title': info.get('title', 'Shutterstock Video') + preview_warning,
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Shutterstock'),
                    'view_count': info.get('view_count', 0),
                    'warning': "Note: Shutterstock content is protected. Only preview/watermarked versions are typically available for download." if is_preview else ""
                }
                
                return render(request, 'tools/shutterstock_download.html', context)
                
        except Exception as e:
            error_message = str(e)
            # Enhanced error handling for Shutterstock-specific issues
            if '403' in error_message or 'forbidden' in error_message.lower():
                error_message = "Access denied. Shutterstock requires a paid subscription to download full-quality, non-watermarked videos. Only preview versions may be available."
            elif '404' in error_message or 'not found' in error_message.lower():
                error_message = "Video not found. Please check the URL and ensure it's a valid Shutterstock video link."
            elif 'timeout' in error_message.lower():
                error_message = "Connection timeout. Shutterstock servers may be slow. Please try again."
            elif 'protected' in error_message.lower() or 'authentication' in error_message.lower():
                error_message = "This content is protected. Shutterstock requires authentication and/or subscription for full access."
            elif 'no video' in error_message.lower() or 'no formats' in error_message.lower():
                error_message = "No downloadable video found. Shutterstock may have blocked access to this content."
            elif 'geo' in error_message.lower():
                error_message = "This content may be geo-restricted. Try using a VPN with a different location."
            else:
                error_message = f"Shutterstock download failed: {error_message}. Note: Shutterstock heavily protects their content and typically only allows downloading for paid subscribers."
                
            return render(request, 'tools/shutterstock_download.html', 
                        {'error': error_message, 
                         'info': "ℹ️ Shutterstock is a paid stock video service. Full-quality downloads typically require a subscription. Only preview/watermarked versions may be accessible without authentication."})
            
    return render(request, 'tools/shutterstock_download.html')

def about(request):
    return render(request, 'tools/about.html')

def contact(request):
    return render(request, 'tools/contact.html')

def youtube_to_mp3(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Validate YouTube URL
            video_id = extract_youtube_video_id(video_url)
            if not video_id:
                return JsonResponse({'error': 'Invalid YouTube URL format. Please check the URL and try again.'}, status=400)
            
            # Use new RapidAPI YouTube to MP3 converter
            api_url = "https://youtube-mp36.p.rapidapi.com/dl"
            
            querystring = {"id": video_id}
            
            headers = {
                "x-rapidapi-key": "cc092825dfmsha262f7b60dca253p158431jsne06852111435",
                "x-rapidapi-host": "youtube-mp36.p.rapidapi.com"
            }
            
            # Make the request to the API
            response = requests.get(api_url, headers=headers, params=querystring)
            
            if response.status_code != 200:
                return JsonResponse({'error': f'API Error: {response.status_code} - {response.text}'}, status=500)
            
            data = response.json()
            
            # Check if conversion is successful
            if data.get('status') == "ok":
                # Get the download URL and title
                download_url = data.get('link')
                title = data.get('title')
                
                if not download_url:
                    return JsonResponse({'error': 'Failed to get download URL from API'}, status=500)
                
                # Clean filename
                if title:
                    title = re.sub(r'[^\w\s-]', '', title).strip().lower()
                    title = re.sub(r'[-\s]+', '-', title)
                else:
                    title = 'youtube_audio'
                
                # Return JSON with download information
                return JsonResponse({
                    'success': True,
                    'download_url': download_url,
                    'title': title,
                    'status': 'COMPLETED'
                })
            else:
                # If not successful, return error
                error_msg = f"Conversion failed: {data.get('msg', 'Unknown error')}"
                return JsonResponse({'error': error_msg}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': f'Failed to convert to MP3: {str(e)}'}, status=500)
            
    return render(request, 'tools/youtube_to_mp3.html')

