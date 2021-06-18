from tqdm import tqdm
import requests
import os
import json

cookie_header = {'X-Requested-With':'XMLHttpRequest'}
package_detail = 'https://dccon.dcinside.com/index/package_detail'
imgdownl_url = 'https://dcimg5.dcinside.com/dccon.php?no='
dccon_home = 'https://dccon.dcinside.com/'


while True: 
    os.system('cls')
    dccon_id = input("디시콘 ID= ")

    s = requests.Session()
    r = s.get(package_detail, headers=cookie_header)
    req = s.post(package_detail, headers=cookie_header, data={'ci_t':r.cookies['ci_c'], 'package_idx':dccon_id})

    json_data = req.json()

    default_dir = (os.path.abspath("./Downloads"))
    download_path = os.path.join(default_dir, json_data['info']['title'])
    title = json_data['info']['title']

    try:
        os.makedirs(download_path)
    except Exception as e:
        print(e)
    else:
        for item in tqdm(json_data['detail']):
            filename = item['title']+'.'+item['ext']
            image = s.get(imgdownl_url+item['path'], headers={'Referer': 'https://dccon.dcinside.com/'})
            with open(os.path.join(download_path, filename), 'wb') as fd:
                for chunk in image.iter_content(chunk_size=128):
                    fd.write(chunk)
                fd.close()
        s.close()
        print('다운로드 경로: ', download_path)
        print('디시콘: ', title, '(', dccon_id, ')','다운 완료')

    os.system("pause")
