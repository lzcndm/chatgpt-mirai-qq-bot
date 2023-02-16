import aiohttp
import asyncio
import json
from PIL import Image
import io
import base64

# default_payload = json.dumps({
#   "prompt": "best quality, ultra high res, (photorealistic:1.4), 1girl, brown blazer, black skirt, glasses, thighhighs, ((school uniform)), (upper body), (Kpop idol), (aegyo sal:1), (platinum blonde hair:1), ((puffy eyes)), looking at viewer, facing front, smiling, laughing, <lora:koreanDollLikeness_v10:0.66>,ulzzang-6500",
# #   "seed": -1,
# #   "batch_size": 1,
#   "steps": 25,
#   "cfg_scale": 7.5,
#   "width": 512,
#   "height": 512,
#   "negative_prompt": "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glan",
#   "sampler_index": "DPM++ SDE Karras"
# })
default_payload = json.dumps({
  "prompt": "best quality, ultra high res, (photo realistic:1.4),1 girl ,(depth of field:1.4), (pov:1.2),(looking at camera:1.4), (symmetry:1.2),(portrait:1.4),(close-up:1.2), 28 years old, (bedroom:1.4),(sitting on bed:1.2), (pale skin),(aegyo sal:1.4),(Kpop idol:1.2),(silver blonde color hair:1.2),(large breasts:1), (bare top mini dress:1.4), <lora:koreanDollLikeness_v10:0.7>,ulzzang-6500",
#   "seed": -1,
#   "batch_size": 1,
  "steps": 30,
  "cfg_scale": 7.5,
  "width": 512,
  "height": 512,
  "negative_prompt": "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.6),DeepNegative,facing away, looking away,tilted head, dutch angle,neckless,nipple,(fat:1.2)",
  "sampler_index": "DPM++ 2M Karras"
})

async def get_image(url, payload=None, authorization=""):
    basic_auth = base64.b64encode(authorization.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': 'Basic {}'.format(basic_auth),
        'Content-Type': 'application/json'
    }
    if not payload:
        payload = default_payload
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as resp:
            if resp.status != 200:
                return '连接失败'
            res = await resp.json()
            return 'data:image/png;base64,' + res['images'][0]

async def main():
    from config import Config
    config = Config.load_config()
    # url = "https://7da10151-4490-4b21.gradio.live/sdapi/v1/txt2img"
    image_str = await get_image(config.stable_diffusion.url, authorization=config.stable_diffusion.auth)
    image = Image.open(io.BytesIO(base64.b64decode(image_str.split(",",1)[0])))
    image.save('output.png')

if __name__ == '__main__':
    asyncio.run(main())

# response = requests.request("POST", url, headers=headers, data=payload)

# r = response.json()
# print(r)

# image = Image.open(io.BytesIO(base64.b64decode(r['images'][0].split(",",1)[0])))

