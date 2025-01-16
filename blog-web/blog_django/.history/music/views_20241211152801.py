from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import quote
from requests_html import HTMLSession
import re, parsel

@api_view(['POST'])
def search_music(request):
    user_input = request.data.get('query', '')
    if not user_input:
        return Response({"error": "请输入歌手或歌曲名"}, status=400)

    def derive_info(user_input):
        session = HTMLSession()
        music_data = []
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
        
        for div in divs:
            music_nama = div.css('.text-primary span::text').get()
            singer = div.css('.text-jade::text').get().strip()
            music_id = div.css('.music-link::attr(href)').get().strip().split('/')[-1]
            url = f'https://www.gequbao.com/music/{music_id}'
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "zh-CN,zh;q=0.9",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "referer": "https://www.gequbao.com/music/31046",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            }
            res = session.get(url, headers=headers).text
            play_id = re.findall('window.play_id = (.*?);', res)

            link = 'https://www.gequbao.com/api/play-url'
            parms = {
                'id': play_id
            }
            res = session.post(link, headers=headers, data=parms).json()
            if 'data' in res and 'url' in res['data']:
                music_url = res['data']['url']
        else:
            music_url = None  # or handle the error as needed

            music_dit = {
                'title': music_nama,
                'singer': singer,
                "url": music_url
            }
            music_data.append(music_dit)
        return music_data

    music_data = derive_info(user_input)  # 使用提供的函数获取音乐数据
    return Response(music_data)