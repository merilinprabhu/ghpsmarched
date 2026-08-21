import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('BridgeCourse.html', 'r', encoding='utf-8') as f:
    bc_code = f.read()

# Add view switcher into Roster Actions Header (lines 847-860)
header_old = """              <!-- Roster Actions Header -->
              <div class="flex justify-between items-center flex-wrap gap-2 pb-3 border-b border-slate-200">
                <h3 class="text-xs font-bold text-slate-800 dark:text-slate-100 uppercase flex items-center gap-1.5">
                  <i class="fa-solid fa-list-check text-indigo-650"></i>
                  <span id="grid-title-info">Evaluation Grid</span>
                </h3>
                <div class="flex gap-2">"""

header_new = """              <!-- Roster Actions Header -->
              <div class="flex justify-between items-center flex-wrap gap-2 pb-3 border-b border-slate-200">
                <div class="flex items-center gap-3">
                  <h3 class="text-xs font-bold text-slate-800 dark:text-slate-100 uppercase flex items-center gap-1.5">
                    <i class="fa-solid fa-list-check text-indigo-650"></i>
                    <span id="grid-title-info">Evaluation Grid</span>
                  </h3>
                  <!-- View Mode Switcher -->
                  <div class="flex items-center gap-1 p-1 bg-slate-200/70 dark:bg-slate-800 rounded-xl">
                    <button type="button" id="btn-bc-view-cards" onclick="setBCViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
                      <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
                    </button>
                    <button type="button" id="btn-bc-view-table" onclick="setBCViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
                      <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
                    </button>
                  </div>
                </div>
                <div class="flex gap-2 items-center">"""

bc_code = bc_code.replace(header_old, header_new, 1)

# Add search/filter bar and bc-cards-container inside #grid-container
table_container_old = """              <!-- Competency Table Wrapper -->
              <div class="overflow-x-auto custom-scrollbar border border-slate-200 dark:border-indigo-500/20 rounded-2xl bg-white dark:bg-slate-900 shadow-sm">"""

table_container_new = """              <!-- Search & Quick Filter Bar -->
              <div id="bc-search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl no-print">
                <div class="relative flex-1">
                  <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                  <input type="text" id="bc-search-input" oninput="applyBCFiltersAndRender()" placeholder="ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರು / STS ಸಂಖ್ಯೆ ಹುಡುಕಿ..." class="w-full pl-8 pr-3 py-2 text-xs bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 dark:text-slate-100 placeholder-slate-400">
                </div>
                <div class="flex items-center gap-1.5 self-end sm:self-auto">
                  <button type="button" onclick="setBCGenderFilter('')" id="bc-gen-all" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer">ಎಲ್ಲಾ</button>
                  <button type="button" onclick="setBCGenderFilter('Boy')" id="bc-gen-boy" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👦 ಬಾಲಕರು</button>
                  <button type="button" onclick="setBCGenderFilter('Girl')" id="bc-gen-girl" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👧 ಬಾಲಕಿಯರು</button>
                </div>
              </div>

              <!-- Mobile Cards View for Bridge Course -->
              <div id="bc-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

              <!-- Competency Table Wrapper -->
              <div id="bc-table-wrapper" class="overflow-x-auto custom-scrollbar border border-slate-200 dark:border-indigo-500/20 rounded-2xl bg-white dark:bg-slate-900 shadow-sm">"""

bc_code = bc_code.replace(table_container_old, table_container_new, 1)

# Add JS state variables
js_state_old = "    let evaluations = {};"
js_state_new = """    let evaluations = {};
    let currentBCViewMode = localStorage.getItem('bc_view_mode') || 'cards';
    let bcGenderFilter = '';
    let bcSearchQuery = '';"""

bc_code = bc_code.replace(js_state_old, js_state_new, 1)

with open('BridgeCourse.html', 'w', encoding='utf-8') as f:
    f.write(bc_code)

print("Updated BridgeCourse.html markup for Cards View")
