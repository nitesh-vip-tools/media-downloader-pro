#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update -y && pkg install -y python ffmpeg aria2
pip install --upgrade yt-dlp
mkdir -p "$HOME/vip_media_downloader"
cp "$(dirname "$0")/vip_media.py" "$HOME/vip_media_downloader/vip_media.py"
cat << 'LAUNCHER' > "$PREFIX/bin/vipdl"
#!/data/data/com.termux/files/usr/bin/bash
python "$HOME/vip_media_downloader/vip_media.py"
LAUNCHER
chmod +x "$PREFIX/bin/vipdl"
echo "Installed! Run 'vipdl' anytime."
