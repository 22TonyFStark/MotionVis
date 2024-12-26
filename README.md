# MotionVis

Please refer to "https://github.com/eth-ait/aitviewer" for setting up the environment.  
  
To prepare the npz file (refer to smplx_viewer_tool/prepare_from_smplify.py), ensure the following format:  
  
trans: (n_frames, 3)  
root_orient: (n_frames, 3)  
pose_body: (n_frames, 63)  
pose_lhand: (n_frames, 45)  
pose_rhand: (n_frames, 45)  
betas: (1, 10)  
gender: str - "male", "female", or "neutral"  
  
For single-person rendering:  
```cd aitviewer/smplx_viewer_tool  ```  
```python render_single.py  ```  
  
For two-person rendering:  
```python render_two.py  ```  
When rendering two people, the camera will automatically focus on the center between them.  

The result could appear as assets/test_1.mp4.