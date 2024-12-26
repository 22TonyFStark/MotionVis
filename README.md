# MotionVis

Please refer to "https://github.com/eth-ait/aitviewer" for setting up the environment.  
  
To prepare the npz file (refer to smplx_viewer_tool/prepare_from_smplify.py), ensure the following format:  
  
trans: (61, 3)  
root_orient: (61, 3)  
pose_body: (61, 63)  
pose_lhand: (61, 45)  
pose_rhand: (61, 45)  
betas: (1, 10)  
gender: (optional) - "male", "female", or "neutral"  
  
For single-person rendering:  
```python render_single.py  ```

For two-person rendering:  
```python render_two.py  ```  
When rendering two people, the camera will automatically focus on the center between them.  

The result could appear as:
<video width="320" height="240" controls>
  <source src="https://github.com/22TonyFStark/MotionVis/raw/main/assets/test_1.mp4" type="video/mp4">
  您的浏览器不支持HTML5视频。
</video>