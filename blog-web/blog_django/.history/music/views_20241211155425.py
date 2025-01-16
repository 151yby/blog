# blog_django/music/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import quote
import re, parsel
import aiohttp
import asyncio

music_data = []

async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def fetch_play_url(session, play_id, headers):
    link = 'https://www.gequbao.com/api/play-url'
    parms = {'id': play_id}
    async with session.post(link, headers=headers, data=parms) as response:
        return await response.json()

async def derive_info(user_input):
    name = quote(user_input)
    search_url = f'https://www.gequbao.com/s/{name}'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, search_url, headers)
        selector = parsel.Selector(response)
        divs = selector.css('.row')[1:-1]
        music_data.clear()  # Clear previous music data

        tasks = []
        for div in divs:
            music_nama = div.css('.text-primary span::text').get()
            singer = div.css('.text-jade::text').get().strip()
            music_id = div.css('.music-link::attr(href)').get().strip().split('/')[-1]
            url = f'https://www.gequbao.com/music/{music_id}'

            # Fetch the music page
            tasks.append(fetch(session, url, headers))

        responses = await asyncio.gather(*tasks)

        for res in responses:
            play_id = re.findall('window.play_id = (.*?);', res)
            if play_id:
                play_url_response = await fetch_play_url(session, play_id[0], headers)
                music_url = play_url_response.get('data', {}).get('url', None)

                music_dit = {
                    'title': music_nama,
                    'singer': singer,
                    "url": music_url
                }
                music_data.append(music_dit)

    return music_data

@api_view(['POST'])
async def search_music(request):
    user_input = request.data.get('query', '')
    if not user_input:
        return Response({"error": "请输入歌手或歌曲名"}, status=400)

    music_data_result = await derive_info(user_input)  # Use the provided function to get music data
    return Response(music_data_result)