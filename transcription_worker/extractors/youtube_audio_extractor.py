import os
import yt_dlp
from .base_audio_extractor import AudioExtractor

class YouTubeExtractor(AudioExtractor):
    def download_and_extract(self, url: str, output_path: str) -> str:
        print(f"[*] Downloading audio from YouTube: {url}")
        
        final_file_name = "audio.wav"
        full_file_path = os.path.join(output_path, final_file_name)
        
        ydl_opts = {
            'format': 'bestaudio/best', 
            'outtmpl': os.path.join(output_path, 'audio.%(ext)s'), 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio', 
                'preferredcodec': 'wav',  
            }],
            'quiet': True,        
            'no_warnings': True  
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not os.path.exists(full_file_path):
                raise FileNotFoundError(f"Expected audio file not found at: {full_file_path}")
                
            return full_file_path
            
        except Exception as e:
            print(f"[!] Failed to extract audio from YouTube: {e}")
            raise