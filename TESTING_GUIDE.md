# 🧪 Testing Guide — macOS UI Redesign

## Quick Start

### 1. Run the Application
```bash
streamlit run app.py
```

### 2. Open in Browser
The app will automatically open at `http://localhost:8501`

---

## ✅ Test Checklist

### 🏠 HOME SCREEN

**Visual Checks:**
- [ ] macOS traffic light buttons (● ● ●) appear in top-left
- [ ] "SnapClass" logo and title centered
- [ ] Tagline "AI-powered attendance made simple" visible
- [ ] Two portal cards (Student / Teacher) side-by-side
- [ ] Cards have white background with subtle border
- [ ] Mascot images display correctly
- [ ] Footer shows at bottom

**Interaction Checks:**
- [ ] Hover over portal cards → lift effect + shadow
- [ ] Click "Continue as Student" → routes to student login
- [ ] Click "Continue as Teacher" → routes to teacher login

---

### 👨‍🏫 TEACHER EXPERIENCE

#### Login Screen
**Visual:**
- [ ] Centered login form (username + password)
- [ ] Clean input fields with proper focus states
- [ ] "← Back to Home" button in top-right
- [ ] Logo in top-left

**Interaction:**
- [ ] Type in inputs → blue focus border appears
- [ ] Click "Login" → validates credentials
- [ ] Invalid credentials → error message shows
- [ ] Click "Register" → switches to registration form

#### Registration Screen
**Visual:**
- [ ] Four input fields (username, name, password, confirm)
- [ ] Centered form layout

**Interaction:**
- [ ] Fill all fields correctly → registration succeeds
- [ ] Passwords don't match → error shows
- [ ] Username exists → error shows
- [ ] Success → redirects to login screen

#### Dashboard - Navigation
**Visual:**
- [ ] Dashboard header shows "SnapClass" logo
- [ ] Welcome message shows teacher name
- [ ] Logout button in top-right
- [ ] Three navigation tabs visible
- [ ] Active tab highlighted in blue

**Interaction:**
- [ ] Click each tab → switches content correctly
- [ ] Active tab styling changes
- [ ] Click logout → returns to home screen

#### Tab: Take Attendance
**Visual:**
- [ ] Page title "Take Attendance"
- [ ] Subject dropdown populated (if subjects exist)
- [ ] "Add Photos" button visible
- [ ] Photo gallery appears after adding photos
- [ ] Three action buttons at bottom

**Interaction:**
- [ ] Click "Add Photos" → dialog opens
- [ ] Dialog has Camera / Upload Files tabs
- [ ] Camera tab → can take photos
- [ ] Upload tab → can select multiple files
- [ ] Photos appear in 4-column gallery
- [ ] Click "Clear All Photos" → gallery clears
- [ ] Click "Run Face Analysis" → spinner shows, results dialog opens
- [ ] Click "Use Voice Attendance" → voice dialog opens
- [ ] Results dialog shows table with Present/Absent
- [ ] Click "Confirm & Save" → attendance saved, toast appears

#### Tab: Manage Subjects
**Visual:**
- [ ] Page title "Manage Subjects"
- [ ] "Create Subject" button visible
- [ ] Subject cards display in list
- [ ] Each card shows: name, code, section, stats
- [ ] Stats show student count and class count
- [ ] "Share Code" button per subject

**Interaction:**
- [ ] Click "Create Subject" → dialog opens
- [ ] Fill code, name, section → subject created
- [ ] New subject appears in list
- [ ] Click "Share Code" → share dialog opens
- [ ] Share dialog shows: code, link, QR code
- [ ] Can copy code and link

#### Tab: Attendance Records
**Visual:**
- [ ] Page title "Attendance Records"
- [ ] Table shows all attendance sessions
- [ ] Columns: Time, Subject, Subject Code, Attendance
- [ ] Sorted by most recent first
- [ ] Clean dataframe styling

**Interaction:**
- [ ] Table scrollable if many records
- [ ] Data displays correctly

---

### 🎓 STUDENT EXPERIENCE

#### Login Screen
**Visual:**
- [ ] Centered "Student Login" title
- [ ] "Sign in with Face ID" subtitle
- [ ] Camera input widget visible
- [ ] "← Back to Home" button in top-right

**Interaction:**
- [ ] Camera captures face
- [ ] Spinner shows "Scanning face..."
- [ ] Recognized face → auto-login with toast
- [ ] Unrecognized face → registration form appears

#### Registration Form
**Visual:**
- [ ] Appears below camera after unrecognized face
- [ ] Name input field
- [ ] "Voice Enrollment (Optional)" section
- [ ] Audio input widget
- [ ] "Create Account" button

**Interaction:**
- [ ] Enter name → validation works
- [ ] Record audio (optional)
- [ ] Click "Create Account" → profile created
- [ ] Success toast appears
- [ ] Redirects to dashboard

#### Dashboard
**Visual:**
- [ ] Header shows student name
- [ ] "Your Subjects" title
- [ ] "Enroll in Subject" button in top-right
- [ ] Subject cards in 2-column grid
- [ ] Each card shows: name, code, section, stats
- [ ] Stats: Total classes, Attended, Attendance %
- [ ] "Unenroll" button per subject

