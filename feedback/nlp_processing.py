import os
import re
import requests
from moviepy import AudioFileClip
from pydub import AudioSegment
from difflib import SequenceMatcher

# STT API 설정
API_URL = "https://api-inference.huggingface.co/models/CookieMonster99/whisper-small-kr"
HEADERS = {"Authorization": "Bearer "}

def process_audio(file_path, output_format="mp3"):
    """
    오디오 파일을 지정된 포맷으로 변환.
    :param file_path: 입력 파일 경로
    :param output_format: 변환할 파일 포맷 (기본값: "mp3")
    :return: 변환된 파일 경로
    """
    output_file_path = os.path.splitext(file_path)[0] + f".{output_format}"
    audio = AudioSegment.from_file(file_path)
    audio.export(output_file_path, format=output_format)
    return output_file_path

def clip_audio(input_audio_path, clip_folder, clip_duration=28):
    """
    오디오 파일을 일정 길이로 나눠 클립으로 저장.
    :param input_audio_path: 입력 오디오 파일 경로
    :param clip_folder: 클립 파일이 저장될 폴더 경로
    :param clip_duration: 클립 길이 (초)
    :return: 클립 파일 목록
    """
    audio_clip = AudioFileClip(input_audio_path)
    audio_duration = audio_clip.duration

    if not os.path.exists(clip_folder):
        os.makedirs(clip_folder)

    clip_paths = []
    for i, start_time in enumerate(range(0, int(audio_duration), clip_duration)):
        end_time = min(start_time + clip_duration, audio_duration)
        sub_clip = audio_clip.subclip(start_time, end_time)
        output_path = os.path.join(clip_folder, f"clip_{i+1}.mp3")
        sub_clip.write_audiofile(output_path)
        clip_paths.append(output_path)

    return clip_paths

def stt_audio(file_path):
    """
    음성 파일을 텍스트로 변환 (STT).
    :param file_path: 입력 파일 경로
    :return: 변환된 텍스트
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=HEADERS, data=data)
        response.raise_for_status()
        return response.json().get("text", "")
    except requests.exceptions.RequestException as e:
        print(f"Error during STT API call: {e}")
        return ""

def calculate_accuracy(script, stt_text):
    """
    스크립트와 STT 결과를 비교해 정확도를 계산.
    :param script: 사용자 제공 스크립트
    :param stt_text: STT로 변환된 텍스트
    :return: 정확도 (0~100%)
    """
    def clean_text(text):
        return re.sub(r'[.,!?\\s]', '', text)

    cleaned_script = clean_text(script)
    cleaned_stt_text = clean_text(stt_text)
    ratio = SequenceMatcher(None, cleaned_script, cleaned_stt_text).ratio()
    return round(ratio * 100, 2)

def analyze_speed(stt_text, duration):
    """
    발화 속도를 분석.
    :param stt_text: STT로 변환된 텍스트
    :param duration: 오디오 길이 (초)
    :return: 초당 음절 개수, 총 음절 개수
    """
    num_syllables = len(re.findall(r'[가-힣ㄱ-ㅎㅏ-ㅣ]', stt_text))
    syllables_per_second = num_syllables / duration if duration > 0 else 0
    return syllables_per_second, num_syllables
