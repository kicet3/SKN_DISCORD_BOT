import discord
from discord.ext import commands
import aiohttp
import io
import getLunchImg as GI  
# import numpy as np
# import cv2
import re
import os
from dotenv import load_dotenv

load_dotenv()

# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

restuarant_url = {
    '대륭 18차': 'https://pf.kakao.com/_YgxdPT/posts',
    '대륭 17차': 'https://pf.kakao.com/_xfWxfCxj/posts',
    '에이스 하이엔드 10차': 'https://pf.kakao.com/_rXxkCn/posts'
}

pattern = re.compile(r'(중식|점심)')
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='점심')
async def lunch(ctx):
    for target_key, target_url in restuarant_url.items():
        image_url = await GI.get_img(target_url)
        try: 
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        await ctx.send("이미지 다운로드에 실패했습니다.")
                        return

                    data = await resp.read()
                    '''
                        주석 처리 된 부분은 이미지를 바탕으로 점심 | 중식 텍스트를 필터링하는 코드입니다.
                        현재 주석된 이유는 OCR 기능이 정확도가 떨어져 정상적인 데이터라도 인식하지 못하는 경우가 있어 주석처리 하였습니다.
                    '''
                    # image_data = io.BytesIO(data)
                    # image_bytes = np.asarray(bytearray(data), dtype=np.uint8)
                    # img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

                    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # text = pytesseract.image_to_string(gray, lang="kor")

                    # if pattern.search(text):
                    send_image_data = io.BytesIO(data)
                    await ctx.send(f"{target_key} 점심 메뉴\n", file=discord.File(send_image_data, filename="image.png"))
                    # else:
                    #     await ctx.send("점심 메뉴 정보가 존재하지 않습니다.")

        except Exception as e:
            print(e)
            await ctx.send(f"에러가 발생했습니다. 관리자에게 문의하거나 [{target_url}] 해당 URL에서 확인해주세요")
    
    await ctx.send('메뉴 정보 전송 완료')
    return 

@bot.command(name='명령어')
async def helpcommand(ctx):
    await ctx.send('''!를 맨 앞에 붙여 명령어를 실행합니다.\n  점심 : 구내식당 메뉴 정보 (중식만 제공)\n  명령어 : 명령어 정보를 제공합니다.''')
    return 

bot.run(os.getenv('DISCORD_API'))
