import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import yt_dlp
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import os
import base64

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
            video = None
            
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

def youtube_reel_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Use yt-dlp to get video info and download URL with more flexible format selection
            ydl_opts = {
                'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',  # Progressive fallback
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(video_url, download=False)
                
                # Get the download URL - yt-dlp will have selected the best available format
                download_url = None
                
                if 'url' in info:
                    # Direct URL available
                    download_url = info['url']
                elif 'formats' in info and info['formats']:
                    # Multiple formats available, get the best one
                    formats = info['formats']
                    
                    # Try to get formats with both video and audio first
                    video_audio_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url')]
                    
                    if video_audio_formats:
                        # Sort by quality and prefer mp4
                        video_audio_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4',
                            x.get('format_id', '').startswith('18')  # Prefer format 18 (360p mp4)
                        ), reverse=True)
                        download_url = video_audio_formats[0]['url']
                    else:
                        # Fallback to any available format
                        available_formats = [f for f in formats if f.get('url')]
                        if available_formats:
                            download_url = available_formats[0]['url']
                
                if not download_url:
                    raise Exception("No downloadable format found for this video")
                
                context = {
                    'download_link': download_url,
                    'title': info.get('title', 'YouTube Video'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0)
                }
                
                return render(request, 'tools/youtube_reel_download.html', context)
                
        except Exception as e:
            error_message = str(e)
            # Clean up the error message for better user experience
            if 'Requested format is not available' in error_message:
                error_message = "This video format is not available for download. Please try a different video."
            elif 'Private video' in error_message:
                error_message = "This video is private and cannot be downloaded."
            elif 'Video unavailable' in error_message:
                error_message = "This video is unavailable or has been removed."
            else:
                error_message = f"Failed to retrieve video: {error_message}"
                
            return render(request, 'tools/youtube_reel_download.html', 
                        {'error': error_message})
            
    return render(request, 'tools/youtube_reel_download.html')

def dailymotion_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Use yt-dlp with enhanced configuration for Dailymotion
            ydl_opts = {
                'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
                'socket_timeout': 30,
                'retries': 5,
                'fragment_retries': 5,
                'sleep_interval_requests': 0.5,  # Add delay between requests
                'geo_bypass': True,  # Try to bypass geo-restrictions
                'geo_bypass_country': 'US',  # Use US as fallback country
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info with better error handling
                info = ydl.extract_info(video_url, download=False)
                
                # Get the download URL - yt-dlp will have selected the best available format
                download_url = None
                
                if 'url' in info:
                    # Direct URL available
                    download_url = info['url']
                elif 'formats' in info and info['formats']:
                    # Multiple formats available, get the best one
                    formats = info['formats']
                    
                    # Filter out invalid formats
                    valid_formats = [f for f in formats if f.get('url') and f.get('vcodec') != 'none']
                    
                    if valid_formats:
                        # Prefer formats with audio, then by quality
                        valid_formats.sort(key=lambda x: (
                            x.get('acodec', 'none') != 'none',  # Prefer formats with audio
                            x.get('height', 0),                # Then by video quality
                            x.get('ext') == 'mp4',             # Prefer mp4
                            x.get('filesize', 0)               # Then by file size
                        ), reverse=True)
                        download_url = valid_formats[0]['url']
                
                if not download_url:
                    raise Exception("No downloadable format found for this video. The video may be geo-restricted or require authentication.")
                
                context = {
                    'download_link': download_url,
                    'title': info.get('title', 'Dailymotion Video'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0)
                }
                
                return render(request, 'tools/dailymotion_download.html', context)
                
        except Exception as e:
            error_message = str(e)
            # Enhanced error handling for Dailymotion-specific issues
            if 'timeout' in error_message.lower() or 'read timed out' in error_message.lower():
                error_message = "Connection timeout with Dailymotion servers. Please try again in a few moments."
            elif '429' in error_message or 'too many requests' in error_message.lower():
                error_message = "Too many requests to Dailymotion. Please wait a few minutes before trying again."
            elif '403' in error_message or 'forbidden' in error_message.lower():
                error_message = "Access denied. This video may be geo-restricted or private."
            elif '404' in error_message or 'not found' in error_message.lower():
                error_message = "Video not found. Please check the URL and try again."
            elif 'unavailable' in error_message.lower():
                error_message = "This video is no longer available on Dailymotion."
            elif 'geo' in error_message.lower() and 'block' in error_message.lower():
                error_message = "This video is geo-blocked in your region."
            elif 'authentication' in error_message.lower() or 'login' in error_message.lower():
                error_message = "This video requires authentication to download."
            else:
                error_message = f"Failed to retrieve video: {error_message}. Try using a VPN if the video is geo-restricted."
                
            return render(request, 'tools/dailymotion_download.html', 
                        {'error': error_message})
            
    return render(request, 'tools/dailymotion_download.html')

def shutterstock_download(request):
    if request.method == 'POST':
        try:
            video_url = request.POST.get('url')
            
            # Use yt-dlp to get video info and download URL with more flexible format selection
            ydl_opts = {
                'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',  # Progressive fallback
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(video_url, download=False)
                
                # Get the download URL - yt-dlp will have selected the best available format
                download_url = None
                
                if 'url' in info:
                    # Direct URL available
                    download_url = info['url']
                elif 'formats' in info and info['formats']:
                    # Multiple formats available, get the best one
                    formats = info['formats']
                    
                    # Try to get formats with both video and audio first
                    video_audio_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url')]
                    
                    if video_audio_formats:
                        # Sort by quality and prefer mp4
                        video_audio_formats.sort(key=lambda x: (
                            x.get('height', 0),
                            x.get('width', 0),
                            x.get('ext') == 'mp4'
                        ), reverse=True)
                        download_url = video_audio_formats[0]['url']
                    else:
                        # Fallback to any available format
                        available_formats = [f for f in formats if f.get('url')]
                        if available_formats:
                            download_url = available_formats[0]['url']
                
                if not download_url:
                    raise Exception("No downloadable format found for this video")
                
                context = {
                    'download_link': download_url,
                    'title': info.get('title', 'Shutterstock Video'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0)
                }
                
                return render(request, 'tools/shutterstock_download.html', context)
                
        except Exception as e:
            error_message = str(e)
            # Clean up the error message for better user experience
            if 'Requested format is not available' in error_message:
                error_message = "This video format is not available for download. Please try a different video."
            elif 'HTTP Error 403' in error_message or 'forbidden' in error_message.lower():
                error_message = "Access denied. This content may be protected or require authentication."
            elif 'HTTP Error 404' in error_message or 'not found' in error_message.lower():
                error_message = "Video not found. Please check the URL and try again."
            elif 'timeout' in error_message.lower():
                error_message = "Connection timeout. Please try again later."
            else:
                error_message = f"Failed to retrieve video: {error_message}"
                
            return render(request, 'tools/shutterstock_download.html', 
                        {'error': error_message})
            
    return render(request, 'tools/shutterstock_download.html')

def about(request):
    return render(request, 'tools/about.html')

def contact(request):
    return render(request, 'tools/contact.html')

