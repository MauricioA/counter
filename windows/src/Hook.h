#ifndef LOGGER_H

#include <windows.h>
#include "MinuteLogger.h"

class Hook {
	public:
		Hook();
		
		void hookIt();
		
		LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam);
		
		LRESULT CALLBACK MouseProc(int nCode, WPARAM wParam, LPARAM lParam);
		
		static LRESULT CALLBACK LowLevelKeyboardProcWrapper(int nCode, WPARAM wParam, LPARAM lParam);

		static LRESULT CALLBACK MouseWrapper(int nCode, WPARAM wParam, LPARAM lParam);
		
		void exit();

		void sessionLock();
       
	private:
		MinuteLogger logger;
		static Hook *objPointer;        
};

#define LOGGER_H
#endif

