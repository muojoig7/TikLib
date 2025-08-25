import asyncio,urllib,aiohttp
from user_agent import generate_user_agent
from SignerPy import *
import requests, SignerPy, json, secrets, uuid, binascii, os, time, random
class TikExt:
    @staticmethod
    def xor(string):
          return "".join([hex(ord(c) ^ 5)[2:] for c in string])
    def GetLevel(self, username):
        username = username.strip().lstrip('@')
        url = f'https://www.tiktok.com/@{username}'
        headers = {'User-Agent': str(generate_user_agent())}

        try:  
            response = requests.get(url, headers=headers)  
            if '{"userInfo":{' in response.text:  
                # محاولة استخراج معرف المستخدم من كتلة userInfo
                match = re.search(r'"userInfo":\{.*?"id":"([^"]+)"', response.text)  
                if match:  
                    user_id = match.group(1)  
            elif '"user":{"id":"' in response.text:  
                # محاولة استخراج معرف المستخدم من كتلة user
                match = re.search(r'"user":{"id":"([^"]+)"', response.text)  
                if match:  
                    user_id = match.group(1)  
            else:
                user_id = None

            # الرجوع إلى API tikwm.com إذا فشل الاستخراج المباشر
            if not user_id:
                api_url = f"https://www.tikwm.com/api/user/info?unique_id={username}"  
                api_response = requests.get(api_url)  
                if api_response.status_code == 200:  
                    data = api_response.json()  
                    if data.get("code") == 0 and "data" in data:  
                        user_id = data["data"]["user"]["id"]  

            if not user_id:
                return None, None
            #print(f"معرف المستخدم لـ @{username}: {user_id}")
            user_details, raw_response = self.get_tiktok_user_details(user_id)

            if user_details and user_details.get('status_code') == 0:  
                data = user_details.get('data', {})  
                badge_list = data.get('badge_list', [])  
                for badge in badge_list:  
                    combine = badge.get('combine', {})  
                    if combine and 'text' in combine:  
                        text_data = combine.get('text', {})  
                        if 'default_pattern' in text_data:  
                            aa = text_data.get('default_pattern')  
                            return {'status':'Good','Level':text_data['default_pattern'],'Dev':'Mustafa','Telegram':'@PPH9P'}
                return user_id, user_details  
            else:
                return {'status':'Bad','Dev':'Mustafa','Telegram':'@PPH9P'}
                #print("فشل في الحصول على تفاصيل المستخدم أو الكود يحتاج تجديد.")  
                return user_id, None  

        except Exception as e:  
            #print(f"حدث خطأ أثناء الحصول على معرف المستخدم: {e}")
            return {'status':'Bad','Info':e,'Dev':'Mustafa','Telegram':'@PPH9P'}  
            return None, None
    def get_tiktok_user_details(self, user_id, custom_headers=None, custom_params=None):
        """
        يحصل على تفاصيل المستخدم من TikTok باستخدام معرف المستخدم.
        """
        url = "https://webcast22-normal-c-alisg.tiktokv.com/webcast/user/"

        # استخدام رؤوس افتراضية إذا لم يتم توفير رؤوس مخصصة  
        headers = {  
            "Host": "webcast22-normal-c-alisg.tiktokv.com",  
            "cookie": "store-idc=alisg; passport_csrf_token=20e9da8b0e16abaa45d4ce2ad75a1325; passport_csrf_token_default=20e9da8b0e16abaa45d4ce2ad75a1325; d_ticket=913261767c3f16148c133796e661c1d83cf5d; multi_sids=7464926696447099909%3A686e699e8bbbc4e9f5e08d31c038c8e4; odin_tt=e2d5cd703c2e155d572ad323d28759943540088ddc6806aa9a9b48895713be4b585e78bf3eb17d28fd84247c4198ab58fab17488026468d3dde38335f4ab928ad1b9bd82a2fb5ff55da00e3368b4d215; cmpl_token=AgQQAPMsF-RPsLemUeAYPZ08_KeO5HxUv5IsYN75Vg; sid_guard=686e699e8bbbc4e9f5e08d31c038c8e4%7C1751310846%7C15552000%7CSat%2C+27-Dec-2025+19%3A14%3A06+GMT; uid_tt=683a0288ad058879bbc16d3b696fa815e1d72c050bdb2d14b824141806068417; uid_tt_ss=683a0288ad058879bbc16d3b696fa815e1d72c050bdb2d14b824141806068417; sid_tt=686e699e8bbbc4e9f5e08d31c038c8e4; sessionid=686e699e8bbbc4e9f5e08d31c038c8e4; sessionid_ss=686e699e8bbbc4e9f5e08d31c038c8e4; store-country-code=eg; store-country-code-src=uid; tt-target-idc=alisg; ttwid=1%7Cmdx9QyT3L35S3CFNpZ_6a1mG2Q3hbfWvwQh6gY5hjhw%7C1751310949%7C253ef523ddc8960c5f52b286d8ce0afc2623ec081a777dac3ba5606ecdc1bd40; store-country-sign=MEIEDPH3p6xlgJXYVovbBgQgMf22gnCf0op7iOSSy6oKKB7paF60OVLAsxbGkh6BUGAEEF0aMxzItZZ03IrkjedsuYY; msToken=Srtgt7p6ncYXI8gph0ecExfl9DpgLtzOynFNZjVGLkKUjqV0J1JI8aBoE8ERmO5f43HQhtJxcU2FeJweSbFIlIOADOHP_z75VvNeA2hp5LN1JZsKgj-wymAdEVJt",  
            "x-tt-pba-enable": "1",  
            "x-bd-kmsv": "0",  
            "x-tt-dm-status": "login=1;ct=1;rt=1",  
            "live-trace-tag": "profileDialog_batchRequest",  
            "sdk-version": "2",  
            "x-tt-token": "034865285659c6477b777dec3ab5cd0aa70363599c1acde0cd4e911a51fed831bdb2ec80a9a379e8e66493471e519ccf05287299287a55f0599a72988865752a3668a1a459177026096896cf8d50b6e8b5f4cec607bdcdee5a5ce407e70ce91d52933--0a4e0a20da4087f3b0e52a48822384ac63e937da36e5b0ca771f669a719cf633d66f8aed12206a38feb1f115b80781d5cead8068600b779eb2bba6c09d8ae1e6a7bc44b46b931801220674696b746f6b-3.0.0",  
            "passport-sdk-version": "6031490",  
            "x-vc-bdturing-sdk-version": "2.3.8.i18n",  
            "x-tt-request-tag": "n=0;nr=011;bg=0",  
            "x-tt-store-region": "eg",  
            "x-tt-store-region-src": "uid",  
            "rpc-persist-pyxis-policy-v-tnc": "1",  
            "x-ss-dp": "1233",  
            "x-tt-trace-id": "00-c24dca7d1066c617d7d3cb86105004d1-c24dca7d1066c617-01",  
            "user-agent": "com.zhiliaoapp.musically/2023700010 (Linux; U; Android 11; ar; SM-A105F; Build/RP1A.200720.012; Cronet/TTNetVersion:f6248591 2024-09-11 QuicVersion:182d68c8 2024-05-28)",  
            "accept-encoding": "gzip, deflate, br",  
            "x-tt-dataflow-id": "671088640"  
        }  

        if custom_headers:  # دمج الرؤوس المخصصة  
            headers.update(custom_headers)  

        # استخدام معلمات افتراضية إذا لم يتم توفير معلمات مخصصة  
        params = {  
            "user_role": '{"7464926696447099909":1,"7486259459669820432":1}',  
            "request_from": "profile_card_v2",  
            "sec_anchor_id": "MS4wLjABAAAAiwBH59yM2i_loS11vwxZsudy4Bsv5L_EYIkYDmxgf-lv3oZL4YhQCF5oHQReiuUV",  
            "request_from_scene": "1",  
            "need_preload_room": "false",  
            "target_uid": user_id,  
            "anchor_id": "246047577136308224",  
            "packed_level": "2",  
            "need_block_status": "true",  
            "current_room_id": "7521794357553400594",  
            "device_platform": "android",  
            "os": "android",  
            "ssmix": "a",  
            "_rticket": "1751311566864",  
            "cdid": "808876f8-7328-4885-857d-8f15dd427861",  
            "channel": "googleplay",  
            "aid": "1233",  
            "app_name": "musical_ly",  
            "version_code": "370001",  
            "version_name": "37.0.1",  
            "manifest_version_code": "2023700010",  
            "update_version_code": "2023700010",  
            "ab_version": "37.0.1",  
            "resolution": "720*1382",  
            "dpi": "280",  
            "device_type": "SM-A105F",  
            "device_brand": "samsung",  
            "language": "ar",  
            "os_api": "30",  
            "os_version": "11",  
            "ac": "wifi",  
            "is_pad": "0",  
            "current_region": "IQ",  
            "app_type": "normal",  
            "sys_region": "IQ",  
            "last_install_time": "1751308971",  
            "timezone_name": "Asia/Baghdad",  
            "residence": "IQ",  
            "app_language": "ar",  
            "timezone_offset": "10800",  
            "host_abi": "armeabi-v7a",  
            "locale": "ar",  
            "content_language": "ar,",  
            "ac2": "wifi",  
            "uoo": "1",  
            "op_region": "IQ",  
            "build_number": "37.0.1",  
            "region": "IQ",  
            "ts": "1751311566",  
            "iid": "7521814657976928001",  
            "device_id": "7405632852996097552",  
            "openudid": "c79c40b21606bf59",  
            "webcast_sdk_version": "3610",  
            "webcast_language": "ar",  
            "webcast_locale": "ar_IQ",  
            "es_version": "3",  
            "effect_sdk_version": "17.6.0",  
            "current_network_quality_info": '{"tcp_rtt":16,"quic_rtt":16,"http_rtt":584,"downstream_throughput_kbps":1400,"quic_send_loss_rate":-1,"quic_receive_loss_rate":-1,"net_effective_connection_type":3,"video_download_speed":1341}'  
        }  

        if custom_params:  # دمج المعلمات المخصصة  
            params.update(custom_params)  

        try:  
            # توقيع الطلب باستخدام SignerPy
            up = get(params=params)  
            def parse_cookie_string(cookie_string):  
                cookie_dict = {}  
                for item in cookie_string.split(';'):  
                    if item.strip():  
                        try:  
                            key, value = item.strip().split('=', 1)  
                            cookie_dict[key.strip()] = value.strip()  
                        except ValueError:  
                            cookie_dict[item.strip()] = ''  
                return cookie_dict  
            cookie_dict = parse_cookie_string(headers["cookie"])  
            sg = sign(params=up, cookie=cookie_dict)  

            headers.update({  
                'x-ss-req-ticket': sg['x-ss-req-ticket'],  
                'x-ss-stub': sg['x-ss-stub'],  
                'x-argus': sg["x-argus"],  
                'x-gorgon': sg["x-gorgon"],  
                'x-khronos': sg["x-khronos"],  
                'x-ladon': sg["x-ladon"],  
            })  
            headers["accept-encoding"] = "identity"  
            response = requests.get(url, headers=headers, params=params)  

            try:  
                json_data = response.json()  
                if json_data.get('status_code') != 0:  
                    return "الكود يحتاج تجديد (قد يكون بسبب انتهاء صلاحية الكوكيز أو التوقيع)"  

                # معالجة البيانات المتدفقة (إذا كانت موجودة)  
                streamed_content = ""  
                for line in response.iter_lines():  
                    if line:  
                        decoded_line = line.decode('utf-8')  
                        if decoded_line.startswith('data: '):  
                            json_part = decoded_line[6:]  
                            try:  
                                data_part = json.loads(json_part)  
                                if 'choices' in data_part and len(data_part['choices']) > 0:  
                                    delta = data_part['choices'][0].get('delta', {})  
                                    if 'content' in delta and delta['content']:  
                                        streamed_content += delta['content']  
                            except json.JSONDecodeError:  
                                continue  
                if streamed_content:  
                    print(f"محتوى متدفق: {streamed_content}")  

                return json_data, response  
            except json.JSONDecodeError:  
                return  "الكود يحتاج تجديد (فشل في فك تشفير JSON)" 
                return None, response  
            except Exception as e:  
                return f"حدث خطأ أثناء معالجة الاستجابة: {e}"  
                return None, response  

        except Exception as e:  
            return f"حدث خطأ أثناء إرسال الطلب: {e}"
            return None, None
    def GetUser(self,es):
        secret = secrets.token_hex(16)
        xor_email=self.xor(es)
        params = {
            "request_tag_from": "h5",
            "fixed_mix_mode": "1",
            "mix_mode": "1",
            "account_param": xor_email,
            "scene": "1",
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "type": "3736",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "cdid": str(uuid.uuid4()),
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5",
            "manifest_version_code": "2023708050",
            "update_version_code": "2023708050",
            "ab_version": "37.8.5",
            "resolution": "1600*900",
            "dpi": "240",
            "device_type": "SM-G998B",
            "device_brand": "samsung",
            "language": "en",
            "os_api": "28",
            "os_version": "9",
            "ac": "wifi",
            "is_pad": "0",
            "current_region": "TW",
            "app_type": "normal",
            "sys_region": "US",
            "last_install_time": "1754073240",
            "mcc_mnc": "46692",
            "timezone_name": "Asia/Baghdad",
            "carrier_region_v2": "466",
            "residence": "TW",
            "app_language": "en",
            "carrier_region": "TW",
            "timezone_offset": "10800",
            "host_abi": "arm64-v8a",
            "locale": "en-GB",
            "ac2": "wifi",
            "uoo": "1",
            "op_region": "TW",
            "build_number": "37.8.5",
            "region": "GB",
            "ts":str(round(random.uniform(1.2, 1.6) * 100000000) * -1),
            "iid": str(random.randint(1, 10**19)),
            "device_id": str(random.randint(1, 10**19)),
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "support_webview": "1",
            "okhttp_version": "4.2.210.6-tiktok",
            "use_store_region_cookie": "1",
            "app_version":"37.8.5"}
        cookies = {
            "passport_csrf_token": secret,
            "passport_csrf_token_default": secret,
            "install_id": params["iid"],
        }
        
        
        
        
        s=requests.session()
        cookies = {
            '_ga_3DVKZSPS3D': 'GS2.1.s1754435486$o1$g0$t1754435486$j60$l0$h0',
            '_ga': 'GA1.1.504663773.1754435486',
            '__gads': 'ID=0cfb694765742032:T=1754435487:RT=1754435487:S=ALNI_MbIZNqLgouoeIxOQ2-N-0-cjxxS1A',
            '__gpi': 'UID=00001120bc366066:T=1754435487:RT=1754435487:S=ALNI_MaWgWYrKEmStGHPiLiBa1zlQOicuA',
            '__eoi': 'ID=22d520639150e74a:T=1754435487:RT=1754435487:S=AA-AfjZKI_lD2VnwMipZE8ienmGW',
            'FCNEC': '%5B%5B%22AKsRol8AtTXetHU2kYbWNbhPJd-c3l8flgQb4i54HStVK8CCEYhbcA3kEFqWYrBZaXKWuO9YYJN53FddyHbDf05q1qY12AeNafjxm2SPp7mhXZaop_3YiUwuo_WHJkehVcl5z4VyD7GHJ_D8nI2DfTX5RfrQWIHNMA%3D%3D%22%5D%5D',
        }
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en,ar;q=0.9,en-US;q=0.8',
            'application-name': 'web',
            'application-version': '4.0.0',
            'content-type': 'application/json',
            'origin': 'https://temp-mail.io',
            'priority': 'u=1, i',
            'referer': 'https://temp-mail.io/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-cors-header': 'iaWg3pchvFx48fY',
        }
        
        json_data = {
            'min_name_length': 10,
            'max_name_length': 10,
        }
        
        response = requests.post('https://api.internal.temp-mail.io/api/v3/email/new', cookies=cookies, headers=headers, json=json_data)
        name=response.json()["email"]
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/account_lookup/email/"
        s.cookies.update(cookies)
        m=SignerPy.sign(params=params,cookie=cookies)
        
        headers = {
          'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-G998B; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
          'x-ss-stub':m['x-ss-stub'],
          'x-tt-dm-status': "login=1;ct=1;rt=1",
          'x-ss-req-ticket':m['x-ss-req-ticket'],
          'x-ladon': m['x-ladon'],
          'x-khronos': m['x-khronos'],
          'x-argus': m['x-argus'],
          'x-gorgon': m['x-gorgon'],
          'content-type': "application/x-www-form-urlencoded",
          'content-length': m['content-length'],
        
        }
        
        response = requests.post(url, headers=headers,params=params,cookies=cookies)
        
        if 'data' in response.json():
            try:passport_ticket=response.json()["data"]["accounts"][0]["passport_ticket"]
            except Exception as e:return {'status':e}
        else:
            return {'status':'Bad'}           
        
        name_xor=self.xor(name)
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/send_code/"
        params.update({"not_login_ticket":passport_ticket,"email":name_xor})
        m = SignerPy.sign(params=params, cookie=cookies)
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-G998B; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
            'Accept-Encoding': "gzip",
            'x-ss-stub': m['x-ss-stub'],
            'x-ss-req-ticket': m['x-ss-req-ticket'],
            'x-ladon': m['x-ladon'],
            'x-khronos': m['x-khronos'],
            'x-argus': m['x-argus'],
            'x-gorgon': m['x-gorgon'],
        }
        response = s.post(url, headers=headers, params=params, cookies=cookies)
        
        time.sleep(5)
        cookies = {
            '_ga': 'GA1.1.504663773.1754435486',
            '__gads': 'ID=0cfb694765742032:T=1754435487:RT=1754435487:S=ALNI_MbIZNqLgouoeIxOQ2-N-0-cjxxS1A',
            '__gpi': 'UID=00001120bc366066:T=1754435487:RT=1754435487:S=ALNI_MaWgWYrKEmStGHPiLiBa1zlQOicuA',
            '__eoi': 'ID=22d520639150e74a:T=1754435487:RT=1754435487:S=AA-AfjZKI_lD2VnwMipZE8ienmGW',
            'FCNEC': '%5B%5B%22AKsRol8AtTXetHU2kYbWNbhPJd-c3l8flgQb4i54HStVK8CCEYhbcA3kEFqWYrBZaXKWuO9YYJN53FddyHbDf05q1qY12AeNafjxm2SPp7mhXZaop_3YiUwuo_WHJkehVcl5z4VyD7GHJ_D8nI2DfTX5RfrQWIHNMA%3D%3D%22%5D%5D',
            '_ga_3DVKZSPS3D': 'GS2.1.s1754435486$o1$g0$t1754435503$j43$l0$h0',
        }
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en,ar;q=0.9,en-US;q=0.8',
            'application-name': 'web',
            'application-version': '4.0.0',
            'content-type': 'application/json',
            'origin': 'https://temp-mail.io',
            'priority': 'u=1, i',
            'referer': 'https://temp-mail.io/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-cors-header': 'iaWg3pchvFx48fY'
        }
        
        response = requests.get(
            'https://api.internal.temp-mail.io/api/v3/email/{}/messages'.format(name),
            cookies=cookies,
            headers=headers,
        )
        import re
        try:
            exEm = response.json()[0]
            match = re.search(r"This email was generated for ([\w.]+)\.", exEm["body_text"])
            if match:
                username = match.group(1)
                #print(username)
                return {'status':'Good','username':username,'Dev':'Mustafa','Telegram':'@PPH9P'}
        except Exception as e:return {'status':'Bad','Info':e,'Dev':'Mustafa','Telegram':'@PPH9P'}    
        #@staticmethod
 
    def GetInfo(self,username):
        try:
            headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    };url = f"https://www.tiktok.com/@{username}";response = requests.get(url, headers=headers,timeout=10).text;data = response.split('''"userInfo":{"user":{''')[1].split('''</sc''')[0];followers = data.split('"followerCount":')[1].split(',')[0];id = data.split('"id":"')[1].split('"')[0];nickname = data.split('"nickname":"')[1].split('"')[0];following = data.split('"followingCount":')[1].split(',')[0];likes = data.split('"heart":')[1].split(',')[0];ff=f'''
『🔥』ʜɪᴛ ᴛɪᴋᴛᴏᴋ『🔥』
________________________
    User : {username}
    Name : {nickname}
    Id : {id}
________________________
𝙛𝙤𝙡𝙡𝙤𝙬𝙚𝙧𝙨: {followers}
𝙛𝙤𝙡𝙡𝙤𝙬𝙞𝙣𝙜: {following}
𝙡𝙞𝙠𝙚:{likes} 
________________________
BY : @D_B_HH  CH :  @k_1_cc
    '''
            return {'status':'Good','Info':ff,'Dev':'Mustafa','Telegram':'@PPH9P'}
        except Exception as e:return {'status':'Bad','Dev':'Mustafa','Telegram':'@PPH9P'}
