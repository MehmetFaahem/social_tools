import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import yt_dlp
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import os

def homepage(request):
    return render(request, "tools/homepage.html")

def instagram_reel_download(request):
    if request.method == 'POST':
        try:
            shortcode = request.POST.get('url').split('/')[4]
            url = f"https://instagram-bulk-scraper-latest.p.rapidapi.com/media_info_from_shortcode/{shortcode}"
            headers = {
                "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
                "x-rapidapi-host": "instagram-bulk-scraper-latest.p.rapidapi.com"
                
            }

            response = requests.get(url, headers=headers)
            data = response.json()
            
            if response.status_code == 200 and 'data' in data and 'video_url' in data['data']:
                return render(request, 'tools/instagram_reel_download.html', 
                            {'download_link': data['data']['video_url']})
            else:
                return render(request, 'tools/instagram_reel_download.html', 
                            {'error': 'Failed to retrieve reel link.'})
        except Exception as e:
            return render(request, 'tools/instagram_reel_download.html', 
                        {'error': 'An error occurred. Please try again.'})
            
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
