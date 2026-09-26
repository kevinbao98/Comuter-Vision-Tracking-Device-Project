#include <opencv2/opencv.hpp>
#include <iostream>

int main () {
    cv::VideoCapture cap(0);

    cv::Mat frame;

    while (true) {
        cap.read(frame); // Read new frame from webcam
        cv.imshow("Live Webcam", frame);
        
        if (cv::waitKey(1) == 27) {
            break;
        }
    }
}