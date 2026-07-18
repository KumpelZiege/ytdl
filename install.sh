#!/data/data/com.termux/files/usr/bin/bash
# 🎵 YTDL - YouTube Music Downloader Installer

# Colors
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
MAGENTA='\033[95m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

clear
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${MAGENTA}  ██╗   ██╗████████╗██████╗ ██╗      █████╗ ██████╗ ██╗  ██╗${RESET}"
echo -e "${BLUE}  ╚██╗ ██╔╝╚══██╔══╝██╔══██╗██║     ██╔══██╗██╔══██╗██║ ██╔╝${RESET}"
echo -e "${CYAN}   ╚████╔╝    ██║   ██║  ██║██║     ███████║██████╔╝█████╔╝ ${RESET}"
echo -e "${GREEN}    ╚██╔╝     ██║   ██║  ██║██║     ██╔══██║██╔══██╗██╔═██╗ ${RESET}"
echo -e "${YELLOW}     ██║      ██║   ██████╔╝███████╗██║  ██║██║  ██║██║  ██╗${RESET}"
echo -e "${RED}     ╚═╝      ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo -e "${BOLD}${YELLOW}   🎵  YTDL INSTALLER  •  YouTube Music Downloader${RESET}"
echo -e "${CYAN}   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

# Check Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}❌ This script must be run in Termux!${RESET}"
    exit 1
fi

echo -e "${BLUE}📦 Installing dependencies...${RESET}"
pkg update -y &>/dev/null
pkg install python python-pip ffmpeg -y &>/dev/null
pip install yt-dlp ytmusicapi mutagen requests &>/dev/null
echo -e "${GREEN}✅ Dependencies installed!${RESET}"

echo -e "${BLUE}📁 Creating directories...${RESET}"
mkdir -p ~/.termux/bin
mkdir -p /storage/emulated/0/Music/YouTube
echo -e "${GREEN}✅ Directories created!${RESET}"

echo -e "${BLUE}⬇️  Downloading YTDL script...${RESET}"
curl -s -o /storage/emulated/0/Download/ytdl.py https://github.com/KumpelZiege/ytdl.git
echo -e "${GREEN}✅ Script downloaded!${RESET}"

echo -e "${BLUE}🔧 Creating ytdl command...${RESET}"
cat > ~/.termux/bin/ytdl << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python /storage/emulated/0/Download/ytdl.py
EOF
chmod +x ~/.termux/bin/ytdl

# Add PATH
if ! grep -q ".termux/bin" ~/.bashrc; then
    echo 'export PATH="$HOME/.termux/bin:$PATH"' >> ~/.bashrc
fi
source ~/.bashrc

echo ""
echo -e "${GREEN}✅ INSTALLATION COMPLETE!${RESET}"
echo ""
echo -e "${YELLOW}🎵 Type 'ytdl' to start downloading music!${RESET}"
echo -e "${CYAN}📁 Music saved to: /storage/emulated/0/Music/YouTube/${RESET}"
echo -e "${MAGENTA}🔥 Happy downloading!${RESET}"
echo ""
