import numpy as np
import mdtraj as md
import glob
import msmbuilder as msmb
import msmbuilder.featurizer

ref_top = ''
ref_dir = ''
test_top = ''
test_dir = ''

ref_trajs = glob.glob(ref_dir + '*.mdcrd')
test_trajs = glob.glob(test_dir + '*.mdcrd')

t0 = md.load(ref_trajs[0], top = ref_top)
n_res = t0.topology.select('name CA').shape[0]

residues = []
for res in range(n_res):
	name = t0.topology.residue(res)
	residues.append(str(name)[:3])

chi1_mapping = []
for n, res in enumerate(residues):
	if (res != 'ALA') and (res != 'GLY'):
		chi1_mapping.append(n)

# The first residue (starting from the N-terminus) will have psi and chi1 (provided 
# it is not ALA or GLY) angles, but no phi angle, while the last residue will 
# similarly lack a psi angle. Therefore, I remove the first psi angle and the 
# last phi angle from the featurized array and ignore the first and last chi1
# angles.

ref = []
for traj in ref_trajs:
	ref.append(md.load(traj, top = ref_top))

test = []
for traj in test_trajs:
	test.append(md.load(traj, top = test_top))

phi_feat = msmb.featurizer.DihedralFeaturizer(['phi'],sincos=False)
psi_feat = msmb.featurizer.DihedralFeaturizer(['psi'],sincos=False)
chi1_feat = msmb.featurizer.DihedralFeaturizer(['chi1'],sincos=False)

phi_ref = phi_feat.fit_transform(ref)
psi_ref = psi_feat.fit_transform(ref)
chi1_ref = chi1_feat.fit_transform(ref)

phi_ref_array = np.vstack(phi_ref)[:,:-1]
psi_ref_array = np.vstack(psi_ref)[:,1:]
chi1_ref_array = np.vstack(chi1_ref)

phi_test = phi_feat.fit_transform(test)
psi_test = psi_feat.fit_transform(test)
chi1_test = chi1_feat.fit_transform(test)

phi_test_array = np.vstack(phi_test)[:,:-1]
psi_test_array = np.vstack(psi_test)[:,1:]
chi1_test_array = np.vstack(chi1_test)

ref_phi_hist = []
ref_psi_hist = []
ref_chi1_hist = []

test_phi_hist = []
test_psi_hist = []
test_chi1_hist = []

chi1_num = 0
for res in range(n_res - 1):
	actual_res = res + 1
	ref_phi_hist.append(np.histogram(phi_ref_array[:,res], bins = 30, range = (-np.pi, np.pi))[0])
	ref_psi_hist.append(np.histogram(psi_ref_array[:,res], bins = 30, range = (-np.pi, np.pi))[0]) 
	if (actual_res in chi1_mapping) and (actual_res != n_res - 1):
		ref_chi1_hist.append(np.histogram(chi1_ref_array[:,chi1_num], bins = 30, range = (-np.pi, np.pi))[0])
	test_phi_hist.append(np.histogram(phi_test_array[:,res], bins = 30, range = (-np.pi, np.pi))[0])
        test_psi_hist.append(np.histogram(psi_test_array[:,res], bins = 30, range = (-np.pi, np.pi))[0])
        if (actual_res in chi1_mapping) and (actual_res != n_res - 1):
                test_chi1_hist.append(np.histogram(chi1_test_array[:,chi1_num], bins = 30, range = (-np.pi, np.pi))[0])	
		chi1_num += 1
