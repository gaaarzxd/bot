# -*- coding: utf-8
# author : angga kurniawan
import os, sys, re, requests, json, time, datetime

web = datetime.datetime.now()
waktu = web.strftime("%H:%M:%S / %d-%m-%Y ")

def menu():
	komen = []
	global token
	os.system("clear")
	print("\n\033[0;97m ? gunakan tanda '\033[0;93m<>\033[0;97m' untuk ganti garis baru")
	print(" * ketik '\033[0;91mhapus\033[0;97m' untuk hapus token facebook")
	print(" ! gunakan dengan bijak, spam komentar jangan brutal\n")

	id = raw_input(" + id target : ")
	if id == "hapus" or id == "Hapus":
		ask = raw_input(" ? yakin ingin hapus token y/t: ")
		if ask == "t":
			print(" + kembali ke menu....")
			time.sleep(1)
			menu()
		elif ask == "y":
			os.system("rm -f login.txt")
			time.sleep(1)
			exit(" ! token berhasil di hapus")
		else:
			time.sleep(1)
			menu()

	kom = raw_input(" + komentar  : ")
	limit = raw_input(" ? limit     : ")
	delay = int(raw_input(" ? delay     : "))
	km = kom.replace("<>","\n")

	try:
		token = open('login.txt').read()
		r = requests.get("https://graph.facebook.com/"+ id+"?fields=feed.limit("+limit+")&access_token="+token)
		f = json.loads(r.text)
		for z in f["feed"]["data"]:
			idpost = z["id"]
			komen.append(idpost)
			pesan = waktu+"\n"+km
			time.sleep(delay)
			su = requests.post("https://graph.facebook.com/"+idpost+"/comments?message="+pesan+"&access_token="+token)
			asu = json.loads(su.text)
			if "id" in asu:
				print("\n + komen \033[0;96m%s/%s\033[0;97m berhasil"%((len(komen)), limit))
				print(" * id post  : \033[0;93m%s\033[0;97m"%(idpost))
				print(" * komentar : \033[0;93m%sxxx\033[0;97m"%(km[:20]))
			elif "error" in asu:
				print("\n + komen \033[0;96m%s/%s\033[0;97m gagal"%((len(komen)), limit))
				print(" * id post  : \033[0;93m%s\033[0;97m"%(idpost))
				print(" * komentar : \033[0;93m%sxxx\033[0;97m"%(km[:20]))
		
		print("\n # sudah selesai") 
		raw_input(" ? kembali ke menu... ") 
		time.sleep(1)
		menu()
	except KeyError:
		exit("\n ! pengguna id "+id+" tidak ditemukan")

if __name__ == "__main__":
	try:
		token = open("login.txt","r").read()
		menu()
	except KeyError, IOError:
		print("\n * ketik 'help' jika tidak tau cara ambil token fb")
		token = raw_input(" + token fb : ")
		try:
			otw = requests.get("https://graph.facebook.com/me?access_token="+token)
			a = json.loads(otw.text)
			avs = open("login.txt","w")
			avs.write(token)
			avs.close()
			time.sleep(1)
			menu()
		except KeyError:
			exit(" ! token kadaluwarsa")
