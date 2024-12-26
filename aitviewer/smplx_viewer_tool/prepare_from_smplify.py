
"""
trans (61, 3)
root_orient (61, 3)
pose_body (61, 63)
pose_lhand (61, 45)
pose_rhand (61, 45)
betas (1, 10)
gender ()
"""

import numpy as np
data = dict(np.load("D:/vmocap_pipeline/results/hmropt/joint2smpl.npz", allow_pickle=True).items())
smpl = data["smpl"].item()
print(smpl.keys())
betas = smpl["betas"]#[0:1]
print(betas.shape)

std_betas = np.mean(betas, axis=0)
print(std_betas, smpl["betas"].sum())

transl = smpl["transl"].reshape(-1, 3)
orient = smpl["global_orient"]
body_pose = smpl["body_pose"]
print(body_pose.shape, orient.shape)
save = {}
save["betas"] = betas
save["trans"] = transl
save["pose_body"] = body_pose[:, :63]
save["root_orient"] = orient.reshape(-1, 3)
save["gender"] = "neutral"  # TODO: check this
save["pose_lhand"] = np.zeros((len(orient), 45))
save["pose_rhand"] = np.zeros((len(orient), 45))
np.savez("smplx_data/hmropt/test1.npz", **save)