
import face_recognition
import cv2
import csv
from datetime import datetime
import numpy as np
import win32com.client


# firstly with the help of cv2 we can capture our webcam video.
video_capturing=cv2.VideoCapture(0)#here 0 implies my first web camp if you want to use second one give 1 and so on.

# now we have to load all the know faces which i had already stored in a directory know_faces.
pawan_img=face_recognition.load_image_file("./know_faces/pawan.jpeg")
'''Now we have to create the image encoding(convert the image into numbers such that it is easier to compare)'''
pawan_encoding=face_recognition.api.face_encodings(pawan_img)[0]

# now create a list of all the faces encoding .here we have 1 but can be many.
know_face_encoding=[pawan_encoding]
# also create a list of all the names in same order.
face_names=["Pawan"]

'''Now here i am building an face_recognition attendence system for that i must have a list of the students.'''
students=know_face_encoding.copy()

# face_location=[]
# student_face_encoding=[]

# now we also want to know the exact time and date when the student has marked the attendence.
# this will return you with current data and time.
now_time=datetime.now()
# print(now_time)
date=now_time.strftime("%y-%m-%d")

# now we have to create an csv writer.
'''for that we have to open a file first.lets create a file.'''
f=open(f"{date}attendence.csv",'w+',newline="")
csv_writer=csv.writer(f)


while True:
    _,frame=video_capturing.read()
    '''
    In the code you provided, the underscore (_) is used:

Discarded Return Value:

In the line _, frame = video_capturing.read(), the underscore appears at the beginning.
The read() function from video_capturing likely returns two values: a status code and the actual frame data.
By using the underscore (_), you're essentially saying you're not interested in the status code and only
want the frame data (assigned to the variable frame).
    '''
    # print(frame)
    # small_frame=cv2.resize(frame,(0,0),fx=0.23,fy=0.23)
    # rgb_small_frame=cv2.cvtColor(small_frame,cv2.COLOR_BGR2GRAY)

     #recognize faces
    face_location=face_recognition.face_locations(frame)
#     print("data face location",face_location)
    face_encoding=face_recognition.api.face_encodings(frame)
#     print("data face encoding",face_encoding)

    for encoding in face_encoding:
        matches=face_recognition.compare_faces(know_face_encoding,encoding)
        # print()
        face_distance=face_recognition.face_distance(know_face_encoding,encoding)
        # print("face-distance",face_distance)
        best_match_index=np.argmin(face_distance)
