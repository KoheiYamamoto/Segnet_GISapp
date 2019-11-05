Kindly handle dependencies among libraries and incompatability issues caused by versions conflicts.
This took a while to be dealed with.

0. Make sure that you have CamVid test/testannot set the corresponding dir before training and run $ preprocess_testdata.py

1. $ train.py
    - with specifyig parameters 

2. Delete test dir from Camvid. Empty out and rename the corresponding test dir, whose dataset was segmented into several batches (test1,2,3 dont name "test"!, fix the run.sh accordingly) as the ps is killed by the overloads (Though testannot dir is going to be piled up with duplicated images with different filenames). 

3. $ ./run.sh
	4. $ preprocess_testdata.py
		- 1. get all the filenames of images in test (after renamed) dir
		- 2. overwrite test.txt
		- 3. duplicate random testannot file, the no. of file is corresponding the length of the above filenames
	5. $ predict.py
		- output segmented results into out dir

6. $ segmented_img_analyser.py
	- pixel_parsed_report.csv is the output (unlabelled will be zero entirely and road_marking class can be regarded as unlabelled)
