import os
import time
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

class KiBot:
    def __init__(self):
        self.url = "https://oyun.kiracbilisim.net/renk_guncelle.php"
        self.image_path = "image.png"
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://oyun.kiracbilisim.net",
            "Referer": "https://oyun.kiracbilisim.net/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_banner(self):
        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "="*50)
        print(Fore.WHITE + Style.BRIGHT + "            🚀 ki-bot v2.0 | Global Edition")
        print(Fore.WHITE + "               Developed by: Ubeyt & Tilbe")
        print(Fore.CYAN + Style.BRIGHT + "="*50 + "\n")

    def process_image(self):
        if not os.path.exists(self.image_path):
            print(Fore.RED + f"[!] Error: {self.image_path} not found.")
            return None

        img = Image.open(self.image_path).convert("RGB")
        img = img.resize((100, 100))
        pixels = img.load()

        tasks = []
        for y in range(100):
            for x in range(100):
                r, g, b = pixels[x, y]
                hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
                cell_id = (y * 100) + x
                tasks.append((cell_id, hex_color))
        return tasks

    def send_batch(self, session, pixel_list, thread_id):
        count = 0
        for cell_id, color in pixel_list:
            try:
                data = {"hucre": str(cell_id), "renk": color}
                response = session.post(self.url, headers=self.headers, data=data, timeout=5)
                count += 1
                
                if count % 50 == 0:
                    print(Fore.BLUE + f"[Thread-{thread_id}] ❯ {count} pixels completed.")
                
                time.sleep(0.05) # Rate limit protection
            except Exception:
                continue
        return f"Thread-{thread_id} finished successfully."

    def start_operation(self):
        self.show_banner()
        tasks = self.process_image()
        if not tasks: return

        try:
            print(Fore.YELLOW + "[?] Configuration")
            thread_count = int(input(Fore.WHITE + "Enter thread count (Recommended: 5): ") or "5")
            
            confirm = input(Fore.WHITE + f"Start drawing with {thread_count} threads? (y/n): ")
            if confirm.lower() != 'y': return

            print(Fore.GREEN + "\n[*] Operation started. Press Ctrl+C to abort.")
            
            # Splitting tasks into chunks for parallel processing
            size = len(tasks) // thread_count
            chunks = [tasks[i:i + size] for i in range(0, len(tasks), size)]

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                with requests.Session() as session:
                    futures = [executor.submit(self.send_batch, session, chunks[i], i+1) for i in range(len(chunks))]
                    for future in as_completed(futures):
                        print(Fore.GREEN + f"✔ {future.result()}")

            print(Fore.CYAN + "\n[+] Task completed. Press Enter to return to menu.")
            input()

        except KeyboardInterrupt:
            print(Fore.RED + "\n\n[!] Aborted by user. Returning to main menu...")
            time.sleep(1.5)
        except ValueError:
            print(Fore.RED + "\n[!] Invalid input. Please enter a number.")
            time.sleep(1.5)

    def menu(self):
        while True:
            self.show_banner()
            print(Fore.WHITE + "1. 🎨 Start Painting")
            print(Fore.WHITE + "2. ℹ️ Information")
            print(Fore.RED + "3. 🚪 Exit")
            
            choice = input(Fore.CYAN + "\nSelection ❯ ")

            if choice == '1':
                self.start_operation()
            elif choice == '2':
                print(Fore.YELLOW + "\n[Info] target: 100x100 Grid")
                print(Fore.YELLOW + "[Info] Input: image.png")
                input("\nPress Enter to continue...")
            elif choice == '3':
                print(Fore.MAGENTA + "Goodbye.")
                break

if __name__ == "__main__":
    bot = KiBot()
    bot.menu()