// GHPS Marched School Portal Shared Navigation Component
// Upgraded to ULTRA-MODERN GLASSMORPHIC STYLE with PREMIUM RADIUM ACCENTS
// Supports three layouts: default_top, modern_top, and side (left sidebar)
(function() {
  const initialLayout = localStorage.getItem('school_nav_layout') || 'default_top';

  function getShortSchoolName(fullName) {
    if (!fullName) return "GHPS MARCHED";
    let name = fullName;
    name = name.replace(/Government Higher Primary School/gi, "GHPS");
    name = name.replace(/Government High School/gi, "GHS");
    name = name.replace(/Government Lower Primary School/gi, "GLPS");
    name = name.replace(/Govt\s+Higher\s+Primary\s+School/gi, "GHPS");
    name = name.replace(/Govt\./gi, "Govt");
    return name.trim();
  }
  
  // Inject layout-adaptive styles immediately to avoid layout flashing
  let layoutStyleEl = document.getElementById('layout-adaptive-styles');
  if (!layoutStyleEl) {
    layoutStyleEl = document.createElement('style');
    layoutStyleEl.id = 'layout-adaptive-styles';
    document.head.appendChild(layoutStyleEl);
  }
  
  function applyBodyPadding(layout) {
    if (layout === 'side') {
      layoutStyleEl.textContent = `
        @media screen and (min-width: 1024px) {
          body {
            padding-left: 260px !important;
            transition: padding-left 0.3s ease;
          }
          .sticky.top-0:not(#navbar-placeholder):not(#navbar-container) {
            left: 260px !important;
            width: calc(100% - 260px) !important;
          }
        }
      `;
    } else {
      layoutStyleEl.textContent = '';
    }
  }
  
  applyBodyPadding(initialLayout);

  // Inject generic custom CSS styles for all layouts
  const styleEl = document.createElement('style');
  styleEl.textContent = `
    #navbar-placeholder {
      position: sticky;
      top: 0;
      z-index: 1000;
      width: 100%;
    }
    /* Dropdown Animation and Layout */
    .nav-dropdown-item {
      position: relative;
    }
    .nav-dropdown-list {
      opacity: 0;
      visibility: hidden;
      transform: translateY(10px) scale(0.95);
      transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), 
                  transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), 
                  visibility 0.25s;
    }
    .nav-dropdown-item:hover .nav-dropdown-list {
      opacity: 1;
      visibility: visible;
      transform: translateY(0) scale(1);
    }
    
    /* Neon Glow & Text Shadow Effects */
    .glow-text-emerald {
      text-shadow: 0 0 10px rgba(52, 211, 153, 0.5), 0 0 20px rgba(52, 211, 153, 0.2);
    }
    .glow-shadow-indigo {
      box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
    }
    .glow-shadow-indigo-hover:hover {
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.45);
      border-color: rgba(99, 102, 241, 0.6) !important;
    }
    .glow-shadow-purple-hover:hover {
      box-shadow: 0 0 20px rgba(168, 85, 247, 0.45);
      border-color: rgba(168, 85, 247, 0.6) !important;
    }
    .glow-shadow-red-hover:hover {
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.45);
      border-color: rgba(239, 68, 68, 0.6) !important;
    }

    /* Active Tab Glow Indicator */
    .active-nav-tab {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
      border-color: rgba(99, 102, 241, 0.3) !important;
      box-shadow: 0 0 10px rgba(99, 102, 241, 0.05);
      color: #4f46e5 !important;
    }

    /* Scrollbar customization for mobile drawer & sidebar */
    .mobile-menu-drawer::-webkit-scrollbar {
      width: 4px;
    }
    .mobile-menu-drawer::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.5);
    }
    .mobile-menu-drawer::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
  `;
  document.head.appendChild(styleEl);

  // Define menu structure
  const menuData = [
    { name: "Dashboard", href: "dashboard.html", icon: "fa-chart-pie", color: "text-indigo-400" },
    { name: "Admin Panel", href: "admin.html", icon: "fa-shield-halved", color: "text-rose-400" },
    {
      name: "Teachers",
      icon: "fa-chalkboard-user",
      color: "text-emerald-400",
      items: [
        { name: "Teacher Dashboard", href: "teachers.html" }
      ]
    },
    {
      name: "Students",
      icon: "fa-graduation-cap",
      color: "text-sky-400",
      items: [
        { name: "New Admission Form", href: "NewAdmission.html" },
        { name: "New Admission List", href: "NewAdmissionList.html" },
        { name: "View Students", href: "StudentList.html" },
        { name: "Update Details", href: "StudentUpdate.html" },
        { name: "Aadhar Update", href: "ApaarModule.html" }
      ]
    },
    {
      name: "Academic",
      icon: "fa-book-open",
      color: "text-pink-400",
      items: [
        { name: "Bridge Course", href: "BridgeCourse.html" },
        { name: "CCE Assessment", href: "CceAssessmet.html" },
        { name: "LBA Assessment", href: "LbaAssessment.html" },
        { name: "FLN Assessment", href: "FlnAssessment.html" },
        { name: "Attendance Management", href: "Attendance.html" }
      ]
    },
    { name: "Custom Reports", href: "custom_reports.html", icon: "fa-file-invoice", color: "text-purple-400" },
    {
      name: "Incentives",
      icon: "fa-gift",
      color: "text-amber-400",
      items: [
        { name: "Incentives Dashboard", href: "incentives.html" }
      ]
    },
    {
      name: "Attendance",
      icon: "fa-calendar-check",
      color: "text-orange-400",
      items: [
        { name: "Manage Attendance", href: "Attendance.html" }
      ]
    },
    {
      name: "Finance",
      icon: "fa-wallet",
      color: "text-rose-400",
      items: [
        { name: "Exam Fee Collection", href: "#" }
      ]
    },
    {
      name: "Govt Portals",
      icon: "fa-globe",
      color: "text-teal-400",
      items: [
        { name: "SATS / STS Portal", href: "https://sts.karnataka.gov.in", external: true },
        { name: "Mid-Day Meals Login", href: "#" },
        { name: "Shikshana Kirana", href: "https://choas.karnataka.gov.in", external: true }
      ]
    }
  ];

  const currentPath = window.location.pathname.split('/').pop() || 'dashboard.html';

  function isLinkActive(item) {
    if (item.href && item.href === currentPath) return true;
    if (item.items) {
      return item.items.some(sub => sub.href === currentPath);
    }
    return false;
  }

  function renderNavbar() {
    const layout = localStorage.getItem('school_nav_layout') || 'default_top';
    const placeholder = document.getElementById('navbar-placeholder');
    if (!placeholder) return;

    applyBodyPadding(layout);

    const defaultLogoUrl = "https://gsayvnnnfrrkwdfwocbu.supabase.co/storage/v1/object/public/school-logo/Gemini_Generated_Image_pjk3eppjk3eppjk3.png";
    const logoUrl = localStorage.getItem('school_logo_url') || defaultLogoUrl;

    let headerHtml = '';

    if (layout === 'side') {
      headerHtml = `
        <div id="navbar-container" class="no-print">
          <!-- Desktop Left Sidebar (screens >= 1024px) -->
          <aside class="hidden lg:flex fixed top-0 left-0 bottom-0 w-[260px] h-screen bg-slate-950/60 border-r border-white/10 backdrop-blur-2xl flex flex-col justify-between text-white z-50 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
            <!-- Brand & User Profile -->
            <div class="p-5 flex flex-col gap-4 border-b border-white/10">
              <div class="flex items-center gap-3">
                <img src="${logoUrl}" alt="School Logo" class="h-16 w-16 object-contain rounded-xl border border-white/20 bg-white/5 p-1 shadow-md">
                <div>
                  <h1 class="text-[11px] font-extrabold uppercase tracking-wider bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent school-title-short truncate max-w-[150px]">GHPS Marched</h1>
                  <p class="text-[8px] text-indigo-300/70 font-semibold tracking-wider school-title-kn truncate max-w-[150px]">ಸ.ಹಿ.ಪ್ರಾ.ಶಾಲೆ, ಮರ್ಚೆಡ್</p>
                </div>
              </div>
              
              <!-- User Badge -->
              <div class="flex items-center gap-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-xl px-3 py-2 shadow-inner">
                <i class="fa-solid fa-user-circle text-lg text-indigo-400"></i>
                <div class="flex flex-col min-w-0">
                  <span id="headerUser" class="font-bold text-slate-200 text-xs truncate max-w-[140px]">User</span>
                </div>
              </div>
            </div>

            <!-- Sidebar Nav Links -->
            <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto mobile-menu-drawer" id="desktopNav">
              <!-- Vertical menu items will be injected here -->
            </nav>

            <!-- Bottom Controls -->
            <div class="p-4 border-t border-slate-800/60 bg-slate-950/50 space-y-3">
              <div class="flex items-center justify-between bg-black/40 border border-slate-800/80 rounded-xl px-3 py-2">
                <span id="liveDate" class="text-[9px] text-slate-400 font-bold uppercase"></span>
                <span id="liveClock" class="font-mono font-black text-emerald-400 text-xs glow-text-emerald"></span>
              </div>
              
              <div class="flex items-center justify-between bg-white/5 border border-white/10 rounded-xl px-3 py-1.5">
                <span class="text-slate-400 font-bold text-[9px] uppercase tracking-wider"><i class="fa-solid fa-palette text-indigo-400 mr-1"></i> Theme:</span>
                <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-white border-0 text-xs font-bold focus:outline-none cursor-pointer">
                  <option class="bg-slate-900 text-white" value="light">Light</option>
                  <option class="bg-slate-900 text-white" value="dark">Dark</option>
                  <option class="bg-slate-900 text-white" value="gray">Gray</option>
                  <option class="bg-slate-900 text-white" value="blue">Blue</option>
                  <option class="bg-slate-900 text-white" value="green">Green</option>
                </select>
              </div>
              
              <button onclick="handleLogout()" class="w-full bg-red-500/10 hover:bg-red-650 border border-red-500/30 hover:border-red-600 text-red-400 hover:text-white py-2 rounded-xl text-xs font-bold transition duration-300 flex items-center justify-center gap-1.5 shadow-sm glow-shadow-red-hover">
                <i class="fa-solid fa-right-from-bracket"></i> Logout
              </button>
            </div>
          </aside>

          <!-- Mobile Top Header (screens < 1024px) -->
          <div class="lg:hidden w-full sticky top-0 z-50 flex flex-col flex-shrink-0 shadow-[0_12px_40px_rgba(0,0,0,0.3)] border-b border-white/10 backdrop-blur-2xl bg-slate-950/50 text-white">
            <!-- Top Neon Gradient line -->
            <div class="h-[2px] w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
            <div class="w-full px-4 py-2.5 flex justify-between items-center z-50">
              <div class="flex items-center gap-2">
                <img src="${logoUrl}" alt="School Logo" class="h-12 w-12 object-contain rounded-lg border border-white/10 bg-white/5 p-0.5">
                <div>
                  <h1 class="text-xs font-extrabold uppercase tracking-wider text-indigo-100 school-title-short truncate max-w-[150px]">GHPS Marched</h1>
                  <p class="text-[8px] text-indigo-300/70 font-semibold tracking-wider school-title-kn truncate max-w-[150px]">ಸ.ಹಿ.ಪ್ರಾ.ಶಾಲೆ, ಮರ್ಚೆಡ್</p>
                </div>
              </div>
              
              <div class="flex items-center gap-2 text-xs">
                <!-- Mobile Logout -->
                <button onclick="handleLogout()" class="bg-red-500/10 hover:bg-red-600 border border-red-500/30 hover:border-red-600 text-red-400 hover:text-white px-3 py-1.5 rounded-full text-xs font-bold transition-all duration-300 flex items-center gap-1 shadow-sm glow-shadow-red-hover">
                  <i class="fa-solid fa-right-from-bracket text-[10px]"></i>
                </button>
                <!-- Hamburger menu button -->
                <button id="mobileMenuBtn" class="flex items-center justify-center p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg focus:outline-none cursor-pointer">
                  <i class="fa-solid fa-bars text-base"></i>
                </button>
              </div>
            </div>
            
            <!-- Mobile Accordion Menu Drawer -->
            <div id="mobileMenuPanel" class="hidden w-full bg-slate-950 border-t border-slate-900 max-h-[75vh] overflow-y-auto mobile-menu-drawer transition-all duration-300 z-35">
              <div class="px-4 py-3 space-y-1.5 text-sm font-semibold" id="mobileNav">
                <!-- Mobile menu items will be injected here -->
                <div class="flex items-center justify-between pt-4 border-t border-slate-850 mt-3 flex-wrap gap-2">
                  <div class="flex items-center gap-1 bg-white/5 px-2 py-0.5 rounded-xl border border-white/10">
                    <span class="text-slate-400 text-[9px] font-bold uppercase"><i class="fa-solid fa-palette text-indigo-400 mr-1"></i>Theme:</span>
                    <select id="themeSelectorMobile" onchange="changeTheme(this.value)" class="bg-transparent text-white border-0 text-xs focus:outline-none">
                      <option class="bg-slate-900 text-white" value="light">Light</option>
                      <option class="bg-slate-900 text-white" value="dark">Dark</option>
                      <option class="bg-slate-900 text-white" value="gray">Gray</option>
                      <option class="bg-slate-900 text-white" value="blue">Blue</option>
                      <option class="bg-slate-900 text-white" value="green">Green</option>
                    </select>
                  </div>
                  <div class="flex flex-col text-right font-medium">
                    <span id="liveDateMobile" class="text-[9px] text-slate-400"></span>
                    <span id="liveClockMobile" class="font-bold text-emerald-400 text-xs"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (layout === 'modern_top') {
      headerHtml = `
        <div id="navbar-container" class="mx-auto mt-3 mb-2 max-w-[98%] rounded-3xl border border-slate-900/10 backdrop-blur-2xl bg-white/50 shadow-[0_12px_40px_rgba(0,0,0,0.12)] text-slate-900 no-print flex flex-col flex-shrink-0">
          <!-- Top Neon Radium Gradient line -->
          <div class="h-[3px] w-full bg-gradient-to-r from-purple-500 via-indigo-500 to-emerald-500 rounded-t-3xl"></div>
          <!-- Main Header Row (Flex column right, logo left) -->
          <div class="w-full flex items-stretch">
            <!-- Left Logo Pane (Spans Row 1 and Row 2 height) -->
            <div class="flex items-center justify-center p-4 border-r border-slate-900/10 flex-shrink-0 rounded-bl-3xl">
              <img src="${logoUrl}" alt="School Logo" class="h-16 w-16 lg:h-24 lg:w-24 object-contain rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.1)] border border-slate-900/10 bg-white/40 p-1.5 transition-all duration-300 hover:scale-105">
            </div>

            <!-- Right Pane: Row 1 (Title/Controls) & Row 2 (Nav Bar) -->
            <div class="flex-1 flex flex-col justify-between min-w-0">
              <!-- Row 1: Brand (School Title) -->
              <div class="w-full px-5 lg:px-7 py-2.5 flex justify-start items-center border-b border-slate-900/5">
                <!-- Brand Text -->
                <div class="min-w-0">
                  <h1 class="text-sm sm:text-base md:text-lg lg:text-xl xl:text-2xl font-black uppercase tracking-wider bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 bg-clip-text text-transparent school-title-full truncate">Government Higher Primary School, Marched</h1>
                  <p class="text-[9px] md:text-[10px] lg:text-xs text-indigo-900/80 font-bold tracking-wider uppercase school-title-kn truncate mt-0.5">ಸ.ಹಿ.ಪ್ರಾ.ಶಾಲೆ, ಮರ್ಚೆಡ್</p>
                </div>
              </div>

              <!-- Row 2: Status Bar (Controls) -->
              <div class="w-full px-5 lg:px-7 py-2 flex justify-between items-center z-50 gap-4 border-b border-slate-900/5 bg-slate-900/[0.01]">
                <!-- Status/Date info left, other controls right -->
                <div class="flex items-center gap-2 text-xs">
                  <div class="flex items-center gap-3 bg-slate-950/95 border border-slate-800/60 rounded-xl px-2.5 py-1.5 shadow-inner">
                    <span id="liveDate" class="hidden sm:inline text-[10px] text-slate-400 font-bold tracking-wider uppercase"></span>
                    <div class="hidden sm:inline w-px h-3 bg-slate-800"></div>
                    <span id="liveClock" class="font-mono font-black text-emerald-400 text-xs tracking-wider glow-text-emerald"></span>
                  </div>
                </div>

                <!-- Right Controls -->
                <div class="flex items-center gap-2 text-xs flex-shrink-0">
                  <!-- Theme Selector -->
                  <div class="hidden sm:flex items-center gap-2 bg-slate-900/5 border border-slate-900/10 rounded-xl px-2.5 py-1.5 shadow-sm">
                    <span class="text-slate-400 font-bold text-[9px] uppercase tracking-wider"><i class="fa-solid fa-palette text-indigo-500 text-[10px]"></i> Theme:</span>
                    <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-slate-800 border-0 text-xs font-bold focus:outline-none cursor-pointer">
                      <option class="bg-slate-900 text-white" value="light">Light</option>
                      <option class="bg-slate-900 text-white" value="dark">Dark</option>
                      <option class="bg-slate-900 text-white" value="gray">Gray</option>
                      <option class="bg-slate-900 text-white" value="blue">Blue</option>
                      <option class="bg-slate-900 text-white" value="green">Green</option>
                    </select>
                  </div>

                  <!-- User Badge Capsule -->
                  <div class="flex items-center gap-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-full px-3 py-1.5 shadow-inner">
                    <i class="fa-solid fa-user-circle text-indigo-500 text-xs"></i>
                    <span id="headerUser" class="font-bold text-slate-850 text-xs truncate max-w-[80px] sm:max-w-[120px]">User</span>
                  </div>

                  <!-- Logout Button -->
                  <button onclick="handleLogout()" class="bg-red-500/10 hover:bg-red-650 border border-red-500/30 hover:border-red-600 text-red-600 hover:text-white px-3 py-1.5 rounded-full text-xs font-bold transition duration-300 cursor-pointer flex items-center gap-1 shadow-sm glow-shadow-red-hover">
                    <i class="fa-solid fa-right-from-bracket text-xs"></i> <span class="hidden sm:inline">Logout</span>
                  </button>

                  <!-- Hamburger menu button -->
                  <button id="mobileMenuBtn" class="flex lg:hidden items-center justify-center p-2 text-slate-600 hover:text-black hover:bg-slate-900/5 rounded-lg focus:outline-none cursor-pointer">
                    <i class="fa-solid fa-bars text-sm"></i>
                  </button>
                </div>
              </div>

              <!-- Row 2: Sticky Center Navigation -->
              <nav class="hidden lg:flex w-full bg-slate-900/[0.02] text-slate-900 px-6 py-2 justify-center items-center gap-2 gap-y-2.5 z-40 flex-wrap rounded-br-3xl" id="desktopNav">
                <!-- Desktop menu items will be injected here -->
              </nav>
            </div>
          </div>

          <!-- Mobile Menu Drawer (screens < 1024px) -->
          <div id="mobileMenuPanel" class="hidden lg:hidden w-full bg-white border-t border-slate-250 max-h-[75vh] overflow-y-auto mobile-menu-drawer transition-all duration-300 z-35 rounded-b-3xl shadow-lg">
            <div class="px-4 py-3 space-y-1.5 text-sm font-semibold" id="mobileNav">
              <!-- Mobile navigation menu items will be injected here -->
              <div class="flex items-center justify-between pt-4 border-t border-slate-200 mt-3 sm:hidden">
                <div class="flex items-center gap-1 bg-slate-900/5 px-2 py-0.5 rounded-xl border border-slate-900/10">
                  <span class="text-slate-500 text-[9px] font-bold uppercase"><i class="fa-solid fa-palette text-indigo-500 mr-1"></i>Theme:</span>
                  <select id="themeSelectorMobile" onchange="changeTheme(this.value)" class="bg-transparent text-slate-800 border-0 text-xs focus:outline-none">
                    <option class="bg-slate-900 text-white" value="light">Light</option>
                    <option class="bg-slate-900 text-white" value="dark">Dark</option>
                    <option class="bg-slate-900 text-white" value="gray">Gray</option>
                    <option class="bg-slate-900 text-white" value="blue">Blue</option>
                    <option class="bg-slate-900 text-white" value="green">Green</option>
                  </select>
                </div>
                <div class="flex flex-col text-right font-medium">
                  <span id="liveDateMobile" class="text-[9px] text-slate-500"></span>
                  <span id="liveClockMobile" class="font-bold text-emerald-600 text-xs"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      // default_top
      headerHtml = `
        <div id="navbar-container" class="mx-auto mt-3 mb-2 max-w-[98%] rounded-3xl border border-slate-900/10 backdrop-blur-2xl bg-white/50 shadow-[0_12px_40px_rgba(0,0,0,0.12)] text-slate-900 no-print flex flex-col flex-shrink-0">
          <!-- Top Neon Radium Gradient line -->
          <div class="h-[3px] w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-t-3xl"></div>
          <!-- Main Header Row (Flex column right, logo left) -->
          <div class="w-full flex items-stretch">
            <!-- Left Logo Pane (Spans Row 1 and Row 2 height) -->
            <div class="flex items-center justify-center p-4 border-r border-slate-900/10 flex-shrink-0 rounded-bl-3xl">
              <img src="${logoUrl}" alt="School Logo" class="h-16 w-16 md:h-24 md:w-24 object-contain rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.1)] border border-slate-900/10 bg-white/40 p-1.5 transition-all duration-300 hover:scale-105">
            </div>

            <!-- Right Pane: Row 1 (Title/Controls) & Row 2 (Nav Bar) -->
            <div class="flex-1 flex flex-col justify-between min-w-0">
              <!-- Row 1: Brand (School Title) -->
              <div class="w-full px-5 md:px-7 py-2.5 flex justify-start items-center border-b border-slate-900/5">
                <!-- Brand Text -->
                <div class="min-w-0">
                  <h1 class="text-sm sm:text-base md:text-lg lg:text-xl xl:text-2xl font-black uppercase tracking-wider bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 bg-clip-text text-transparent school-title-full truncate">Government Higher Primary School, Marched</h1>
                  <p class="text-[9px] md:text-[10px] lg:text-xs text-indigo-900/80 font-bold tracking-widest uppercase school-title-kn truncate mt-0.5">ಸ.ಹಿ.ಪ್ರಾ.ಶಾಲೆ, ಮರ್ಚೆಡ್</p>
                </div>
              </div>

              <!-- Row 2: Status Bar (Controls) -->
              <div class="w-full px-5 md:px-7 py-2 flex justify-between items-center z-50 gap-4 border-b border-slate-900/5 bg-slate-900/[0.01]">
                <!-- Clock / Date Left -->
                <div class="flex items-center gap-2 text-xs">
                  <div class="flex items-center gap-3 bg-slate-950/95 border border-slate-800/60 rounded-2xl px-3 py-1.5 shadow-inner">
                    <span id="liveDate" class="hidden sm:inline text-[10px] text-slate-400 font-bold tracking-wider uppercase"></span>
                    <div class="hidden sm:inline w-px h-3 bg-slate-800"></div>
                    <span id="liveClock" class="font-mono font-black text-emerald-400 text-xs tracking-wider glow-text-emerald"></span>
                  </div>
                </div>

                <!-- Controls Right -->
                <div class="flex items-center gap-2 md:gap-4 text-xs flex-shrink-0">
                  <!-- Theme Selector -->
                  <div class="hidden sm:flex items-center gap-2 bg-slate-900/5 border border-slate-900/10 rounded-2xl px-3 py-1.5 shadow-sm transition-all duration-300">
                    <span class="text-slate-400 font-bold text-[10px] uppercase tracking-wider"><i class="fa-solid fa-palette text-indigo-500 text-[10px]"></i> Theme:</span>
                    <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-slate-800 border-0 rounded text-xs font-bold focus:outline-none cursor-pointer">
                      <option class="bg-slate-900 text-white" value="light">Light</option>
                      <option class="bg-slate-900 text-white" value="dark">Dark</option>
                      <option class="bg-slate-900 text-white" value="gray">Gray</option>
                      <option class="bg-slate-900 text-white" value="blue">Blue</option>
                      <option class="bg-slate-900 text-white" value="green">Green</option>
                    </select>
                  </div>
                  
                  <!-- User Badge -->
                  <div class="flex items-center gap-2 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 hover:border-indigo-500/40 rounded-full px-3.5 py-1.5 shadow-inner transition-all duration-300 group">
                    <i class="fa-solid fa-user-circle text-xs text-indigo-500 group-hover:scale-105 transition-transform"></i>
                    <span id="headerUser" class="font-bold text-slate-850 text-xs truncate max-w-[90px] md:max-w-[140px]">User</span>
                  </div>

                  <!-- Logout Button -->
                  <button onclick="handleLogout()" class="bg-red-500/10 hover:bg-red-650 border border-red-500/30 hover:border-red-600 text-red-600 hover:text-white px-3.5 py-1.5 rounded-full text-xs font-bold transition-all duration-300 cursor-pointer flex items-center gap-1.5 shadow-sm hover:scale-[1.02] active:scale-[0.98] glow-shadow-red-hover">
                    <i class="fa-solid fa-right-from-bracket text-xs"></i> <span class="hidden sm:inline">Logout</span>
                  </button>

                  <!-- Hamburger menu button -->
                  <button id="mobileMenuBtn" class="flex md:hidden items-center justify-center p-2 text-slate-600 hover:text-black hover:bg-slate-900/5 rounded-lg focus:outline-none cursor-pointer">
                    <i class="fa-solid fa-bars text-sm"></i>
                  </button>
                </div>
              </div>

              <!-- Row 2: Sticky Desktop Menu -->
              <nav class="hidden md:flex w-full bg-slate-900/[0.02] text-slate-900 px-6 py-2 justify-start items-center gap-2 gap-y-2.5 z-40 flex-wrap rounded-br-3xl" id="desktopNav">
                <!-- Navigation menu items will be injected here -->
              </nav>
            </div>
          </div>

          <!-- Mobile Menu Panel -->
          <div id="mobileMenuPanel" class="hidden md:hidden w-full bg-white border-t border-slate-250 max-h-[75vh] overflow-y-auto mobile-menu-drawer transition-all duration-300 z-30 rounded-b-3xl shadow-lg">
            <div class="px-4 py-3 space-y-1.5 text-sm font-semibold" id="mobileNav">
              <!-- Mobile navigation menu items will be injected here -->
              <div class="flex items-center gap-2 pt-4 border-t border-slate-200 mt-3 sm:hidden justify-between">
                <div class="flex items-center gap-1 bg-slate-900/5 px-2.5 py-1 rounded-xl border border-slate-900/10">
                  <span class="text-slate-500 text-[10px] font-bold uppercase"><i class="fa-solid fa-palette text-indigo-500 mr-1"></i>Theme:</span>
                  <select id="themeSelectorMobile" onchange="changeTheme(this.value)" class="bg-transparent text-slate-800 border-0 text-xs focus:outline-none">
                    <option class="bg-slate-900 text-white" value="light">Light</option>
                    <option class="bg-slate-900 text-white" value="dark">Dark</option>
                    <option class="bg-slate-900 text-white" value="gray">Gray</option>
                    <option class="bg-slate-900 text-white" value="blue">Blue</option>
                    <option class="bg-slate-900 text-white" value="green">Green</option>
                  </select>
                </div>
                <div class="flex flex-col text-right font-medium">
                  <span id="liveDateMobile" class="text-[10px] text-slate-500"></span>
                  <span id="liveClockMobile" class="font-bold text-emerald-600 text-xs"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    placeholder.innerHTML = headerHtml;

    const desktopNav = document.getElementById('desktopNav');
    const mobileNav = document.getElementById('mobileNav');

    let menuHtmlDesktop = '';
    let menuHtmlMobile = '';

    // Filter menuData based on feature permissions for regular teachers
    const cachedPerms = localStorage.getItem('school_permissions');
    let permissions = {};
    if (cachedPerms) {
      try {
        permissions = JSON.parse(cachedPerms);
      } catch (e) {
        // ignore
      }
    }
    const userRole = localStorage.getItem('user_role') || 'Teacher';

    const pagePermissionMap = {
      'NewAdmission.html': 'new_admission',
      'NewAdmissionList.html': 'admission_list',
      'StudentList.html': 'student_list',
      'StudentUpdate.html': 'student_update',
      'ApaarModule.html': 'aadhar_update',
      'BridgeCourse.html': 'bridge_course',
      'CceAssessmet.html': 'cce_assessment',
      'LbaAssessment.html': 'lba_assessment',
      'FlnAssessment.html': 'fln_assessment',
      'custom_reports.html': 'custom_reports',
      'incentives.html': 'incentives',
      'teachers.html': 'teachers_directory'
    };

    const activeMenuData = menuData.map(item => {
      // Hide Admin Panel for non-admin/non-developer users
      if (item.href === "admin.html" && userRole !== 'Admin' && userRole !== 'developer') {
        return null;
      }

      // check direct item permission
      const itemKey = pagePermissionMap[item.href];
      if (itemKey && userRole !== 'Admin' && userRole !== 'developer') {
        const isAllowed = permissions[itemKey] === true;
        if (!isAllowed) return null;
      }

      if (item.items) {
        let filteredItems = item.items.filter(sub => {
          const subKey = pagePermissionMap[sub.href];
          if (subKey && userRole !== 'Admin' && userRole !== 'developer') {
            return permissions[subKey] === true; // strictly true, defaults to false!
          }
          return true;
        });
        if (filteredItems.length === 0) return null;
        return { ...item, items: filteredItems };
      }
      return item;
    }).filter(Boolean);

    activeMenuData.forEach(item => {
      const active = isLinkActive(item);
      let activeClassDesktop = '';
      if (layout === 'side') {
        activeClassDesktop = active 
          ? 'bg-gradient-to-r from-indigo-500/15 to-purple-500/15 border-l-4 border-indigo-500 text-indigo-400 font-bold shadow-inner' 
          : 'text-slate-350 hover:bg-white/5 hover:text-white border-l-4 border-transparent';
      } else {
        activeClassDesktop = active 
          ? 'active-nav-tab border border-indigo-500/30' 
          : 'text-slate-800 hover:bg-black/5 hover:text-black border border-transparent';
      }
      
      const activeClassMobile = active 
        ? (layout === 'side' 
            ? 'bg-indigo-950/40 text-indigo-400 border-l-4 border-indigo-500 font-bold shadow-inner' 
            : 'bg-indigo-50 text-indigo-600 border-l-4 border-indigo-500 font-bold') 
        : (layout === 'side' 
            ? 'text-slate-300 hover:bg-slate-850 hover:text-white border-l-4 border-transparent' 
            : 'text-slate-800 hover:bg-slate-50 hover:text-black border-l-4 border-transparent');

      if (item.items) {
        if (layout === 'side') {
          // Accordion for sidebar
          const sidebarCollapseId = `sidebar-collapse-${item.name.replace(/\s+/g, '')}`;
          const isCollapsed = !active;
          
          menuHtmlDesktop += `
            <div class="w-full">
              <button onclick="toggleSidebarAccordion('${sidebarCollapseId}')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all duration-200 focus:outline-none ${activeClassDesktop}">
                <span class="flex items-center gap-2">
                  <i class="fa-solid ${item.icon} ${item.color} text-xs"></i>
                  <span>${item.name}</span>
                </span>
                <i id="${sidebarCollapseId}-arrow" class="fa-solid fa-chevron-right text-[9px] opacity-70 transition-transform duration-200 ${!isCollapsed ? 'rotate-90' : ''}"></i>
              </button>
              <div id="${sidebarCollapseId}" class="${isCollapsed ? 'hidden' : ''} pl-6 pr-2 py-1 space-y-0.5 mt-1 border-l border-slate-800 ml-5">
                ${item.items.map(sub => {
                  const subActive = sub.href === currentPath;
                  return `
                    <a href="${sub.href}" ${sub.external ? 'target="_blank"' : ''} class="block py-2 px-2.5 text-xs font-bold rounded-lg transition-all duration-200 ${
                      subActive 
                        ? 'text-indigo-400 bg-indigo-950/30 shadow-inner' 
                        : 'text-slate-400 hover:text-white hover:bg-slate-900/50'
                    }">
                      ${sub.name}
                      ${sub.external ? '<i class="fa-solid fa-arrow-up-right-from-square text-[8px] opacity-50 ml-1"></i>' : ''}
                    </a>
                  `;
                }).join('')}
              </div>
            </div>
          `;
        } else {
          // Dropdown for horizontal nav
          menuHtmlDesktop += `
            <div class="nav-dropdown-item group relative">
              <button class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold ${activeClassDesktop} transition focus:outline-none cursor-pointer">
                <i class="fa-solid ${item.icon} ${item.color} text-xs"></i>
                <span>${item.name}</span>
                <i class="fa-solid fa-chevron-down text-[9px] opacity-70 ml-0.5 group-hover:rotate-180 transition-transform duration-200"></i>
              </button>
              <div class="nav-dropdown-list absolute left-0 mt-1 w-56 rounded-2xl bg-white border border-slate-200 text-slate-900 shadow-xl backdrop-blur-2xl py-2 z-50">
                ${item.items.map(sub => `
                  <a href="${sub.href}" ${sub.external ? 'target="_blank"' : ''} class="flex items-center justify-between px-4 py-2.5 text-xs font-bold text-slate-800 hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-white hover:shadow-[0_0_15px_rgba(99,102,241,0.2)] transition-all duration-200 rounded-xl mx-1.5">
                    <span>${sub.name}</span>
                    ${sub.external ? '<i class="fa-solid fa-arrow-up-right-from-square text-[9px] opacity-50"></i>' : ''}
                  </a>
                `).join('')}
              </div>
            </div>
          `;
        }

        // Mobile accordion
        const mobileCollapseId = `mobile-collapse-${item.name.replace(/\s+/g, '')}`;
        menuHtmlMobile += `
          <div class="border-b border-slate-900/50">
            <button onclick="toggleMobileAccordion('${mobileCollapseId}')" class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg ${activeClassMobile} transition text-left focus:outline-none">
              <span class="flex items-center gap-2">
                <i class="fa-solid ${item.icon} ${item.color} text-xs"></i>
                <span>${item.name}</span>
              </span>
              <i id="${mobileCollapseId}-arrow" class="fa-solid fa-chevron-right text-[10px] opacity-50 transition-transform duration-200"></i>
            </button>
            <div id="${mobileCollapseId}" class="hidden pl-8 pr-3 py-1 bg-slate-950/20 border-l border-slate-850 space-y-1 mt-1 rounded-lg">
              ${item.items.map(sub => `
                <a href="${sub.href}" ${sub.external ? 'target="_blank"' : ''} class="block py-2.5 text-xs font-bold text-slate-400 hover:text-white transition">
                  ${sub.name}
                  ${sub.external ? '<i class="fa-solid fa-arrow-up-right-from-square text-[8px] opacity-50 ml-1"></i>' : ''}
                </a>
              `).join('')}
            </div>
          </div>
        `;
      } else {
        // Direct link (Desktop)
        menuHtmlDesktop += `
          <a href="${item.href}" class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold ${activeClassDesktop} transition">
            <i class="fa-solid ${item.icon} ${item.color} text-xs"></i>
            <span>${item.name}</span>
          </a>
        `;

        // Direct link (Mobile)
        menuHtmlMobile += `
          <a href="${item.href}" class="flex items-center gap-2 px-3 py-2.5 rounded-lg ${activeClassMobile} transition">
            <i class="fa-solid ${item.icon} ${item.color} text-xs"></i>
            <span>${item.name}</span>
          </a>
        `;
      }
    });

    if (desktopNav) desktopNav.innerHTML = menuHtmlDesktop;
    if (mobileNav) mobileNav.innerHTML = menuHtmlMobile;

    // Mobile Hamburger
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenuPanel = document.getElementById('mobileMenuPanel');
    if (mobileMenuBtn && mobileMenuPanel) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileMenuPanel.classList.toggle('hidden');
        const icon = mobileMenuBtn.querySelector('i');
        if (mobileMenuPanel.classList.contains('hidden')) {
          icon.className = 'fa-solid fa-bars text-lg';
        } else {
          icon.className = 'fa-solid fa-xmark text-lg';
        }
      });
    }

    // Sync theme
    const savedTheme = localStorage.getItem('portal_theme') || 'light';
    const sel = document.getElementById('themeSelector');
    const selMobile = document.getElementById('themeSelectorMobile');
    if (sel) sel.value = savedTheme;
    if (selMobile) selMobile.value = savedTheme;
    document.body.setAttribute('data-theme', savedTheme);

    initSessionAndUser();
  }

  async function initSessionAndUser() {
    let client = window.supabaseClient;
    if (!client && window.supabase) {
      client = window.supabase.createClient("https://gsayvnnnfrrkwdfwocbu.supabase.co", "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS");
    }
    if (!client) return;

    try {
      const { data: { session } } = await client.auth.getSession();
      if (session) {
        const user = session.user;
        const name = user.user_metadata?.name || user.email || 'User';
        
        const headerUser = document.getElementById('headerUser');
        if (headerUser) headerUser.innerText = name;

        const { data: profile } = await client
          .from('profiles')
          .select('name, role, school_id')
          .eq('id', user.id)
          .maybeSingle();

        if (profile && profile.school_id) {
          localStorage.setItem('school_id', profile.school_id);
        }
        const cachedRole = localStorage.getItem('user_role');
        if (profile && profile.role) {
          if (profile.role !== cachedRole) {
            localStorage.setItem('user_role', profile.role);
            renderNavbar();
            return;
          }
        }

        const displayName = profile?.name || name;
        if (headerUser) {
          if (profile && profile.role === 'developer') {
            headerUser.innerHTML = `<span class="bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 px-1.5 py-0.5 rounded text-[9px] font-bold mr-1.5 uppercase">Dev</span>${displayName}`;
            injectDeveloperLink();
          } else if (profile && profile.role === 'Admin') {
            headerUser.innerHTML = `<span class="bg-rose-600/30 text-rose-400 border border-rose-500/30 px-1.5 py-0.5 rounded text-[9px] font-bold mr-1.5 uppercase">HM</span>${displayName}`;
          } else {
            headerUser.innerText = displayName;
          }
        }

        let schoolNameEn = localStorage.getItem('school_name_en');
        let schoolNameKn = localStorage.getItem('school_name_kn');

        if (profile && profile.school_id && (!schoolNameEn || !schoolNameKn)) {
          try {
            const { data: school } = await client
              .from('schools')
              .select('school_name_en, school_name_kn')
              .eq('id', profile.school_id)
              .maybeSingle();
            if (school) {
              if (school.school_name_en) {
                schoolNameEn = school.school_name_en;
                localStorage.setItem('school_name_en', schoolNameEn);
              }
              if (school.school_name_kn) {
                schoolNameKn = school.school_name_kn;
                localStorage.setItem('school_name_kn', schoolNameKn);
              }
            }
          } catch (err) {
            console.error("Error fetching school details in navbar:", err);
          }
        }

        if (schoolNameEn) {
          const shortName = getShortSchoolName(schoolNameEn);
          
          const shortTitles = document.querySelectorAll('.school-title-short');
          shortTitles.forEach(el => { 
            el.innerText = shortName; 
          });
          
          const fullTitles = document.querySelectorAll('.school-title-full');
          fullTitles.forEach(el => { 
            el.innerText = schoolNameEn; 
          });
        }

        if (schoolNameKn) {
          const titlesKn = document.querySelectorAll('.school-title-kn');
          titlesKn.forEach(el => { 
            el.innerText = schoolNameKn; 
          });
        }

        // Fetch db config to check layout consistency
        if (profile && profile.school_id) {
          const { data: configData } = await client
            .from('school_settings')
            .select('settings_value')
            .eq('school_id', profile.school_id)
            .eq('settings_key', 'web_design')
            .maybeSingle();

          if (configData && configData.settings_value) {
            const dbLayout = configData.settings_value.nav_layout || 'default_top';
            const cachedLayout = localStorage.getItem('school_nav_layout') || 'default_top';
            const dbLogo = configData.settings_value.logo_url || '';
            const cachedLogo = localStorage.getItem('school_logo_url') || '';
            if (dbLayout !== cachedLayout || dbLogo !== cachedLogo) {
              localStorage.setItem('school_nav_layout', dbLayout);
              localStorage.setItem('school_logo_url', dbLogo);
              renderNavbar();
              return;
            }
          }

          // Fetch feature permissions to check consistency
          const { data: permData } = await client
            .from('school_settings')
            .select('settings_value')
            .eq('school_id', profile.school_id)
            .eq('settings_key', 'feature_permissions')
            .maybeSingle();

          if (permData && permData.settings_value) {
            const dbPerms = JSON.stringify(permData.settings_value);
            const cachedPerms = localStorage.getItem('school_permissions');
            if (dbPerms !== cachedPerms) {
              localStorage.setItem('school_permissions', dbPerms);
              renderNavbar();
              return;
            }
          } else {
            // Default to empty permissions (all disabled) if database has no record
            const defaultPerms = {};
            const pageKeys = ['new_admission', 'admission_list', 'student_list', 'student_update', 'aadhar_update', 'bridge_course', 'cce_assessment', 'lba_assessment', 'fln_assessment', 'custom_reports', 'incentives', 'teachers_directory'];
            pageKeys.forEach(k => { defaultPerms[k] = false; });
            const dbPerms = JSON.stringify(defaultPerms);
            const cachedPerms = localStorage.getItem('school_permissions');
            if (dbPerms !== cachedPerms) {
              localStorage.setItem('school_permissions', dbPerms);
              renderNavbar();
              return;
            }
          }

          // Centralized Route Guard
          if (profile.role !== 'Admin' && profile.role !== 'developer') {
            const cachedPerms = localStorage.getItem('school_permissions');
            let permissions = {};
            if (cachedPerms) {
              try {
                permissions = JSON.parse(cachedPerms);
              } catch (e) {
                // ignore
              }
            }
            const pagePermissionMap = {
              'NewAdmission.html': 'new_admission',
              'NewAdmissionList.html': 'admission_list',
              'StudentList.html': 'student_list',
              'StudentUpdate.html': 'student_update',
              'ApaarModule.html': 'aadhar_update',
              'BridgeCourse.html': 'bridge_course',
              'CceAssessmet.html': 'cce_assessment',
              'LbaAssessment.html': 'lba_assessment',
              'FlnAssessment.html': 'fln_assessment',
              'custom_reports.html': 'custom_reports',
              'incentives.html': 'incentives',
              'teachers.html': 'teachers_directory'
            };
            const permKey = pagePermissionMap[currentPath];
            if (permKey) {
              const isAllowed = permissions[permKey] === true; // strictly true, defaults to false!
              if (!isAllowed) {
                alert("ಅನಧಿಕೃತ ಪ್ರವೇಶ! ಮುಖ್ಯೋಪಾಧ್ಯಾಯರು ಈ ಪುಟದ ಪ್ರವೇಶವನ್ನು ನಿಷ್ಕ್ರಿಯಗೊಳಿಸಿದ್ದಾರೆ.\nUnauthorized! Access to this page is disabled by the Headmaster.");
                window.location.href = "dashboard.html";
                return;
              }
            }
          }
        }
      }
    } catch (err) {
      console.error("Navbar failed to fetch user profile:", err);
    }
  }

  function injectDeveloperLink() {
    const desktopNav = document.getElementById('desktopNav');
    const mobileNav = document.getElementById('mobileNav');
    const isActive = (currentPath === 'developer.html');
    const isSide = (localStorage.getItem('school_nav_layout') === 'side');

    if (desktopNav && !document.getElementById('nav-DeveloperConsole')) {
      const devLink = document.createElement('a');
      devLink.href = "developer.html";
      devLink.id = "nav-DeveloperConsole";
      
      devLink.className = `flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition ${
        isSide 
          ? (isActive ? 'bg-gradient-to-r from-purple-500/15 to-indigo-500/15 border-l-4 border-purple-500 text-purple-400 font-bold shadow-inner' : 'text-purple-400 hover:bg-white/5 hover:text-purple-300 border-l-4 border-transparent')
          : (isActive ? 'active-nav-tab border border-purple-500/30 text-purple-600 font-extrabold shadow-[0_0_10px_rgba(168,85,247,0.15)]' : 'text-purple-600 hover:bg-purple-50 hover:text-purple-800 border border-transparent')
      }`;
      devLink.innerHTML = `<i class="fa-solid fa-screwdriver-wrench text-purple-600 text-sm"></i> <span>Developer Console</span>`;
      desktopNav.insertBefore(devLink, desktopNav.firstChild);
    }

    if (mobileNav && !document.getElementById('nav-DeveloperConsoleMobile')) {
      const devLinkMobile = document.createElement('a');
      devLinkMobile.href = "developer.html";
      devLinkMobile.id = "nav-DeveloperConsoleMobile";
      devLinkMobile.className = `flex items-center gap-2 px-3 py-2.5 rounded-lg border-l-4 transition ${
        isActive 
          ? (isSide ? 'bg-purple-950/40 text-purple-400 border-purple-500 font-bold' : 'bg-purple-50 text-purple-600 border-purple-500 font-bold') 
          : (isSide ? 'text-purple-400 hover:bg-slate-850 hover:text-purple-300 border-transparent' : 'text-purple-600 hover:bg-purple-50 hover:text-purple-800 border-transparent')
      }`;
      devLinkMobile.innerHTML = `<i class="fa-solid fa-screwdriver-wrench ${isSide ? 'text-purple-400' : 'text-purple-600'} text-sm"></i> <span>Developer Console</span>`;
      mobileNav.insertBefore(devLinkMobile, mobileNav.firstChild);
    }
  }

  // injectAdminLink removed since Admin Panel is now a first-class member of menuData

  function startNavbarClock() {
    function update() {
      const now = new Date();
      let h = now.getHours(), m = now.getMinutes(), s = now.getSeconds();
      const ampm = h >= 12 ? 'PM' : 'AM';
      h = h % 12; h = h ? h : 12;
      m = m < 10 ? '0'+m : m; s = s < 10 ? '0'+s : s;

      const clockStr = h + ':' + m + ':' + s + ' ' + ampm;
      const dateStr = now.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' });

      const desktopClock = document.getElementById('liveClock');
      const desktopDate = document.getElementById('liveDate');
      if (desktopClock) desktopClock.innerText = clockStr;
      if (desktopDate) desktopDate.innerText = dateStr;

      const mobileClock = document.getElementById('liveClockMobile');
      const mobileDate = document.getElementById('liveDateMobile');
      if (mobileClock) mobileClock.innerText = clockStr;
      if (mobileDate) mobileDate.innerText = dateStr;
    }
    setInterval(update, 1000);
    update();
  }

  window.changeTheme = function(themeName) {
    document.body.setAttribute('data-theme', themeName);
    localStorage.setItem('portal_theme', themeName);
    
    const sel = document.getElementById('themeSelector');
    const selMobile = document.getElementById('themeSelectorMobile');
    if (sel) sel.value = themeName;
    if (selMobile) selMobile.value = themeName;
  };

  window.handleLogout = async function() {
    let client = window.supabaseClient;
    if (!client && window.supabase) {
      client = window.supabase.createClient("https://gsayvnnnfrrkwdfwocbu.supabase.co", "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS");
    }
    if (client) {
      await client.auth.signOut();
    }
    localStorage.removeItem('school_id');
    localStorage.removeItem('user_role');
    localStorage.removeItem('school_name_en');
    localStorage.removeItem('school_name_kn');
    localStorage.removeItem('school_udise');
    window.location.href = "index.html";
  };

  window.toggleMobileAccordion = function(collapseId) {
    const el = document.getElementById(collapseId);
    const arrow = document.getElementById(collapseId + '-arrow');
    if (el) {
      const isHidden = el.classList.contains('hidden');
      if (isHidden) {
        el.classList.remove('hidden');
        if (arrow) arrow.classList.add('rotate-90');
      } else {
        el.classList.add('hidden');
        if (arrow) arrow.classList.remove('rotate-90');
      }
    }
  };

  window.toggleSidebarAccordion = function(collapseId) {
    const el = document.getElementById(collapseId);
    const arrow = document.getElementById(collapseId + '-arrow');
    if (el) {
      const isHidden = el.classList.contains('hidden');
      if (isHidden) {
        el.classList.remove('hidden');
        if (arrow) arrow.classList.add('rotate-90');
      } else {
        el.classList.add('hidden');
        if (arrow) arrow.classList.remove('rotate-90');
      }
    }
  };

  window.applyNavLayout = function(layout, logoUrl) {
    if (layout) localStorage.setItem('school_nav_layout', layout);
    if (logoUrl !== undefined) localStorage.setItem('school_logo_url', logoUrl);
    renderNavbar();
  };

  // Run on Document Load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      renderNavbar();
      startNavbarClock();
    });
  } else {
    renderNavbar();
    startNavbarClock();
  }
})();
