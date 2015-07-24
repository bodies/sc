"""
Chkpool for Shutter Counter

"""

from bottle import Bottle, template

from glob import iglob
from os import path, mkdir
from subprocess import call


DIR_POOL = 'pool/'
DIR_ARCH = DIR_POOL + 'arch/'

app = Bottle()


@app.route("/")
def check_pool():
    """ TO-DO: 오류시 처리 방법  """

    print("In check_pool... ")

    global DIR_POOL, DIR_ARCH
    file_size = 0
    totla_size = 0
    file_count = 0
    output = []

    if not path.exists(DIR_ARCH):
        mkdir(DIR_ARCH)

    for file in iglob(DIR_POOL + '/*'):

        if not path.isfile(file):  # 디렉토리는 패스
            continue

        # 원래 파일 준비 & 사이즈 측정
        file_name = path.basename(file)
        path_orig = DIR_POOL + file_name
        file_size = path.getsize(path_orig)
        totla_size += file_size
        file_count += 1

        name, ext = path.splitext(file_name)
        ext = ext.lower()

        if ext in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):

            # 원본이 JPEG이 아니라면, 결과 파일의 확장자를 jpg로 변경 (convert 처리를 위해)
            if not (ext == '.jpg' or ext == '.jpeg'):
                path_new = DIR_ARCH + name + '.jpg'
                path_tn = DIR_ARCH + 'tn_' + name + '.jpg'
            else:
                path_new = DIR_ARCH + file_name
                path_tn = DIR_ARCH + "tn_" + file_name

            # 리사이즈 & 썸네일 파일이 없으면 만듬
            if not path.exists(path_new):
                call(['convert', '-resize', '1024', '-quality', '80%', path_orig, path_new])
                call(['convert', '-resize', '100', '-quality', '80%', path_orig, path_tn])

            output.append('<a href="{}" target="_new"><img src="{}" /></a>'.format(path_new, path_tn))
        else:
            output.append(file_name)

        output.append('({}, {:,} KB)<br />'.format(file_name, round(file_size / 1024)))

    output.append('<br \><br \>{} file(s), {:,} KB<br /><br />\
        <a href="chkpool/clear">Clear All</a>'.format(file_count, round(totla_size / 1024)))

    return template("chkpool.tpl", result=''.join(output))


@app.route("/clear")
def clear_pool():
    global DIR_POOL, DIR_ARCH

    call(("rm", "-rf", DIR_POOL))
    mkdir(DIR_POOL)

    return ('<a href="./">Back</a>')
