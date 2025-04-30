joint_list = ((7,6,5), (11,10,9), (15,14,13), (19,18,17), (3,2,1),(6,5,0),(10,9,0),(14,13,0),(18,17,0),(2,1,0))
headers = ("date","Index","Middle","Ring", "Pinky", "Thumb")

#called header_angle
headerAngle = ("date","Index Max","Index Min","Middle Max","Middle Min","Ring Max","Ring Min", "Pinky Max", "Pinky Min", "Thumb Max","Thumb Min")

#LEFT
counter_name,counter_name2,counter_name3,counter_name4,counter_name5 = 0,0,0,0,0
stage,stage2,stage3,stage4,stage5 = "None","None","None","None","None"

minangle,minangle_2,minangle_3,minangle_4,minangle_5 = [],[],[],[],[]
anglelist,anglelist_2,anglelist_3,anglelist_4,anglelist_5 = [180],[180],[180],[180],[180]
maxangle,maxangle_2,maxangle_3,maxangle_4,maxangle_5,Anglelist,Anglelist_2,Anglelist_3,Anglelist_4,Anglelist_5 = [0],[0],[0],[0],[0],[0],[0],[0],[0],[0]
L1,L2,L3,L4,L5 = [],[],[],[],[]

#RIGHT
Rcounter_name,Rcounter_name2,Rcounter_name3,Rcounter_name4,Rcounter_name5 = 0,0,0,0,0
Rstage,Rstage2,Rstage3,Rstage4,Rstage5 = "None","None","None","None","None"

Rminangle,Rminangle_2,Rminangle_3,Rminangle_4,Rminangle_5 = [],[],[],[],[]
Ranglelist,Ranglelist_2,Ranglelist_3,Ranglelist_4,Ranglelist_5 = [180],[180],[180],[180],[180]
Rmaxangle,Rmaxangle_2,Rmaxangle_3,Rmaxangle_4,Rmaxangle_5,RAnglelist,RAnglelist_2,RAnglelist_3,RAnglelist_4,RAnglelist_5 = [0],[0],[0],[0],[0],[0],[0],[0],[0],[0]
R1,R2,R3,R4,R5 = [],[],[],[],[]