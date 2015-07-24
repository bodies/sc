"""
    Shutter Counter

    Version 0.1
"""

import os
import subprocess
from bottle import Bottle, template, request, response, static_file

import chkpool


"""
FUNCTIONS
"""


def get_text_form():
    """ 업로드 페이지에 사용할 텍스트를 반환한다.
        사용자 언어 확인 & 설정 후, 언어에 맞는 텍스트를 반환.

        TO-DO: 텍스트를 파일로 따로 저장하고 불러올까?
    """

    t = {}
    if get_lang() == 'ko':
        t['lang'] = 'ko'
        t['title'] = 'DSLR 셔터 카운터'
        t['kword'] = '셔터 카운트, 컷수, 셔터 카운터, 촬영 횟수, Exif, DSLR, 카메라, 사진기, 니콘, 펜탁스'
        t['main'] = 'DSLR 사진기의 촬영 횟수를 확인하는 웹 프로그램입니다.<br />편집하지 않은 사진 파일을 업로드하시면 촬영 시점의 컷수가 표시됩니다.'
        t['info'] = '* 현재 <u>니콘</u>과 <u>펜탁스</u> 카메라만 지원합니다.<br />* 편집(리사이즈 포함)한 파일은 제대로 분석되지 않을 수 있습니다.<br />* 서버 여건 상, 되도록 JPEG 파일로 업로드해주시길 부탁드립니다. (최대 <u>20MB</u>)<br />* 이용자의 개인정보와 파일은 저장되지 않습니다.'
        t['h3'] = '사진 파일 업로드'
        t['btn'] = '업로드'
        t['uploading'] = '업로딩 중..'
        t['js_nofile'] = '사진 파일을 선택해주십시오.'
        t['js_notype'] = '지원하는 형식이 아닙니다.'
        t['lang_sel'] = 'English'
    else:
        t['lang'] = 'en'
        t['title'] = 'DSLR Shutter Counter'
        t['kword'] = 'shutter count, shutter counter, shutter actuation count, Exif, DSLR, camera, Nikon, Pentax'
        t['main'] = 'Online camera shutter counter.<br />Upload a photo from your camera, and find out how many shots it has taken!'
        t['info'] = '* For now, only <u>Nikon</u> and <u>Pentax</u> cameras are supported.<br />* The photo file must be <u>unedited</u>. (Max file size: <u>20MB</u>)<br />* The file will not be stored.'
        t['h3'] = 'UPLOAD A PHOTO'
        t['btn'] = 'Upload'
        t['uploading'] = 'Uploading..'
        t['js_nofile'] = 'Please select a file.'
        t['js_notype'] = 'Not supported format.'
        t['lang_sel'] = '한국어'
    return t


def get_text_result():
    """ 결과 페이지에서 사용할 텍스트를 반환한다. (get_text_form과 거의 같음)  """

    t = {}
    if get_lang() == 'ko':
        t['lang'] = 'ko'
        t['title'] = 'DSLR 셔터 카운터'
        t['wrng_acc'] = '부적절한 접근입니다!'
        t['js_big'] = '파일이 너무 큽니다! (최대 크기: 20MB)'
        t['up_fail'] = '업로드를 실패했습니다!'
        t['exif_fail'] = 'Exif 정보를 해석할 수 없는 파일입니다.'
        t['no_sc'] = '파일 내 촬영 횟수 정보가 존재하지 않습니다.'
        t['sc1'] = '총 촬영 횟수는 '
        t['sc2'] = ' 회입니다.'
        t['goback'] = '돌아가기'
    else:
        t['lang'] = 'en'
        t['title'] = 'DSLR Shutter Counter'
        t['wrng_acc'] = 'Invalid Access!'
        t['js_big'] = 'The file is TOO BIG! (Max size: 20MB)'
        t['up_fail'] = 'Can\'t upload the file!'
        t['exif_fail'] = 'This file contains no Exif data.'
        t['no_sc'] = 'There is no shutter count information in this file.'
        t['sc1'] = 'Shutter Count: '
        t['sc2'] = ''
        t['goback'] = 'BACK'
    return t


def get_lang():
    """ 언어 확인 & 쿠키 설정 후, 언어값 반환.  """

    if request.forms.get('lang'):       # 사용자가 언어 변경을 요청했을 때
        lang = 'ko' if request.forms['lang'] == 'ko' else 'en'
    elif request.cookies.get('lang'):
        return 'ko' if request.cookies['lang'] == 'ko' else 'en'
    elif request.environ.get("HTTP_ACCEPT_LANGUAGE"):
        lang = 'ko' if request.environ['HTTP_ACCEPT_LANGUAGE'] == 'ko' else 'en'
    else:
        lang = 'en'

    response.set_cookie('lang', lang)
    return lang


"""
EXCEPTIONS
"""


class MyUploadError(Exception):
    def __init__(self, value):
            self.value = value


class MyAnalyzeError(Exception):
    def __init__(self, value):
            self.value = value


"""
CLASSES
"""


