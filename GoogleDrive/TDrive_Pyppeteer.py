import asyncio
from pyppeteer import launch

import json
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


pyppeteer_args = None
teamDriveDict = None

url = r'https://drive.google.com/drive/u/'
isCompleted = False


def save_pyppeteer_args():
    args = {
        'chromePath': r'*\Google\Chrome\Application\chrome.exe',
        'userDataDir': r'*\User Data',
        'userDataDir1': r'*\User Data 1',
        'userDataDir2': r'*\User Data 2',
    }

    with open(r'.cache/pyppeteer.args', 'w') as f:
        f.write(json.dumps(args, indent=4, separators=(',', ':')))


# save_pyppeteer_args()


def load_pyppeteer_args():
    global pyppeteer_args
    with open(r'.cache/pyppeteer.args', 'r') as f:
        pyppeteer_args = json.loads(f.read())


load_pyppeteer_args()
########################################################################################################################


def load_cache():
    global teamDriveDict
    with open(r'.cache/teamDriveDict.json', 'r') as f:
        teamDriveDict = json.loads(f.read())


def save_cache():
    global teamDriveDict
    with open(r'.cache/teamDriveDict.json', 'w') as f:
        f.write(json.dumps(teamDriveDict, indent=4, separators=(',', ':')))
########################################################################################################################


async def intercept_response(res):
    global teamDriveDict
    global isCompleted

    if res.request.resourceType == 'xhr' \
            and res.request.method == 'GET' \
            and 'content-type' in res.headers and 'json' in res.headers['content-type'] \
            and r'teamdrives?fields=' in res.request.url:

        resp = await res.json()

        if 'kind' in resp and resp['kind'] == 'drive#teamDriveList':
            for item in resp['items']:
                teamDriveDict[item['id']] = item

            if 'nextPageToken' not in resp and isCompleted is False:
                isCompleted = True
                print(f'isCompleted is {isCompleted}')
            if 'nextPageToken' in resp and isCompleted is True:
                isCompleted = False
                print(f'isCompleted is {isCompleted}')


async def main():
    global isCompleted

    load_cache()

    browser = await launch(
        executablePath=pyppeteer_args['chromePath'],
        userDataDir=pyppeteer_args['userDataDir2'],
        headless=False,
        # devtools=True,
        # autoClose=False,
        # defaultViewport=None,
        args=[
            '--disable-infobars',
            # f'--user-data-dir={pyppeteer_args['userDataDir2']}',
            # f'--profile-directory={pyppeteer_args['profileDir2']}',
        ]
    )

    page = await browser.newPage()
    page.on('response', intercept_response)
    # await page.setViewport({'width': 1200, 'height': 900})

    for i in range(0, 6):
        isCompleted = False
        await page.goto(
            url+str(i)+r'/my-drive',
            # waitUntil='load',
        )
        while isCompleted is False:
            await asyncio.sleep(5)

    save_cache()
    print("Saved!")

    await asyncio.sleep(5)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
