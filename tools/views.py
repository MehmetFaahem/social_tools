import requests
from django.shortcuts import render
from django.http import JsonResponse

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
        image_url = request.POST.get('image_url')
        url = "https://instagram-hashtags-generator.p.rapidapi.com/"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "instagram-hashtags-generator.p.rapidapi.com"
        }
        params = {"image_url": image_url, "name": "Image", "max_labels": "15", "min_confidence": "85"}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200 and 'hashtags' in data:
            return JsonResponse({'hashtags': data['hashtags']})
        else:
            return JsonResponse({'error': 'Failed to generate hashtags.'}, status=400)
    return render(request, 'tools/instagram_hashtag_generator.html')

def instagram_story_download(request):
    if request.method == 'POST':
        story_url = request.POST.get('url')
        url = "https://instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com/get-info-rapidapi"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com"
        }
        params = {"url": story_url}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200 and 'media' in data:
            return JsonResponse({'download_link': data['media']})
        else:
            return JsonResponse({'error': 'Failed to retrieve story link.'}, status=400)
    return render(request, 'tools/instagram_story_download.html')

def instagram_to_mp3(request):
    if request.method == 'POST':
        audio_url = request.POST.get('url')
        url = "https://instagram-audio-downloader.p.rapidapi.com/"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "instagram-audio-downloader.p.rapidapi.com"
        }
        params = {"url": audio_url}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200 and 'audio_link' in data:
            return JsonResponse({'download_link': data['audio_link']})
        else:
            return JsonResponse({'error': 'Failed to retrieve MP3 link.'}, status=400)
    return render(request, 'tools/instagram_to_mp3.html')

def instagram_photo_download(request):
    if request.method == 'POST':
        photo_url = request.POST.get('url')
        url = "https://instagram-photo-downloader.p.rapidapi.com/get-photo"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "instagram-photo-downloader.p.rapidapi.com"
        }
        params = {"url": photo_url}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200 and 'image_url' in data:
            return JsonResponse({'download_link': data['image_url']})
        else:
            return JsonResponse({'error': 'Failed to retrieve photo link.'}, status=400)
    return render(request, 'tools/instagram_photo_download.html')

def facebook_reel_download(request):
    if request.method == 'POST':
        reel_url = request.POST.get('url')
        url = "https://facebook-reels-downloader.p.rapidapi.com/get-video"
        headers = {
            "x-rapidapi-key": "03a60e6e87msh86247b7465ddf69p131bccjsn9e01b4bca8a9",
            "x-rapidapi-host": "facebook-reels-downloader.p.rapidapi.com"
        }
        params = {"url": reel_url}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200 and 'video_url' in data:
            return JsonResponse({'download_link': data['video_url']})
        else:
            return JsonResponse({'error': 'Failed to retrieve Facebook reel link.'}, status=400)
    return render(request, 'tools/facebook_reel_download.html')
