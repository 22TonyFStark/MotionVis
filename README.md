# MotionVis

To prepare the npz file (refer to smplx_viewer_tool/prepare_from_smplify.py), ensure the following format:

trans: (61, 3)
root_orient: (61, 3)
pose_body: (61, 63)
pose_lhand: (61, 45)
pose_rhand: (61, 45)
betas: (1, 10)
gender: (optional) - "male", "female", or "neutral"
For single-person rendering:

python render_single.py
For two-person rendering:

python render_two.py
When rendering two people, the camera will automatically focus on the center between them.