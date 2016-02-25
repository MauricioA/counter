#include "Hook.h"

Hook *Hook::objPointer = NULL;

Hook::Hook() {
	objPointer = this;
}

void Hook::hookIt() {
    HINSTANCE appInstance = GetModuleHandle(NULL);
    SetWindowsHookEx(WH_KEYBOARD_LL, Hook::LowLevelKeyboardProcWrapper, appInstance, 0);
	SetWindowsHookEx(WH_MOUSE_LL, Hook::MouseWrapper, appInstance, 0);
}

LRESULT CALLBACK Hook::LowLevelKeyboardProcWrapper(int nCode, WPARAM wParam, LPARAM lParam) {
	return objPointer->LowLevelKeyboardProc(nCode, wParam, lParam);
}

LRESULT CALLBACK Hook::MouseWrapper(int nCode, WPARAM wParam, LPARAM lParam) {
	return objPointer->MouseProc(nCode, wParam, lParam);
}

LRESULT CALLBACK Hook::LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (wParam == WM_KEYUP) {
		logger.log(KEY_UP);
    }
    
    return 0;
}

LRESULT CALLBACK Hook::MouseProc(int nCode, WPARAM wParam, LPARAM lParam) {
	switch (wParam) {
		case WM_LBUTTONDOWN:
			logger.log(LEFT_BUTTON_DOWN);	
			break;
		case WM_RBUTTONDOWN:
			logger.log(RIGHT_BUTTON_DOWN);
			break;
		case WM_MBUTTONDOWN:
			logger.log(MIDDLE_BUTTON_DOWN);
			break;
		case WM_MOUSEWHEEL:
			logger.log(WHEEL_SCROLL);
			break;
	}
    
    return 0;
}

void Hook::exit() {
	logger.exit();
}

void Hook::sessionLock() {
	logger.sessionLock();
}

