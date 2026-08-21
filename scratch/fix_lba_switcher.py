import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('LbaAssessment.html', 'r', encoding='utf-8') as f:
    lba_code = f.read()

# Add view switcher into action toolbar
tb_old = """              <!-- Settings -->
              <button onclick="toggleSettingsPanel()" title="ಪಾಠಗಳ ಸೆಟ್ಟಿಂಗ್ಸ್ / Lesson Settings" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer">"""

tb_new = """              <!-- View Mode Switcher -->
              <div class="flex items-center gap-1 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl">
                <button type="button" id="btn-lba-cards" onclick="setViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
                  <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
                </button>
                <button type="button" id="btn-lba-table" onclick="setViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
                  <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
                </button>
              </div>

              <!-- Settings -->
              <button onclick="toggleSettingsPanel()" title="ಪಾಠಗಳ ಸೆಟ್ಟಿಂಗ್ಸ್ / Lesson Settings" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer">"""

lba_code = lba_code.replace(tb_old, tb_new, 1)

# Ensure setViewMode updates button classes correctly
svm_old = """    function setViewMode(mode, triggerRender = true) {
      currentViewMode = mode || 'cards';
      localStorage.setItem('lba_view_mode', currentViewMode);

      const btnCards = document.getElementById('btn-view-cards');
      const btnTable = document.getElementById('btn-view-table');"""

svm_new = """    function setViewMode(mode, triggerRender = true) {
      currentViewMode = mode || 'cards';
      localStorage.setItem('lba_view_mode', currentViewMode);

      const btnCards = document.getElementById('btn-lba-cards') || document.getElementById('btn-view-cards');
      const btnTable = document.getElementById('btn-lba-table') || document.getElementById('btn-view-table');"""

lba_code = lba_code.replace(svm_old, svm_new, 1)

with open('LbaAssessment.html', 'w', encoding='utf-8') as f:
    f.write(lba_code)

print("Added View Switcher to LbaAssessment.html")
