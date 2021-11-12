import os
import datetime
import requests
import json
# import multiprocessing.forking
import sys
# import threading
import multiprocessing
from time import sleep


try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    forking.Popen = _Popen

def lookup(lock, n, numbers, proxy_no, proxies):
	name = ""
	non_match = ""
	
	def write(file, num, type):
		with open(file, type) as f:
			f.write(num+"\n")
	try:
		try:
			name = ""
			non_match = ""
			carrier_name = ""
			unmatch = ""
			non_number = ""
			taken = ""
			number = ""
			r = ""
			data = ""

			with lock:
				if proxy_no.value == len(proxies)-1:
					proxy_no.value = 0
				proxy = proxies[proxy_no.value].strip()
				http_proxy  = "http://{}".format(proxy)
				https_proxy = "https://{}".format(proxy)
				http_proxy = { 
				              "http"  : http_proxy, 
				            }				
				https_proxy = { 
				              "https"  : https_proxy, 
				            }
			
				proxy_no.value +=1
				try:
					number = numbers[n.value].strip()
					n.value += 1
				except KeyboardInterrupt as e:
					write("count/count.txt", str(n.value), "w")			
				except Exception as e:
					print(e)					
			try:
				print(n.value)
				url = ""
				url = "https://api.telnyx.com/anonymous/v2/number_lookup/{}".format(number)				
				r = requests.get(url, proxies=https_proxy, timeout=10)
				data = json.loads(r.text)
				name = data['data']['carrier']['name']
			except KeyboardInterrupt as e:
				write("count/count.txt", str(n.value), "w")
				
			except Exception as e:
				try:
					r = requests.get(url, proxies=http_proxy, timeout=10)
					data = json.loads(r.text)
					name = data['data']['carrier']['name']
					if name is "":
						print("yes")
				except KeyboardInterrupt as e:
					write("count/count.txt", str(n.value), "w")
				except Exception as e:
					print("Api request failed. Number moved to 'not_found.txt'")					
				try:
					carrier_name = name.upper()
				except KeyboardInterrupt as e:
					write("count/count.txt", str(n.value), "w")
				except Exception as e:
					print(e)
					
			print(carrier_name)
			if carrier_name is "" and number is not "":
				write("results/not_found.txt", number, "a")
			elif "CELLCO" in carrier_name and "PARTNERSHIP" in carrier_name and "DBA" in carrier_name:
				taken = number[1:]+"@vtext.com"
				write("results/results.txt", taken, "a")
			elif "VERIZON" in carrier_name:
				taken = number[1:]+"@vtext.com"
				write("results/results.txt", taken, "a")
			elif "SPRINT" in carrier_name:
				taken = number[1:]+"@messaging.sprintpcs.com"
				write("results/results.txt", taken, "a")
			elif "NEW" in carrier_name and "CINGULAR" in carrier_name and "WIRELESS" in carrier_name:
				taken = number[1:]+"@txt.att.net"
				write("results/results.txt", taken, "a")
			elif "AT&T" in carrier_name:
				taken = number[1:]+"@txt.att.net"
				write("results/results.txt", taken, "a")
			elif "PACIFIC" in carrier_name and "BELL" in carrier_name:
				taken = number[1:]+"@pacbellpcs.net"
				write("results/results.txt", taken, "a")
			elif "BANDWIDTH" in carrier_name and "CLEC" in carrier_name:
				taken = number[1:]+"@email.uscc.net"
				write("results/results.txt", taken, "a")
			elif "AERIAL" in carrier_name and "COMMUNICATIONS" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "STPCS" in carrier_name and "JOINT" in carrier_name and "VENTURE" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "POWERTEL" in carrier_name and "ATLANTA" in carrier_name and "LICENSES" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "POWERTEL" in carrier_name:
				taken = number[1:]+"@ptel.net"
				write("results/results.txt", taken, "a")
			elif "OMNIPOINT" in carrier_name and "COMMUNICATIONS" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "OMNIPOINT" in carrier_name and "MIAMI" in carrier_name and "LICENSE" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "OMNIPOINT" in carrier_name:
				taken = number[1:]+"@omnipoint.com"
				write("results/results.txt", taken, "a")
			elif "METRO" in carrier_name:
				taken = number[1:]+"@mymetropcs.com"
				write("results/results.txt", taken, "a")
			elif "T-MOBILE" in carrier_name and "USA" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "SUNCOM" in carrier_name and "DBA" in carrier_name and "T-MOBILE" in carrier_name:
				taken = number[1:]+"@tmomail.net"
				write("results/results.txt", taken, "a")
			elif "SUNCOM" in carrier_name:
				taken = number[1:]+"@tms.suncom.com"
				write("results/results.txt", taken, "a")				
			elif "UNION" in carrier_name and "TELEPHONE" in carrier_name:
				taken = number[1:]+"@union-tel.com"
				write("results/results.txt", taken, "a")			
			elif "VOICESTREAM" in carrier_name:
				taken = number[1:]+"@voicestream.net"
				write("results/results.txt", taken, "a")
			elif "CELLULAR" in carrier_name and "SOUTH" in carrier_name and "SVR/2" in carrier_name:
				taken = number[1:]+"@cspire1.com"
				write("results/results.txt", taken, "a")			
			elif "UNITED" in carrier_name and "CELLULAR" in carrier_name:
				taken = number[1:]+"@email.uscc.net"			
			elif "CELLULAR" in carrier_name:
				taken = number[1:]+"@email.uscc.net"
			elif "BLUEGRASS" in carrier_name and "CELLULAR" in carrier_name and "RSA4-SVR/2" in carrier_name:
			 	taken = number[1:]+"@sms.bluecell.com"
			 	write("results/results.txt", taken, "a")
			elif "BOOST" in carrier_name and "MOBILE" in carrier_name:
			 	taken = number[1:]+"@myboostmobile.com"
			 	write("results/results.txt", taken, "a")
			elif "US" in carrier_name and "CELLULAR" in carrier_name:
			 	taken = number[1:]+"@email.uscc.net"
			 	write("results/results.txt", taken, "a")
			elif "CRICKET" in carrier_name:
			 	taken = number[1:]+"@sms.mycricket.com"
			 	write("results/results.txt", taken, "a")
			elif "NEXTEL" in carrier_name:
			 	taken = number[1:]+"@messaging.nextel.com"
			 	write("results/results.txt", taken, "a")
			elif "VIRGIN" in carrier_name:
			 	taken = number[1:]+"@vmobl.com"
			 	write("results/results.txt", taken, "a")
			elif "CINGULAR" in carrier_name and "GSM" in carrier_name:
			 	taken = number[1:]+"@cingularme.com"
			 	write("results/results.txt", taken, "a")
			elif "CINGULAR" in carrier_name and "TDMA" in carrier_name:
			 	taken = number[1:]+"@mmode.com"
			 	write("results/results.txt", taken, "a")
			elif "BELL" in carrier_name and "MOBILITY" in carrier_name:
			 	taken = number[1:]+"@txt.bellmobility.ca"
			 	write("results/results.txt", taken, "a")			
			elif "BELL" in carrier_name and "ATLANTIC" in carrier_name and "NYNEX" in carrier_name:
			 	taken = number[1:]+"@vtext.com"
			 	write("results/results.txt", taken, "a")
			elif "BELL" in carrier_name:
			 	taken = number[1:]+"@txt.bell.ca"
			 	write("results/results.txt", taken, "a")
			elif "KOODO" in carrier_name and "MOBILE" in carrier_name:
			 	taken = number[1:]+"@msg.koodomobile.com"
			 	write("results/results.txt", taken, "a")
			elif "FIDO" in carrier_name and "Microcell" in carrier_name:
			 	taken = number[1:]+"@fido.ca"
			 	write("results/results.txt", taken, "a")
			elif "MANITOBA" in carrier_name and "TELECOM" in carrier_name and "SYSTEMS" in carrier_name:
			 	taken = number[1:]+"@text.mtsmobility.com"
			 	write("results/results.txt", taken, "a")
			elif "NBTEL" in carrier_name:
			 	taken = number[1:]+"@wirefree.informe.ca"
			 	write("results/results.txt", taken, "a")
			elif "PAGENET" in carrier_name:
			 	taken = number[1:]+"@pagegate.pagenet.ca"
			 	write("results/results.txt", taken, "a")
			elif "ROGERS" in carrier_name:
			 	taken = number[1:]+"@pcs.rogers.com"
			 	write("results/results.txt", taken, "a")
			elif "SASKTEL" in carrier_name:
			 	taken = number[1:]+"@sms.sasktel.com"
			 	write("results/results.txt", taken, "a")
			elif "TELUS" in carrier_name:
			 	taken = number[1:]+"@msg.telus.com"
			 	write("results/results.txt", taken, "a")
			elif "O2" in carrier_name:
			 	taken = number[1:]+"@mmail.co.uk"
			 	write("results/results.txt", taken, "a")
			elif "ORANGE" in carrier_name:
			 	taken = number[1:]+"@orange.net"
			 	write("results/results.txt", taken, "a")
			else:
				unmatch = carrier_name
				non_number = number
				non_match = "{}, {}".format(non_number, unmatch)
				write("results/unmatches.txt", non_match, "a")
		except KeyboardInterrupt as e:
			write("count/count.txt", str(n.value), "w")
		except Exception as e:
			print(e)
	except KeyboardInterrupt as e:
		print(e)
		write("count/count.txt", str(n.value), "w")
	except Exception as e:
		print(e)

