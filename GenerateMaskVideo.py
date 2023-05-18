# Generate masking video from FastTrack output

# Loading Libraries
import cv2
import sys
import numpy as np
import glob
import csv
import pprint
import os
import pandas as pd

# ---------------------------------------------------------------------------------------------
# Main part of video generation
# ---------------------------------------------------------------------------------------------


def VideoGeneration(idir, odir, tandem_windows_size = 20):

    # Loading data
    video_path = glob.glob(idir + os.sep + "*.mp4")
    coord_path = glob.glob(idir + os.sep + "*.txt")
    for i in range(len(video_path)):
        
        # region ----- 0. Convert tracking data -----
        X = pd.read_csv(coord_path[i], sep="\t", header=0)
        new_X = X[["xBody", "yBody", "imageNumber", "id"]]
        mask = new_X["id"] <1
        df = new_X[mask]

        new_df = df.set_index('imageNumber').reindex(range(max(df.imageNumber))).reset_index()
        new_df['xBody'] = new_df['xBody'].interpolate()
        new_df['yBody'] = new_df['yBody'].interpolate()
        location = new_df

        # region ----- 1. Get file information -----
        v = video_path[i]
        video = cv2.VideoCapture(v)
        ## video information
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        print("width:{}, height:{}, count:{}, fps:{}".format(width,height,count,fps))

        # region ----- 2. Make background -----
        has_next, i_frame = video.read()

        # background
        back_frame = i_frame.astype(np.float32)

        # converting
        num = 1
        while has_next == True:
            if num % 100 == 0:
                # convert image to float
                f_frame = i_frame.astype(np.float32)

                # diff calcuration
                diff_frame = cv2.absdiff(f_frame, back_frame)

                # update background
                cv2.accumulateWeighted(f_frame, back_frame, 0.025)

            num = num + 1
            # next frame
            has_next, i_frame = video.read()

        cv2.imwrite(idir + "/background.jpg", back_frame)

        #########################
        #### 3. Video Create ####
        #########################
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        writer = cv2.VideoWriter(v.replace('.mp4', '_extract.mp4'), fourcc, fps, (int(width), int(height)))
        num = 0
        video.set(cv2.CAP_PROP_POS_FRAMES, 0) 

        video = cv2.VideoCapture(v)

        while(video.isOpened()):
            ret, frame = video.read()
            if num < location.shape[0]:
                x = int(location.xBody[num])
                y = int(location.yBody[num])

                #cv2.circle(frame, (x,y), 2, color=(0,0,255), thickness=-1)
                bg = cv2.imread(idir + "/background.jpg")
                cv2.rectangle(bg, (x-tandem_windows_size+1,y-tandem_windows_size+1), (x+tandem_windows_size-1, y+tandem_windows_size-1), (0,0,0), -1, cv2.LINE_4)

                cv2.rectangle(frame, (1,1), (x-tandem_windows_size, int(height)), (0,0,0), -1, cv2.LINE_4)
                cv2.rectangle(frame, (x+tandem_windows_size,1), (int(width), int(height)), (0,0,0), -1, cv2.LINE_4)
                cv2.rectangle(frame, (1,1), (int(width), y-tandem_windows_size), (0,0,0), -1, cv2.LINE_4)
                cv2.rectangle(frame, (1,y+tandem_windows_size), (int(width), int(height)), (0,0,0), -1, cv2.LINE_4)

                frame=cv2.add(bg,frame)
                
                ## plot
                cv2.imshow('frame', frame)
                cv2.waitKey(1)

                writer.write(frame)
                #cv2.imwrite(HOME + "Plots/Visualize/p8-13/" + "picture{:0=5}".format(num)+".jpg", frame)
                #print("save picture{:0=5}".format(num)+".jpg")

            else:
                break

            num += 1

        cv2.destroyAllWindows()
        writer.release()
    cv2.destroyAllWindows()

VideoGeneration(idir = "F:/Dropbox/research/papers_and_projects/2023/STARPROTOCOL/GenerateMaskVideo/sample", odir="")