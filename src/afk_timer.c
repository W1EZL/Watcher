#include <X11/extensions/scrnsaver.h>
#include <stdio.h>

int main(){
    Display *dis = XOpenDisplay(0);

    if (!dis){
        return 1;
    }

    XScreenSaverInfo *info = XScreenSaverAllocInfo();
    XScreenSaverQueryInfo(dis, DefaultRootWindow(dis), info);

    if (info){
        printf("%lu", info->idle);
        XFree(info);
        return 0;
    }
    return -1;
}