#
  
    def __init__(self):
        self.users = set()
        self.user_queue = asyncio.Queue()
        self.lock = asyncio.Lock()
        self.a = 0
        self.ALLOWED_COUNTRIES = {"IN", "KZ", "PK", "CO","SE"}

    def Vals(self):
        return {
            "manifest_version_code": "330802",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "app_language": "ar",
            "app_type": "normal",
            "iid": str(random.randint(1, 10 ** 19)),
            "channel": "googleplay",
            "device_type": "RMX3511",
            "language": "ar",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "resolution": "1080*2236",
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "update_version_code": "330802",
            "ac2": "lte",
            "cdid": str(uuid.uuid4()),
            "sys_region": "IQ",
            "os_api": "33",
            "timezone_name": "Asia/Baghdad",
            "dpi": "360",
            "carrier_region": "IQ",
            "ac": "4g",
            "device_id": str(random.randint(1, 10 ** 19)),
            "os_version": "13",
            "timezone_offset": "10800",
            "version_code": "330802",
            "app_name": "musically_go",
            "ab_version": "33.8.2",
            "version_name": "33.8.2",
            "device_brand": "realme",
            "op_region": "IQ",
            "ssmix": "a",
            "device_platform": "android",
            "build_number": "33.8.2",
            "region": "IQ",
            "aid": "1340",
            "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1)
        }, {
            'User-Agent': 'com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)'
        }

    def sign(self, params, payload: str = None, sec_device_id: str = "", cookie: str or None = None,
             aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n",
             sdk_version: int = 2, platform: int = 19, unix: int = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload is not None else None
        if not unix:
            unix = int(time.time())
        return Gorgon(params, unix, payload, cookie).get_value() | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid,
                                      license_id=license_id, sec_device_id=sec_device_id,
                                      sdk_version=sdk_version_str, sdk_version_int=sdk_version)
        }

    async def get_following(self, session, user_id):
        token = None
        while True:
            try:
                p, h = self.Vals()
                signed = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
                h.update({
                    'x-ss-req-ticket': signed['x-ss-req-ticket'],
                    'x-argus': signed["x-argus"],
                    'x-gorgon': signed["x-gorgon"],
                    'x-khronos': signed["x-khronos"],
                    'x-ladon': signed["x-ladon"]
                })
                base_url = f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&count=50&source_type=1&request_tag_from=h5&{urllib.parse.urlencode(p)}'
                if token:
                    base_url += f"&page_token={urllib.parse.quote(token)}"
                async with session.get(base_url, headers=h) as response:
                    data = await response.json()
                for user in data.get("followings", []):
                    reg = user.get("region")
                    fol = user.get("follower_count")
                    username = user.get("unique_id")
                    async with self.lock:
                        if username and reg in self.ALLOWED_COUNTRIES:
                            if int(fol) > 99 and username not in self.users:
                                self.a += 1
                                self.users.add(username)
                                
                if not data.get("has_more"):
                    break
                token = data.get("next_page_token")
                if not token:
                    break
            except Exception:
                break

    async def info(self, session, username):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6394.70 Mobile Safari/537.36 trill_350402 JsSdk/1.0 NetType/MOBILE Channel/googleplay AppName/trill app_version/35.3.1 ByteLocale/en ByteFullLocale/en Region/IN AppId/1180 Spark/1.5.9.1 AppVersion/35.3.1 BytedanceWebview/d8a21c6"
        }
        try:
            async with session.get(f'https://www.tiktok.com/@{username}', headers=headers) as resp:
                tikinfo = await resp.text()
            info = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
            try:
                user_id = str(info.split('id":"')[1]).split('",')[0]
                following = str(info.split('followingCount":')[1]).split(',"')[0]
                country = str(info.split('region":"')[1]).split('",')[0]
                
                if country in self.ALLOWED_COUNTRIES:
                    async with self.lock:
                        if username not in self.users:
                            self.a += 1
                            self.users.add(username)
                            await self.user_queue.put(user_id)
            except:
                pass
        except:
            pass

    def V12(self):
        kew = random.choice(['abcdefghijklmnopqrstuvwxyz','abcdefghijklmnopqrstuvwxyzñáéíóúü','abcdefghijklmnopqrstuvwxyzṣọẹ̀áéíóú','abcdefghijklmnopqrstuvwxyzñáéíóúü','ကခဂဃငစဆဇဈဉညတထဒဓနပဖဗဘမယရလဝသဟဠအ','abcdefghijklmnopqrstuvwxyzɛɔŋ'])
        k = ''.join((random.choice(kew) for i in range(random.randrange(2, 9))))
        return k

    async def search(self, session):
        while True:
            try:
                username = self.V12()
                url = "https://search16-normal-c-alisg.tiktokv.com/aweme/v1/search/user/sug/?iid=" + str(
                    random.randint(1, 10 ** 19)) + "&device_id=" + str(random.randint(1, 10 ** 19)) + "&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid=" + str(
                    binascii.hexlify(os.urandom(8)).decode()) + "&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket=" + str(
                    round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632" + "&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts=" + str(
                    round(random.uniform(1.2, 1.6) * 100000000) * -1) + "&cdid=" + str(uuid.uuid4()) + ""
                payload = {
                    'keyword': username,
                    'count': "100",
                    'source': "tt_ffp_add_friends",
                    'mention_type': "0"}
                headers = {'Host': 'search16-normal-c-alisg.tiktokv.com',
                           'User-Agent': "com.zhiliaoapp.musically/2023105030 (Linux; U; Android 13; ar_IQ; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:2fdb62f9 2023-09-06 QuicVersion:bb24d47c 2023-07-19)"}
                headers.update(self.sign(url.split('?')[1], payload=urllib.parse.urlencode(payload)))
                async with session.post(url, data=payload, headers=headers) as response:
                    data = await response.json()
                ids = [
                    item["extra_info"].get("sug_uniq_id")
                    for item in data.get("sug_list", [])
                    if "extra_info" in item
                       and "sug_uniq_id" in item["extra_info"]
                       and re.fullmatch(r"[A-Za-z0-9_]+", item["extra_info"]["sug_uniq_id"])
                ]
                for user in ids:
                    await self.info(session, user)
            except Exception as e:
                return {'status':'Bad','Info':e,'Dev': 'Mustafa', 'Telegram': '@PPH9P'}
    async def worker(self, session):
        while True:
            try:
                user_id = await self.user_queue.get()
                await self.get_following(session, user_id)
                self.user_queue.task_done()
            except Exception:
                pass

    async def main(self):
        async with aiohttp.ClientSession() as session:
            workers = [asyncio.create_task(self.worker(session)) for _ in range(50)]
            searches = [asyncio.create_task(self.search(session)) for _ in range(40)]
            await asyncio.gather(*workers, *searches)
    def GetUsers(self):
        asyncio.run(self.main())
        return {'status':'Good','usernames':list(self.users),'Dev': 'Mustafa', 'Telegram': '@PPH9P'}           


