# 🚀 Setup Guide — Avanade Uploader Component

## For Next.js / React Projects

This guide shows how to integrate the Avanade-branded Google Drive uploader component into your React/Next.js project.

---

## ✅ Prerequisites

Your project must have:
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.0.0",
    "postcss": "^8.0.0"
  }
}
```

### Check Your Setup
```bash
# Verify React version
npm list react

# Verify TypeScript
npm list typescript

# Verify Tailwind CSS
cat tailwind.config.js
```

---

## 📦 Step 1: Install Dependencies

```bash
# Install lucide-react for icons
npm install lucide-react

# Or with yarn
yarn add lucide-react

# Or with pnpm
pnpm add lucide-react
```

**Verify installation:**
```bash
npm list lucide-react
# Should show: lucide-react@X.X.X
```

---

## 📁 Step 2: Create Component Directory

If you don't have `/components/ui`, create it:

```bash
# Linux/Mac
mkdir -p src/components/ui

# Windows PowerShell
New-Item -ItemType Directory -Path "src\components\ui" -Force
```

**Why `/components/ui`?**
- Standard location for shadcn projects
- Keeps component library organized
- Easy for team collaboration
- Follows industry conventions

---

## 📋 Step 3: Copy Component Files

### Option A: Manual Copy-Paste
1. Copy `google-drive-uploader-toast-avanade.tsx` content
2. Create file: `src/components/ui/google-drive-uploader-toast-avanade.tsx`
3. Paste the code

### Option B: Command Line
```bash
# Copy from template
cp ./reports/_templates/google-drive-uploader-toast-avanade.tsx src/components/ui/
```

**File structure after:**
```
your-project/
├── src/
│   ├── components/
│   │   └── ui/
│   │       └── google-drive-uploader-toast-avanade.tsx ✓
│   ├── pages/ (or app/ for Next.js 13+)
│   └── ...
└── package.json
```

---

## 🎯 Step 4: Use in Your App

### Next.js 13+ (App Router)
```tsx
// app/upload/page.tsx
import { Component } from '@/components/ui/google-drive-uploader-toast-avanade';

export default function UploadPage() {
  return (
    <div>
      <h1>Upload Files</h1>
      <Component />
    </div>
  );
}
```

### Next.js 12 or Create React App
```tsx
// pages/upload.tsx or src/pages/Upload.tsx
import { Component } from '@/components/ui/google-drive-uploader-toast-avanade';

export default function UploadPage() {
  return (
    <div>
      <h1>Upload Files</h1>
      <Component />
    </div>
  );
}
```

### Traditional React
```tsx
// src/pages/Upload.tsx
import { Component } from '../components/ui/google-drive-uploader-toast-avanade';

export function Upload() {
  return (
    <div>
      <h1>Upload Files</h1>
      <Component />
    </div>
  );
}

export default Upload;
```

---

## 🎨 Step 5: Verify Tailwind CSS Setup

The component uses Tailwind classes. Ensure your `tailwind.config.js` includes:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',  // Adjust path if needed
    './app/**/*.{js,ts,jsx,tsx}',  // For Next.js
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Verify Tailwind is working:**
```bash
npm run dev
# Visit your app and check if styles load
```

---

## 🧪 Step 6: Test the Component

### Quick Test
```tsx
// test-upload.tsx
import { Component } from '@/components/ui/google-drive-uploader-toast-avanade';

export default function TestPage() {
  return <Component />;
}
```

Visit: `http://localhost:3000/test-upload` (or your dev port)

**Expected behavior:**
✓ Orange/blue Avanade branding  
✓ Upload buttons visible  
✓ Click buttons to simulate uploads  
✓ Toast appears bottom-right  
✓ Progress bar animates  
✓ Expandable/collapsible toast

---

## 🔧 Step 7: Customization (Optional)

