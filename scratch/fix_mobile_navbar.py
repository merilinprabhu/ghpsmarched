import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('navbar.js', 'r', encoding='utf-8') as f:
    nav_code = f.read()

# Let's inspect the modern_top / default_top mobile header section
old_header_pattern = r'<!-- EXPANDED FULL HEADER -->[\s\S]*?<!-- Bottom Row: Navigation menu -->'

new_header = """<!-- EXPANDED FULL HEADER -->
          <div class="nav-expanded-content flex flex-col w-full">
            <!-- Top Row (Logo, School Name, Controls) -->
            <div class="w-full px-3.5 sm:px-6 py-2.5 sm:py-3.5 flex items-center justify-between gap-2 sm:gap-4">
              <!-- Left Logo & Brand -->
              <div class="flex items-center gap-2 sm:gap-3 shrink min-w-0 cursor-pointer group" onclick="window.togglePortalNav(true)" title="ಕ್ಲಿಕ್ ಮಾಡಿ ಕುಗ್ಗಿಸಿ (Click to Collapse Navigation)">
                <img src="${logoUrl}" alt="School Logo" class="h-10 w-10 sm:h-14 sm:w-14 md:h-16 md:w-16 object-contain rounded-xl sm:rounded-2xl shadow-sm border border-slate-900/5 dark:border-white/10 bg-white/40 dark:bg-slate-800 p-1 shrink-0 transition-all duration-300 group-hover:scale-105">
                <div class="flex flex-col min-w-0">
                  <h1 class="text-xs sm:text-sm md:text-lg font-black uppercase tracking-wider bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 dark:from-white dark:via-indigo-200 dark:to-white bg-clip-text text-transparent truncate school-title-full">GHPS Marched</h1>
                  <p class="text-[9px] sm:text-[10px] md:text-xs text-indigo-800 dark:text-indigo-300 font-extrabold tracking-wider uppercase truncate school-title-kn mt-0.5">ಸ.ಹಿ.ಪ್ರಾ.ಶಾಲೆ, ಮರ್ಚೆಡ್</p>
                </div>
              </div>

              <!-- Right Status & Controls for Desktop (Hidden on Mobile) -->
              <div class="hidden md:flex items-center gap-1.5 text-[10px] shrink-0 justify-end">
                <div class="flex items-center gap-2 bg-slate-950/95 border border-slate-800/60 rounded-lg px-2 py-1 shadow-inner">
                  <span id="liveDate" class="text-[8px] text-slate-400 font-bold tracking-wider uppercase"></span>
                  <div class="w-px h-2.5 bg-slate-800"></div>
                  <span id="liveClock" class="font-mono font-black text-emerald-400 text-[10px] tracking-wider glow-text-emerald"></span>
                </div>

                <!-- Theme Selector -->
                <div class="flex items-center gap-1.5 bg-slate-900/5 dark:bg-white/10 border border-slate-900/10 dark:border-white/10 rounded-lg px-2 py-1 shadow-sm transition-all duration-300">
                  <span class="text-slate-400 font-bold text-[8px] uppercase tracking-wider"><i class="fa-solid fa-palette text-indigo-500 text-[8px]"></i> Theme:</span>
                  <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-slate-800 dark:text-white border-0 rounded text-[10px] font-bold focus:outline-none cursor-pointer py-0">
                    <option class="bg-slate-900 text-white" value="light">Light</option>
                    <option class="bg-slate-900 text-white" value="dark">Dark</option>
                    <option class="bg-slate-900 text-white" value="gray">Gray</option>
                    <option class="bg-slate-900 text-white" value="blue">Blue</option>
                    <option class="bg-slate-900 text-white" value="green">Green</option>
                  </select>
                </div>
                
                <!-- Version Badge Button -->
                <button onclick="window.openWhatsNewModal()" class="flex items-center gap-1 bg-gradient-to-r from-amber-500/10 via-emerald-500/10 to-indigo-500/10 hover:from-amber-500/20 hover:to-indigo-500/20 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 font-extrabold px-2 py-0.5 rounded-full text-[10px] transition cursor-pointer shadow-sm" title="Version 2.5.1">
                  <i class="fa-solid fa-wand-magic-sparkles text-amber-500 text-[10px]"></i>
                  <span>v2.5.1</span>
                </button>

                <!-- User Badge Capsule -->
                <div class="flex items-center gap-1 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-full px-2.5 py-0.5 shadow-inner">
                  <i class="fa-solid fa-user-circle text-[10px] text-indigo-500"></i>
                  <span id="headerUser" class="font-bold text-slate-850 dark:text-slate-200 text-[10px] truncate max-w-[100px]">User</span>
                </div>

                <!-- Collapse Toggle Button -->
                <button type="button" onclick="window.togglePortalNav(true)" class="flex items-center gap-1 bg-slate-900/5 hover:bg-indigo-600 hover:text-white dark:bg-white/10 dark:hover:bg-indigo-600 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 px-2.5 py-1 rounded-full text-[10px] font-bold transition-all duration-200 cursor-pointer shadow-xs" title="ಕುಗ್ಗಿಸಿ">
                  <i class="fa-solid fa-compress text-indigo-500"></i>
                  <span>ಕುಗ್ಗಿಸಿ</span>
                </button>

                <!-- Logout Button -->
                <button onclick="handleLogout()" class="bg-red-500/10 hover:bg-red-650 border border-red-500/30 hover:border-red-650 text-red-600 hover:text-white px-2.5 py-0.5 rounded-full text-[10px] font-bold transition-all duration-300 cursor-pointer flex items-center gap-1.5 shadow-sm">
                  <i class="fa-solid fa-right-from-bracket text-[10px]"></i> <span>Logout</span>
                </button>
              </div>

              <!-- Mobile Top Right (Hamburger & User Capsule) -->
              <div class="flex md:hidden items-center gap-2 shrink-0">
                <!-- User Capsule Mobile -->
                <div class="flex items-center gap-1 bg-indigo-50 dark:bg-slate-800 border border-indigo-200/60 dark:border-slate-700 rounded-full px-2 py-0.5 text-[10px]">
                  <i class="fa-solid fa-user text-indigo-600 dark:text-indigo-400 text-[9px]"></i>
                  <span id="headerUserMobile" class="font-black text-indigo-950 dark:text-slate-100 max-w-[65px] truncate">User</span>
                </div>

                <!-- Mobile Hamburger Button -->
                <button id="mobileMenuBtn" class="flex items-center justify-center p-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm border-0 cursor-pointer transition active:scale-95">
                  <i class="fa-solid fa-bars text-sm"></i>
                </button>
              </div>
            </div>

            <!-- Bottom Row: Navigation menu -->"""

nav_code = re.sub(old_header_pattern, new_header, nav_code)

with open('navbar.js', 'w', encoding='utf-8') as f:
    f.write(nav_code)

print("Updated mobile navbar header in navbar.js")
