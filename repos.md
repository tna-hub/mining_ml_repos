tensorflow: https://github.com/tensorflow/models/tree/master/research/deep_speech 

pytorch https://github.com/pytorch/examples/tree/master/dcgan

Used quartile methods and the filtered Paper With Code dataset:
  - 4930 repos
  - Selected projects that are python3 compatible
  - Removed projects without requirements.txt and readme.md
  - Q1 = 755Kb
  - Median = 7.5 Mb
  - Q3 = 32 Mb
  - Maximum Q3 + 1.5*IQR = 80 Mb
Repos following the described methodology:

Extra Large projects (size > maxumum)
  1) https://github.com/monaen/LightFieldReconstruction, size: 5.6 Gb
  2) https://github.com/hsalhab/Coloring-in-the-Deep, size: 516 Mb
  3) Potential other project: https://github.com/dragnet-org/dragnet, size: 347 Mb
  
Large projects: size between Q3 and maximum
  1) __https://github.com/Baidi96/text2sql, Fork: https://github.com/tna-hub/text2sql, size: 49.9 Mb__
  2) https://github.com/Svito-zar/NN-for-Missing-Marker-Reconstruction, size: 72 Mb
  3) https://github.com/doronharitan/human_activity_recognition_LRCN, size: 35 Mb
  
Medium projects: size between median and Q3
  1) __https://github.com/astorfi/sequence-to-sequence-from-scratch, Fork: https://github.com/tna-hub/sequence-to-sequence-from-scratch, size: 15.1 Mb__
  2) https://github.com/brightmart/text_classification, Fork: https://github.com/tna-hub/text_classification, size: 14.7Mb
  
Small projects: size between Q1 and median
  1) https://github.com/YoungXiyuan/DCA, Fork: https://github.com/tna-hub/DCA, size: 1.5 Mb
  2) __https://github.com/crowdbotp/socialways, Fork: https://github.com/tna-hub/socialways, size: 5.0 Mb__

Very small projects: size < Q1
  - Will be ignored because too small and not relevant
