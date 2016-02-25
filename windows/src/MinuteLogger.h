#define _CRT_SECURE_NO_WARNINGS
#ifndef MINUTELOGGER_H

#include <fstream>
#include <ctime>

enum {
	KEY_UP,
	LEFT_BUTTON_DOWN,
	RIGHT_BUTTON_DOWN,
	MIDDLE_BUTTON_DOWN,
	WHEEL_SCROLL,
};

const int INITIAL_KEYS = 7;

class MinuteLogger {
	public:
		MinuteLogger() {
			time_t t = time(NULL);
			lastMinute = *localtime(&t);
			resetCounters();
			for (int i = 0; i < INITIAL_KEYS; i++) {
				log(KEY_UP);
			}
		}
		
		void log(int type) {
			time_t t = time(NULL);
			struct tm currentMinute = *localtime(&t);
			if (
				currentMinute.tm_min  != lastMinute.tm_min  || 
				currentMinute.tm_hour != lastMinute.tm_hour || 
				currentMinute.tm_yday != lastMinute.tm_yday || 
				currentMinute.tm_year != lastMinute.tm_year
			) {	
				clear(currentMinute, "");
			}
			
			switch (type) {
				case KEY_UP:
					keyUps++;
					break;
				case LEFT_BUTTON_DOWN:
					leftButtonDowns++;
					break;
				case RIGHT_BUTTON_DOWN:
					rightButtonDowns++;
					break;
				case MIDDLE_BUTTON_DOWN:
					middleButtonDowns++;
					break;
				case WHEEL_SCROLL:
					wheelScrolls++;
					break;
			}
		}
		
		void exit() {
			time_t t = time(NULL);
			struct tm currentMinute = *localtime(&t);
			clear(currentMinute, "# ---- SALIDA SEGURA ----\n");
		}
		
		void sessionLock() {
			for (int i = 0; i < INITIAL_KEYS; i++) {
				log(KEY_UP);
			}
		}
		
    private:
		tm lastMinute;
		int keyUps;
		int leftButtonDowns;
		int rightButtonDowns;
		int middleButtonDowns;
		int wheelScrolls;
		
		void resetCounters() {
			keyUps = leftButtonDowns = rightButtonDowns = middleButtonDowns = wheelScrolls = 0;
		}
		
		void clear(tm currentMinute, char* message) {
			std::ofstream file;
			char filename[32];
			sprintf(filename, "keys/%d-%d-%d.txt", lastMinute.tm_year + 1900, lastMinute.tm_mon + 1, lastMinute.tm_mday);
			file.open(filename, std::ios::app);
			file << 
				lastMinute.tm_hour << "\t" << 
				lastMinute.tm_min << "\t" << 
				keyUps << "\t" << 
				leftButtonDowns + rightButtonDowns + middleButtonDowns << "\t" << 
				leftButtonDowns << "\t" << 
				rightButtonDowns << "\t" << 
				middleButtonDowns << "\t" << 
				wheelScrolls << "\n" <<
				message;
			file.close();
			
			resetCounters();
			lastMinute = currentMinute;
		}
};

#define MINUTE_LOGGER_H
#endif

