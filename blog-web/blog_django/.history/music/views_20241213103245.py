# blog_django/music/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests_html import HTMLSession
from urllib.parse import quote
import re
import parsel

session = HTMLSession()

@api_view(['POST'])
def search_music(request):
    user_input = request.data.get('query', '')
    if not user_input:
        return Response({"error": "请输入歌手或歌曲名"}, status=status.HTTP_400_BAD_REQUEST)

    name = quote(user_input)
    search_url = f'https://www.gequbao.com/s/{name}'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    
    response = session.get(search_url, headers=headers).text
    selector = parsel.Selector(response)
    divs = selector.css('.row')[1:-1]
    
    music_data = []
    for div in divs[1:]:
        music_nama = div.css('.text-primary span::text').get()
        singer = div.css('.text-jade::text').get().strip()
        music_id = div.css('.music-link::attr(href)').get().strip().split('/')[-1]
        music_dit = {
            '歌名': music_nama,
            '歌手': singer,
            'music_id': music_id
        }
        music_data.append(music_dit)

    return Response(music_data)

@api_view(['POST'])
def download_music(request):
    music_id = request.data.get('music_id', '')
    if not music_id:
        return Response({"error": "音乐 ID 不能为空"}, status=status.HTTP_400_BAD_REQUEST)

    url = f'https://www.gequbao.com/music/{music_id}'
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    res = session.get(url, headers=headers).text
    play_id = re.findall('window.play_id = (.*?);', res)
    album_cover = re.findall('window.mp3_cover = (.*?);',res)[0]
    link = 'https://www.gequbao.com/api/play-url'
    parms = {
        'id': play_id[0]  # 确保 play_id 是字符串
    }
    res = session.post(link, headers=headers, data=parms).json()
    music_url = res['data']['url']

    return Response({"music_url": music_url})