# Copyright (C) 2023  ETH Zurich, Manuel Kaufmann, Velko Vechev, Dario Mylonopoulos
import os

import numpy as np
from aitviewer.configuration import CONFIG as C
from aitviewer.headless import HeadlessRenderer
from aitviewer.renderables.smpl import SMPLSequence
from aitviewer.models.smpl import SMPLLayer

def find_point_D(A, B, L, up=False):
    # 计算中点C
    C = (A + B) / 2
    
    # 计算AB的方向向量并单位化
    AB_vector = B - A
    AB_normalized = AB_vector / np.linalg.norm(AB_vector)
    
    # 计算垂直于AB的单位向量（通过旋转90度得到）
    # 这里使用了一个简单的技巧：交换x,y,z坐标并改变其中一个坐标的符号来得到垂直向量

    if up:
        perpendicular_vector = np.array([-AB_normalized[1], AB_normalized[0], 0])
        if np.linalg.norm(perpendicular_vector) == 0:  # To handle the case when AB is along the z-axis
            perpendicular_vector = np.array([0, -AB_normalized[2], AB_normalized[1]])
    else:
        # y是竖直方向
        perpendicular_vector = np.array([-AB_normalized[1], 0, AB_normalized[0]])
    
    
    # 单位化垂直向量
    perpendicular_vector = perpendicular_vector / np.linalg.norm(perpendicular_vector)
    
    # 在垂线上找到距离C点L的点D
    D = C + L * perpendicular_vector
    
    return D


# height = 1080
# width = 1920

height = 1440
width = 2560

C.update_conf({'window_width': width, 'window_height': height})
C.update_conf({'smplx_models':'./body_models'})


def render_pair(npy_folder, output_folder, fps):

    smplx_path_p1 = os.path.join(npy_folder, 'P1.npz')
    smplx_path_p2 = os.path.join(npy_folder, 'P2.npz')
    params_p1 = np.load(smplx_path_p1, allow_pickle=True)
    params_p2 = np.load(smplx_path_p2, allow_pickle=True)
    nf_p1 = params_p1['pose_body'].shape[0]
    nf_p2 = params_p2['pose_body'].shape[0]

    betas_p1 = params_p1['betas']
    poses_root_p1 = params_p1['root_orient']
    poses_body_p1 = params_p1['pose_body'].reshape(nf_p1,-1)
    poses_lhand_p1 = params_p1['pose_lhand'].reshape(nf_p1,-1)
    poses_rhand_p1 = params_p1['pose_rhand'].reshape(nf_p1,-1)
    transl_p1 = params_p1['trans']
    gender_p1 = str(params_p1['gender'])

    betas_p2 = params_p2['betas']
    poses_root_p2 = params_p2['root_orient']
    poses_body_p2 = params_p2['pose_body'].reshape(nf_p2,-1)
    poses_lhand_p2 = params_p2['pose_lhand'].reshape(nf_p2,-1)
    poses_rhand_p2 = params_p2['pose_rhand'].reshape(nf_p2,-1)
    transl_p2 = params_p2['trans']
    gender_p2 = str(params_p2['gender'])
    # smpl_seq.color = smpl_seq.color[:3] + (0.75,)  # Make the sequence a bit transparent.

    smplx_layer_p1 = SMPLLayer(model_type='smplx',gender=gender_p1,num_betas=10,device=C.device)
    smplx_layer_p2 = SMPLLayer(model_type='smplx',gender=gender_p2,num_betas=10,device=C.device)

    # create smplx sequence for two persons
    smplx_seq_p1 = SMPLSequence(poses_body=poses_body_p1,
                        smpl_layer=smplx_layer_p1,
                        poses_root=poses_root_p1,
                        betas=betas_p1,
                        trans=transl_p1,
                        poses_left_hand=poses_lhand_p1,
                        poses_right_hand=poses_rhand_p1,
                        device=C.device,
                        color=(0.11, 0.53, 0.8, 1.0)
                        )
    smplx_seq_p2 = SMPLSequence(poses_body=poses_body_p2,
                        smpl_layer=smplx_layer_p2,
                        poses_root=poses_root_p2,
                        betas=betas_p2,
                        trans=transl_p2,
                        poses_left_hand=poses_lhand_p2,
                        poses_right_hand=poses_rhand_p2,
                        device=C.device,
                        color=(1.0, 0.27, 0, 1.0)
                        )


    # Create the headless renderer and add the sequence.
    v = HeadlessRenderer()
    v.scene.add(smplx_seq_p1)
    v.scene.add(smplx_seq_p2)

    pos1 = transl_p1[0]
    pos2 = transl_p2[0]


    targets = (pos1 + pos2) / 2
    positions = find_point_D(pos1, pos2, 4)

    from aitviewer.scene.camera import PinholeCamera
    camera = PinholeCamera(positions, targets, v.window_size[0], v.window_size[1], viewer=v)
    v.set_temp_camera(camera)
    #print("playback_fps", v.playback_fps)
    v.playback_fps = 120  # 数据实际fps

    # Have the camera automatically follow the SMPL sequence. For every frame, the camera points to the center of the
    # bounding box of the SMPL mesh while keeping a fixed relative distance. The smoothing is optional but ensures that
    # the view is not too jittery.
    # v.lock_to_node(smplx_seq_p1, (2, 2, 2), smooth_sigma=5.0)
    v.save_video(
        video_dir=os.path.join(output_folder, "test.mp4"),
        output_fps=fps,  # 输出fps
        quality="high"
        )
    


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default="smplx_data/p2_samples")
    parser.add_argument('--fps', type=int, default=60)
    parser.add_argument('--output_folder', type=str, default="result_videos")
    parser.add_argument('--file_name', type=str, default="gt.npz")
    args = parser.parse_args()
    render_pair(npy_folder=args.folder, output_folder=args.output_folder, fps=args.fps)
    # render_pair(file_name="gt.npz")
    # render_pair(file_name="motions_output.npz")