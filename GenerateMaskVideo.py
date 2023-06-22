# Generate masking video from FastTrack output

# Loading Libraries
import cv2
import sys
import glob
import os
import pandas as pd
import numpy as np
import PySimpleGUI as sg
from tqdm import tqdm

# ---------------------------------------------------------------------------------------------
# Main part of video generation
# ---------------------------------------------------------------------------------------------
def VideoGeneration(idir, tandem_windows_size):

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
        print(v)
        print("width:{}, height:{}, count:{}, fps:{}".format(width,height,count,fps))
        # endregion ------

        # region ----- 2. Make background -----
        print("Creating background...")
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

        cv2.imwrite(idir + os.sep + "background.jpg", back_frame)
        # endregion ------

        # region ----- 3. Video Create -----
        print("Video generation")
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        new_v = v.replace(idir, idir+os.sep+"output"+os.sep)
        writer = cv2.VideoWriter(new_v.replace('.mp4', '_extract.mp4'), fourcc, fps, (int(width), int(height)))
        video.set(cv2.CAP_PROP_POS_FRAMES, 0) 

        video = cv2.VideoCapture(v)

        for num in tqdm(range(location.shape[0])):
            ret, frame = video.read()
            x = int(location.xBody[num])
            y = int(location.yBody[num])

            #cv2.circle(frame, (x,y), 2, color=(0,0,255), thickness=-1)
            bg = cv2.imread(idir + os.sep + "background.jpg")
            cv2.rectangle(bg, (x-tandem_windows_size+1,y-tandem_windows_size+1), (x+tandem_windows_size-1, y+tandem_windows_size-1), (0,0,0), -1, cv2.LINE_4)

            cv2.rectangle(frame, (1,1), (x-tandem_windows_size, int(height)), (0,0,0), -1, cv2.LINE_4)
            cv2.rectangle(frame, (x+tandem_windows_size,1), (int(width), int(height)), (0,0,0), -1, cv2.LINE_4)
            cv2.rectangle(frame, (1,1), (int(width), y-tandem_windows_size), (0,0,0), -1, cv2.LINE_4)
            cv2.rectangle(frame, (1,y+tandem_windows_size), (int(width), int(height)), (0,0,0), -1, cv2.LINE_4)

            frame=cv2.add(bg,frame)
            
            ## plot
            #cv2.imshow('frame', frame)
            #cv2.waitKey(1)

            writer.write(frame)
        # endregion ------

        cv2.destroyAllWindows()
        writer.release()
    cv2.destroyAllWindows()
    return("Done")

def gui():
    sg.theme('Dark')
    frame_file = sg.Frame('', [
        [sg.Text("In   "),
         sg.InputText('Input folder', enable_events=True, size=(25, 1)),
         sg.FolderBrowse(button_text='select', size=(6, 1), key="-IN_FOLDER_NAME-")
         ],
        [sg.Text("Tandem window size (def = 20px):", size=(25,1)),
         sg.In(key='-WINDOW_SIZE-', size=(6, 1))
        ]
    ], size=(300, 80))

    frame_buttom = sg.Frame('', [
        [sg.Submit(button_text='Start', size=(10, 10), key='START')]], 
        size=(50, 50))
    
    layout = [[frame_file, frame_buttom]]
    
    window = sg.Window('Tandem masking',
                       layout, resizable=True)
    
    while True:
        event, values = window.read()
    
        if event is None:
            print('exit')
            break
        else:
            if event == 'START':

                # file info
                if len(values["-IN_FOLDER_NAME-"]) == 0:
                    print("no input!")
                    continue
                else:
                    in_dir = values["-IN_FOLDER_NAME-"]+os.sep
                
                # parameters
                if len(values['-WINDOW_SIZE-']) == 0:
                    tandem_windows_size = 20
                else:
                    tandem_windows_size = int(values["-WINDOW_SIZE-"])

                print("input dir: "+str(in_dir))
                message = VideoGeneration(in_dir, tandem_windows_size)
                sg.popup(message)            
    window.close()


gui()