import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    cce_code = f.read()

# 1. Add search and filter bar and student-cards-container above table-container
stats_bar_old = """            <!-- Separate Grade Cards (Total, A+, A, B+, B, C+/Others) -->
            <div id="stats-bar" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 no-print hidden">"""

search_and_cards_new = """            <!-- Search & Quick Gender Filter Bar -->
            <div id="search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl no-print hidden">
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

            <!-- Mobile Cards Container for CCE -->
            <div id="student-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

            <!-- Separate Grade Cards (Total, A+, A, B+, B, C+/Others) -->
            <div id="stats-bar" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 no-print hidden">"""

cce_code = cce_code.replace(stats_bar_old, search_and_cards_new, 1)

# In renderActiveView: ensure #competency-table and #table-container visibility are properly managed
cce_code = cce_code.replace(
    """    function renderActiveView() {
      const tableEl = document.getElementById('table-container');
      const cardsEl = document.getElementById('student-cards-container');

      if (currentViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderGrid();
        }
      }
      updateTotals();
    }""",
    """    function renderActiveView() {
      const tableEl = document.getElementById('table-container');
      const cardsEl = document.getElementById('student-cards-container');
      const tableTag = document.getElementById('competency-table');
      const sfBar = document.getElementById('search-filter-bar');

      if (sfBar) sfBar.classList.remove('hidden');

      if (currentViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          if (tableTag) tableTag.classList.remove('hidden');
          renderGrid();
        }
      }
      updateTotals();
    }"""
)

with open('CceAssessmet.html', 'w', encoding='utf-8') as f:
    f.write(cce_code)

print("Fixed CceAssessmet.html DOM elements and table visibility")
