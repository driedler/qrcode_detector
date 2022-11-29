#include <iostream>
#include <ctime>
#include <opencv2/opencv.hpp>
#include "ImageBinarization.hpp"
#include "CodeFinder.hpp"

using namespace std;
using namespace cv;

void cameraMode();


void printLogo() {
	cout << "+---------------------------------------------------------------------------+\n"
		"|     _______  _______    _______  _______  ______   _______                |\n"
		"|    (  ___  )(  ____ )  (  ____ \\(  ___  )(  __  \\ (  ____ \\               |\n"
		"|    | (   ) || (    )|  | (    \\/| (   ) || (  \\  )| (    \\/               |\n"
		"|    | |   | || (____)|  | |      | |   | || |   ) || (__                   |\n"
		"|    | |   | ||     __)  | |      | |   | || |   | ||  __)                  |\n"
		"|    | | /\\| || (\\ (     | |      | |   | || |   ) || (                     |\n"
		"|    | (_\\ \\ || ) \\ \\__  | (____/\\| (___) || (__/  )| (____/\\               |\n"
		"|    (____\\/_)|/   \\__/  (_______/(_______)(______/ (_______/               |\n"
		"+---------------------------------------------------------------------------+" << endl;
}




int main(int argc, const char *argv[]) {
	srand(time(0));	//Seed Randomizer
	cout << "Path to executable: " << argv[0] << endl;
	printLogo();

	cout << "Starting Camera Mode..." << endl;
	cameraMode();


#ifdef _WIN32
	//system("pause");
#else
	waitKey(0);
#endif

	return 0;
}


/**
 * \brief Try to open the camera and constantly search for qrcodes.
 */
void cameraMode() {
	VideoCapture cap(0); // open the default camera
	if (!cap.isOpened())  // check if we succeeded
	{
		cout << "Could not open camera." << endl;
		return;
	}


	namedWindow("Video", 1);
	while (1) {
		Mat frame;
		cap >> frame;         // get a new frame from camera
		imshow("Video", frame);

		CodeFinder codeFinder(frame, false);

		Mat qrcode;
		auto data = codeFinder.findAndDecode(qrcode);
		if(data.length() > 0) {
			std::cout << "Decoded data: " << data << std::endl;
			imshow("qrcode", qrcode);
		}
		
		// Press 'c' to escape
		if (waitKey(30) == 'c') break;
	}
}
