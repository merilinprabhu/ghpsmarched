import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    cce_html = f.read()

# 1. Add view mode switch into toolbar
toolbar_target = """                  <!-- Action Buttons shifted directly aside of DDs -->
                  <div class="flex items-center gap-1.5 flex-wrap">"""

toolbar_replacement = """                  <!-- View Mode Switcher -->
                  <div class="flex items-center gap-1 p-1 bg-slate-200/70 dark:bg-slate-800 rounded-xl w-fit">
                    <button type="button" id="btn-view-cards" onclick="setViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
                      <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
                    </button>
                    <button type="button" id="btn-view-table" onclick="setViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
                      <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
                    </button>
                  </div>

                  <!-- Action Buttons shifted directly aside of DDs -->
                  <div class="flex items-center gap-1.5 flex-wrap">"""

cce_html = cce_html.replace(toolbar_target, toolbar_replacement, 1)

# 2. Add Search, Filter Bar and Cards Container inside #page-enter-marks
table_container_old = """            <div class="flex-grow overflow-auto custom-scrollbar relative p-4 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 min-h-[350px]" id="table-container">"""

table_container_new = """            <!-- Search & Quick Filter Bar -->
            <div id="search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hidden no-print">
              <div class="relative flex-1">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                <input type="text" id="search-student-input" oninput="applyFiltersAndRender()" placeholder="ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರು / STS ಸಂಖ್ಯೆ ಹುಡುಕಿ..." class="w-full pl-8 pr-3 py-2 text-xs bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 dark:text-slate-100 placeholder-slate-400">
              </div>
              <div class="flex items-center gap-1.5 self-end sm:self-auto">
                <button type="button" onclick="setGenderFilter('')" id="gen-btn-all" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer">ಎಲ್ಲಾ</button>
                <button type="button" onclick="setGenderFilter('Boy')" id="gen-btn-boy" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👦 ಬಾಲಕರು</button>
                <button type="button" onclick="setGenderFilter('Girl')" id="gen-btn-girl" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👧 ಬಾಲಕಿಯರು</button>
              </div>
            </div>

            <!-- Cards View (Mobile Touch Optimized) -->
            <div id="student-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

            <div class="flex-grow overflow-auto custom-scrollbar relative p-4 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 min-h-[350px]" id="table-container">"""

cce_html = cce_html.replace(table_container_old, table_container_new, 1)

# 3. Add JavaScript State & Card Engine functions
js_state_old = """    let currentSubjects = [];
    let students = [];
    let evaluations = {};
    let isEditing = false;
    let originalEvaluations = {};"""

js_state_new = """    let currentSubjects = [];
    let students = [];
    let evaluations = {};
    let isEditing = false;
    let originalEvaluations = {};
    let currentViewMode = localStorage.getItem('cce_view_mode') || 'cards';
    let genderFilter = '';
    let searchQuery = '';"""

cce_html = cce_html.replace(js_state_old, js_state_new, 1)

with open('CceAssessmet.html', 'w', encoding='utf-8') as f:
    f.write(cce_html)

print("Updated HTML markup and state in CceAssessmet.html")
