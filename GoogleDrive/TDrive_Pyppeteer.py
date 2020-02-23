import asyncio
from pyppeteer import launch

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


from .Cache import cache

url = r'https://drive.google.com/drive/u/'
isCompleted = False


async def intercept_response(res):

    global isCompleted

    if res.request.resourceType == 'xhr' \
            and res.request.method == 'GET' \
            and 'content-type' in res.headers and 'json' in res.headers['content-type'] \
            and r'teamdrives?fields=' in res.request.url:

        resp = await res.json()

        if 'kind' in resp and resp['kind'] == 'drive#teamDriveList':
            print(resp)
            for item in resp['items']:
                cache.TeamDriveDict[item['id']] = item

            if 'nextPageToken' not in resp and isCompleted is False:
                isCompleted = True
                print(f'isCompleted is {isCompleted}')
            if 'nextPageToken' in resp and isCompleted is True:
                isCompleted = False
                print(f'isCompleted is {isCompleted}')


async def main():
    global isCompleted
    global url

    browser = await launch(
        executablePath=cache.pyppeteer_args['chromePath'],
        userDataDir=cache.pyppeteer_args['userDataDir1'],
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

    for i in range(0, 1):
        isCompleted = False
        await page.goto(
            url+str(i)+r'/shared-drives',
            # waitUntil='load',
        )
        while isCompleted is False:
            await asyncio.sleep(5)
        # goto 'shared-drives' will not request hidden drive list.

        """
        isCompleted = False
        await page.goto(
            url+str(i)+r'/shared-drives-hidden',
            # waitUntil='load',
        )
        while isCompleted is False:
            await asyncio.sleep(5)
        """
        # goto 'shared-drives-hidden' will request un-hidden drive list again.

    cache.TeamDriveDict = None  # do save actually!
    print("Saved!")

    await asyncio.sleep(5)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
