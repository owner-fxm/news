from User.models import User
from libs.http import render_json
from common import status_code
from libs.nqcloud import upload_qncloud


def check_params(username,password,repassword,nickname):
    """
    验证参数
    :param username: 用户名
    :param password: 密码
    :param repassword: 确认密码
    :param nickname: 昵称
    :return:
    """
    if not all([username,password,repassword,nickname]):
        return render_json(code=status_code.PARMERR,resultValue='参数缺失')
    if password !=repassword:
        return render_json(code=status_code.PARMERR,resultValue='两次密码不一致')

    user = User.objects.filter(username=username).first()
    if user:
        return render_json(code=status_code.PARMERR,resultValue='此用户名已被注册')
    user = User.objects.filter(nick_name=nickname).first()
    if user:
        return render_json(code=status_code.PARMERR,resultValue='昵称已被使用')
    return True

def save_avatar(avatar,username):
    """
    保存头像
    :param avatar: 头像图片
    :param username: 用户名
    :return: url: 头像路径
    """
    filename = "New_avatar_%s" % username
    avatar_data = avatar.read()
    status,url = upload_qncloud(filename,avatar_data)
    if not status:
        return render_json(code=status_code.THIRDERR,resultValue='头像保存失败')
    return url