**Interaction:**
- [ ] Click "Enroll in Subject" → dialog opens
- [ ] Enter subject code → validates
- [ ] Valid code → enrollment succeeds
- [ ] Invalid code → error shows
- [ ] Already enrolled → warning shows
- [ ] New subject appears in grid
- [ ] Click "Unenroll" → confirmation, subject removed
- [ ] Logout works

---

### 🔗 URL JOIN CODE

**Test:**
1. As teacher: Create a subject, get its code (e.g., "CS101")
2. Copy the join link or manually craft: `http://localhost:8501/?join-code=CS101`
3. Open in new tab (or send to someone)
4. If not logged in as student → redirects to student login first
5. After student login → auto-enroll dialog appears
6. Dialog shows subject name
7. Click "Yes, Enroll!" → enrollment succeeds
8. Redirects to dashboard with new subject

---

## 🎨 Visual Quality Checks

### Color Palette
- [ ] Background is light gray (#F5F5F7), not purple
- [ ] Cards are white (#FFFFFF)
- [ ] Primary buttons are Apple Blue (#007AFF)
- [ ] Text is near-black (#1D1D1F)
- [ ] Secondary text is gray (#6E6E73)

### Typography
- [ ] Font looks system-native (SF Pro fallback)
- [ ] Headings are bold but not decorative
- [ ] Letter-spacing is tight (-0.02em)
- [ ] No "Climate Crisis" or "Outfit" fonts

### Spacing
- [ ] Generous whitespace everywhere
- [ ] Content is centered (max-width)
- [ ] Consistent padding in cards
- [ ] Clean margins between sections

### Buttons
- [ ] Border-radius is subtle (~8px), not pill-shaped
- [ ] Hover effect is lift + shadow, not scale
- [ ] Primary buttons are blue
- [ ] Secondary buttons are gray
- [ ] Tertiary buttons are transparent with red text

### Inputs
- [ ] Clean borders (1px solid, light gray)
- [ ] Focus state shows blue border + blue glow
- [ ] No excessive styling

### Cards
- [ ] White background
- [ ] Subtle border (not thick colored border)
- [ ] Soft shadow
- [ ] Hover lifts with shadow elevation

### Dialogs
- [ ] Clean white surfaces
- [ ] Proper headers with descriptions
- [ ] Consistent button placement
- [ ] No color overload

---

## 🐛 Bug Testing

### Edge Cases to Test:
- [ ] No subjects exist (teacher) → warning message shows
- [ ] No students enrolled in subject → warning shows
- [ ] Camera permission denied → error handled
- [ ] Upload invalid image → error handled
- [ ] Multiple faces in photo → warning shows
- [ ] No face in photo → warning shows
- [ ] Empty form submission → validation errors
- [ ] Duplicate subject code → error handled
- [ ] Join with invalid code → error handled
- [ ] Already enrolled in subject → warning shows

---

## 📱 Responsive Testing

### Desktop (1200px+)
- [ ] Content centered with max-width
- [ ] Two-column grids work
- [ ] No horizontal overflow

### Tablet (768px - 1199px)
- [ ] Layout adapts properly
- [ ] Cards stack if needed
- [ ] Still readable

### Mobile (< 768px)
- [ ] Single column layout
- [ ] Buttons stack vertically
- [ ] Forms are usable
- [ ] Camera input works

---

## ✨ Polish Checks

### Transitions
- [ ] All transitions are smooth (150ms)
- [ ] Hover states are subtle
- [ ] No jarring animations

### Icons
- [ ] Material icons display correctly
- [ ] Icon colors match text colors
- [ ] Icons are sized appropriately

### Feedback
- [ ] Toast notifications appear on actions
- [ ] Success messages are green
- [ ] Error messages are red
- [ ] Warning messages are orange
- [ ] Loading spinners show during async operations

### Accessibility
- [ ] Focus indicators visible
- [ ] Tab navigation works
- [ ] Keyboard shortcuts work (Ctrl+Enter, Ctrl+Backspace)
- [ ] Color contrast is sufficient

---

## 🚀 Performance

- [ ] App loads quickly
- [ ] No console errors
- [ ] Face recognition responds in reasonable time
- [ ] No lag in UI interactions
- [ ] Images load properly

---

## ✅ Final Approval Checklist

- [ ] Does it look like a macOS application?
- [ ] Does it NOT look like a generic SaaS dashboard?
- [ ] Is the typography clean and professional?
- [ ] Is the color palette restrained (neutral + blue)?
- [ ] Do all teacher features work?
- [ ] Do all student features work?
- [ ] Do all dialogs work?
- [ ] Is the design consistent across all screens?
- [ ] Would you be proud to show this in an interview?

---

## 📸 Screenshot Locations for Portfolio

Take screenshots of:
1. Home screen with portal cards
2. Teacher dashboard with subjects
3. Take attendance with photo gallery
4. Attendance results dialog
5. Student dashboard with subject cards
6. Face ID login screen
7. Subject card with share dialog
8. Clean dataframe view

---

**If all checks pass:** ✅ The redesign is complete and production-ready!

**If issues found:** Document them and fix before considering complete.
