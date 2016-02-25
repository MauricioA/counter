#include <windows.h>
#include <wtsapi32.h>
#include "hook.h"

//TODO check block screen (WM_WTSSESSION_CHANGE)
//TODO memoria

Hook hook;

LRESULT CALLBACK WndProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam) {
	switch(Message) {
		case WM_QUERYENDSESSION:
			hook.exit();
			return TRUE;
		
		default:
			return DefWindowProc(hwnd, Message, wParam, lParam);
	}
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
	WNDCLASSEX wc;
	HWND hwnd;
	MSG msg;

	memset(&wc, 0, sizeof(wc));
	wc.cbSize = sizeof(WNDCLASSEX);
	wc.lpfnWndProc = WndProc;
	wc.hInstance = hInstance;
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	
	wc.hbrBackground = (HBRUSH) (COLOR_WINDOW + 1);
	wc.lpszClassName = "WindowClass";
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

	if(!RegisterClassEx(&wc)) {
		MessageBox(NULL, "Counter: Window Registration Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
		return 0;
	}
	
	hwnd = CreateWindowEx(WS_EX_CLIENTEDGE, "WindowClass", "", WS_OVERLAPPEDWINDOW,	CW_USEDEFAULT,
		CW_USEDEFAULT, 640, 480, NULL, NULL, hInstance, NULL);

	if (hwnd == NULL) {
		MessageBox(NULL, "Counter: Window Creation Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
		return 0;
	}
	
	hook.hookIt();
	
//	WTSRegisterSessionNotification(hwnd, NOTIFY_FOR_THIS_SESSION);
	
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
	
	return msg.wParam;
}

