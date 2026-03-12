"""
Audio Processor Service
Handles audio format conversion and preprocessing for dysarthric speech
"""

import os
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Audio preprocessing pipeline:
    1. Convert to WAV format
    2. Resample to 16kHz
    3. Convert to mono
    4. Apply basic noise reduction (optional)
    """
    
    def __init__(self):
        self.target_sample_rate = 16000
        self.target_channels = 1
        self._ffmpeg_available = self._check_ffmpeg()
        self._ready = True
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("FFmpeg not found. Audio conversion may be limited.")
            return False
    
    def is_ready(self):
        """Check if audio processor is ready"""
        return self._ready
    
    def process(self, input_path):
        """
        Process audio file for speech recognition
        
        Args:
            input_path: Path to input audio file
            
        Returns:
            Path to processed WAV file
        """
        # Get file extension
        _, ext = os.path.splitext(input_path)
        ext = ext.lower()
        
        # If already a proper WAV, just return
        if ext == '.wav':
            if self._validate_wav(input_path):
                return input_path
        
        # Convert to WAV
        return self._convert_to_wav(input_path)
    
    def _convert_to_wav(self, input_path):
        """Convert audio to WAV format with correct parameters"""
        output_path = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.wav'
        ).name
        
        if self._ffmpeg_available:
            return self._convert_with_ffmpeg(input_path, output_path)
        else:
            return self._convert_with_python(input_path, output_path)
    
    def _convert_with_ffmpeg(self, input_path, output_path):
        """Use FFmpeg for conversion"""
        try:
            command = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-i', input_path,
                '-ar', str(self.target_sample_rate),  # Sample rate
                '-ac', str(self.target_channels),  # Channels
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-af', 'highpass=f=80,lowpass=f=8000',  # Basic filtering
                output_path
            ]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise Exception("Audio conversion failed")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timeout")
            raise Exception("Audio conversion timed out")
    
    def _convert_with_python(self, input_path, output_path):
        """
        Fallback conversion using Python libraries
        Requires pydub or similar
        """
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(input_path)
            
            # Convert to mono
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Resample
            audio = audio.set_frame_rate(self.target_sample_rate)
            
            # Export as WAV
            audio.export(output_path, format='wav')
            
            return output_path
            
        except ImportError:
            logger.warning("pydub not available, copying file as-is")
            import shutil
            shutil.copy(input_path, output_path)
            return output_path
    
    def _validate_wav(self, file_path):
        """Check if WAV file has correct parameters"""
        try:
            import wave
            with wave.open(file_path, 'rb') as wav:
                channels = wav.getnchannels()
                sample_rate = wav.getframerate()
                return (channels == self.target_channels and 
                       sample_rate == self.target_sample_rate)
        except Exception:
            return False
    
    def apply_noise_reduction(self, audio_path):
        """
        Apply basic noise reduction using FFmpeg
        
        Note: For production, consider using more sophisticated
        noise reduction libraries like noisereduce
        """
        if not self._ffmpeg_available:
            return audio_path
        
        output_path = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.wav'
        ).name
        
        try:
            command = [
                'ffmpeg',
                '-y',
                '-i', audio_path,
                '-af', 'afftdn=nf=-20:nr=10:nt=w',  # Adaptive noise reduction
                output_path
            ]
            
            subprocess.run(command, capture_output=True, timeout=60)
            return output_path
            
        except Exception as e:
            logger.warning(f"Noise reduction failed: {e}")
            return audio_path
    
    def normalize_amplitude(self, audio_path):
        """Normalize audio amplitude"""
        if not self._ffmpeg_available:
            return audio_path
        
        output_path = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.wav'
        ).name
        
        try:
            command = [
                'ffmpeg',
                '-y',
                '-i', audio_path,
                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                output_path
            ]
            
            subprocess.run(command, capture_output=True, timeout=60)
            return output_path
            
        except Exception as e:
            logger.warning(f"Normalization failed: {e}")
            return audio_path
    
    def trim_silence(self, audio_path, threshold='-40dB', duration=0.5):
        """Remove silence from beginning and end"""
        if not self._ffmpeg_available:
            return audio_path
        
        output_path = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.wav'
        ).name
        
        try:
            command = [
                'ffmpeg',
                '-y',
                '-i', audio_path,
                '-af', f'silenceremove=start_periods=1:start_threshold={threshold}:start_duration={duration}',
                output_path
            ]
            
            subprocess.run(command, capture_output=True, timeout=60)
            return output_path
            
        except Exception as e:
            logger.warning(f"Silence trimming failed: {e}")
            return audio_path
