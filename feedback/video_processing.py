import os
import cv2
import numpy as np
import torch
from video_tools.CameraLoader import CamLoader_Q
from video_tools.Detection.Utils import ResizePadding
from video_tools.ObjectDetect_Loader import TinyYOLOv3_onecls
from video_tools.PoseEstimate_Loader import SPPE_FastPose
from video_tools.Visualization import draw_single
from video_tools.Track.Tracker import Detection, Tracker
from video_tools.ActionsEstLoader import TSSTG

class VideoProcessor:
    def __init__(self, source, save_out=None, device='cuda', detection_input_size=384, pose_input_size='224x160'):
        """
        VideoProcessor 초기화
        :param source: 입력 비디오 파일 경로
        :param save_out: 출력 비디오 파일 경로 (None일 경우 저장하지 않음)
        :param device: 실행 장치 ('cuda' 또는 'cpu')
        :param detection_input_size: Object Detection 입력 사이즈
        :param pose_input_size: Pose Estimation 입력 사이즈
        """
        self.source = source
        self.save_out = save_out
        self.device = device
        self.detection_input_size = detection_input_size
        self.pose_input_size = pose_input_size

        # 모델 초기화
        self.detect_model = TinyYOLOv3_onecls(detection_input_size, device=device)
        self.pose_model = SPPE_FastPose('resnet50', 224, 160, device=device)
        self.action_model = TSSTG()

        # 비디오 작성기 초기화
        self.writer = None
        if save_out:
            self.writer = self._init_writer(save_out)

        # 트래커 초기화
        self.tracker = Tracker(max_age=30, n_init=3)

    def _init_writer(self, save_out):
        """
        비디오 저장을 위한 VideoWriter 초기화
        :param save_out: 출력 비디오 경로
        :return: cv2.VideoWriter 객체
        """
        code = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(save_out, code, 30, (self.detection_input_size * 2, self.detection_input_size * 2))

    def process_video(self):
        """
        비디오 처리 및 행동 분석 수행
        :return: 분석 결과 (제스처 통계)
        """
        cam = CamLoader_Q(self.source, queue_size=100000, preprocess=self.preprocess).start()
        bad_gesture_count = 0
        good_gesture_count = 0
        standing_on_one_leg_count = 0

        while cam.grabbed():
            frame = cam.getitem()
            image = frame.copy()

            # Object Detection
            detected = self.detect_model.detect(frame, need_resize=False, expand_bb=10)

            # Kalman Filter를 통한 예측
            self.tracker.predict()
            for track in self.tracker.tracks:
                det = torch.tensor([track.to_tlbr().tolist() + [0.5, 1.0, 0.0]], dtype=torch.float32)
                detected = torch.cat([detected, det], dim=0) if detected is not None else det

            # Pose Estimation
            detections = []
            if detected is not None:
                poses = self.pose_model.predict(frame, detected[:, 0:4], detected[:, 4])
                detections = [Detection(self.bounding_box(ps['keypoints'].numpy()),
                                        np.concatenate((ps['keypoints'].numpy(), ps['kp_score'].numpy()), axis=1),
                                        ps['kp_score'].mean().numpy()) for ps in poses]
            self.tracker.update(detections)

            # 행동 분석
            for track in self.tracker.tracks:
                if not track.is_confirmed():
                    continue

                if len(track.keypoints_list) == 30:
                    keyPoint_list = np.array(track.keypoints_list, dtype=np.float32)
                    out = self.action_model.predict(keyPoint_list, frame.shape[:2])
                    action_name = self.action_model.class_names[out[0].argmax()]

                    if action_name == 'Bad_Gesture':
                        bad_gesture_count += 1
                    elif action_name == 'Good_Gesture':
                        good_gesture_count += 1
                    elif action_name == 'standing on one leg':
                        standing_on_one_leg_count += 1

            # 비디오 저장
            if self.save_out:
                self.writer.write(frame)

        cam.stop()
        if self.save_out:
            self.writer.release()

        return {
            "bad_gesture_count": bad_gesture_count,
            "good_gesture_count": good_gesture_count,
            "standing_on_one_leg_count": standing_on_one_leg_count
        }

    def preprocess(self, image):
        """
        입력 이미지를 전처리
        :param image: 입력 이미지
        :return: 전처리된 이미지
        """
        padding = ResizePadding(self.detection_input_size, self.detection_input_size)
        image = padding(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def bounding_box(self, kpt, ex=20):
        """
        Keypoint 영역을 포함하는 Bounding Box 생성
        :param kpt: Keypoint 좌표
        :param ex: 확장 영역
        :return: Bounding Box 좌표
        """
        return np.array((kpt[:, 0].min() - ex, kpt[:, 1].min() - ex,
                         kpt[:, 0].max() + ex, kpt[:, 1].max() + ex))