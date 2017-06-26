import requests
import hashlib
import re
from bs4 import BeautifulSoup

# 构造 Request headers
agent = 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.6.1.15524'
headers = {
    'User-Agent': agent,
    'Host': "user.zxxk.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive"
}

session = requests.session()


# 密码的 md5 加密
# def get_md5(password):
#     md5 = hashlib.md5()
#     md5.update(password.encode())
#     return md5.hexdigest().upper()


# 手机号登录
def login(telephone, password):
    url = 'http://user.zxxk.com/'
    session.get(url, headers=headers)  # 访问首页产生 cookies
    headers['Referer'] = "http://user.zxxk.com/"
    login_url = "http://user.zxxk.com/?PersonalData.aspx"
    postdata = {
        "username": telephone,
        "password": password,
        "lt":"LT-111124-Xff94Q1xhQRC2o7dHgJm-sso2.zxxk.com",
        "execution":"a624066d-d70b-4ccb-8786-797329a7a541_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuTjB0NmNrZHNPVzlyVHpJeVMxQnllVlJ4ZDJKelZteG9TRGhxZVRoRlkyTlpZbEZrVmxKbFozVm5SME55ZUZaMGNUQmlhR1p2WmpRek9WUkdSRXQ0VW1obmIyNTRjSGxITDFCRFZrdHNhR1F2U3pWSlVTdEJkVWt3ZHpNelRXTnFkbk4yYVVkSFNrRktPVVl3VUdwbGJIRkRNa012VG5wcldXRnRWRlZzWmxWdE5uaG9jbHB4TkRaMGNqZE9jR3d3WW5neWVXVTFZbVEyTHpoSFoxb3JSWGxTUlRSck1IbHFiWFJoWlVoUFVuaFVjMlJXVVVSMU1rWjBXSGN3VFdoaE5HZGpaakVyWlcxVGEwUnJTbWhGUVdGWkwzZEtVVFJOWVhoUGRtRkdZa0ZhTWxwVVIwNUdOVGhFYkdOVFZGQmtLMXBHTUc5cFEwTjVVMVZLZEZaV2NFUmhiWGN3TURadWJtMVJaMnB3UkVGbU9FVXdjVXhWWVVkV1ZVSnRTRlpCUXpSc1dFWjRUVEJKZEhZd01WbG9WSFFyWVc0MVozWm5kREUzZDJadFduZFpaV1JuZURsdVpXbE9hREp0WVdwWVZpdGtkSEpoTUhCSVNuQllVRFZ1WWtWM1oweHBiVGhZUjJKSVJIRTBaelp6VUhKNFZWaEhPR1ZWWlU0MVRXb3ZZbEJNT1RWM2FIWTVkeXR2TldKWWVYY3pjakkxZFVaMGMyTlhVMVp4UVZvM1IwVjNTWFJaUkRGSGEyWm9aRzVYWTNWaE4zVk9kVXRUVDNGVGFVeE9iRUp0TWpGNFMwdGhUMnMyVkVKTlJTczRVSGRvU2poVFJUSkdSVGxIWTI5aGJsRlpaME1yVFdKV04wSlNhbkY2WmtsVmIycExXbWsyZFRKSFZVOXRNMDlWYTJWa1IycFdZbmxVTkVkRVNsUlhabWhHU1RGSlRGTnhSM0JQYjJWNVIzTk9jbkZCV1hCTVlqWk1XR2RNVlVweE15dERUalY1V0RkMU1EbHhXVUY2Y2pkSFUxTkdPQzl6TjFKemJHaEpNbU5uWm5sTWRXTm9hWGxsYkVKVFpIcHRVamsyVUZoeGQyTlphVkUySzFoaGFYbHdlV0ZoU0N0bFYxZDFRVUZuY0VGVWFtVXJVVEZQYW1kU2RrYzBiMlUyTTBaMVdtdGthMGxsVUhrdllWcGhSM2hqVlZRdmNsaHNPRkkyV1ROQlRWUjNZbUp6ZGtaVkswRmtOMEYyVG5GT0wydDNURnBUZFhKamNISlhhRVpaSzNOMGMxY3phRVJ3YVhGbGFuZERObk14UlRWTk1IUnpWbHBLTm5oT1kyVjNOVEkyZFdGSWFHUmFUMHBTZVdWWVEwSTFjM2hPYUVKdmFuSXdXVGxpYjFCT1RrbHNkbTFZYTNsdFptYzRNVzFwUzJOVWVYaDVUa3BJT0VSV1FqWjRWVmgwVG1OeFNVeHZUVXRCVlhsVU9EQldTMHB2VkRRcllrSmtRbGcyYVZGTlYyaG9TRzVtUlhwNlRtNWlVSEZqWXpOb1pqSXhUMmhNZDB3eE5WVkxTM05yZW5NMlZYRm9VaXR3VldWWmNYSjNSWGhyVERKaFUwWTVNVVJQY0ZJclJpdERTamN2VUhaUFNraEhVazlaYnpOVk4wY3ZLMmxzWnk5MmRWVTBUV294UWtWbFNrbzFVRmN4U0VoRlF6QnhVMlpRUVVKc1pYVnhWV0ZQVFdkSVkxbEplazB6TUdoblNEUnhSRVUzYm1wNmFIQmxXRFY1SzI5NFQwd3hiVWxIZG14bE1Fc3lZbGwzUVVNMVlWWkhWbVpVWXpsMWMyUkZOa2hxVTJoMFUwMVRjRVpCZVU5clJqTkVVbTlvVm0xRmNUaHhhR05NZUV4S09VZHlMMVkwWlVOSVRHNTJibTlwZWxGRk1tOU5jblprTjBOWGNFUklPRzg1YlRSM2MwUXhNVlYyYURsMGVrUm1hUzk2UlVvMmJEQTNSMmREVUhadE1VMTRlWEpXWXpsWGJEQXdkRVJ4VnpWdmNFMXNPRE5uSzNkS1ZHcFdhbGR4Vm5OTlZVUnlWRTlDZUN0NGJDOHhVbWRvZWxaVFZqaHVhVU13VFZkeU5tNHJiRTFOWmk5cU5GWnBNVlpSYXpReU1rdG5la2x4ZUdkbGRYZEhNWG81UjBneVFWVlZUa05zVURBelpFaHFjSEpFV25WamFVNTRXRk5aTTJsU1JXcEZNVEpKY2tGak9XeEpOalY2ZEVaUFkxRXlMelp3U0dVMVJ5dEtZWGxqTlRJeVptTkVNblJNWTJFeFp5c3ZhR1ZqT1daSWF6TnJMMGxpUVhWRlUzbE5RekJ5TW1vck1rWk5ibmsxTDFReWNFZGljemRvTlhoWk9XVkNVbkpIYnpFMFdIbG9Oa3BYTVd0VFlrRmtWRXBuUkdNM1ZYVmpWbXRwVWxsRk1Xa3hVQzlKWm5aSGJrRnpRM2h5TUdFd2FXTXZkRFl4U1VkaE1rNXJSVU5YVFZSVU5IWkhNR1I2ZEd0VFV6ZzNRVEZrUm1SQ2NtVTNjbWxpVm1vNGFVTkJOUzl6WTBwMk5TOTNSbEVyZVRoamJVSXZUMmRDZEhsbFEzVjVNbEJMTUVJdlJESkVWbU5NTmtGV1YwSXdjVzR5V0hacU1TdHllV3hFWWxOWkt6SnhlVUpFWkhSUGQyeFFiREZOYUM4Mk1rUkZiVkkwVFVadlRuSnFNVmRDZHpsR2NXNUVNRTVTWXpoMFkxUlFiRzVSVDJ3eGJWZFZVV05MU0dOb1RsUXpTMlJoVDA1SWFVZFFSMk0wZVVVNFprVlNZVU51WWxOYWJUVTBiME5RUmtZelZtNDNOVzlRZUZOcFNuUXpZVk13Y1dSYVRTdEZhbXh0TTBsdGRGUlNSMDB3WjNGblUyVjRSbGhwWkhoQ1NYVnhXRmRvVURWRVpWVTJhMEV4TlhJd2JVTm1VbTVxU2k5clVETlpRV3B3UjFCc1FrSnhTbUpMVlRkWWNHUnRkbmhVSzFsdFJYbzFRakprVkZVd1NsUndkV2hPYzFVNWVFa3hZbVE0ZWtWd2NtUlFNbWcwT1RoRVIwc3lhazR2TkVZdmNuY3dORGxvWm1SV1drWlhPVmx2U2tSMFF6ZHBiRXhtUXpVNWJqSTJNMkpaU2xGaGNHdFpSMjgxZHk5VU5YTnViMUZsTTB4VE1rcERiak40YjB0Q04yOVpiU3RNWm1oamFXWTBXVkpzVEhGRVREQkdUQzlhY1Uwdk1TdGhhelJwUkRaQlYxbzVhVmRhTTBsSlJWQlBUMUpSVDIxVmNFcFNlRGR6UTFFeVNrZHVLMHhuYjNKU1pqZGlPRVoxVDBVeFZUUlNlQ3M1T0d4b1FYZFNTRGRTVDJKSU1rYzJiekpwUnpkMFIza3ZNbmwwVWtwVlkxRldkazlETW5wSk1VVkhRVWQwUVVJclZFMVFjek5NVWpGUlpXOXdSMGxzY25kdmJqSlRkbVJrT1d3cmNITnFUMVUyY21GamVEZERRMlJJTlU5dFpIcDJaRGhHWm5KTFRuY3pUbGxOUlV4RFQwOXdaVTlrVjBsQ2RqWTNUMDUwZDBwbVNWYzFkVUZLV1VwSVRsWlZhemhFYVVsamJrSXlUVUZsY1VrNFNqZHNaWEpTY1UwNE5tNXFiV3RDYVVwWlpGcHVUbVZDTWpWalRqaG5kMnRuTTFkM0x6UkpkMDQzVDJOclZWQlBTazFEWVdaa1YwaHJOalJRYUhSSFZHMURRVzlETlRsS1dTOU1WR3c1YjNjM2RHUktlQzgyVUdSNk1tczNibnBuYldaQlJFbEhja3RVVVRkcldFOWhVVzFvVTBVMGVTOU1RMWh4TVVoTGRYaGlVek5IUlZsWFdUSmhiQzl0VmpoUFFUUXliMGw2UXpFNVFVVXllRGw0V20xM2QwOUlZM29yVVZsM1lrTTVjbGRrUzI5eU1UUlVSbWhDWkV0c1JVcE1WVEpQVjA1bVVtSmtWblpwYlN0cGMzVmpWWGsxWVdGeGNXb3liVUpxU0d3MFJUTkNaVFJpTXpNM1RVSlFTRkJHTjB3MVFXSmtXVWQ2UTNOUGFETktOemRaUm5BM1FWWnBZelpyYVUxV2IxVXdhVmx4UzFOblkwMDFRMkZXWlZoMk9WZ3ZXWGhZYWtoVlRYVTBWbTV0Vkc1QmIxQnhjMUJDUWxKNVZsWjRPRXg0U1ZWNk5tbFZVRVo2TVU1TU1UVlZSVmM0U3k5MmRrMVJkRXBVVGpKbk0xUldMM0JEYlVwRWJGaEZRemx6UjFGa09FNVVUbTA0VFdKTWF5OVJUVXhJY1ZOUGNtTmhibGgxUjJjNVNHOXdTMkkzZUZobGRFeG1kM3BKVG1KNEwwSjNaSGh0S3paSE0ybFpSbTlIUXpCR1dXOUJSMDU1VVNzNE5WSjNabk5xVkdFd1NUVTRWelJqTmtKbFpHbFRibmMwY25OTFlUZFZiMnRTY0dGd05uaHdSRTE0YTBzeGNWVjNOV2d5T1c5Qk5taGxSekZuVGk5U00zaDBVVlpzWnpWMWRIZDVXVGhtVlc1elFTOVRXV0ZyTTNaMmVXcE1Sa1YxWm5kaFRVcFZWV2hzVW5OcWIxQTNjR0oyT1Rkb1NETk9TelphVjNrMFoxRkxVakJvVW01d1UyTlNRblpHY2xkcmJVcFlTRkZxTm1sdlZEazVZbmhqUW5kWFlqUlVTWFpwUTFsa2IxTmlWbkJrZERKQmNFRlRiMFpWVWtGSGVsQm5kbVZOVkhGUmMyeHlVM3BTYm1Sall6Tk5Oemx0UXlzeVNIUnBjVU0xTkZWWE4xVTVhbk40V0dOcVYwZFNTV1prVFd4TmJWTndSVkJoZFhSa01VNW1kR2tyVFZGbVpUaE9XbFJKZEV4dVozRm5TekJXUm10WFZXTTJia2sxY2xjMU9GUTJMMWhoWjNaWFdEZFhZVmxyWVROck5VcFVXbXRuU1V0eGFYRlJZa2N6TVdGc2N6UnZaVzVMYlRSaVZtNWpNMnh1Wm5Wb1ZWWTJaelpTWkM4ck1HeHdOalZHTTJWUlVuTktWbVJ4Vm5KUldtTjNSbE4zVXprdlMzWkdZVzAwTTJOVmMxbEZTV2wwUlZSb09GSlNiM0F5VERkclJXcDJPRmxUTVRsMlV6aHJZV1p0T1RkRU9IVTBRMFJ6Wm1SaVoyZFBUblV3YW1Jd1F5dEJPVlJTVEd4TGNFVndOMk5yV0N0TGIzWm9VVTFyUzJKeE1VdGlTMlJPWVRVMkx5OXpiRUUwT0dScmNqbEVjME5xY210Q1ZWSlpTRGgxTDJoMlkxRTBjMVZwYldGTmJuWkNUREZQYkdWb05YcHBaMnMyS3pjeVEzWlJUR2hMWVdsUFNGRktRMUZMU20xWmJYWTFhbUZpWXpBeGNVcFpVRzA1ZDFsR1JVWXZaMWxFTDBrd2MwUldORU4xUzJGck9YcHlLMVZaYzFaQk9FSTRXamMxYWtkNFRXNXVSV2xDTVRaT1oyTmFOSFJXUkdSdVRVSllMMFk1TVZsQ2NWQnNOSEJuU25kTlEzaE1aelZ2YjJNMlduRkVlRGhDYkhWS0wzZE1VbkpGT0VkUWVWZ3JURnBMWWxScmFYUnJWamhYZEVsVGNVWldUemh3YlM5a0szQnlPWEF2UVd4QlpWbElWalZSYUdGRUwxRXhWbnBxUm1kcFFVaHNZWEpCUFQwLldtVC1ldTJkZ2hyamhiRjAtU2JNZGtMMDd5X1E5bEVrOTNxVnBKVDlnXzBWcGVIeEptRXJqaWRVV0ZUOE90dnJuYzU1UXZ3NDNNZWgyQUZ0SGhDUGRR",
        "_eventId":"submit",
        "rememberMe": "true"

    }
    log = session.post(login_url, data=postdata, headers=headers)
    log = session.get("http://user.zxxk.com/Default.aspx", headers=headers)
    print(log.text)
    pa = r'<strong class ="bl-name">\s+(.*)\s+</strong>'
    print(pa)
    res = re.findall(pa, log.text)
    print(res)
    if res == []:
        print("登录失败，请检查你的手机号和密码输入是否正确")
    else:
        print('欢迎使用模拟登录')


if __name__ == '__main__':
    telephone = "15221638601"
    password = "511322"
    login(telephone, password)