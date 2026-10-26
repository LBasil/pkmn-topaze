#ifndef GUARD_TOPAZE_JOURNAL_H
#define GUARD_TOPAZE_JOURNAL_H

#define JOURNAL_MAX_ENTRIES 24

u8 TopazeJournalGetSections(u8 *out);
const u8 *TopazeJournalSectionName(u8 section);
void TopazeJournalCount(u8 section, u8 *done, u8 *total);
u8 TopazeJournalGetEntries(u8 section, u16 *out);
const u8 *TopazeJournalEntryName(u16 entry);
const u8 *TopazeJournalEntryHint(u16 entry);
bool8 TopazeJournalEntryDone(u16 entry);
void TopazeJournalOpenScreen(void);

#endif // GUARD_TOPAZE_JOURNAL_H
