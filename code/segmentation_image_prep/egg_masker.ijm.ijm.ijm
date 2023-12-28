t = getTitle();
roiManager("Deselect");
numROIs = roiManager("count");

if (numROIs > 0) {
	roiManager("Combine");
	
	run("Create Mask");
	saveAs("Tiff", "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/embryomap/" + t);
	close();
	roiManager("Deselect");
	roiManager("delete");
	close();
	
} else {
	newImage("no_embryo", "16-bit Black", getWidth(), getHeight(), 1);
	selectImage("no_embryo");
	saveAs("Tiff", "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/embryomap/" + t);
	close();
	selectImage(t);
	close();
}
