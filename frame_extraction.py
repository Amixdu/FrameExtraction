import cv2
import os

def createFolder(name):
    d = os.path.dirname(__file__) # directory of script
    p = (r'{}/'+str(name)).format(d) # path to be created

    try:
        os.makedirs(p)
    except OSError:
        pass


# Open video and split into frames (frames will be saved in /frames)
def split_to_frames(video_path, video_name, start1, stop1, start2, stop2):

    current = os.getcwd() 
    save_path = "frames"
    framesFolder = os.path.join(current, save_path)

    cap= cv2.VideoCapture(video_path)
    i=1
    while(cap.isOpened()):

        # Extraction point
        ret, frame = cap.read()
        if ret == False:
            break
        
        # Frame selection conditions
        if i >= start1 and i <= stop1:
            name = video_name+'_Frame'+str(i)+'.jpg'
            save_path = os.path.join(framesFolder, name)
            cv2.imwrite(save_path,frame)

        if i > stop1 and start2 <= -1:
            break

        if i >= start2 and i <= stop2:
            name = 'Frame'+str(i)+'.jpg'
            save_path = os.path.join(framesFolder, name)
            cv2.imwrite(save_path,frame)

        if i > stop2 and stop2 > 0:
            break

        i+=1
 
    cap.release()
    cv2.destroyAllWindows()


# Create a new video from extracted frames
def create_video(video_name):

    current = os.getcwd() 
    save_path = "frames"
    frames_folder = os.path.join(current, save_path)
    
    images = [img for img in os.listdir(frames_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(frames_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(video_name, fourcc, 30, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(frames_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def clear_frames():
    current = os.getcwd() 
    save_path = "frames"
    frames_folder = os.path.join(current, save_path)

    for f in os.listdir(frames_folder):
        os.remove(os.path.join(frames_folder, f))



# EDIT THE PATH BELOW TO THE ANNOTATION FOLDER
with open('Temporal_Anomaly_Annotation_for_Testing_Videos.txt') as f:
    lines = f.readlines()


# Read the annotation file and store in arrays
def read_data():
    video_names = []
    crime_positions = {}
    for line in lines:
        line = line.strip()
        words = line.split()
        video_names.append(words[0])
        crime_positions[words[0]] = ([words[2], words[3], words[4], words[5]])

    return video_names, crime_positions



def get_cropped_vids():

    createFolder("frames")

    # CHANGE BELOW PATH TO WHERE THE ORIGNIAL VIDEOS ARE STORED
    video_src_path = 'D:\Study\SEM_6\FIT3162\FrameExtraction\src'

    # CHANGE BELOW PATH TO WHERE THE VIDEOS NEED TO BE STORED
    video_destination_path = 'D:\Study\SEM_6\FIT3162\FrameExtraction\\output_vids'

    video_names, crime_positions = read_data()

    for video in os.listdir(video_src_path):

        if video in video_names:

            crime_data = crime_positions[video]

            start1 = int(crime_data[0])
            stop1 = int(crime_data[1]) + 5

            start2 = int(crime_data[2]) - 5
            stop2 = int(crime_data[3])

            input_vid_path = os.path.join(video_src_path, video)
                
            split_to_frames(input_vid_path, video, start1, stop1, start2, stop2)

            vid_save_path = os.path.join(video_destination_path, video)
            create_video(vid_save_path)

            clear_frames()

            print(video + " complete")


get_cropped_vids()