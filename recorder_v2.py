import cv2,time
import os,glob
import numpy as np
import threading

class recorder():
    def __init__(self,i=0,out_filename="out.avi",snapinterval=-1,w=0,h=0):
        self.cv2=cv2
        self.source=i
        self.source_type="camera"
        self.width  = w
        self.height = h
        self.rescaling=True
        self.out_filename=out_filename
        self.snapinterval=snapinterval
        self.recording="preview"
        self.snap_cnt=0
        self.frame_cnt=0
        self.current_dir=""
        self.set_source_type()
        self.non_block()

    def check_lidar_file(self):
        for file in glob.iglob(os.path.join(self.current_dir, '*.jpg')):  
            title, ext = os.path.splitext(os.path.basename(file))
        pass

    def process(self,frame):

        return frame

    def set_source_type(self):
        if type(self.source) == "int":
            self.source_type="camera"+ str(self.source) +"_"
        else:
            self.source_type="file_"+ str(self.source)


    def end(self):
        if self.recording=="recording":
            self.recording="end"
        

    def pause(self):
        if self.recording=="paused":
            self.recording="recording"
        elif self.recording=="recording":
            self.recording="paused"
        

    def recored(self):
        if self.recording=="saved" or self.recording=="preview" :
            self.recording="start"
            print(self.recording)
        

    def snap(self):
        self.img_name="images/"+self.source_type+"_"+str(self.frame_cnt)+'.jpg'
        #self.snap_cnt+=1
        self.cv2.imwrite(self.img_name, self.frame, [int(self.cv2.IMWRITE_JPEG_QUALITY), 90])
        self.cv2.putText(self.frame, 'snap:'+self.img_name, self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        self.cv2.waitKey(1)
        self.cv2.imshow('snap'+str(self.source),self.frame)

    def non_block(self):
        self.thead1 = threading.Thread(target=self.open_stream)
        #self.thead1.daemon = True
        self.thead1.start()
        pass

    def rescale(self):
        if self.rescaling:
            self.frame = self.cv2.resize(self.frame, (self.width, self.height))

    def open_stream(self):
        self.cap    = self.cv2.VideoCapture(self.source)
        self.fps    = int(self.cap.get(self.cv2.CAP_PROP_FPS))
        if self.width == 0 or self.height == 0:
            self.width  = int(self.cap.get(self.cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(self.cv2.CAP_PROP_FRAME_HEIGHT))
            self.rescaling=False
        self.pos= ( int( self.width/10) ,int( self.height/10) )


        # Check if camera opened successfully
        if (self.cap.isOpened() == False): 
            print("Unable to read camera feed")

        while(True):
            ret, self.frame = self.cap.read()

            self.frame=self.process(self.frame)

            #self.cv2.waitKey(1)
            if ret == True: 
                self.rescale()
                self.frame_cnt+=1
                self.snap_cnt+=1
                if self.snapinterval > 0:
                    if self.snap_cnt==self.snapinterval:
                        self.snap()
                        self.snap_cnt=0
                elif self.snapinterval == 0:
                    self.snap()

                self.pre_frame=self.frame.copy()

                self.cv2.putText(self.pre_frame, 'S /Snap - R/Record - E/End record - P/Pause', (0, self.height - 20), self.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, 10)

                if self.recording=="recording":
                    self.out.write(self.frame)  
                    self.cv2.putText(self.pre_frame, 'recording', self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                elif self.recording=="preview":
                    self.cv2.putText(self.pre_frame, 'preview', self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                elif self.recording=="start":
                    start_time=str( int( time.time() ) )
                    self.out_filename="camera_"+str(self.source)+"_"+start_time+".avi"
                    self.out = self.cv2.VideoWriter(self.out_filename,self.cv2.VideoWriter_fourcc('M','J','P','G'), self.fps, (self.width,self.height))
                    self.recording="recording"

                elif self.recording=="paused":
                    self.cv2.putText(self.pre_frame, 'paused', self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                elif self.recording=="end":
                    self.recording="saved"
                    self.cv2.putText(self.pre_frame, 'Saved: '+ self.out_filename, self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    self.cv2.imshow('frame'+str(self.source),self.pre_frame)
                    time.sleep(3)
                    self.out.release()

                self.cv2.imshow('frame'+str(self.source),self.pre_frame)
                
            else:
                self.cv2.putText(self.pre_frame, 'File End', self.pos, self.cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                self.cv2.imshow('frame'+str(self.source),self.pre_frame)
                
                time.sleep(3)
                break

                pass
               
            # Press Q on keyboard to stop recording
            key=self.cv2.waitKey(1)

            if key == ord('q'):
                # Closes all the frames
                self.cap.release()
                self.cv2.destroyAllWindows()
                #self.out.release()
                break

            elif key == ord('s'):
                self.snap()

            elif key == ord('r'):
                self.recored()
            elif key == ord('e'):
                self.end()

            elif key == ord('p'):
                self.pause()


if __name__=="__main__":
    #rec=recorder(i="pass.mp4",snapinterval=15)
    rec1=recorder(i=0)
