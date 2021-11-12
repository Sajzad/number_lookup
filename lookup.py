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
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen

def lookup(lock, n, numbers, proxy_no, proxies):

	name = ""
	non_match = ""
	
	def write(file, num):
		with open(file, "a") as f:
			f.write(num+"\n")
	try:
		while True:
			try:
				with lock:
					if proxy_no.value == len(proxies)-1:
						proxy_no.value = 0
					proxy = proxies[proxy_no.value].strip()
					print(proxy)
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
						print(number)
					except KeyboardInterrupt as e:
						with open("count/count.txt", "w") as f:
							f.write(str(n.value))
						break
					except Exception as e:
						print(e)
						break
					n.value += 1

				try:
					url = ""
					url = "https://api.telnyx.com/anonymous/v2/number_lookup/{}".format(number)				
					r = requests.get(url, proxies=https_proxy)
					data = json.loads(r.text)
					name = data['data']['carrier']['name']
					write("proxy.txt", proxy)

				except KeyboardInterrupt as e:
					with open("count/count.txt", "w") as f:
						f.write(str(n.value))
					break
				except Exception as e:
					try:
						r = requests.get(url, proxies=http_proxy)
						data = json.loads(r.text)
						name = data['data']['carrier']['name']
						write("proxy.txt", proxy)
					except KeyboardInterrupt as e:
						with open("count/count.txt", "w") as f:
							f.write(str(n.value))
						break
					except Exception as e:
						print("Api request failed. Number moved to 'not_found.txt'")
						write("not_found.txt", number)
						continue

				carrier_name = ""
				try:
					carrier_name = name.upper()
				except KeyboardInterrupt as e:
					with open("count/count.txt", "w") as f:
						f.write(str(n.value))
					break
				except Exception as e:
					continue
				print(carrier_name)
				if "CELLCO" in carrier_name and "PARTNERSHIP" in carrier_name and "DBA" in carrier_name:
					carrier_name = number[1:]+"@vtext.com"
					write("results.txt", carrier_name)
				elif "VERIZON" in carrier_name:
					carrier_name = number[1:]+"@vtext.com"
					write("results.txt", carrier_name)
				elif "SPRINT" in carrier_name:
					carrier_name = number[1:]+"@messaging.sprintpcs.com"
					write("results.txt", carrier_name)
				elif "NEW" in carrier_name and "CINGULAR" in carrier_name and "WIRELESS" in carrier_name:
					carrier_name = number[1:]+"@txt.att.net"
					write("results.txt", carrier_name)
				elif "AT&T" in carrier_name:
					carrier_name = number[1:]+"@txt.att.net"
					write("results.txt", carrier_name)
				elif "PACIFIC" in carrier_name and "BELL" in carrier_name:
					carrier_name = number[1:]+"@pacbellpcs.net"
					write("results.txt", carrier_name)
				elif "POWERTEL" in carrier_name:
					carrier_name = number[1:]+"@ptel.net"
					write("results.txt", carrier_name)
				elif "BANDWIDTH" in carrier_name and "CLEC" in carrier_name:
					carrier_name = number[1:]+"@email.uscc.net"
					write("results.txt", carrier_name)
				elif "AERIAL" in carrier_name and "COMMUNICATIONS" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "STPCS" in carrier_name and "JOINT" in carrier_name and "VENTURE" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "POWERTEL" in carrier_name and "ATLANTA" in carrier_name and "LICENSES" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "OMNIPOINT" in carrier_name and "COMMUNICATIONS" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "OMNIPOINT" in carrier_name and "MIAMI" in carrier_name and "LICENSE" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "OMNIPOINT" in carrier_name:
					carrier_name = number[1:]+"@omnipoint.com"
					write("results.txt", carrier_name)
				elif "METRO" in carrier_name:
					carrier_name = number[1:]+"@mymetropcs.com"
					write("results.txt", carrier_name)
				elif "T-MOBILE" in carrier_name and "USA" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "SUNCOM" in carrier_name and "DBA" in carrier_name and "T-MOBILE" in carrier_name:
					carrier_name = number[1:]+"@tmomail.net"
					write("results.txt", carrier_name)
				elif "SUNCOM" in carrier_name:
					carrier_name = number[1:]+"@tms.suncom.com"
					write("results.txt", carrier_name)				
				elif "UNION" in carrier_name and "TELEPHONE" in carrier_name:
					carrier_name = number[1:]+"@union-tel.com"
					write("results.txt", carrier_name)			
				elif "VOICESTREAM" in carrier_name:
					carrier_name = number[1:]+"@voicestream.net"
					write("results.txt", carrier_name)
				elif "CELLULAR" in carrier_name and "SOUTH" in carrier_name and "SVR/2" in carrier_name:
					carrier_name = number[1:]+"@cspire1.com"
					write("results.txt", carrier_name)			
				elif "UNITED" in carrier_name and "CELLULAR" in carrier_name:
					carrier_name = number[1:]+"@email.uscc.net"			
				elif "CELLULAR" in carrier_name:
					carrier_name = number[1:]+"@email.uscc.net"
				elif "BLUEGRASS" in carrier_name and "CELLULAR" in carrier_name and "RSA4-SVR/2" in carrier_name:
				 	carrier_name = number[1:]+"@sms.bluecell.com"
				 	write("results.txt", carrier_name)
				elif "BOOST" in carrier_name and "MOBILE" in carrier_name:
				 	carrier_name = number[1:]+"@myboostmobile.com"
				 	write("results.txt", carrier_name)
				elif "US" in carrier_name and "CELLULAR" in carrier_name:
				 	carrier_name = number[1:]+"@email.uscc.net"
				 	write("results.txt", carrier_name)
				elif "CRICKET" in carrier_name:
				 	carrier_name = number[1:]+"@sms.mycricket.com"
				 	write("results.txt", carrier_name)
				elif "NEXTEL" in carrier_name:
				 	carrier_name = number[1:]+"@messaging.nextel.com"
				 	write("results.txt", carrier_name)
				elif "VIRGIN" in carrier_name:
				 	carrier_name = number[1:]+"@vmobl.com"
				 	write("results.txt", carrier_name)
				elif "CINGULAR" in carrier_name and "GSM" in carrier_name:
				 	carrier_name = number[1:]+"@cingularme.com"
				 	write("results.txt", carrier_name)
				elif "CINGULAR" in carrier_name and "TDMA" in carrier_name:
				 	carrier_name = number[1:]+"@mmode.com"
				 	write("results.txt", carrier_name)
				elif "BELL" in carrier_name and "MOBILITY" in carrier_name:
				 	carrier_name = number[1:]+"@txt.bellmobility.ca"
				 	write("results.txt", carrier_name)			
				elif "BELL" in carrier_name and "ATLANTIC" in carrier_name and "NYNEX" in carrier_name:
				 	carrier_name = number[1:]+"@vtext.com"
				 	write("results.txt", carrier_name)
				elif "BELL" in carrier_name:
				 	carrier_name = number[1:]+"@txt.bell.ca"
				 	write("results.txt", carrier_name)
				elif "KOODO" in carrier_name and "MOBILE" in carrier_name:
				 	carrier_name = number[1:]+"@msg.koodomobile.com"
				 	write("results.txt", carrier_name)
				elif "FIDO" in carrier_name and "Microcell" in carrier_name:
				 	carrier_name = number[1:]+"@fido.ca"
				 	write("results.txt", carrier_name)
				elif "MANITOBA" in carrier_name and "TELECOM" in carrier_name and "SYSTEMS" in carrier_name:
				 	carrier_name = number[1:]+"@text.mtsmobility.com"
				 	write("results.txt", carrier_name)
				elif "NBTEL" in carrier_name:
				 	carrier_name = number[1:]+"@wirefree.informe.ca"
				 	write("results.txt", carrier_name)
				elif "PAGENET" in carrier_name:
				 	carrier_name = number[1:]+"@pagegate.pagenet.ca"
				 	write("results.txt", carrier_name)
				elif "ROGERS" in carrier_name:
				 	carrier_name = number[1:]+"@pcs.rogers.com"
				 	write("results.txt", carrier_name)
				elif "SASKTEL" in carrier_name:
				 	carrier_name = number[1:]+"@sms.sasktel.com"
				 	write("results.txt", carrier_name)
				elif "TELUS" in carrier_name:
				 	carrier_name = number[1:]+"@msg.telus.com"
				 	write("results.txt", carrier_name)
				elif "O2" in carrier_name:
				 	carrier_name = number[1:]+"@mmail.co.uk"
				 	write("results.txt", carrier_name)
				elif "ORANGE" in carrier_name:
				 	carrier_name = number[1:]+"@orange.net"
				 	write("results.txt", carrier_name)
				else:
					non_match = "{}, {}".format(number, carrier_name)
					write("unmatches.txt", non_match)
			except KeyboardInterrupt as e:
				with open("count/count.txt", "w") as f:
					f.write(str(n.value))
				break
			except Exception as e:
				continue
	except KeyboardInterrupt as e:
		print(e)
		write("count/count.txt", str(n.value))
	except Exception as e:
		print(e)



def main():
	time = datetime.datetime.now()
	password = input("Enter your password\n")
	if password == "123456":
		pass
	else:
		print("Wrong password, Please try again")
		import sys
		sys.exit()

	if int(time.day)<28:

		files = os.listdir("number/")
		file = files[0]
		with open("unmatches.txt", "r") as f:
			unmatch = f.readlines()

		with open(f'number/{file}', "r") as f:
			numbers = f.readlines()

		numbers = unmatch+numbers		
		numbers = list(dict.fromkeys(numbers))
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
		threads_no = input("how many thread you would like to run?\n")
		try:
			threads_no = int(threads_no)
		except:
			print("Threads must be a number")
			import sys
			sys.exit()
		processes = [multiprocessing.Process(target=lookup, args=(lock, n, numbers, proxy_no, proxies)) for _ in range(threads_no)]
		for process in processes:
			process.start()
		for process in processes:
			process.join()
	else:
		print("Please contact with Developer \nGive a phone call at 01856309604")

if __name__ == "__main__":
	multiprocessing.freeze_support()
	main()