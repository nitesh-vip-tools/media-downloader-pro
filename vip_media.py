import os
import sys
import subprocess

R = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"

shared_dir = os.path.expanduser("~/storage/shared/VIP_TOOLS")
fallback_dir = os.path.expanduser("~/VIP_TOOLS")
SAVE_DIR = shared_dir if os.path.exists(os.path.expanduser("~/storage/shared")) else fallback_dir
os.makedirs(SAVE_DIR, exist_ok=True)


def banner():
    os.system("clear")
    print(f"{MAGENTA}{BOLD}=========================================================={R}")
    print(f"{CYAN}{BOLD}   ██╗   ██╗██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗{R}")
    print(f"{CYAN}{BOLD}   ██║   ██║██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝{R}")
    print(f"{MAGENTA}{BOLD}   ██║   ██║██║██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗{R}")
    print(f"{MAGENTA}{BOLD}   ╚██╗ ██╔╝██║██╔═══╝        ██║   ██║   ██║██║   ██║██║     ╚════██║{R}")
    print(f"{CYAN}{BOLD}    ╚████╔╝ ██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║{R}")
    print(f"{CYAN}{BOLD}     ╚═══╝  ╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝{R}")
    print(f"{MAGENTA}{BOLD}=========================================================={R}")
    print(f"{GREEN}{BOLD}   TOOL      : {YELLOW}MEDIA DOWNLOADER PRO{R}")
    print(f"{GREEN}{BOLD}   DEVELOPER : {CYAN}Nitesh Yadav{R}")
    print(f"{GREEN}{BOLD}   SAVE PATH : {BLUE}{SAVE_DIR}{R}")
    print(f"{MAGENTA}{BOLD}=========================================================={R}\n")


def menu():
    print(f"{CYAN}{BOLD}[1]{R} {GREEN}Best Quality Video (MP4 Merged){R}")
    print(f"{CYAN}{BOLD}[2]{R} {YELLOW}High Quality Audio (MP3 320kbps){R}")
    print(f"{CYAN}{BOLD}[3]{R} {BLUE}Photo / Thumbnail / Direct Media{R}")
    print(f"{CYAN}{BOLD}[4]{R} {MAGENTA}Batch Links (Multiple URLs at once){R}")
    print(f"{CYAN}{BOLD}[0]{R} {RED}Exit{R}")
    return input(f"\n{BOLD}{CYAN}Select Mode ➤ {R}").strip()


def run_yt_dlp(url, mode):
    out_tmpl = os.path.join(SAVE_DIR, "%(title).80s [%(id)s].%(ext)s")
    base_cmd = [
        "yt-dlp",
        "--no-warnings",
        "--newline",
        "--console-title",
        "-o", out_tmpl,
    ]

    if subprocess.call(["command", "-v", "aria2c"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        base_cmd += ["--downloader", "aria2c", "--downloader-args", "aria2c:-x 8 -s 8 -k 1M"]

    if mode == "1":
        cmd = base_cmd + [
            "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
            "--merge-output-format", "mp4",
            url,
        ]
    elif mode == "2":
        cmd = base_cmd + [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            url,
        ]
    elif mode == "3":
        cmd = base_cmd + [
            "--skip-download",
            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            url,
        ]
    else:
        return 1

    print(f"\n{YELLOW}{BOLD}Downloading... Please wait...{R}\n")
    return subprocess.call(cmd)


def main():
    while True:
        banner()
        choice = menu()

        if choice == "0":
            print(f"\n{GREEN}{BOLD}Thanks for using VIP TOOLS — Developer: Nitesh Yadav{R}\n")
            sys.exit(0)

        if choice not in {"1", "2", "3", "4"}:
            print(f"\n{RED}Invalid option! Press Enter to try again...{R}")
            input()
            continue

        if choice == "4":
            print(f"\n{CYAN}Paste links separated by space (or press Enter after each, then type 'done'):{R}")
            urls = []
            while True:
                line = input(f"{YELLOW}URL (or 'done') ➤ {R}").strip()
                if line.lower() == "done":
                    break
                if line:
                    urls.extend(line.split())
            sub_mode = input(f"{CYAN}Format for batch [1=MP4 Video, 2=MP3 Audio, 3=Photo/Thumb] ➤ {R}").strip()
            for u in urls:
                rc = run_yt_dlp(u, sub_mode if sub_mode in {"1", "2", "3"} else "1")
                if rc == 0:
                    print(f"\n{GREEN}{BOLD}✓ Completed: {u}{R}")
                else:
                    print(f"\n{RED}{BOLD}✗ Failed: {u}{R}")
            input(f"\n{CYAN}Press Enter to continue...{R}")
        else:
            url = input(f"\n{YELLOW}{BOLD}Paste Video / Photo / Audio Link ➤ {R}").strip()
            if not url:
                print(f"{RED}Link empty hai!{R}")
                input(f"\n{CYAN}Press Enter to continue...{R}")
                continue
            rc = run_yt_dlp(url, choice)
            if rc == 0:
                print(f"\n{GREEN}{BOLD}✓ Download Successful! Saved in: {SAVE_DIR}{R}")
            else:
                print(f"\n{RED}{BOLD}✗ Download failed. Link check karein ya yt-dlp update karein.{R}")
            input(f"\n{CYAN}Press Enter to continue...{R}")


if __name__ == "__main__":
    main()
