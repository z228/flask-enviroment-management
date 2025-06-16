from PIL import ImageGrab
import xlwings as xw
import pythoncom
import os
from time import sleep, localtime
import traceback
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import numpy
from shutil import rmtree
from json import dump, load
from logging import getLogger

task_logger = getLogger("task")
work_path = r'D:\code\python\yhenv\flaskProject\apps\productApp\jobs\genReport'
res_path = r'D:\\code\\python\\yhenv\\flaskProject\\apps\\productApp\\res'


def key_in_dict(key, key_dict):
    for i in key_dict:
        if i in key:
            return True
    return False


def create_muli_excel_save_img(files):
    '''
    Parameters
    ----------
    files : list
        Excel文件列表
    Returns
    -------
    None.
    '''
    # 读取excel内容转换为图片
    with os.popen('tasklist|findstr EXCEL') as runRes:
        if 'EXCEL' in runRes.read():
            os.system('TASKKILL /F /IM EXCEL.exe /T')
    pythoncom.CoInitialize()
    # 使用xlwings的app启动
    app = xw.App(visible=False, add_book=False, )
    app.display_alerts = False
    app.screen_updating = False
    # listener = MsgBoxListener('Microsoft Excel', 3)
    # listener.start()
    imgs = []
    exclude_file = ['Bug52030__Properties2', '特殊字符_1__Properties2']
    weekday = int(localtime()[6])
    for file in files:
        if not os.path.exists(file):
            continue
        file_name = os.path.basename(file)
        file_path = os.path.dirname(file)
        if key_in_dict(file_name, exclude_file):
            continue
        # 打开文件
        try:
            wb = app.books.open(file)
        except Exception as e:
            task_logger.error(e)
            # traceback.print_stack()
            # traceback.print_exc()
            continue
        sheet_length = len(wb.sheets)
        for i in range(sheet_length):
            # 选定sheet
            sheet = wb.sheets(wb.sheets[i].name)
            sheet_name = wb.sheets[i].name
            img_name = os.path.join(file_path, f'{file_name.split(".")[0]}_{sheet_name}.png')
            img_name = img_name.replace(' ', '_')
            if os.path.exists(img_name):
                if weekday == 6:
                    os.remove(img_name)
                else:
                    imgs.append(img_name)
                    continue
            # task_logger.info(img_name)
            count = 0
            while 1:
                try:
                    count += 1
                    # 获取有内容的区域
                    all_cell = sheet.used_range
                    sleep(1)
                    # 复制图片区域
                    all_cell.api.CopyPicture()
                    # 粘贴
                    sheet.api.Paste()
                    # 当前图片
                    pic = sheet.pictures[-1]
                    # 复制图片
                    pic.api.Copy()
                    # sleep(1)  # 延迟一下操作，不然获取不到图片
                    # 获取剪贴板的图片数据
                    # img = ImageGrab.grabclipboard()
                    # # 保存图片
                    # img.save(img_name)
                    # imgs.append(img_name)
                    if img := ImageGrab.grabclipboard():
                        img.save(img_name)
                        imgs.append(img_name)
                        task_logger.info(f"保存成功: {img_name}")
                    else:
                        task_logger.info(f"剪贴板无内容: {img_name}")
                    break
                except Exception as e:
                    if count == 5:
                        count += 1
                        break
                    task_logger.error(e)
                    sleep(3)  # 延迟一下操作，不然获取不到图片
                    task_logger.info(f'{img_name}保存失败,等待3s后尝试')
                # finally:
                #     pic.delete()  # 删除sheet上的图片
            if count <= 5:
                pic.delete()
        # 不保存，直接关闭
        wb.close()
    app.screen_updating = True
    app.quit()
    # listener.stop()
    pythoncom.CoUninitialize()  # 关闭多线程
    return imgs


def cv_imread(file_path):
    cv_img = cv2.imdecode(numpy.fromfile(file_path, dtype=numpy.uint8), -1)
    return cv_img


