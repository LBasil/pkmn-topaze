// harnais mGBA : lit des commandes sur stdin. rom <f> | run <n> <keys> | poke8 <addr> <v> | peek <addr> <n> | shot <f.ppm> | pokeeach <addr> <v>... 
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <mgba-util/vfs.h>
#include <mgba/gba/core.h>
#include <mgba/core/serialize.h>
#include <fcntl.h>
#include <mgba/core/log.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void nolog(struct mLogger* l, int cat, enum mLogLevel lv, const char* f, va_list a) {}
int main(int argc, char** argv) {
    static struct mLogger lg = { .log = nolog }; mLogSetDefaultLogger(&lg);
    struct mCore* core = mCoreFind(argv[1]);
    core->init(core); mCoreInitConfig(core, NULL);
    unsigned w, h; core->desiredVideoDimensions(core, &w, &h);
    uint32_t* buf = malloc(w * h * 4); core->setVideoBuffer(core, buf, w);
    mCoreLoadFile(core, argv[1]); core->reset(core);
    uint32_t pa[16], pv[16]; int np = 0; char line[512];
    while (fgets(line, sizeof line, stdin)) {
        char cmd[32]; unsigned a, b; char f[256];
        if (sscanf(line, "%31s", cmd) != 1) continue;
        if (!strcmp(cmd, "run")) { unsigned n, k; sscanf(line, "run %u %x", &n, &k); core->setKeys(core, k);
            for (unsigned i = 0; i < n; i++) { for (int j = 0; j < np; j++) core->busWrite8(core, pa[j], pv[j]); core->runFrame(core); } puts("ok"); }
        else if (!strcmp(cmd, "poke8")) { sscanf(line, "poke8 %x %x", &a, &b); core->busWrite8(core, a, b); puts("ok"); }
        else if (!strcmp(cmd, "pin")) { sscanf(line, "pin %x %x", &a, &b); if (np < 16) { pa[np] = a; pv[np] = b; np++; } puts("ok"); }
        else if (!strcmp(cmd, "unpin")) { np = 0; puts("ok"); }
        else if (!strcmp(cmd, "peek")) { sscanf(line, "peek %x %u", &a, &b); for (unsigned i = 0; i < b; i++) printf("%02x", core->busRead8(core, a + i)); puts(""); }
        else if (!strcmp(cmd, "shot")) { sscanf(line, "shot %255s", f); FILE* o = fopen(f, "wb"); fprintf(o, "P6\n%u %u\n255\n", w, h);
            for (unsigned i = 0; i < w * h; i++) { uint32_t p = buf[i]; fputc(p & 0xff, o); fputc((p >> 8) & 0xff, o); fputc((p >> 16) & 0xff, o); } fclose(o); puts("ok"); }
        else if (!strcmp(cmd, "ss")) { sscanf(line, "ss %255s", f); struct VFile* vf = VFileOpen(f, O_CREAT | O_TRUNC | O_RDWR);
            int ok = vf ? mCoreSaveStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC) : 0; if (vf) vf->close(vf); puts(ok ? "ok" : "fail"); }
        else if (!strcmp(cmd, "ls")) { sscanf(line, "ls %255s", f); struct VFile* vf = VFileOpen(f, O_RDONLY);
            int ok = vf ? mCoreLoadStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC) : 0; if (vf) vf->close(vf); puts(ok ? "ok" : "fail"); }
        else if (!strcmp(cmd, "quit")) break;
        fflush(stdout);
    }
    return 0;
}