class Encryption:
    @staticmethod
    def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, 
             aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n",
             sdk_version: int = 2, platform: int = 19, unix: int = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload is not None else None
        if not unix:
            unix = int(time.time())
        return Gorgon(params, unix, payload, cookie).get_value() | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id,
                                      sec_device_id=sec_device_id, sdk_version=sdk_version_str,
                                      sdk_version_int=sdk_version)
        }

    def __init__(self):
        self.secret = secrets.token_hex(16)
        self.session = requests.Session()
        self.session_list = [
            "62f665d8fef41027c569a264e39d1884", "ffea1b72a3de8ebb5c1e48c91d3886cc",
            "ff1713546c7a7662abc0e0e93c969389", "88c024610ed4bf8ceb37cc92e78b4438",
            "4c5fae74420dc27e119ff5eb2bf56102", "d8f6f9558e1807a1cd083f13de997693",
            "f2a3ec8f71217f2fa2ed8507a8641920", "b18a44f1169bfdcd307474ceada8090c",
            "8799b7c86a83c99eb082e963e930b426", "30514372833cc1b571f8dc8a0f55db94",
            "859921010e1e9987fdf884a57fadf2c0", "837c4064fe0a64dc4f142ccf2c13b23b",
            "a40870bb53dc677c0ce604e681f15905", "b054149c7a2fa4681298030e91d0c033",
            "fb32c6bfd5bdef0cd0b9e5c999cf9e46", "32df03aa0a45104c29c0eb241bfaf052",
            "bb9bb2cb430f275879a60ba999f14b3e", "1e7f464b70cbc5a5f10d17a0c6f2b157",
            "555afc40837701fb54504a7e1f12df03", "6f7a25ed7db6c0620d7d4b1a1779813d",
            "1715803b0d3ac0d74b4ded219e2dc29f", "ab47913dc08abeb336556e9418449995",
            "4bb1079bdd4d7461e49e9d7ca4bc9d62", "c4392269a5de973a130c1d8659efcc17",
            "c5913e6c105f88b19e4a6da96225b0a5", "3e815d7ed8d5ee5ed26394221cb94814",
            "8d04f1fc7d786b955be5a34ae9b2f32f", "b4452e44aeef216e7c2b4b314b550362",
            "fc1f9672a6d4177993114198414be131", "63cbc72d81fd2230fde48b255038fe3a",
            "497a97f73536f4f24831bebfed672258", "c3b41475865dd21e2a42be682cbbeec7",
            "ac8cdd63d992feda7eb1be63cd5d3cbe", "277641c2bd68423af3c97ee64116c9ea",
            "b9d8b79367847fd9dfb8647bb96edd41", "8f68c10b8a60b64e8d2dd3fcb1cdc6be",
            "3e99fe2e40577af27dc4fb15f9b438f7", "6452b4925edad1b34284d9cf4887d281",
            "ecbce30174a3109533e8c9db2b400e9f", "b521fc106d86884df7392b0d47094b42",
            "2d3b23c564d18404371c6cb9b6e34532", "4d11b056afddc31ec72deddad2326765",
            "136ee26c51401fccb38c624e16ec71ca", "5e4e1267e08331d25ed7012d84f78243",
            "2baf060615d6a5d9daba5a612a9ec8ff", "def6f7881ea24c7c6e2f2faafd749e33",
            "333c2f1fa9ccc31d05e3433f33379f23", "8efef9a8fc0bad95cb399251f513cab0",
            "f98471c9220848e8fa3ad8ea31c86225", "70e134536c70bbd31b540bfb9abd9f16",
            "1701c221c9719dcc25ebe117759c06b3", "da2fbb565878a4f97d51e0763087c29a",
            "d34bf184d8f40f06e50f466d1c7a8385", "f2ebd1a84b6891d9881cb18ec880be93",
            "114f488327fe3f9e0cb7e5d0c93e18da", "30ad5eb572241440c7f642ad07c3972e",
            "86fd5bd98326e1478e6eec4aeb581640", "d93155afde179fac47815722a8988fab",
            "36726a0145f85571c4d7919a564a330d", "1b9867aa336e42deceb19d7bbf045bfe",
            "f2da58a0f3b534620e8ca7d070be1457", "fe087743cb83b87fe511c4dcc2b54b9e",
            "98ac6a1ed1cea0cd7dd86da4ad548983", "cd0f53b4792b963e9d0a2330d2bba74b",
            "6fcad57feb38a57155455fadf8fb8caa", "373350af36cc1113a831c7b705bda684",
            "f9c05a9003abfa1cb8559f6c4619e41a", "800266a1b9550a662a533bbe0a51edff",
            "9a8916da2bb338659104506974720173", "3a3ad8e66b4a328280aeb8def7e4526c",
            "f6c32b0881229967ea0e5c90635fa19e", "f6e7f6e669a689a4433acd46eace2cb1",
            "8d40480a584859232cf9db44895307c8", "12700e53ced122977a6705435f8dc433",
            "475880946e2be5c2539a6c51746d2a27", "e6be1a32ae14b07e95a33d79e907ab75",
            "4b6a87e13d505bbacafb57f18b646e0b", "38df69157cd19f89825ad86e40533b3e",
            "b573dc5a165bd4d407c4e258f24943a0", "611254e09febca06d81e7f4ee9acf739",
            "df9f5cef1f2d05757af659235150e5a6", "9b19bb4e743f4220cc05770ab88164af",
            "3c639274b33f920b4e2509382a26e737", "46bfa28933895ace05a96a0ba0608476",
            "d2d36db7cd7830a3ebf5a58c7b1e592d", "8a127cc4be5a9cfa63e6c6f67219a490",
            "d7f340e143dbb4eab73dd8f675d20b97", "cba9fc1957583e626dcc0fdf1d0846e4",
            "e56d4e0c3f4034f9d6aada115759169c", "026268b95716b09091705c48002a7e95",
            "37c113b605d2c23f14a2f42bbe2ea894", "6805b2b6487750f8a9ed74661eca0a18",
            "2c528b6328e4eddbfc2b49a0dcf3fed3", "759fca154d2a4e1f801842e3a79f6766",
            "c832e75c4d20fb078b287fb230dc6dab", "88c3338cf6f470771ede62a0d13f6f51",
            "a79666d0aedf81af7dec5e7302ce1a6a", "cd4489ef3fe23ddc68ad4454c9cabc41",
            "be5d43022279aae0fbb2810645e3a655", "2b37fd4151b4eaf7196f5f5e7e659f64",
            "589aa1ccd336f68806fc8c9c0ff1fe0b", "ce3a13b32c7da9085e3b25f8aa1ed10f",
            "808e2a97bd95972563bc915739cd2b3f", "4bfc3a16fc141d2bda156c13108e3586",
            "563c76e23b0f1c8fb34fc4b2016192a2", "7de5eee54214f4193593f8f3135082b2",
            "796299fe163dd952a856d622abb07dfb", "eb3fa50f60dd60f3a415f4d57d5c368d",
            "1e5aa603077be314c594aa05c85a29c7", "ba0cb1b483e91b176e0a9e8991d24d29",
            "336a32fd882ea7a9a209f5f6f1001aec", "c075d398cbf3a2b2c07684df36984341",
            "3686a9458f6af84138fbb2fd9f4ffda0", "72e433ec19e499dd25255f6378d68e32",
            "2675c0445217ed43acaa90e9835d3801", "b848e09658da067adc08221282fe8cce",
            "686a259b53d792a96eb099e6326536f3", "0f2d6256d2252a5cecd575b76009e8c2",
            "959c67bd75dce25e3913ddbe7831013c", "f7a3b3d4b075b192cffd1beb30b813c7",
            "65586cba785fbed5f28b9626a8ef7dce", "7872475d47b25e925845cb90e42e4c31",
            "c33e3da3ec3b8e611625db85fb8ea360", "74df66f2ffb81a6ea8ba82ded5660462",
            "711326a9ce06c555903b43e5d0a8f64e", "562ce0d6e308336b6b35a2377ff81d8a",
            "3e23691485fbc4903e763c1f7041b2c1", "91197ac26c308d4a5142374af959117d",
            "145406ad9a7bed24c47130a592f11280", "dc7d2164919b5432676b4a8315d8f8b3",
            "300d027cc70fd71efa2dc4e1661bd053", "531e7ed1aa699a929b313b8960677c07",
            "4564dbbb3c2a6a38c6be3bab23c3fbb8", "7a5f9b1ac1dd2208b5de5429e6cc8a4e",
            "2c973cfb6559bc0369cefdbb75d5cbb7", "07df88ae4f58bdd8e491e57dad95f0b2",
            "85bae7724ff412e6416add3975d7578f", "58eb1b123fbe7117564f3bf938bae169",
            "99b2c615978200c679b321f04d314d49", "df7246019b382003c7d438e2eec3f812",
            "e0931644e0e00b2abafe66c7ff6bd1ae", "810bb2e31fac51248e97056794f2b9ab",
            "f7990c6cc30d7a198988291dbccbd6b3", "77e24da2dd86794d0233b45f9122dd6a",
            "703ac330c391437e49fbf64b88b8a9a2", "c33a0ef15486debe17f4a38fc4bcb1b0",
            "160ca3c436693fcdc1165149c04d26c6", "8a9e4778c7074dc6497bce8fbc3e7be6",
            "a7a6042fd8bb7aa59496346d9646e46f", "de296140fdf052974d313dffaeac39a8",
            "f699c60e0671ac8cf07b47b98876e750", "86be838627f099740d32bb8b40ef9c72",
            "a3bb5e75308e2e39b87edbfb14913e4e", "8b8e6c66621495028a8736288d4b9f60",
            "23126441f9d70e4b3a09d6b02b88f4db", "cca19e4d58fc1501dc8c43aa8b88503a",
            "313f9320debd8578a8b003b5509e164e", "01a71c6e05be681cbf54b63761bc3e97",
            "76d6f8f67084805f06b6564ba7cb24b5", "853592114370ff71b41440dca049d35c",
            "107a5389f057ffd593703db26e1a6d41", "3fc28ef28e8b046f4a355240824b0e21",
            "c7ed9dcf6c6fe6e536caee305b4176d8", "95239e5a5133b359e6c145c106ff4290",
            "fd4cd15633d1ebceccc492d509a9522b", "234dd649173aa93f67b01d202f5ebb5f",
            "41dede88fec05de213462698b04ce27f", "69aea7af5e0e1524a5071b2bf158aecd",
            "048ad72afd245e1f2cd0013f0298558d", "2fdde166b803a9ccf032adf2236966e9",
            "7b7230e76e67e6d467aa6c6e33694b23", "e75ed27910bc3b0d134faa20f7d6be86",
            "fbc3755aa0a64e9f2426551fd7494190", "9e42fb4166611ce207b8bfcf8e76193d",
            "3f2130a53db5d89a5a0f1893e8e2a458", "87b5fecacc094664095ca06a987504a4",
            "77ae27678d788d549427dbf2b7029e4f", "278b94bbb57a92ff23d92c5c52e1d57e",
            "13453eb8a4859fef9e3bb2bbb692fd5b", "9b41367dfce20d1e60803d476436c3b7",
            "374882523eadf76e3cd5195b0d3bfb5f", "a3b91f7d92a916ce843690a99f0c43ee",
            "acee9b72897b1f68508da506970c817e", "7bc91a1520086b82c8ddd807c4529649",
            "40035d852d85c40b180d5154dce74e32", "5498466fbb252a5c34408a0e5751390d",
            "db5aed4cc13b8c33d4a409948ba8b677", "a4cfed2672245de968fe7f0153d80920",
            "3d034db5510fb4577acea1bb7853285f", "f2dbfc92b25541c5bce8cf50239a1c8b",
            "816f54a8ef101bd79e0309f0a8da9e78", "d47c091970b7ebe7eceb45f6db5bf377",
            "5fdd7957547d882ca1e3c5b3d33420e1", "6bf28abdc354288b73bf99008f6a361f",
            "e0a008174fbb2f2c1923e7ca2d7ae0ba", "10830e1da11fb34796f4142cbaa471bd",
            "e1c31444718342437f68468b7ec63ae5", "ade285e52270bcc0291623766218821a",
            "f60c544b5014358574cd7df1c1751f42", "73d108ee305e5c4e2abb81354ee69eef",
            "4bebce373dae99851b842d7f83e01678", "98b6f608bcb1a1714f7d14ec97397dad",
            "256cfbcce57745c765a0cba9d9b6a9cf", "9bb881516b14276d1506c5b13201a641",
            "ad597479d1c78c6d7c07135b98883ec7", "608e50f670227682805b6c4db9008025",
            "ad60747cbef3f4d18220ebe993639a5b", "01d9a4ee761a44ab1f80d4554cc10301",
            "99199284fc83817a51844b35e12b9a18", "82b3b6f4598846326d794291c180bd6f",
            "5706974cb7a333f2aa6344182fa9e24c", "0159c8bd9617c49ac0d2294a2ef6b97d",
            "fb049fc6801bc30563f7239c7bb35530", "31798578bda2b66f1a019e9b1a9e5214",
            "7c67d00d73751c447972067da77b9c08", "56f049210392ffaadf30836155d642f3",
            "33422b62d24bed998ea3e5c5dc6a5850", "f4fd0301c875e5a5da06c14fd136934c",
            "63ab5a670d8d6a9fbd14f7d3fd0b30da", "4dd9dba22d9b3faa2d8a866fb7fd403b",
            "5e1078840499161441c8a8ca40295fb1", "40e796fc33872c367984b9ff66080caa",
            "21e7a5993c20a21cd3db5d22abda0194", "3b6ae27e9438af200e6bc9f8dac0fb32",
            "e4f9a311e23f55cd2219bbb358f6f38a", "7013e9767ad43770d1a86cdd45b880e5",
            "1d93b099848608933a1a190a1c39a4c4", "7a35f4c1fe2909ee619f881438757502",
            "aabcf70996014cceaca2c5b5de17026d", "fb3ecd7a225441bcdf0f82a153976c51",
            "a1976683109377aeaf23d331f696e785", "0359bb8217ffc2669f7c4c0b3ac63e52",
            "cec657d01305d24d62ead1ebca1ea0de", "1fd7b1579b9e724a182d0168a0091744",
            "76cecb47873574fe52b941bfea37109c", "c3272f09e2f4a64539b79c149c8d1a12",
            "277c766fa34f1093a4df0e37da4f6312", "555afc40837701fb54504a7e1f12df03",
            "27e7f6c1f44408fb70d9d374f67f64ac", "6f4076069b6de17461c9d29ed1322821",
            "547497458ad53d248709e4a7edbdfae4", "94fa96e1fc5ed700901c37a2a03966c0",
            "bc4d7382e95f3b9fa79d9164dac426e6", "c8769958835459633034c1ff06b127bb",
            "cb15ed355eaca3c44cec880d96631248", "8d99d73bb36f1fece3ac5335eda9c51e",
            "1cd5c445cb7cce8dd4eddf6134f830a6", "ab47a0aee0420bbb4ad5ab9e10f13592",
            "368d6857bc5c755288cbe8e52d6439e1", "525d663adcec79b1601cdfa2125627dc",
            "2398c01408d6653d08b725af79f89447", "4bfc3a16fc141d2bda156c13108e3586",
            "ada25f00d415c4132222e4effa5ce82d", "27ea1b3c8a253ea83a2fe37dc284e68e",
            "24f4c7a509a22e8ab857214a57f84f47", "1106c8fe2411b79f2a7721fd4f8b5f27",
            "de2319ad927bad889e66008a9bcfbc6a", "8799b7c86a83c99eb082e963e930b426",
            "befcea68deff3c0877b5f632281d0e5c", "401c36fc2d0abbdda740a52838cd31c2",
            "2a8bb71410fb99e849d2b9a9b2c54342", "982f6703ac3aa4473f607ffc74e7d1bd",
            "2baf060615d6a5d9daba5a612a9ec8ff", "c6a7baaba35d133ac8097e07b791f28c",
            "f4ea0fc94454b6a47fafb09a00aeb0e8", "32df03aa0a45104c29c0eb241bfaf052",
            "28e5067ca59aefefe8a5716a4c257019", "da2fbb565878a4f97d51e0763087c29a",
            "bb9bb2cb430f275879a60ba999f14b3e", "31fffc2561f90d7780c034db4f458dad",
            "d0900ba89c1a62c7334db51b90d08046", "594702557c899105c69d9fed98af8ea8",
            "1f725345ce9db86e806433387449924a", "1e7f464b70cbc5a5f10d17a0c6f2b157",
            "859921010e1e9987fdf884a57fadf2c0", "f1b2fee1dd90c445fd9c91de64b3bdbb",
            "2d3b23c564d18404371c6cb9b6e34532", "b521fc106d86884df7392b0d47094b42",
            "ab47913dc08abeb336556e9418449995", "47d6ccf5f6c2c55d1ee89041519f7261",
            "35d963b32bab29e4ccf1729751de78cf", "a79666d0aedf81af7dec5e7302ce1a6a",
            "e54ae478d3928c1980661d3dcc81127e", "74ec3f5c1d33d16ee3a1f6785fe78ec3",
            "5e4e1267e08331d25ed7012d84f78243", "fe087743cb83b87fe511c4dcc2b54b9e",
            "c68ccd27f5573a94d3f7d78cef0fa2fd", "be5d43022279aae0fbb2810645e3a655",
            "fe761e2849fe5c4b09a01c7eca87818d", "f68c1a1432e1bec4b55edbcedb22f5da",
            "5a0d6b2ca82d8824852148c22e146910", "d93155afde179fac47815722a8988fab",
            "1715803b0d3ac0d74b4ded219e2dc29f", "871319a3e34f2034d5204f3e9d3fc9bc",
            "874f51b16b387ec5817f0b6b519935f1", "18b53d20afa826762975db9ae5cad261",
            "8a9e4778c7074dc6497bce8fbc3e7be6", "d176247e0d0e5991755527960c9bac6e",
            "f8bdc9ece565fcc3441f991b480e28fa", "2c528b6328e4eddbfc2b49a0dcf3fed3",
            "1fab0a86ef4e14452c2cec08c695ae9e", "d972be2b916d7cb7a3e2c534dac73439",
            "70e134536c70bbd31b540bfb9abd9f16", "de296140fdf052974d313dffaeac39a8",
            "8de6f06d2d8940559417198c6193c1f0", "74df66f2ffb81a6ea8ba82ded5660462",
            "8f68c10b8a60b64e8d2dd3fcb1cdc6be", "837c4064fe0a64dc4f142ccf2c13b23b",
            "98b6f608bcb1a1714f7d14ec97397dad", "85bae7724ff412e6416add3975d7578f",
            "98ac6a1ed1cea0cd7dd86da4ad548983", "37c113b605d2c23f14a2f42bbe2ea894",
            "2c973cfb6559bc0369cefdbb75d5cbb7", "c46f26a1aa31f443e6b73a2baab4fcb4",
            "c075d398cbf3a2b2c07684df36984341", "e396fd3973bf6c3030a87e599d578e94",
            "32d46be3c5a307684370f458bdb512aa", "ce716be979856be6160fe37d40e7cf39",
            "adfe96d147a5f0b8c400a065e4f7ba75", "ac8cdd63d992feda7eb1be63cd5d3cbe",
            "4bb1079bdd4d7461e49e9d7ca4bc9d62", "ad597479d1c78c6d7c07135b98883ec7",
            "b8f86957a52616badf8897c94c3705d6", "c33e3da3ec3b8e611625db85fb8ea360",
            "eb3fa50f60dd60f3a415f4d57d5c368d", "5a7e7c83f61e6e0e1c3ca128cd3ee79a",
            "43a6dccb7cceedd2f40e73e9ba104e01", "bb4cef9ef619cb46f0a45c308c0d1e25",
            "871319a3e34f2034d5204f3e9d3fc9bc", "f2a3ec8f71217f2fa2ed8507a8641920",
            "026268b95716b09091705c48002a7e95", "333c2f1fa9ccc31d05e3433f33379f23",
            "a99d5b0c09d9f48cc0ea2a5e1c1d563f", "390650d4f00c3ae0364c789b7398cc3f",
            "475880946e2be5c2539a6c51746d2a27", "f6c32b0881229967ea0e5c90635fa19e",
            "e64ed96b8c3ea51c4524b7dd25bf0abd", "8100a904b508f86fa19c3b3a2146a979",
            "d8f6f9558e1807a1cd083f13de997693", "31798578bda2b66f1a019e9b1a9e5214",
            "70b89d86c34091ed1bbde6b1c2f31627", "f2ebd1a84b6891d9881cb18ec880be93",
            "2d6932f3b644bc16b7a1ccc89f106e20", "63cbc72d81fd2230fde48b255038fe3a",
            "136ee26c51401fccb38c624e16ec71ca", "93bf67de66b6ddff3a75c3aec78e7276",
            "5a4a4c8c746d55a3cae7f32a127513aa", "46bfa28933895ace05a96a0ba0608476",
            "c3b41475865dd21e2a42be682cbbeec7", "c4392269a5de973a130c1d8659efcc17",
            "790a751e85a51bd40eb41edb5297bce1", "db5aed4cc13b8c33d4a409948ba8b677",
            "3a3ad8e66b4a328280aeb8def7e4526c", "828fa1b2d11b74e18007178c0632cda6",
            "ffea1b72a3de8ebb5c1e48c91d3886cc", "b18a44f1169bfdcd307474ceada8090c",
            "9a8916da2bb338659104506974720173", "8a127cc4be5a9cfa63e6c6f67219a490",
            "f80b8abf5291f2d958ca9bbc8285eb8a", "a40870bb53dc677c0ce604e681f15905",
            "3686a9458f6af84138fbb2fd9f4ffda0", "f71206a0db3826312b821fabd6e740c1",
            "41dede88fec05de213462698b04ce27f", "7de5eee54214f4193593f8f3135082b2",
            "6fa98a5d216b91fb49e8bd0f50b6dc29", "759fca154d2a4e1f801842e3a79f6766",
            "62f665d8fef41027c569a264e39d1884", "959c67bd75dce25e3913ddbe7831013c",
            "5d29739e1b0087eff7bf04d443e9b25c", "86fd5bd98326e1478e6eec4aeb581640",
            "f6e7f6e669a689a4433acd46eace2cb1", "5e1078840499161441c8a8ca40295fb1",
            "982f6703ac3aa4473f607ffc74e7d1bd", "45b0fd55843aa436ffc53183b44b40f9",
            "d34bf184d8f40f06e50f466d1c7a8385", "3d034db5510fb4577acea1bb7853285f",
            "1f3b742316070c621848a7a17e4d9563", "114f488327fe3f9e0cb7e5d0c93e18da",
            "160ca3c436693fcdc1165149c04d26c6", "072ebf49f34e265d2b574e791551cb09",
            "800ddc3ce5b43b76b1dd3219d9683df2", "5ee5d7b8db9ea6adc488a6d8922f41db",
            "531e7ed1aa699a929b313b8960677c07", "300d027cc70fd71efa2dc4e1661bd053",
            "7b7230e76e67e6d467aa6c6e33694b23", "711326a9ce06c555903b43e5d0a8f64e",
            "d749bca683b46995bfc6397f5888d150", "388bde3f4bafd62d8bfd9ee64dbc5b7e",
            "94fa96e1fc5ed700901c37a2a03966c0", "df9f5cef1f2d05757af659235150e5a6",
            "f4118e6a419fb1b75385d229d64e9cff", "648c1df7cef3ed3bd814c932939ce846",
            "6905fa7e7025b29797794784d019bbe0", "7c67d00d73751c447972067da77b9c08",
            "277641c2bd68423af3c97ee64116c9ea", "1b9867aa336e42deceb19d7bbf045bfe",
            "3a98a4df701d27a68f8704fca43e4968", "e56d4e0c3f4034f9d6aada115759169c",
            "eed1faec934a151fe3f9e07ca38fbef4", "6fa98a5d216b91fb49e8bd0f50b6dc29",
            "6f7a25ed7db6c0620d7d4b1a1779813d", "bce10e2d58fc1a4d554a660ad3396583",
            "01d9a4ee761a44ab1f80d4554cc10301", "d2d36db7cd7830a3ebf5a58c7b1e592d",
            "def6f7881ea24c7c6e2f2faafd749e33", "ff1713546c7a7662abc0e0e93c969389",
            "30ad5eb572241440c7f642ad07c3972e", "62ce3b7afc11cc60503d57c50d46eb4a",
            "cd0f53b4792b963e9d0a2330d2bba74b", "9fd94fedf60e364a77b5d3f9157daba2",
            "f9c05a9003abfa1cb8559f6c4619e41a", "d92b8e122c3fbbece76cbda4a341e247",
            "6805b2b6487750f8a9ed74661eca0a18", "e87cd069c9ecd07a0eeac4567c49ce3e",
            "563c76e23b0f1c8fb34fc4b2016192a2", "36726a0145f85571c4d7919a564a330d",
            "ba0cb1b483e91b176e0a9e8991d24d29", "f80b8abf5291f2d958ca9bbc8285eb8a",
            "497a97f73536f4f24831bebfed672258", "f699c60e0671ac8cf07b47b98876e750"
        ]
        
    def GetStatus(self, email):
        try:
            if '@' in email:
                user = email.split('@')[0]
            cookies = {
                "passport_csrf_token": self.secret, 
                "passport_csrf_token_default": self.secret,
                "sessionid": random.choice(self.session_list)
            }
            self.session.cookies.update(cookies)
            
            # إعداد البارامترات
            params = {
                '_rticket': str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
                'cdid': str(uuid.uuid4()),
                'ts': str(round(random.uniform(1.2, 1.6) * 100000000) * -1),
                'iid': str(random.randint(1, 10 ** 19)),
                'device_id': str(random.randint(1, 10 ** 19)),
                'openudid': str(binascii.hexlify(os.urandom(8)).decode())
            }
            full_params = {
                '_rticket': params["_rticket"], 'ab_version': '37.8.5', 'ac': 'WIFI', 'ac2': 'wifi', 'aid': '1233',
                'app_language': 'ar', 'app_name': 'musical_ly', 'app_type': 'normal', 'build_number': '37.8.5',
                'carrier_region': 'US', 'carrier_region_v2': '460', 'cdid': params['cdid'], 'channel': 'googleplay',
                'cronet_version': '75b93580_2024-11-28', 'device_brand': 'rockchip', 'device_id': params['device_id'],
                'device_platform': 'android', 'device_type': 'rk3588s_q', 'dpi': '320', 'fixed_mix_mode': '1',
                'host_abi': 'arm64-v8a', 'iid': params['iid'], 'is_pad': '0', 'language': 'ar',
                'last_install_time': '1745162892', 'locale': 'ar', 'manifest_version_code': '2023708050',
                'mix_mode': '1', 'op_region': 'US', 'openudid': params['openudid'], 'os': 'android', 'os_api': '29',
                'os_version': '10', 'region': 'IQ', 'request_tag_from': 'h5', 'resolution': '720%2A1280',
                'rrb': '%7B%7D', 'scene': '4', 'ssmix': 'a', 'support_webview': '1', 'sys_region': 'IQ',
                'timezone_name': 'Europe%2FAmsterdam', 'timezone_offset': '3600', 'ts': '1745163105',
                'ttnet_version': '4.2.210.6-tiktok', 'uoo': '0', 'update_version_code': '2023708050',
                'use_store_region_cookie': '1', 'version_code': '370805', 'version_name': '37.8.5',
                'app_version': '32.9.5'
            }
            user_agent = (
                f"com.zhiliaoapp.musically/{random.randint(2000000000, 3000000000)} "
                f"(Linux; U; Android {random.randint(10, 15)}; {random.choice(['ar_AE', 'en_US', 'fr_FR', 'es_ES'])}; "
                f"{random.choice(['phone', 'tablet', 'tv'])}; Build/UP1A.{random.randint(200000000, 300000000)}; "
                f"Cronet/{random.randint(10000000, 20000000)} {random.randint(2023, 2025)}-"
                f"{random.randint(1, 12):02}-{random.randint(1, 28):02}; "
                f"QuicVersion:{random.randint(10000000, 20000000)} {random.randint(2023, 2025)}-"
                f"{random.randint(1, 12):02}-{random.randint(1, 28):02})"
            )
            
            # توقيع الطلب
            m = Encryption.sign(urlencode(full_params), '',
                                "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), 
                                None, 1233)
            
            # إعداد الهيدرات
            headers = {
                'User-Agent': user_agent,
                'x-tt-passport-csrf-token': self.secret,
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'x-argus': m["x-argus"],
                'x-gorgon': m["x-gorgon"],
                'x-khronos': m["x-khronos"],
                'x-ladon': m["x-ladon"]
            }

            # إرسال الطلب
            url = "https://api16-normal-c-alisg.tiktokv.com/passport/email/bind_without_verify/?passport-sdk-version=0&app_language=en&"
            res = requests.post(url, params=full_params, headers=headers, data={"email": email}, cookies=cookies).text
            
            # التحقق من النتيجة
            if 'Email is linked to another account. Unlink or try another email.' in res:
                return {'status': 'Good', 'Dev': 'Mustafa', 'Telegram': '@PPH9P'}
            else:
                return {'status': 'Bad','Error':res, 'Dev': 'Mustafa', 'Telegram': '@PPH9P'}

        except Exception as e:
            return {'status': 'Error', 'message': str(e), 'Dev': 'Mustafa', 'Telegram': '@PPH9P'}
