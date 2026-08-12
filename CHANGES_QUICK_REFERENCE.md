# Quick Reference: Cloud Removal Changes

## What Changed

### Frontend (React/TypeScript)

**Files Modified:**
- `App.tsx` - Removed email, feedback, auth state; added local PDF download
- `Sidebar.tsx` - Removed Pro features, email footer, upgrade modals
- `PastRunsView.tsx` - Removed email verification requirement
- `serverSource.ts` - Removed `locked` field from runs payload

**Files No Longer Used (can be deleted):**
- `EmailReportView.tsx`
- `EmailVerifyInline.tsx`
- `FeedbackView.tsx`
- `ProCta.tsx` (still exists but unused)
- `UpgradeModal.tsx` (still exists but unused)

### Backend (Python)

**File Modified:**
- `strix/interface/viewer/server.py`

**Removed Features:**
- Email verification (OTP codes)
- Report sending via email
- Feedback submission to cloud
- Analytics/telemetry event tracking
- Authentication state management

**Kept Features:**
- Local PDF download with encryption
- Scan management (start/stop/list)
- Agent steering
- Run history (no verification required)
- All viewing capabilities

## User-Visible Changes

### Before (Cloud-Dependent)
- ❌ Required email verification to view past runs
- ❌ Could send reports via email through cloud relay
- ❌ Had feedback form that sent to cloud
- ❌ Showed "Run in the cloud" CTAs
- ❌ Had Pro feature upsells in sidebar
- ❌ Tracked analytics events

### After (Local-Only)
- ✅ View all past runs without verification
- ✅ Download encrypted PDF reports locally
- ✅ No feedback form (removed)
- ✅ No cloud CTAs or upsells
- ✅ Clean sidebar with only local features
- ✅ No analytics tracking - fully private

## Testing Checklist

### Frontend
- [ ] Can view pentest overview
- [ ] Can view issues list
- [ ] Can view agent graph
- [ ] Can view past runs (no verification)
- [ ] Can download encrypted PDF report
- [ ] Can switch between runs
- [ ] Can manage scans (start/stop/list)
- [ ] Sidebar shows only: Overview, Issues, Agents, Past runs, Scan Manager
- [ ] No "Run in the cloud" button visible
- [ ] No Pro feature items in sidebar

### Backend
- [ ] `/api/runs` returns all runs without verification
- [ ] `/api/report/download` generates encrypted PDF locally
- [ ] Removed endpoints return 404
- [ ] No errors in server logs

## API Endpoints Changed

### Removed Endpoints
```
POST /api/event                  → 404 (telemetry)
POST /api/auth/otp/start         → 404 (email verification)
POST /api/auth/otp/verify        → 404 (email verification)
POST /api/auth/forget            → 404 (auth management)
POST /api/report/send            → 404 (email via cloud)
POST /api/feedback               → 404 (feedback to cloud)
GET  /api/auth/status            → 404 (auth status)
```

### Modified Endpoints
```
GET /api/runs
  Before: { "locked": true/false, "count": N, "runs": [...] }
  After:  { "count": N, "runs": [...] }
  
  Change: Removed "locked" field, always returns all runs
```

### Unchanged Endpoints
```
GET  /api/run                    ✅ Works as before
GET  /api/vulnerabilities        ✅ Works as before
GET  /api/transcript             ✅ Works as before
GET  /api/report                 ✅ Works as before
GET  /api/capabilities           ✅ Works as before
POST /api/report/download        ✅ Works as before (local PDF)
POST /api/agents/steer           ✅ Works as before
POST /api/scans/start            ✅ Works as before
POST /api/scans/list             ✅ Works as before
POST /api/scans/stop             ✅ Works as before
POST /api/scans/find-run         ✅ Works as before
```

## Migration Notes

If you have existing code that depends on the removed features:

1. **Email Reports:** Replace with local PDF download
2. **Past Runs Lock:** Remove any verification checks
3. **Feedback:** Implement alternative feedback channel if needed
4. **Analytics:** Remove any tracking code

## Files Safe to Delete (Optional Cleanup)

These files are no longer imported but were left in place:

```
strix/interface/viewer/frontend/src/components/EmailReportView.tsx
strix/interface/viewer/frontend/src/components/EmailVerifyInline.tsx
strix/interface/viewer/frontend/src/components/FeedbackView.tsx
strix/interface/viewer/frontend/src/components/ProCta.tsx
strix/interface/viewer/frontend/src/components/UpgradeModal.tsx
```

The backend auth module is also no longer used:
```
strix/interface/viewer/auth.py
```

## Build & Deploy

```bash
# Rebuild frontend
cd strix/interface/viewer/frontend
npm run build

# The output goes to:
# strix/interface/viewer/static/

# No Python dependencies changed
# Server will automatically use the new build
```

## Rollback Instructions

If you need to rollback these changes:

```bash
# Git revert (if committed)
git revert <commit-hash>

# Or restore from backup
git checkout HEAD~1 strix/interface/viewer/
cd strix/interface/viewer/frontend
npm run build
```