#         print("index",best_match_index)
        student_name=""
        if matches[best_match_index]:
            name = face_names[0]  # Assuming a single known face (modify if you have more)
            student_name=name
            # Put the name on the frame (adjust position as needed)
            cv2.putText(frame, name+"(Present)", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            # Write name and timestamp to CSV (assuming successful match)
            csv_writer.writerow([name, datetime.now().strftime("%H:%M:%S")])

    cv2.imshow("attendence",frame)
    speak=win32com.client.Dispatch("SAPI.SpVoice")
    speak.Speak(f"your attendence have benn marked{student_name}")

    if cv2.waitKey(1) & 0xFF==ord('q'):

        break

video_capturing.release()
cv2.destroyAllWindows()
f.close()







'''
1. Infinite Loop (while True:):

This line starts an infinite loop that will continue running until manually stopped.
This is a common pattern in video processing applications where you continuously read frames from the video stream.
2. Reading Video Frames (_, frame = video_capturing.read()):

This line uses the video_capturing object (presumably created earlier to capture video from a webcam or video file) to read the
 next frame from the video stream.
The read() function returns a status code and the actual frame data. The code discards the status code using the underscore (_)
 and assigns the frame data to the variable frame.
3. Commented Code (Resizing and Color Conversion):

These lines are currently commented out (using #). They would resize the frame (frame) and convert it to grayscale 
(cv2.COLOR_BGR2GRAY).
Resizing could improve performance, while grayscale conversion might be useful for some face recognition algorithms.
You can uncomment these lines if needed.
4. Face Recognition (face_location = face_recognition.face_locations(frame)):

This line calls the face_locations function from the face_recognition library.
It passes the frame (the current video frame) as input.
This function attempts to detect faces within the frame and returns a list of bounding boxes (coordinates) for each 
detected face. The list face_location will store this information.
5. Printing Face Locations (print("data face location", face_location)):

This line simply prints the contents of the face_location variable for debugging or informational purposes. 
It shows the detected face locations (bounding boxes).
6. Face Encoding (face_encoding = face_recognition.api.face_encodings(frame)):

This line utilizes face_recognition.api.face_encodings(frame).
It also uses the frame as input.
This function aims to extract facial encodings for each detected face in the frame.
A facial encoding is a numerical representation that captures the essential features of a face, allowing for comparison 
with other faces. The list face_encoding will hold these encodings.
7. Printing Face Encodings (print("data face encoding", face_encoding)):

Similar to the previous print statement, this line again serves debugging purposes by showing the extracted facial 
encodings for detected faces.
8. Looping Through Encodings (for student_face_encoding in face_encoding):

This loop iterates through each facial encoding present in the face_encoding list (one for each detected face).
The variable student_face_encoding holds the encoding of a single face within the current iteration.
9. Face Matching (matches = face_recognition.compare_faces(know_face_encoding, student_face_encoding)):

This line performs face recognition using face_recognition.compare_faces.
It compares a known face encoding (know_face_encoding) (presumably loaded from a file or created earlier) with the current 
student's face encoding (student_face_encoding).
The compare_faces function returns a list (matches) where each element represents whether there's a match (True) or not 
(False) between the known face and the current student's face encoding.
10. Printing Matches (print(matches)):

This line prints the matches list, again for debugging or verification purposes. It shows if a match was found for each 
detected face in the current frame.
11. Face Distance (face_distance = face_recognition.face_distance(know_face_encoding, student_face_encoding)):

This line calculates the face distance between the known face and the current student's face using face_recognition.
face_distance.
Face distance is a metric that measures how similar two facial encodings are. Lower distances indicate a closer resemblance.
The result is stored in the face_distance variable.
12. Finding Best Match (best_match_index = np.argmin(face_distance)):

This line assumes you have multiple known faces. It uses the numpy library (np) to find the index of the minimum value 
in the face_distance list.
This index (best_match_index) corresponds to the known face encoding that has the closest distance (most similar) 
to the current


Displaying the Video Stream (cv2.imshow("attendence", frame)):

This line uses OpenCV's cv2.imshow function to display the current frame (frame) on a window titled "attendence."
This allows you to see the video stream with the recognized faces and attendance markings (if any) in real-time.
Waiting for User Input (cv2.waitKey(1) & 0xFF == ord('q')):

This line utilizes cv2.waitKey(1).
cv2.waitKey() function pauses the program execution for a specified time (in milliseconds) and checks if any key was pressed.
Here, it waits for 1 millisecond (essentially non-blocking) to see if there's any keyboard input.
The & 0xFF part performs a bitwise AND operation with 255 (represented by 0xFF in hexadecimal). This removes any higher-order bits that might be present in the keycode, ensuring compatibility across different systems.
The comparison == ord('q') checks if the pressed key's code (returned by cv2.waitKey(1)) matches the code for the letter 'q' (obtained using ord('q')).
Exiting the Program (break):

If the user presses the 'q' key, the condition cv2.waitKey(1) & 0xFF == ord('q') becomes True.
This triggers the break statement, which exits the while loop, effectively stopping the program.
Releasing Resources (video_capturing.release() and cv2.destroyAllWindows()):

Once the loop exits, the program cleans up by releasing resources using:
video_capturing.release(): This properly releases the video capture object, closing the connection to the webcam.
cv2.destroyAllWindows(): This closes all OpenCV windows that were created using cv2.imshow.
Closing the CSV File (f.close()):

Finally, the line f.close() closes the CSV file object (f) that was opened earlier for writing attendance records. This ensures proper file handling and prevents data corruption.
In essence, this section displays the video stream with recognition results, waits for the user to press 'q' to quit, and then cleans up resources before exiting the program.
'''