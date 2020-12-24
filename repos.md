tensorflow: https://github.com/tensorflow/models/tree/master/research/deep_speech 
pytorch https://github.com/pytorch/examples/tree/master/dcgan

Used quartile methods and the filtered Paper With Code dataset:
  - 4930 repos
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
  1) https://github.com/rikichou/face_recognition_insight_face, size: 66 Mb
  2) https://github.com/Svito-zar/NN-for-Missing-Marker-Reconstruction, size: 72 Mb
  3) https://github.com/doronharitan/human_activity_recognition_LRCN, size: 35 Mb
  
Medium projects: size between median and Q3
  1) https://github.com/bearpaw/pytorch-pose, size: 7 Mb
  2) https://github.com/JunweiLiang/Object_Detection_Tracking, size: 8.4 Mb
  3) https://github.com/brightmart/text_classification, size: 14.7Mb
  
Small projects: size between Q1 and median
  1) https://github.com/YoungXiyuan/DCA, size: 1.5 Mb
  2) https://github.com/crowdbotp/socialways, size: 5.0 Mb

Very small projects: size < Q1
  - Will be ignored because too small and not relevant
