# fiz isso em umas 2 horas, provavelmente não vou tentar melhorar isso, não reclame desse codigo lixo, fiz 4fun + não codo em python kk

import sys

import asyncio
import aiohttp

from itertools import product

from colorama import init, Fore, Style

init(autoreset = True)

POSSIBLE_CHARS = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		  '1', '2', '3', '4', '5', '6', '7', '8', '9', '_' ] # vou me matar

config = { 
	"log_valids": True,
	"log_invalids": False,
	"nick_length": 3,
	"req_size": 10,
	"delay": 2
}

URL = "https://api.mojang.com/profiles/minecraft"

FILE_LOCK = asyncio.Lock()

async def get_all_combinations():
	nicks = [ "".join(p) for p in product(POSSIBLE_CHARS, repeat = config["nick_length"]) ]

	return nicks

async def process_response(nicks, data):
	print(Fore.YELLOW + "[Info] Nicks:", nicks)
	
	if not isinstance(data, list):
		print(Fore.RED + Style.BRIGHT + "[Fail] Invalid API response, ignoring...")
		return

	if not data:
		valid_nicks = nicks
		invalid_nicks = []
	else:
		invalid_nicks = [ player["name"] for player in data ]

		invalid_nicksl = { player["name"].lower() for player in data }
		valid_nicks = [ name for name in nicks if name.lower() not in invalid_nicksl ]

	async with FILE_LOCK: # sim, isso vai dar gargalo, mas quem liga
		if config["log_invalids"]:
			with open("data/invalids.txt", "a") as invalids:
				for nick in invalid_nicks:
					invalids.write(nick + "\n")

		if config["log_valids"]:
			with open("data/valids.txt", "a") as valids:
				for nick in valid_nicks:
					valids.write(nick + "\n")

	if len(valid_nicks) > 0:
		print(Fore.GREEN + Style.BRIGHT + "[Success] Found valids:", valid_nicks)

async def send_request(session, nicks):
	async with session.post(URL, json = nicks) as response:
		data = await response.json()
		await process_response(nicks, data)

async def main():
	print(Style.BRIGHT + Fore.CYAN + "[Info] Getting All nicks combinations...")
	print(Style.BRIGHT + Fore.RED + "[Alert] This is python: More than 4 chars length nicks will cause delay in this part...")

	nicks = await get_all_combinations()

	async with aiohttp.ClientSession() as session:
		for i in range(0, len(nicks), config["req_size"]):
			asyncio.create_task(send_request(session, nicks[i : i + config["req_size"]]))
			await asyncio.sleep(config["delay"])

		while True:
			pass

def handle_args(args):
	final = []

	for i in args:
		if "=" in i:
			arg, value = i.split("=", 1)
			final.extend([arg, value])

	if len(final) <= 0:
		return
	
	if len(final) % 2 != 0:
		print(Style.BRIGHT + Fore.RED + "[Error] Invalid args format")
		print(Style.BRIGHT + Fore.CYAN + "Example: \"py (path_to_main.py) -size=3 -delay=1 -only_letters=True -req_size=5\"")
		return
	
	for i in range(0, len(final), 2):
		arg = final[i]
		value = final[i + 1]

		if not arg.startswith("-"):
			continue

		if arg == "-delay":
			try:
				config["delay"] = int(value)

				if config["delay"] <= 0:
					config["delay"] = 1
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid delay value: Value needs to be a int value (seconds)...")
				print("Example: \"-delay=10\" (10 seconds)")

		if arg == "-size":
			try:
				config["nick_length"] = int(value)

				if config["nick_length"] > 16:
					config["nick_length"] = 16

				if config["nick_length"] < 2:
					config["nick_length"] = 2
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid size value: Value needs to be a int value (chars length, max is 16)...")
				print(Style.BRIGHT + Fore.CYAN + "Example: \"-size=3\" (3 chars, max is 16)")

		if arg == "-req_size":
			try:
				config["req_size"] = int(value)

				if config["req_size"] > 10:
					config["req_size"] = 10

				if config["req_size"] <= 0:
					config["req_size"] = 1
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid requests size value: Value needs to be a int value (length of nicks checked p/request, max is 10)...")
				print(Style.BRIGHT + Fore.CYAN + "Example: \"-req_size=10\" (10 nicks checked p/request, max is 10)")

		if arg == "-only_letters":
			try:
				global POSSIBLE_CHARS

				boolean = value.lower() == "true"

				if boolean:
					POSSIBLE_CHARS = POSSIBLE_CHARS[0::27]
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid only letters value: Value needs to be a bool value...")
				print(Style.BRIGHT + Fore.CYAN + "Example: \"-only_letters=True\"")

		if arg == "-log_invalids":
			try:
				config["log_invalids"] = value.lower() == "true"
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid log invalids value: Value needs to be a bool value...")
				print(Style.BRIGHT + Fore.CYAN + "Example: \"-log_invalids=True\"")

		if arg == "-log_valids":
			try:
				config["log_valids"] = value.lower() == "true"
			except:
				print(Style.BRIGHT + Fore.RED + "[Error] Invalid log valids value: Value needs to be a bool value...")
				print(Style.BRIGHT + Fore.CYAN + "Example: \"-log_valids=True\"")

if __name__ == "__main__":
	handle_args(sys.argv[::1])
	asyncio.run(main())