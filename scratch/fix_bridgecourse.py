import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('BridgeCourse.html', 'r', encoding='utf-8') as f:
    bc_code = f.read()

# 1. In loadRosterGrid, include gender in roster mapping
roster_old = """        const roster = (classStudents[cls] || []).map(s => ({
          id: s.id,
          student_name_kn: s.student_name || '',
          name_english: s.name_english || '',
          father_name_kn: s.father_name_kn || '',
          father_name_az: s.father_name_az || '',
          adminNo: s.app_no
        }));"""

roster_new = """        const roster = (classStudents[cls] || []).map(s => ({
          id: s.id,
          student_name_kn: s.student_name || '',
          name_english: s.name_english || '',
          father_name_kn: s.father_name_kn || '',
          father_name_az: s.father_name_az || '',
          gender: s.gender || '',
          caste: s.caste || '',
          adminNo: s.app_no || s.student_sts || s.id
        }));"""

bc_code = bc_code.replace(roster_old, roster_new, 1)

# 2. When switching to marks tab, if no filters selected, select default Class 1, KANNADA, PRE_TEST and load
switch_tab_old = """    function switchTab(tabName) {
      const isAnalytics = tabName === 'analytics';
      const isMarks = tabName === 'marks';
      const isRef = tabName === 'reference';

      document.getElementById('panel-analytics').classList.toggle('hidden', !isAnalytics);
      document.getElementById('panel-marks').classList.toggle('hidden', !isMarks);
      document.getElementById('panel-reference').classList.toggle('hidden', !isRef);"""

switch_tab_new = """    function switchTab(tabName) {
      const isAnalytics = tabName === 'analytics';
      const isMarks = tabName === 'marks';
      const isRef = tabName === 'reference';

      document.getElementById('panel-analytics').classList.toggle('hidden', !isAnalytics);
      document.getElementById('panel-marks').classList.toggle('hidden', !isMarks);
      document.getElementById('panel-reference').classList.toggle('hidden', !isRef);

      if (isMarks) {
        if (!classFilter.value) classFilter.value = "1";
        if (!subjectFilter.value) subjectFilter.value = "KANNADA";
        if (!testTypeFilter.value) testTypeFilter.value = "PRE_TEST";
        if (classFilter.value && subjectFilter.value && testTypeFilter.value) {
          loadRosterGrid();
        }
      }"""

bc_code = bc_code.replace(switch_tab_old, switch_tab_new, 1)

# 3. Ensure renderActiveBCView handles unhiding competency table properly
render_active_old = """    function renderActiveBCView() {
      const tableEl = document.getElementById('bc-table-wrapper');
      const cardsEl = document.getElementById('bc-cards-container');

      if (currentBCViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderBCCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderRosterGrid();
        }
      }
      updateRowTotalsAndFooter();
    }"""

render_active_new = """    function renderActiveBCView() {
      const tableEl = document.getElementById('bc-table-wrapper');
      const cardsEl = document.getElementById('bc-cards-container');
      const sfBar = document.getElementById('bc-search-filter-bar');

      if (sfBar) sfBar.classList.remove('hidden');

      if (currentBCViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderBCCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderRosterGrid();
        }
      }
      updateRowTotalsAndFooter();
    }"""

bc_code = bc_code.replace(render_active_old, render_active_new, 1)

with open('BridgeCourse.html', 'w', encoding='utf-8') as f:
    f.write(bc_code)

print("Fixed BridgeCourse.html student roster mapping and auto-load on tab switch")
