import nipype.interfaces.dcmstack as dcmstack
from dcmstack.extract import minimal_extractor
from dicom import read_file
from os import listdir, path, makedirs, getcwd

def dcm_to_nii(dicom_dir, d5_key="EchoTime", node=True):
	if not node:
		nii_dir = dicom_dir.replace("dicom", "nii")
		if not path.exists(nii_dir):
			makedirs(nii_dir)
	else:
		nii_dir = getcwd()
	stacker = dcmstack.DcmStack()

	if d5_key:
		dicom_files = listdir(dicom_dir)
		echo_times=[]
		for dicom_file in dicom_files:
			meta = minimal_extractor(read_file(dicom_dir+dicom_file, stop_before_pixels=True, force=True))
			echo_times += [float(meta[d5_key])]

		for echo_time in list(set(echo_times)):
			echo_indices = [i for i, j in enumerate(echo_times) if j == echo_time]
			stacker.inputs.embed_meta = True
			stacker.inputs.dicom_files = [dicom_dir+dicom_files[index] for index in echo_indices]
			stacker.inputs.out_path = nii_dir+"/"
			stacker.inputs.out_format = "EPI"+str(echo_time)[:2]
			result = stacker.run()

	else:
		stacker.inputs.dicom_files = dicom_dir
		stacker.inputs.out_path = nii_dir+"/"
		result = stacker.run()

	return [nii_dir+nii_file for nii_file in listdir(nii_dir)]

if __name__ == "__main__":
	for nr in [4460]:
		convert_dcm_to_nifti("/home/chymera/data/dc.rs/export_ME/dicom/"+str(nr)+"/1/EPI/")