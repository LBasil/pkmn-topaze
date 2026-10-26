#ifndef GUARD_TOPAZE_JOURNAL_H
#define GUARD_TOPAZE_JOURNAL_H

#define JOURNAL_MAX_ENTRIES 32
#define JOURNAL_MAX_SECTIONS 12

u8 TopazeJournalGetSections(u8 *out);
const u8 *TopazeJournalSectionName(u8 section);
void TopazeJournalCount(u8 section, u8 *done, u8 *total);
u8 TopazeJournalGetEntries(u8 section, u16 *out);
const u8 *TopazeJournalEntryName(u16 entry);
const u8 *TopazeJournalEntryHint(u16 entry);
bool8 TopazeJournalEntryDone(u16 entry);
bool8 TopazeJournalEntryVisible(u16 entry);
bool8 TopazeJournalEntryProgress(u16 entry, u32 *cur, u32 *target);
void TopazeJournalOpenScreen(void);

#endif // GUARD_TOPAZE_JOURNAL_H
