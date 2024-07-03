from make import genimg
import time
from datetime import datetime
from datetime import timedelta as TD
import win32con
import win32api
import win32gui
import os.path
from win32api import GetMonitorInfo
from win32api import MonitorFromPoint
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor = monitor_info.get('Monitor')
timetype_translate = {'秒':'SECONDS','分钟':'MINUTES','小时':'HOURS',
                                '天':'DAYS','月':'MONTHS','年':'YEARS', 
                                '时':'HOURS', '节课':'LESSONS',}
def set_wallpaper(image_path):
	key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
	win32api.RegSetValueEx(key, "WallpaperStyle", 6, win32con.REG_SZ, "6")
	win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, image_path, 1 + 2)
def countdown(end_h, end_m, end_s, year, month, day, zh, en, offset=9):
	refresh_rate = 0
	current = datetime.today()
	exact_time = datetime.today().replace(year=year, month=month, day=day, hour=end_h, minute=end_m, second=end_s)+TD(seconds=offset)
	while current < exact_time:
		current = datetime.today()
		time.sleep(refresh_rate)
		if current >= exact_time:
			break
		# timedelta的两个属性：days和seconds
		delta = (exact_time-current)
		delta_days, delta_seconds = delta.days, delta.seconds
		if delta_days>365:
			e = '年'
			l = delta_days//365
			refresh_rate = 1919810
			 # no need to refresh. more than a year away.
		elif delta_days>30:
			e='月'
			l=delta_days//30
			refresh_rate = 1919810
		elif delta_days>0:
			e='天'
			l = delta_days
			refresh_rate = 1919810
		else:
			lefth = timedelta // 3600
			leftm = (timedelta - 3600*lefth) // 60
			lefts = timedelta % 60
			if lefth > 0:
				e = '小时'
				l = lefth
				refresh_rate = leftm*60+1
			elif leftm > 5:
				e = '分钟'
				l = (leftm//5+1)*5
				refresh_rate = 180
			elif leftm > 0:
				e = '分钟'
				l = leftm
				refresh_rate = 10
			else:
				e = '秒'
				l = lefts
				refresh_rate = 0.4
		genimg((zh, en), e, l, outpath='pic.png')
		set_wallpaper(os.path.realpath('.')+'\\pic.png')
		if delta_days > 0:
			exit(0)
	exit(0)


if os.path.exists('data.txt'):
	try: 
		with open('data.txt', encoding='utf-8') as f:
			content = [line.strip() for line in f.readlines()]
			zh = content[0]
			en = content[1]
			year, month, day, hour, minute, second = [int(i) for i in content[2].split()]
		countdown(hour, minute, second, year, month, day, zh, en)
	except Exception:
		pass

zh = input("输入中文提示语，距：").strip('距离')
en = input("输入英文提示语，翻译以上中文即可：").upper().strip().strip('TILL').strip('IN')

y, m, d, end_h, end_m, end_s = [int(i) for i in input("请输入倒计时结束时间，年、月、日、时、分、秒用空格隔开：").split()]
with open('data.txt', 'w', encoding='utf-8',) as f:
	f.write(zh+'\n')
	f.write(en+'\n')
	f.write(' '.join(str(i) for i in [y, m, d, end_h, end_m, end_s]))
countdown(end_h, end_m, end_s, y, m, d, zh, en)
