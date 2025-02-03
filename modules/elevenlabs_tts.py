from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import os

class ElevenLabsTTS:
    def __init__(self, api_key=None):
        load_dotenv()
        api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(
            api_key=api_key
        )
#        self.client = ElevenLabs()
        self.voice_id = 'wuWdl4Iz37U6Vlao5GGo'
        self.output_format = 'mp3_44100_128'
        self.model_id = 'eleven_multilingual_v2'
        self.language_code = 'pt-BR'


    def generate_audio(self, text, voice="default", output_file="output.mp3"):
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            output_format=self.output_format,
            model_id=self.model_id,
            voice_settings= {
                'stability': 0.7,
                'similarity_boost': 0.8,
                'style': 1,
                'use_speaker_boost': True
            }
        )
        return audio
    
    def save_audio(self, audio, output_file):
        save(audio, output_file)

# Exemplo de uso
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    tts = ElevenLabsTTS()
    audio = tts.generate_audio("Olá... 'Seja bem vinda!' disse com entusiasmo. Seja bem vindo! este é um teste de geração de áudio.", output_file="teste.mp3")
    save(audio, "teste3_0.7_0.8_1.mp3")
