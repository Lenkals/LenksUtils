#include <windows.h>
#include <windowsx.h>
#include <stdio.h>

#define ID_TIMER 1

HFONT hFontTime = NULL;
HFONT hFontClose = NULL;
COLORREF bgColor = RGB(30, 30, 30); // Dark grey background
COLORREF fgColor = RGB(0, 255, 0); // Green text
COLORREF closeColor = RGB(255, 100, 100); // Red close button

RECT g_closeRect = {0}; // Track exact position of the X button

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE:
            SetTimer(hwnd, ID_TIMER, 100, NULL);
            // Default fonts, will be resized immediately in WM_SIZE anyway
            hFontTime = CreateFontA(30, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, ANSI_CHARSET, 
                                    OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, 
                                    DEFAULT_PITCH | FF_SWISS, "Segoe UI");
            hFontClose = CreateFontA(16, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, ANSI_CHARSET, 
                                     OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, 
                                     DEFAULT_PITCH | FF_SWISS, "Arial");
            return 0;

        case WM_TIMER:
            InvalidateRect(hwnd, NULL, TRUE);
            return 0;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            
            RECT rect;
            GetClientRect(hwnd, &rect);

            // Fill background
            HBRUSH hBrush = CreateSolidBrush(bgColor);
            FillRect(hdc, &rect, hBrush);
            DeleteObject(hBrush);

            // Get time string
            SYSTEMTIME st;
            GetLocalTime(&st);
            char timeStr[64];
            sprintf(timeStr, "%02d:%02d:%02d", st.wHour, st.wMinute, st.wSecond);

            // Measure dimensions
            SIZE sizeTime, sizeClose;
            SelectObject(hdc, hFontTime);
            GetTextExtentPoint32A(hdc, timeStr, strlen(timeStr), &sizeTime);
            
            SelectObject(hdc, hFontClose);
            GetTextExtentPoint32A(hdc, "X", 1, &sizeClose);

            // Center the combined block (Time + Margin + X)
            int margin = 10;
            int totalWidth = sizeTime.cx + margin + sizeClose.cx;

            int startX = (rect.right - totalWidth) / 2;
            if (startX < 0) startX = 0;

            int timeY = (rect.bottom - sizeTime.cy) / 2;
            RECT timeRect = { startX, timeY, startX + sizeTime.cx, timeY + sizeTime.cy };

            // Place X next to the text, aligned to top of text
            int closeX = startX + sizeTime.cx + margin;
            int closeY = timeY;

            g_closeRect.left = closeX;
            g_closeRect.top = closeY;
            g_closeRect.right = closeX + sizeClose.cx;
            g_closeRect.bottom = closeY + sizeClose.cy;

            // Draw Time
            SetTextColor(hdc, fgColor);
            SetBkMode(hdc, TRANSPARENT);
            SelectObject(hdc, hFontTime);
            DrawTextA(hdc, timeStr, -1, &timeRect, DT_LEFT | DT_TOP | DT_SINGLELINE);

            // Draw X
            SetTextColor(hdc, closeColor);
            SelectObject(hdc, hFontClose);
            DrawTextA(hdc, "X", -1, &g_closeRect, DT_LEFT | DT_TOP | DT_SINGLELINE);

            EndPaint(hwnd, &ps);
            return 0;
        }

        case WM_NCHITTEST: {
            LRESULT hit = DefWindowProc(hwnd, uMsg, wParam, lParam);
            if (hit != HTCLIENT) {
                return hit; // Allow edge resizing
            }

            POINT pt;
            pt.x = GET_X_LPARAM(lParam);
            pt.y = GET_Y_LPARAM(lParam);
            ScreenToClient(hwnd, &pt);

            // Expand hit area slightly around the X
            RECT hitRect = g_closeRect;
            InflateRect(&hitRect, 10, 10);

            if (PtInRect(&hitRect, pt)) {
                return HTCLIENT; // Close button hover/click
            }

            return HTCAPTION; // Allow dragging anywhere else
        }

        case WM_LBUTTONDOWN: {
            POINT pt;
            pt.x = GET_X_LPARAM(lParam);
            pt.y = GET_Y_LPARAM(lParam);

            RECT hitRect = g_closeRect;
            InflateRect(&hitRect, 10, 10);

            if (PtInRect(&hitRect, pt)) {
                DestroyWindow(hwnd);
            }
            return 0;
        }

        case WM_SIZE: {
            if (hFontTime) DeleteObject(hFontTime);
            if (hFontClose) DeleteObject(hFontClose);
            int height = HIWORD(lParam);
            
            // Re-scale both fonts dynamically based on window height
            int fontSize = (int)(height * 0.75);
            hFontTime = CreateFontA(fontSize, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, ANSI_CHARSET, 
                                    OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, 
                                    DEFAULT_PITCH | FF_SWISS, "Segoe UI");
                                    
            int closeFontSize = (int)(height * 0.4);
            if (closeFontSize < 12) closeFontSize = 12;
            hFontClose = CreateFontA(closeFontSize, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, ANSI_CHARSET, 
                                     OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, 
                                     DEFAULT_PITCH | FF_SWISS, "Arial");
            return 0;
        }

        case WM_DESTROY:
            if (hFontTime) DeleteObject(hFontTime);
            if (hFontClose) DeleteObject(hFontClose);
            KillTimer(hwnd, ID_TIMER);
            PostQuitMessage(0);
            return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR pCmdLine, int nCmdShow) {
    const char CLASS_NAME[]  = "DesktopClockClass";
    
    WNDCLASS wc = {0};
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
        CLASS_NAME,
        "Desktop Clock",
        WS_POPUP | WS_VISIBLE | WS_THICKFRAME,
        100, 100, 180, 45,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    SetLayeredWindowAttributes(hwnd, 0, 200, LWA_ALPHA);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
