# 🎙️ 발표 평가 플랫폼: **Attention Please**

## 🛠️ 프로젝트 개요

### 📌 프로젝트 배경
현대 사회에서 발표는 학생과 직장인 모두에게 필수적인 기술입니다. 하지만 많은 사람들이 발표에 대한 두려움과 경험 부족으로 어려움을 겪고 있습니다. 이를 해결하기 위해, **"Attention Please"**는 사용자가 발표를 연습하고 개선할 수 있도록 **발표 평가 및 피드백 플랫폼**을 개발했습니다.

### 🎯 프로젝트 목표
- 발표의 **언어적 요소(발음, 발화 속도 등)**와 **비언어적 요소(자세, 제스처 등)**를 분석하여 사용자에게 **구체적인 피드백**을 제공합니다.
- 발표 연습을 통해 **자신감을 키우고 실력을 향상**시킬 수 있는 도구를 제공합니다.

---

## 🔍 프로젝트 주요 기능

### 1. **발표 연습 영상 평가**
- **언어적 분석**: 
  - 발음 정확도, 발화 속도, 목소리 크기, 말더듬 횟수 등 분석
- **비언어적 분석**: 
  - 자세, 제스처, 시각적 요소 평가
- 결과를 기반으로 **맞춤형 피드백 제공**

### 2. **발표 능력 추적**
- **히스토리 기능**:
  - 사용자별 평가 결과를 저장하고, 개선 추이를 시각적으로 확인 가능
- **맞춤형 팁 제공**:
  - 발표 스킬 향상을 위한 실질적이고 구체적인 팁 제공

---

## 💡 AI 구현 과정

### 🎤 음성처리
1. **모델 선정**:
   - Open AI의 Whisper 모델을 기반으로 STT(Speech-to-Text) 구현.
2. **데이터셋 선정**:
   - **아나운서 발화 데이터**(Hugging Face: Bingsu, Zeroth-Korean)를 활용하여 학습.
3. **모델 학습**:
   - WER(Word Error Rate)를 기준으로 하이퍼파라미터 튜닝 후, Whisper 모델을 **Fine-Tuning**.
4. **평가 알고리즘**:
   - 발음 정확도: STT로 변환된 텍스트와 제공된 스크립트를 비교하여 정확도 계산.
   - 발화 속도: 텍스트를 분석하여 초당 음절 수 계산.
   - 말더듬 횟수 및 목소리 크기 분석.

### 🎥 영상처리
1. **데이터셋 선정**:
   - AI Hub의 '사람 동작 영상' + 직접 촬영한 추가 데이터셋 활용.
2. **전처리**:
   - Action 라벨링 및 Skeleton 구조 추출.
3. **모델 학습**:
   - Skeleton 정보를 활용한 Human Activity Recognition 학습.
   - LSTM 모델(85% 정확도)을 ST-GCN 모델(96% 정확도)로 개선.
4. **모델 개선**:
   - 사람만 인식하도록 **Object Detection**으로 Bounding Box 생성 후 Skeleton 추출.

---

## 🎯 기대 효과
1. **발표 두려움 극복**:
   - 학생 및 사회초년생들이 발표에 대한 자신감을 얻을 수 있습니다.
2. **시장 경쟁력**:
   - 발표 연습을 지원하는 국내 서비스 부재로 초기 시장 진입이 용이.
3. **발표 능력 개선**:
   - 체계적인 분석과 피드백을 통해 발표 실력을 점진적으로 향상.

---

## 👤 타겟 유저
- **학생**: 발표 기술을 향상시키고자 하는 중·고등학생 및 대학생.
- **직장인**: 회의 및 프레젠테이션 준비가 필요한 사회초년생.

---

## 🚀 기술 스택
- **Backend**: Django, Django REST Framework
- **Frontend**: React (구현 예정)
- **AI**:
  - 음성처리: Open AI Whisper 모델, Hugging Face
  - 영상처리: ST-GCN, YOLOv3, Skeleton-based Action Recognition
- **데이터베이스**: PostgreSQL
- **기타**: Celery, Redis (비동기 처리)
