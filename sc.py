"""
	Shutter Counter
"""

from bottle import Bottle, run, template, request, response


##### FUNCTIONS #####

def get_text_form():
	""" 업로드 페이지에 사용할 텍스트를 반환한다.
		사용자 언어 확인 & 설정 후, 언어에 맞는 텍스트를 반환.

		TO-DO: 텍스트를 파일로 따로 저장하고 불러올까?
	"""

	t = {}
	if get_lang() == 'ko':
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
		t['title'] = 'DSLR 셔터 카운터'
		t['wrng_acc'] = '부적절한 접근입니다!'
		t['js_big'] = '파일이 너무 큽니다! (최대 크기: 20MB)'
		t['up_fail'] = '업로드 실패!'
		t['exif_fail'] = 'Exif 정보를 해석할 수 없는 파일입니다.'
		t['no_sc'] = '파일 내 촬영 횟수 정보가 존재하지 않습니다.'
		t['sc1'] = '총 촬영 횟수는 '
		t['sc2'] = ' 회입니다.'
		t['goback'] = '돌아가기'
	else:
		t['title'] = 'DSLR Shutter Counter'
		t['wrng_acc'] = 'Invalid Access!'
		t['js_big'] = 'The file is TOO BIG! (Max size: 20MB)'
		t['up_fail'] = 'Uploading failed.'
		t['exif_fail'] = 'This file contains no Exif data.'
		t['no_sc'] = 'There is no shutter count information in this file.'
		t['sc1'] = 'Shutter Count: '
		t['sc2'] = ''
		t['goback'] = 'BACK'
	return t

def get_lang():
	""" 언어 확인 & 쿠키 설정 후, 언어값 반환.  """

	if request.forms.get('lang'):		# 사용자가 언어 변경을 요청했을 때
		lang = 'ko' if request.forms['lang'] == 'ko' else 'en'
	elif request.cookies.get('lang'):
		return 'ko' if request.cookies['lang'] == 'ko' else 'en'
	elif request.environ.get("HTTP_ACCEPT_LANGUAGE"):
		lang = 'ko' if request.environ['HTTP_ACCEPT_LANGUAGE'] == 'ko' else 'en'
	else:
		lang = 'en'

	response.set_cookie('lang', lang)
	return lang


##### ROUTING #####

app = Bottle()

@app.route('/')
def show_form():
	""" 첫 페이지. 사진 업로드 폼 출력  """
	t = get_text_form()
	return template('upload.tpl', t=t)

@app.route('/result', methods="POST")
def show_result():
	"""" 사진 분석 & 결과 출력  """
	t = get_text_result()
	return template('result.tpl', t=t)

@app.route('/result')
@app.route('/result/')
def access_error():
	""" 결과 페이지에 대한 잘못된 접근 처리 """


##### MAIN #####

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)