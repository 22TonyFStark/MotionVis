# Copyright (C) 2023  ETH Zurich, Manuel Kaufmann, Velko Vechev, Dario Mylonopoulos
import os

import numpy as np
from aitviewer.configuration import CONFIG as C
from aitviewer.headless import HeadlessRenderer
from aitviewer.renderables.smpl import SMPLSequence
from aitviewer.models.smpl import SMPLLayer


# height = 1080
# width = 1920

height = 1440
width = 2560

C.update_conf({'window_width': width, 'window_height': height})
C.update_conf({'smplx_models':'./body_models'})


def render_pair(npy_folder = "smplx_data/intergen", file_name = "fake_noisy_motion.npz", output_folder="result_videos", fps=30):

    smplx_path_p1 = os.path.join(npy_folder, file_name)
    params_p1 = np.load(smplx_path_p1, allow_pickle=True)
    nf_p1 = params_p1['pose_body'].shape[0]

    #betas_p1 = params_p1['betas']
    betas_p1 = np.zeros((10,))
    poses_root_p1 = params_p1['root_orient']
    poses_body_p1 = params_p1['pose_body'].reshape(nf_p1,-1)
    poses_lhand_p1 = params_p1['pose_lhand'].reshape(nf_p1,-1)
    poses_rhand_p1 = params_p1['pose_rhand'].reshape(nf_p1,-1)
    transl_p1 = params_p1['trans']
    #gender_p1 = str(params_p1['gender'])
    gender_p1 = "neutral"

    # smpl_seq.color = smpl_seq.color[:3] + (0.75,)  # Make the sequence a bit transparent.

    smplx_layer_p1 = SMPLLayer(model_type='smplx',gender=gender_p1,num_betas=10,device=C.device)

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


    # Create the headless renderer and add the sequence.
    v = HeadlessRenderer()
    v.scene.add(smplx_seq_p1)

    pos1 = transl_p1[0]


    targets = pos1
    positions = pos1 + np.array([0, 1, 4])

    from aitviewer.scene.camera import PinholeCamera
    camera = PinholeCamera(positions, targets, v.window_size[0], v.window_size[1], viewer=v)
    v.set_temp_camera(camera)
    #print("playback_fps", v.playback_fps)
    v.playback_fps = 30  # 数据实际fps

    # Have the camera automatically follow the SMPL sequence. For every frame, the camera points to the center of the
    # bounding box of the SMPL mesh while keeping a fixed relative distance. The smoothing is optional but ensures that
    # the view is not too jittery.
    # v.lock_to_node(smplx_seq_p1, (2, 2, 2), smooth_sigma=5.0)
    save_name = file_name.split(".")[0]
    v.save_video(
        video_dir=os.path.join(output_folder, f"{save_name}.mp4"),
        output_fps=fps,  # 输出fps
        quality="high"
        )
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default="smplx_data/intergen")
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--output_folder', type=str, default="result_videos")
    parser.add_argument('--file_name', type=str, default="gt.npz")
    args = parser.parse_args()
    render_pair(file_name=args.file_name, npy_folder=args.folder, output_folder=args.output_folder, fps=args.fps)
    # render_pair(file_name="gt.npz")
    # render_pair(file_name="motions_output.npz")