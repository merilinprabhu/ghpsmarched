import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('FlnAssessment.html', 'r', encoding='utf-8') as f:
    fln_code = f.read()

# Add view switcher in toolbar (lines 508-520)
tb_old = """            <!-- Toolbar buttons -->
            <div class="flex items-center gap-2 mt-auto sm:ml-auto">"""

tb_new = """            <!-- Toolbar buttons -->
            <div class="flex items-center gap-2 mt-auto sm:ml-auto flex-wrap">
              <!-- View Mode Switcher -->
              <div class="flex items-center gap-1 p-1 bg-slate-200/70 dark:bg-slate-800 rounded-xl">
                <button type="button" id="btn-fln-view-cards" onclick="setFlnViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
                  <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
                </button>
                <button type="button" id="btn-fln-view-table" onclick="setFlnViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
                  <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
                </button>
              </div>"""

fln_code = fln_code.replace(tb_old, tb_new, 1)

# Add search/filter bar and cards container inside Table Container (lines 568-580)
cont_old = """          <!-- Table Container -->
          <div class="border-t pt-4 border-slate-100 overflow-hidden">
            <div id="empty-state" class="p-16 text-center flex flex-col items-center justify-center">"""

cont_new = """          <!-- Table Container -->
          <div class="border-t pt-4 border-slate-100 overflow-hidden space-y-4">
            <!-- Search & Quick Filter Bar -->
            <div id="fln-search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hidden no-print">
              <div class="relative flex-1">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                <input type="text" id="fln-search-input" oninput="applyFlnFiltersAndRender()" placeholder="ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರು / STS ಸಂಖ್ಯೆ ಹುಡುಕಿ..." class="w-full pl-8 pr-3 py-2 text-xs bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 dark:text-slate-100 placeholder-slate-400">
              </div>
              <div class="flex items-center gap-1.5 self-end sm:self-auto">
                <button type="button" onclick="setFlnGenderFilter('')" id="fln-gen-all" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer">ಎಲ್ಲಾ</button>
                <button type="button" onclick="setFlnGenderFilter('Boy')" id="fln-gen-boy" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👦 ಬಾಲಕರು</button>
                <button type="button" onclick="setFlnGenderFilter('Girl')" id="fln-gen-girl" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👧 ಬಾಲಕಿಯರು</button>
              </div>
            </div>

            <!-- Mobile Cards View for FLN Assessment -->
            <div id="fln-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

            <div id="empty-state" class="p-16 text-center flex flex-col items-center justify-center">"""

fln_code = fln_code.replace(cont_old, cont_new, 1)

# Add JS state variables
js_state_old = "    let gridData = {}; // keyed by studentId: { colKey: grade }"
js_state_new = """    let gridData = {}; // keyed by studentId: { colKey: grade }
    let currentFlnViewMode = localStorage.getItem('fln_view_mode') || 'cards';
    let flnGenderFilter = '';
    let flnSearchQuery = '';"""

fln_code = fln_code.replace(js_state_old, js_state_new, 1)

with open('FlnAssessment.html', 'w', encoding='utf-8') as f:
    f.write(fln_code)

print("Updated FlnAssessment.html markup for Cards View")
