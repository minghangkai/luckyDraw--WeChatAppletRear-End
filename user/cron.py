import time
import os

def create_dir_according_time():
    localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('localtime='+localtime)
    # 系统当前时间年份
    year=time.strftime('%Y',time.localtime(time.time()))
    # 月份
    month=time.strftime('%m',time.localtime(time.time()))
    # 日期
    day=time.strftime('%d',time.localtime(time.time()))
    #具体时间 小时分钟毫秒
    mdhms=time.strftime('%m%d%H%M%S',time.localtime(time.time()))
    print('1111'+os.getcwd())
    fileYear=os.getcwd()+'/PycharmProjects/luckyDraw--WeChatAppletRear-End/media/uploadfile'+'/'+year
    fileMonth=fileYear+'/'+month
    fileDay=fileMonth+'/'+day
    if not os.path.exists(fileYear):
      os.mkdir(fileYear)
      os.mkdir(fileMonth)
      os.mkdir(fileDay)
    else:
        if not os.path.exists(fileMonth):
            os.mkdir(fileMonth)
            os.mkdir(fileDay)
        elif not os.path.exists(fileDay):
            os.mkdir(fileDay)
    print("自动执行成功")
    return 0


def doprint():
    print('111111')