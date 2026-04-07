from .youtube_audio_extractor import YouTubeExtractor
from .base_audio_extractor import AudioExtractor
class AudioExtractorFactory:
    @staticmethod
    def get_extractor(source_type: str) -> AudioExtractor:
        if source_type == "youtube":
            return YouTubeExtractor()
        else:
            raise ValueError(f"Unsupported audio source for: {source_type}")