def auth():
	password = input("Enter your password\n")
	if password == "123456":
		return True
	else:
		print("Wrong password, Please try again")
		import sys
		sys.exit()
def main(threads_no ):
	with open("results/unmatches.txt", "w") as f:
		f.write("")	

	# time = datetime.datetime.now()
	creds = ""

	# if int(time.day)<=30:
	files = os.listdir("number/")
	file = files[0]
	try:
		with open("results/not_found.txt", "r") as f:
			n_found = f.readlines()
	except:
		pass
	with open("results/not_found.txt", "w") as f:
		f.write("")
	try:
		with open(f'number/{file}', "r") as f:
			numbers = f.readlines()
	except:
		pass

	numbers = n_found+numbers		
	numbers = list(dict.fromkeys(numbers))
	if len(numbers)==0:
		print("No number is given")
		sys.exit()
	files = os.listdir("proxy/")
	file = files[0]
	with open(f'proxy/{file}', "r") as f:
		proxies = f.readlines()
	lock = multiprocessing.Lock()
	# shared memory
	try:
		with open("count/count.txt", "r") as f:
			count = int(f.read())
	except:
		count = 0
	n = multiprocessing.Value("i",  count)
	proxy_no = multiprocessing.Value("i",  0)
	print("Crawling is going to begin from {}\n".format(count))
	try:
		threads_no = int(threads_no)
	except:
		print("Threads must be a number")
		import sys
		sys.exit()
	total_threads = 0

	# numbers = numbers[:20]
	
	total_numbers = len(numbers)
	print("Total numbers: {}".format(total_numbers))
	while True:
		processes = []
		if total_threads>total_numbers:
			numbers = []
			# to check not_found is empty
			with open("results/not_found.txt", "r") as f:
				numbers = f.readlines()
			numbers = list(dict.fromkeys(numbers))
			if len(numbers) == 0:
				print("No number left to check!!!!!!!!\nTry with new ONE.")
				break 
			else:
				print("Reinitiating program!!!!!")
				with open("count/count.txt", "w") as f:
					f.write("0")
				# numbers = list(dict.fromkeys(numbers))
				# total_numbers = len(numbers)
				files = os.listdir("number/")
				file = files[0]
				with open(f'number/{file}', "w") as f:
					f.write("")
				main(threads_no)
		total_threads = total_threads+threads_no
		for _ in range(threads_no):
			p = multiprocessing.Process(target=lookup, args=(lock, n, numbers, proxy_no, proxies))
			processes.append(p)
		for process in processes:
			process.start()
		for process in processes:
			process.join()

if __name__ == "__main__":
	multiprocessing.freeze_support()
	try:
		if auth():
			threads_no = input("how many thread you would like to run?\n")
			main(threads_no)
	except:
		pass
	try:
		os.remove("creds.txt")
	except:
		pass
