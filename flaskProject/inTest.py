import time
import os

log_content = """
2025.06.10_14.47.08___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr executablePath: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\thirdsbin\puppeteer\win-x64\node_modules\.cache\puppeteer\chrome\win64-130.0.6723.69\chrome-win64\chrome.exe
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param url: ___http://localhost:8080/bi/Viewer?proc=1&action=viewer&hback=true&renderAll=true&frameid=%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311&db=%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC&au_act=pptr&_EXPORT_ELEMENT_=%E5%AE%9A%E5%88%B6%E7%BB%84%E4%BB%B61
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param cookie: ___[object Object],[object Object],[object Object],[object Object]
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param dbSize: ___1422,539
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param captureInfo: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\temp\b3f661c1f84d426789e9b09dc433401b.png~2.0~266.0~1410~263
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param pptrTS: ___1749538028802
2025.06.10_14.47.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr is pptr ready ___start
2025.06.10_14.50.13___<%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610144640-311,%E9%A2%84%E8%A7%88%3A+%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr runtime exception err: ___timeout
2025.06.10_14.52.36___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr executablePath: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\thirdsbin\puppeteer\win-x64\node_modules\.cache\puppeteer\chrome\win64-130.0.6723.69\chrome-win64\chrome.exe
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param url: ___http://localhost:8080/bi/Viewer?proc=1&action=viewer&hback=true&renderAll=true&frameid=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138&db=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC&au_act=pptr&_EXPORT_ELEMENT_=%E5%AE%9A%E5%88%B6%E7%BB%84%E4%BB%B61
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param pptrTS: ___1749538356827
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param dbSize: ___1422,539
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param captureInfo: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\temp\0d79eec4ef6d4629b2db5caf2b46401a.png~2.0~266.0~1410~263
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param cookie: ___[object Object],[object Object],[object Object],[object Object]
2025.06.10_14.52.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr is pptr ready ___start
2025.06.10_14.55.40___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145231-138,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr runtime exception err: ___timeout
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param url: ___http://localhost:8080/bi/Viewer?proc=1&action=viewer&hback=true&renderAll=true&frameid=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676&db=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC&au_act=pptr&_EXPORT_ELEMENT_=%E5%AE%9A%E5%88%B6%E7%BB%84%E4%BB%B61
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param captureInfo: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\temp\c11ed6c8f83a41d9bb0cba5fde4bdb64.png~2.0~266.0~1410~263
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param cookie: ___[object Object],[object Object],[object Object],[object Object]
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param pptrTS: ___1749538647115
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param dbSize: ___1422,539
2025.06.10_14.57.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr is pptr ready ___start
2025.06.10_15.00.27___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610145628-1676,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr runtime exception err: ___timeout
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param cookie: ___[object Object],[object Object],[object Object],[object Object]
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param captureInfo: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\temp\8af87974c8234ad8b762368bc3337a6a.png~2.0~266.0~1410~263
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param dbSize: ___1422,539
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param url: ___http://localhost:8080/bi/Viewer?proc=1&action=viewer&hback=true&renderAll=true&frameid=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894&db=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC&au_act=pptr&_EXPORT_ELEMENT_=%E5%AE%9A%E5%88%B6%E7%BB%84%E4%BB%B61
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param pptrTS: ___1749539795842
2025.06.10_15.16.35___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151626-894,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr is pptr ready ___start
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param url: ___http://localhost:8080/bi/Viewer?proc=1&action=viewer&hback=true&renderAll=true&frameid=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330&db=%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC&au_act=pptr&_EXPORT_ELEMENT_=%E5%AE%9A%E5%88%B6%E7%BB%84%E4%BB%B61
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param cookie: ___[object Object],[object Object],[object Object],[object Object]
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param pptrTS: ___1749539808401
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param captureInfo: ___D:\yhbi\YonghongZSuite_v11.0.1\vividime\temp\2da5beabc0cd4d30835b242fa34bebe4.png~2.0~266.0~1410~263
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr param dbSize: ___1422,539
2025.06.10_15.16.49___<%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC20250610151648-1330,%E6%81%92%E9%80%9A%E7%90%86%E8%B4%A2_%E5%AF%BC%E5%87%BA%E5%AF%8C%E6%96%87%E6%9C%AC>___pptr is pptr ready ___start"""

# date_time = strftime('[[%Y-%m-%d]]', localtime())

time_tulpe = time.time() - 60 * 60 * 24 * 7
# time_tulpe.tm_year = 2023
# time_tulpe.tm_mon = 10




def gen_pptr_log():
    for i in range(300,400):
        time_tulpe = time.time() - 60 * 60 * 24 * i
        date_time = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime(time_tulpe))
        # time.sleep(0.8)
        filename = f"pptr.log_{date_time}"
        print(filename)
        with open(f'D:\old_version\pptrLog\{filename}','w') as file:
            file.write(log_content)
        # print(f"pptr.log_{date_time}")
    
def change_log_time():
    log_path = [r'D:\old_version\102_vividime\vividime\log',r'D:\old_version\102_vividime\vividime\logpack']
    for path in log_path:
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            continue
        for i in os.listdir(path):
            if i.startswith('pptr.log_2024'):
                bash = f"powershell -command \"(Get-Item '{path}\\{i}').LastWriteTime = '2024-08-14 15:17:36'\""
                # powershell -command "(Get-Item 'C:\path\to\your\file.txt').LastWriteTime = '2024-08-14 15:17:36'"
                with os.popen(bash, 'r') as file:
                    file.read()
                    print(file.read(),end='')
                    print(f"Changed time for file: {i}")
                # print(f'{log_path}\{i}')


change_log_time()