class ImageProcessor:
    """ 이미지 업로드 & EXIF 분석용 클래스  """

    err_msg = ""
    dest = ""
    t = {}

    def __init__(self, post_name, dest_dir, txt):
        self.file_obj = request.files.get(post_name)
        self.dest = dest_dir
        self.t = txt

    def chk_file_size(self):
        MAX_FILE_SIZE = 20 * 1024 * 1024
        print("file size: " + str(os.stat(self.file_obj.file.fileno()).st_size))
        if os.stat(self.file_obj.file.fileno()).st_size > MAX_FILE_SIZE:
            return False
        else:
            return True

    def upload(self):
        try:
            if not self.file_obj:
                # self.err_msg = self.t['up_fail']
                print('no file.obj')
                # return False
                raise MyUploadError(self.t['up_fail'])
            if not self.chk_file_size():
                # self.err_msg = self.t['js_toobig']
                # return False
                raise MyUploadError(self.t['js_toobig'])
            self.dest = self.dest + "/" + self.file_obj.raw_filename
            self.file_obj.save(self.dest, overwrite=True)
            # self.file_obj.save(self.dest)
        except MyUploadError:
            raise
        except Exception:
            raise MyUploadError(self.t['up_fail'])
        else:
            print("Uploaded successfully")
            return True

    def analyze(self):
        """ Exiftool을 이용해서 이미지 분석 후, 결과값 반환  """

        cmd = "exiftool -ShutterCount -ImageNumber -Make -Model -FileName -FileType -CreateDate -j".split()
        cmd.append(self.dest)
        try:
            # cmd에 파일명까지 넣고 split()할 경우, 파일명에 공백이 있을 경우, 에러가 난다

            res = eval(subprocess.check_output(cmd, universal_newlines=True).replace("\n", ""))
            if not res or not res[0]:
                print("RES?")
                raise Exception
        except Exception as e:
            print("???:", e.args[0])
            raise
        else:
            return res[0]

    def get_result(self):
        """ 이미지를 분석하고, 결과를 출력할 HTML 테이블을 만들어서 반환 """

        try:
            data = self.analyze()
        except:
            print("GET_RESULT")
            raise MyAnalyzeError(self.t['exif_fail'])

        # 셔터 카운트 얻기
        if 'ShutterCount' in data:
            shutter_count = data['ShutterCount']
        elif 'ImageNumber' in data:
            shutter_count = data['ImageNumber']
        else:
            shutter_count = 0

        if shutter_count:
            shutter_count = '{:,}'.format(int(shutter_count))
            res_sc = self.t['sc1'] + "<span class=\"count-num\">" + shutter_count + "</span>" + self.t['sc2']
        else:
            print(type(shutter_count))
            res_sc = '<div class="no_sc">' + self.t['no_sc'] + '</div>'

        # 필요한 데이터만 옮겨담기 (data -> result) & 항목명 번역
        res_dic = {}
        key_names = {"Make": "제작사", "Model": "제품명", "FileType": "파일 종류", "CreateDate": "촬영일자"}
        if self.t['lang'] == 'ko':
            for data_key in data.keys():
                if data_key in key_names:
                    res_dic[key_names[data_key]] = data[data_key]
        else:
            for data_key in data.keys():
                if data_key in key_names:
                    res_dic[data_key] = data[data_key]

        if res_dic:
            tbl = []
            tbl.append('<div class="sctable">{}</div>\n<table cellspacing="0" id="resultTable">'.format(res_sc))
            for k, v in res_dic.items():
                tbl.append('<tr class="etcinfo"><td><b>{0}</b></td><td>{1}</td></tr>'.format(k, v))
            tbl.append('</table>')
        else:
            tbl = [self.t['exif_fail']]

        return ''.join(tbl)


"""
ROUTING
"""

app = Bottle()

app.mount('/chkpool', chkpool.app)


@app.route('/')
@app.route('/', method="POST")
def show_form():
    """ 첫 페이지. 사진 업로드 폼 출력  """
    t = get_text_form()
    return template('upload.tpl', t=t)


@app.route('/result', method="POST")
def show_result():
    """" 사진 분석 & 결과 출력  """

    t = get_text_result()
    img = ImageProcessor('imagefile', 'pool', t)

    try:
        img.upload()
        result = img.get_result()
    except (MyUploadError, MyAnalyzeError) as e:
        return template('error.tpl', error=e.args[0])

    return template('result.tpl', t=t, result=result)


@app.route('/result')
@app.route('/result/')
def access_error():
    """ 결과 페이지에 대한 잘못된 접근 처리 """
    """ 고칠 것!! """
    return template('error.tpl', error='Invalid Access')


# @app.route('/clrpool')
# def clear_pool():
#     print("Clearing pool...")

#     pool_dir = 'pool/'
#     # arch_dir = pool_dir + 'arch/'
#     print('ClEARING...')

#     subprocess.call(("rm", "-rf", pool_dir))
#     os.mkdir('pool')

#     return ('<a href="chkpool">Go Back</a>')


@app.route('/static/<filename>')
def serve_static(filename):
    """ 정적 파일에 대한 요청을 처리 """
    return static_file(filename, root='static')


@app.route('/pool/arch/<filename>')
def serve_image(filename):
    """ For chkpool """
    return static_file(filename, root='pool/arch')


@app.error(404)
def error404(error):
    """ 없는 URL 접근 처리  """
    return "Nothing Here"


"""
MAIN
"""

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True, reloader=True)
