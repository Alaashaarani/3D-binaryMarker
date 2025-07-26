'''In this code we propose a class to detect the underwater markers in a given Image or video '''
import cv2 as cv 
import numpy as np
import time
# the name Aqualoc is the origin of the 3dimension-binary marker 
class aquaLocDetector():
   def __init__(self):

      # Default Dictionary and ids 
      self.ids = [13,14,15,28,30,34,35,41,42]
      self.marker_dict = cv.aruco.DICT_4X4_50 
      self.method = 0 # 0=CLAHA # 1=iterative Threshold 
      self.avg_time = []
      #defining the ArUco Detector using OPENCV library 
      self.dictionary = cv.aruco.getPredefinedDictionary(self.marker_dict)
      self.parameters = cv.aruco.DetectorParameters()
      self.detector = cv.aruco.ArucoDetector(self.dictionary, self.parameters) 

      # Clahe Defining 
      self.clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(32,32)) 
      # image gain
      self.k = 1 
      # blur kernel  
      self.kernel  = np.array([[1/16,1/8,1/16],
                                [1/8,1/4,1/8],
                                [1/16,1/8,1/16]]) 
      # Display images (post-processed)
      self.display_imgs_flag = False 
      #detected number of markers 
      self.num_detection = 0 

      # display wait key ( image = 0 , video  = 1)
      self.wait_value = 0 
   
   def detect_aqualoc(self,frame):
      #raw image
      self.raw_img = frame
      #normalized Image
      self.norm_img= cv.normalize(frame,None,0,255, cv.NORM_MINMAX)
      # Reading the frame 
      self.gray_img = cv.cvtColor(self.norm_img,cv.COLOR_RGB2GRAY)
      starting_time = time.time()
      if self.method==0:self.CLAHE_method()
      elif self.method==1:self.iterative_threshold_method()
      elif self.method==2:self.normalization_method()
      
      execution_time = time.time() - starting_time
      self.avg_time.append(execution_time)

   
   def CLAHE_method(self): 
      # applying clahe 
      cl1 = self.clahe.apply(self.gray_img)
      #  Normalization and Flippling 
      np_img = np.asarray(cl1, dtype = np.float32)
      img_min = np_img.min()
      img_max = np_img.max()
      ## flipping is done by the negative while normalization is done by new_value = ((old_value - a) * (d - c) / (b - a) + c )
      rescaled_img = -(np.multiply(np_img-img_max, ((-127-127)/(img_min-img_max))) + 127)
      applied_kernel = self.k*self.kernel
      modified_Img = cv.filter2D(src=rescaled_img, ddepth=-1, kernel=applied_kernel)
      modified_Img = modified_Img+127.5
      ## clipping the Image to [1 , 254] 
      value1,value2 = [254,1]
      modified_Img[modified_Img > value1] = 254
      modified_Img[modified_Img < value2] = 1
      ## reformating the image to uint8  
      self.modified_Img = np.asarray(modified_Img, dtype = np.uint8)
      
      self.detection()
      self.detected_markers()

   def iterative_threshold_method(self):
      kernel = np.array([[1,1,1],[1,1,1],[1,1,1]])/9
      best_threshold = 125
      highest_detection= 0 
      for x in range(90,190,5): 
         _, threshold = cv.threshold(self.gray_img, x, 255, cv.THRESH_BINARY_INV)
         self.modified_Img = cv.filter2D(src=threshold, ddepth=-1, kernel=kernel) # This can be removed
         self.detection(display=False)
         if len(self.markerCorners) != 0:
            if len(self.markerIds) > highest_detection: 
               highest_detection=len(self.markerIds)
               best_threshold = x 

      _, threshold = cv.threshold(self.gray_img, best_threshold, 255, cv.THRESH_BINARY_INV)
      self.modified_Img = cv.filter2D(src=threshold, ddepth=-1, kernel=kernel)
      self.detection()
      self.detected_markers()
      
   def normalization_method(self):
      np_img = np.asarray(self.gray_img, dtype = np.float32)
      img_min = np_img.min()
      img_max = np_img.max()
      ## flipping is done by the negative while normalization is done by new_value = ((old_value - a) * (d - c) / (b - a) + c )
      rescaled_img = -(np.multiply(np_img-img_max, ((-127-127)/(img_min-img_max))) + 127)
      modified_Img = rescaled_img+127.5
      ## clipping the Image to [1 , 254] 
      value1,value2 = [254,1]
      modified_Img[modified_Img > value1] = 254
      modified_Img[modified_Img < value2] = 1
      self.modified_Img=modified_Img.astype("uint8")
      self.detection()
      self.detected_markers()


   def detection(self,display=True):

      self.markerCorners, self.markerIds, self.rejectedCandidates = self.detector.detectMarkers(self.modified_Img)
      self.modified_out=cv.cvtColor(self.modified_Img.copy(),cv.COLOR_GRAY2RGB)
      self.raw_img_out=self.raw_img.copy()
      # logic can be improved  
      if len(self.markerCorners) != 0 : 
         self.num_detection=self.id_detection() # <- this line can be improved 
         if self.num_detection>0:
            self.origin = cv.aruco.drawDetectedMarkers(self.raw_img_out, self.markerCorners, self.markerIds)
            self.modified = cv.aruco.drawDetectedMarkers(self.modified_out, self.markerCorners, self.markerIds)
      else: 
         self.origin = self.raw_img_out
         self.modified = self.modified_out
      if display:
         self.display_imgs() 

   def display_imgs(self):
      if self.display_imgs_flag : 
         
         cv.imshow("Raw_image_withCountour",self.origin) 
         cv.imshow("Preprocessed_image_withCountour",self.modified) 
          

         if self.wait_value == 0 : 
            print("press SPACE to change Frame Or Change the Display Setting to VIDEO")
         cv.waitKey(self.wait_value) 

      # else: 
      #    print("Images display is set to false, with ",self.num_detection," detections",end='\r')


   # can be improved 
   def id_detection(self,):
      #checking if the id provided by the detector is in the predefined dictionary of the markers 
      markers_detected = 0
      for id in self.markerIds:
         for available_id in self.ids: 
            if id == available_id: 
               markers_detected+=1  

      return markers_detected     
      
   def assign_dict(self,dict):
      self.marker_dict = dict 
      self.dictionary = cv.aruco.getPredefinedDictionary(dict)
      self.detector = cv.aruco.ArucoDetector(self.dictionary, self.parameters)
      self.ids = []
      print("new dictionary ",dict," is applied.\nReseting the list of IDs. ")

   def print_execution_time(self):
      return np.average(self.avg_time)

   def used_dict(self):
      print("The used dictionary is", self.marker_dict)

   def id_list(self): 
      print("Marker detector can detect these IDs", self.ids )

   def add_id(self,id):
      self.ids.append(id)

   def write_img_gain(self,gain):
      self.k = gain 
   # disply time of the image, zero means wait for keyboard key (ms)
   def display_images(self): 
      self.wait_value = 0
   # display time in ms, 1 means 1ms and then switch to the next frame
   def display_video(self): 
      self.wait_value = 1
   # Use this function to allow custom the display waiting time
   def edit_display_wait_value(self,value): 
      self.wait_value = value 

   def enable_display(self): 
      self.display_imgs_flag = True
      print("display Enabled")

   def disable_display(self):
      self.display_imgs_flag = False 
      print("display disabled")

   def read_img_gain(self): 
      print("image Gain applied while detection", self.k)

   def detected_markers(self):
      return self.markerCorners, self.markerIds, self.rejectedCandidates
   
   def set_method(self,method):
      self.avg_time = []
      self.method= method

   '''More function can be added to edit all the parameters inside the detector'''