### Change Brand Colors
In `google-drive-uploader-toast-avanade.tsx`, modify:
```typescript
const AVANADE_COLORS = {
  primary: "#ff6b35",      // Avanade Orange → Change this
  secondary: "#1f3a93",    // Avanade Blue
  accent: "#f7931e",       // Light Orange
  dark: "#0f1d4d",         // Dark Blue
  light: "#f9f9f9",        // Light Gray
  border: "#e0e0e0",       // Border Gray
};
```

### Add More File Types
```typescript
const FILE_TYPES = {
  // ... existing types
  svg: { icon: FileCode, color: "text-indigo-500" },
  csv: { icon: File, color: "text-green-500" },
};
```

### Change Max Uploads
```typescript
const MAX_UPLOADS = 10;  // Default is 6
```

---

## 🚀 Step 8: Production Integration

### Replace Simulated Uploads with Real API

```tsx
// Custom hook for real uploads
const useRealUpload = (updateItem: any) => {
  return useCallback(
    async (id: string, file: File) => {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          updateItem(id, { status: 'ERROR', error: 'Upload failed' });
          return;
        }

        updateItem(id, { status: 'SUCCESS', progress: 100 });
      } catch (error) {
        updateItem(id, { 
          status: 'ERROR', 
          error: error.message 
        });
      }
    },
    [updateItem]
  );
};
```

### Add File Input
```tsx
// In your component
const fileInputRef = useRef<HTMLInputElement>(null);

const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
  const files = event.currentTarget.files;
  if (files) {
    Array.from(files).forEach(file => {
      const id = addItem(file.name, getFileType(file.name));
      simulateUpload(id); // Replace with real upload
    });
  }
};

return (
  <input
    ref={fileInputRef}
    type="file"
    multiple
    onChange={handleFileSelect}
    style={{ display: 'none' }}
  />
);
```

---

## 🐛 Troubleshooting

### Issue: Component not rendering
**Solution:** Check import path matches your file location
```tsx
// ✓ Correct
import { Component } from '@/components/ui/google-drive-uploader-toast-avanade';

// ✗ Wrong
import { Component } from './google-drive-uploader-toast-avanade';
```

### Issue: Tailwind classes not applying
**Solution:** Verify `tailwind.config.js` includes component paths
```javascript
content: [
  './src/**/*.{js,ts,jsx,tsx}',  // Add this line
],
```

### Issue: lucide-react icons missing
**Solution:** Install lucide-react
```bash
npm install lucide-react
npm run dev  # Restart dev server
```

### Issue: Dark mode not working
**Solution:** Add dark mode config to `tailwind.config.js`
```javascript
module.exports = {
  darkMode: 'class', // or 'media'
  // ... rest of config
}
```

### Issue: TypeScript errors
**Solution:** Ensure `typescript` is installed
```bash
npm install --save-dev typescript
npm run type-check
```

---

## 📋 Integration Checklist

- [ ] Node/npm installed and updated
- [ ] React 18+ project created
- [ ] TypeScript configured
- [ ] Tailwind CSS installed and configured
- [ ] lucide-react installed
- [ ] Component file copied to `/components/ui/`
- [ ] Component imported correctly
- [ ] Dev server running without errors
- [ ] Component renders with Avanade branding
- [ ] Upload buttons functional
- [ ] Progress bar animates
- [ ] Dark mode works (optional)

---

## 📚 Next Steps

1. **Customize colors** if using different brand
2. **Replace simulated uploads** with real API calls
3. **Add file validation** (size, type checks)
4. **Integrate with backend** for actual storage
5. **Add error handling** for network failures
6. **Test on mobile** and different browsers

---

## 💡 Tips

- **Multiple instances?** Each component has its own upload state
- **Want global state?** Use Redux/Zustand/Context API
- **Need file preview?** Add preview panel in DriveUploadToast
- **Want email notifications?** Add webhook after upload completes

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `npm install lucide-react` |
| Start dev server | `npm run dev` |
| Build for production | `npm run build` |
| Check types | `npm run type-check` |
| Format code | `npm run format` |

---

**Setup Time:** ~5 minutes  
**Difficulty:** ⭐ Easy  
**Status:** ✅ Ready to use  

---

Generated: 2026-06-05  
Project: Avanade Data Migration Factory
