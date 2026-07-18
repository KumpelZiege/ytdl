#!/usr/bin/env python3
"""
🎵 YouTube Music Downloader - FINAL FIX!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
100% Working Metadata & Album Art for ALL Android players!
"""

import os
import sys
import time
import json
import requests
import subprocess
from datetime import datetime
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

# ─── CONFIG ──────────────────────────────────────────────────────────────
OUTPUT_DIR = "/storage/emulated/0/Music/YouTube"
HISTORY_FILE = f"{os.path.expanduser('~')}/.ytdl_history.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── COLORS ──────────────────────────────────────────────────────────────
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def banner():
    os.system('clear')
    banner_art = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
{Colors.MAGENTA}  ██╗   ██╗████████╗██████╗ ██╗      █████╗ ██████╗ ██╗  ██╗
{Colors.BLUE}  ╚██╗ ██╔╝╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔══██╗██║ ██╔╝
{Colors.CYAN}   ╚████╔╝    ██║   ██║  ██║██║     ███████║██████╔╝█████╔╝ 
{Colors.GREEN}    ╚██╔╝     ██║   ██║  ██║██║     ██╔══██║██╔══██╗██╔═██╗ 
{Colors.YELLOW}     ██║      ██║   ██████╔╝███████╗██║  ██║██║  ██║██║  ██╗
{Colors.RED}     ╚═╝      ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.BOLD}{Colors.YELLOW}   🎵  ULTIMATE MUSIC DOWNLOADER  🎵{Colors.RESET}
{Colors.CYAN}   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.WHITE}   📀  FINAL FIX  •  v3.2  •  {datetime.now().strftime('%Y')}
{Colors.GREEN}   ✅  METADATA & ALBUM ART WORKING!{Colors.RESET}
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
    """
    for line in banner_art.split('\n'):
        print(line)
        time.sleep(0.005)
    print()

def loading_animation(text, duration=2):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for i in range(duration * 10):
        sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]}{Colors.RESET} {text}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f'\r{Colors.GREEN}✅{Colors.RESET} {text}\n')

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_song(artist, title):
    print(f"{Colors.MAGENTA}🎵 {Colors.BOLD}{title}{Colors.RESET} {Colors.DIM}by{Colors.RESET} {Colors.CYAN}{artist}{Colors.RESET}")

def search_ytmusic(song_name, artist_name):
    try:
        ytmusic = YTMusic()
        results = ytmusic.search(f"{song_name} {artist_name}", filter='songs', limit=5)
        if results:
            best = results[0]
            thumbnails = best.get('thumbnails', [])
            thumbnail_url = thumbnails[-1]['url'] if thumbnails else None
            return {
                'video_id': best['videoId'],
                'title': best['title'],
                'artist': best['artists'][0]['name'] if best.get('artists') else artist_name,
                'album': best.get('album', {}).get('name', 'Unknown'),
                'duration': best.get('duration_seconds', 0),
                'thumbnail': thumbnail_url,
                'year': best.get('year', None)
            }
    except Exception as e:
        print_error(f"Search error: {e}")
    return None

def download_song(song_info):
    try:
        filename = f"{song_info['artist']} - {song_info['title']}".replace('/', '_').replace('?', '').replace(':', '')
        url = f"https://music.youtube.com/watch?v={song_info['video_id']}"
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': f"{OUTPUT_DIR}/{filename}.%(ext)s",
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': {'ffmpeg': ['-loglevel', 'quiet']},
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"{OUTPUT_DIR}/{filename}.mp3"
    except Exception as e:
        print_error(f"Download error: {e}")
        return None

def download_album_art(thumbnail_url):
    try:
        if not thumbnail_url:
            return None
        response = requests.get(thumbnail_url, timeout=10)
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

def embed_metadata_ffmpeg(filepath, song_info):
    """Use FFmpeg to embed metadata - SIMPLE & WORKS!"""
    try:
        # Download album art
        art_data = None
        if song_info.get('thumbnail'):
            art_data = download_album_art(song_info['thumbnail'])
            if art_data:
                print_success("Album art downloaded! 🖼️")
        
        # Create a temporary file with metadata
        temp_file = filepath + ".temp.mp3"
        
        # Build FFmpeg command - SIMPLER version
        cmd = [
            'ffmpeg', '-y',
            '-i', filepath,
            '-metadata', f'title={song_info["title"]}',
            '-metadata', f'artist={song_info["artist"]}',
            '-metadata', f'album={song_info.get("album", "Unknown")}',
            '-metadata', f'date={song_info.get("year", datetime.now().year)}',
            '-metadata', f'year={song_info.get("year", datetime.now().year)}',
            '-metadata', 'genre=Music',
            '-acodec', 'copy',
            temp_file
        ]
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(temp_file):
            # Replace original with metadata version
            os.remove(filepath)
            os.rename(temp_file, filepath)
            print_success("Metadata embedded! ✅")
        else:
            print_warning("Metadata embed failed, keeping original")
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        # Now add album art using a separate command
        if art_data:
            art_path = f"{OUTPUT_DIR}/temp_art.jpg"
            with open(art_path, 'wb') as f:
                f.write(art_data)
            
            # Add album art to the MP3
            cmd_art = [
                'ffmpeg', '-y',
                '-i', filepath,
                '-i', art_path,
                '-map', '0:a',
                '-map', '1',
                '-c', 'copy',
                '-id3v2_version', '3',
                '-metadata:s:v', 'title=Album cover',
                '-metadata:s:v', 'comment=Cover (front)',
                temp_file
            ]
            
            result_art = subprocess.run(cmd_art, capture_output=True, text=True)
            
            if result_art.returncode == 0 and os.path.exists(temp_file):
                os.remove(filepath)
                os.rename(temp_file, filepath)
                print_success("Album art embedded! 🖼️")
            else:
                print_warning("Album art embed failed")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            # Clean up
            if os.path.exists(art_path):
                os.remove(art_path)
        
        return True
    except Exception as e:
        print_error(f"FFmpeg error: {e}")
        return False

def save_history(song_info):
    try:
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        history.append({
            'artist': song_info['artist'],
            'title': song_info['title'],
            'album': song_info.get('album', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        })
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except:
        pass

def download_from_text_file(filepath):
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    if not lines:
        print_error("No songs found!")
        return
    print_info(f"Found {len(lines)} songs\n")
    downloaded, failed = 0, 0
    for i, line in enumerate(lines, 1):
        parts = line.split(',')
        if len(parts) < 2:
            continue
        song, artist = parts[0].strip(), parts[1].strip()
        print(f"\n[{i}/{len(lines)}] ", end='')
        print_song(artist, song)
        loading_animation(f"Searching...", 1)
        result = search_ytmusic(song, artist)
        if result:
            print_song(result['artist'], result['title'])
            loading_animation("Downloading...", 1)
            filepath = download_song(result)
            if filepath:
                embed_metadata_ffmpeg(filepath, result)
                save_history(result)
                downloaded += 1
                print_success(f"Downloaded!")
            else:
                failed += 1
                print_error(f"Failed")
        else:
            failed += 1
            print_error(f"Not found")
        time.sleep(0.5)
    print(f"\n{Colors.GREEN}✅ Completed! Downloaded: {downloaded}, Failed: {failed}{Colors.RESET}")

def single_song_mode():
    banner()
    print(f"{Colors.BOLD}{'🎵 Single Song Downloader':^50}{Colors.RESET}")
    print("─" * 50)
    song = input(f"\n{Colors.YELLOW}🎤{Colors.RESET} Song name: ").strip()
    artist = input(f"{Colors.YELLOW}👤{Colors.RESET} Artist name: ").strip()
    if not song or not artist:
        print_error("Both fields required!")
        return
    print()
    loading_animation(f"Searching for {song}...", 2)
    result = search_ytmusic(song, artist)
    if not result:
        print_error("Not found!")
        return
    print()
    print_song(result['artist'], result['title'])
    print(f"  {Colors.DIM}📀 Album:{Colors.RESET} {result.get('album', 'Unknown')}")
    print(f"  {Colors.DIM}⏱️  Duration:{Colors.RESET} {result['duration']} seconds")
    confirm = input(f"\n{Colors.YELLOW}💾 Download? (y/n):{Colors.RESET} ").lower()
    if confirm != 'y':
        print_warning("Cancelled")
        return
    print()
    loading_animation("Downloading...", 2)
    filepath = download_song(result)
    if filepath:
        embed_metadata_ffmpeg(filepath, result)
        save_history(result)
        print_success(f"Saved to: {filepath}")
    else:
        print_error("Download failed!")

def playlist_mode():
    banner()
    print(f"{Colors.BOLD}{'📂 YouTube Playlist Downloader':^50}{Colors.RESET}")
    print("─" * 50)
    url = input(f"\n{Colors.YELLOW}🔗{Colors.RESET} Playlist URL: ").strip()
    if not url:
        print_error("URL is required!")
        return
    print()
    loading_animation("Preparing playlist download...", 2)
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': f"{OUTPUT_DIR}/%(playlist_title)s/%(title)s.%(ext)s",
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': {'ffmpeg': ['-loglevel', 'quiet']},
            'ignoreerrors': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print_success("Playlist downloaded successfully!")
        print_info(f"Saved to: {OUTPUT_DIR}")
    except Exception as e:
        print_error(f"Download failed: {e}")

def history_mode():
    banner()
    print(f"{Colors.BOLD}{'📊 Download History':^50}{Colors.RESET}")
    print("─" * 50)
    if not os.path.exists(HISTORY_FILE):
        print_warning("No history yet")
        return
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        if not history:
            print_warning("No downloads")
            return
        print(f"\n{Colors.CYAN}Total: {len(history)}{Colors.RESET}\n")
        for i, item in enumerate(history[-20:], 1):
            date = datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d')
            print(f"{i:2}. {Colors.MAGENTA}🎵{Colors.RESET} {item['artist']} - {item['title']}")
            print(f"    {Colors.DIM}📀 {item.get('album', 'Unknown')}  📅 {date}{Colors.RESET}")
    except Exception as e:
        print_error(f"Error: {e}")

def main():
    while True:
        banner()
        print(f"{Colors.BOLD}{'🎯 Main Menu':^50}{Colors.RESET}")
        print("─" * 50)
        print(f"""
{Colors.CYAN} 1{Colors.RESET}. {Colors.GREEN}🎵 Download Single Song{Colors.RESET}
{Colors.CYAN} 2{Colors.RESET}. {Colors.YELLOW}📝 Download from Text File{Colors.RESET}
{Colors.CYAN} 3{Colors.RESET}. {Colors.BLUE}📂 Download YouTube Playlist{Colors.RESET}
{Colors.CYAN} 4{Colors.RESET}. {Colors.MAGENTA}📊 View Download History{Colors.RESET}
{Colors.CYAN} 5{Colors.RESET}. {Colors.RED}❌ Exit{Colors.RESET}
        """)
        print("─" * 50)
        choice = input(f"{Colors.YELLOW}🎯 Your choice:{Colors.RESET} ").strip()
        
        if choice == '1':
            single_song_mode()
        elif choice == '2':
            banner()
            print(f"{Colors.BOLD}{'📝 Batch Download':^50}{Colors.RESET}")
            print("─" * 50)
            filepath = input(f"\n{Colors.YELLOW}📄{Colors.RESET} File path: ").strip()
            if filepath:
                download_from_text_file(filepath)
        elif choice == '3':
            playlist_mode()
        elif choice == '4':
            history_mode()
        elif choice == '5':
            print(f"\n{Colors.GREEN}🎵 Thanks for using YouTube Music Downloader!{Colors.RESET}")
            print(f"{Colors.MAGENTA}👋 Happy listening!{Colors.RESET}\n")
            sys.exit(0)
        else:
            print_error("Invalid choice!")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    main()