def gen_diff_png(exp, res):
    """
    :param exp:
    :param res:
    :return: 对比结果
    """
    # load the two input images
    exp_png = cv_imread(exp)
    res_png = cv_imread(res)
    file_base_name = os.path.basename(res).split('.')[0]

    diff_path = os.path.dirname(res).replace('res', 'diff')
    original_png = file_base_name + '_Exp.jpg'
    modify_png = file_base_name + '_Res.jpg'
    diff_png = file_base_name + '_diff.jpg'
    thresh_png = file_base_name + '_thresh.png'

    if exp_png.shape != res_png.shape:
        # task_logger.info(f'大小不匹配，{exp}:{exp_png.shape},{res}:{res_png.shape}')
        return f'大小不匹配，{exp}:{exp_png.shape},{res}:{res_png.shape}'

    # 先判断两张图片是否一致
    difference = cv2.subtract(exp_png, res_png)
    result = not numpy.any(difference)  # if difference is all zeros it will return False

    if result is True:
        # task_logger.info(f'{res} pass')
        return f'{res} pass'

    if not os.path.exists(diff_path):
        os.makedirs(diff_path)

    # convert the images to grayscale
    grayA = cv2.cvtColor(exp_png, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(res_png, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(exp_png, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(res_png, (x, y), (x + w, y + h), (0, 0, 255), 1)

    cv2.imencode(original_png, exp_png)[1].tofile(os.path.join(diff_path, original_png))
    cv2.imencode(modify_png, res_png)[1].tofile(os.path.join(diff_path, modify_png))

    cv2.putText(exp_png, 'exp', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
    cv2.putText(res_png, 'res', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
    diff_img = cv2.hconcat([exp_png, res_png])
    # cv2.imwrite(os.path.join(diff_path, thresh_png), thresh)
    cv2.imencode(diff_png, diff_img)[1].tofile(os.path.join(diff_path, diff_png))
    cv2.destroyAllWindows()
    # task_logger.info(f'{res} failed,diff:{diff_path}')
    return f'{res} failed,diff:{diff_path}'


def gen_xls_diff_png(file_root, current_version, branch):
    """
    :param current_version: 版本
    :param file_root: res根目录
    :return: none
    """
    # res_pngs = []
    with open(f'{res_path}/{branch}_fail_cases.json', 'r', encoding='utf-8') as fail_cases:
        fails = load(fail_cases)
        all_fails = [fail.split('/')[-1] for fail in list(fails['Export'].keys())]
    exp_xls_list = []
    res_xls_list = []
    for root, dirs, files in os.walk(file_root):
        for name in files:
            if '.xls' in name and '~$' not in name  and name.split('.xls')[0] in all_fails:
                res_xls_full_path = os.path.join(root, name)
                res_xls_list.append(res_xls_full_path)
                exp_xls_list.append(res_xls_full_path.replace('res', 'exp'))
    pngs = create_muli_excel_save_img(res_xls_list)
    create_muli_excel_save_img(exp_xls_list)
    with open(f'{work_path}\\{current_version}pngs.json', 'w', encoding='utf-8') as pngs_json:
        dump(pngs, pngs_json, indent=4, ensure_ascii=False)
    # with open('pngs.json', 'r', encoding='utf-8') as pngs_json:
    #     pngs = load(pngs_json)
    res_list = ''
    for res_png in pngs:
        exp_png = res_png.replace('res', 'exp')
        if not os.path.exists(exp_png) or not os.path.exists(res_png):
            continue
        try:
            res_list += gen_diff_png(exp_png, res_png) + '\n'
        except Exception:
            # traceback.print_exc()
            continue
    with open(f'{work_path}\\{current_version}-result.txt', 'w', encoding='utf-8') as result:
        result.write(res_list)


if __name__ == '__main__':
    versions = ['trunk', '10', '10.1']
    root_path = f'D:\\share\\export_xls_img\\{versions[0]}\\res'
    diff_img_path = root_path.replace('res', 'diff')
    if os.path.exists(diff_img_path):
        rmtree(diff_img_path)
    gen_xls_diff_png(root_path, versions[0])
