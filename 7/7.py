import asyncio
from pyppeteer import launch
from pyppeteer.network_manager import Response

import os
import json
from io import StringIO
import copy

import pyamf
from pyamf import remoting as pyamf_remoting

import chardet

########################################################################################################################


def patch_pyppeteer():
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method

patch_pyppeteer()

# https://github.com/miyakogi/pyppeteer/pull/160
########################################################################################################################

with open(
        os.path.join(
            os.path.dirname(__file__),
            r".cache/.json"
        ),
        'r'
) as f:
    cache = json.loads(f.read())
    # cache = eval(f.read())
########################################################################################################################


async def intercept_response(res: Response):
    if res.request.resourceType == 'other' \
            and res.request.method == 'POST' \
            and 'content-type' in res.headers \
            and 'amf' in res.headers['content-type']:

        res_body: bytes = await res.buffer()
        # failed to return raw bytes!!!
        # print(chardet.detect(res_body))


        # res_body_b = res_body.encode()
        # with open(r'.cache/amf_res', 'wb') as f:
        #     f.write(res_body_b)
        # with open(r'.cache/amf_res', 'rb') as f:
        #     content = f.read()

        try:
            # Failed to decode amf!!!
            amf = pyamf_remoting.decode(res_body)
            print("successed!!")
        except Exception as e:
            print(e)
            print(res_body)
        # print(res_body)
        # print(amf)


async def intercept_request(req):
    if req.resourceType == 'other' \
            and req.method == 'POST' \
            and 'content-type' in req.headers \
            and 'amf' in req.headers['content-type']:

        req_body = req.postData
        # amf = pyamf_remoting.decode(req_body)
        amf = pyamf.decode(req_body)
        # await req.abort()
        print(req_body)
        print(amf)

########################################################################################################################


async def main():

    browser = await launch(
        executablePath=cache["pyppeteer"]['chromePath'],
        userDataDir=cache["pyppeteer"]['userDataDir'],
        headless=False,
        # devtools=True,
        # autoClose=False,
        # defaultViewport=None,
        args=[
            '--disable-infobars',
            # '--no-sandbox',
            # f'--user-data-dir={pyppeteer_args['userDataDir2']}',
            # f'--profile-directory={pyppeteer_args['profileDir2']}',
        ]
    )

    page = (await browser.pages())[0]
    await page.setViewport({'width': 1200, 'height': 900})

    # await page.setRequestInterception(True)
    # page.on('request', intercept_request)
    page.on('response', intercept_response)

    await page.goto(
        cache["game"]['url'],
        # waitUntil='load',
    )

    await asyncio.sleep(300)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())


# with open(r'.cache/amf', 'rb') as f:
#     content = f.read()
#     decoded = pyamf_remoting.decode(content)
#     print(decoded)
