import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('LbaAssessment.html', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 1. Update subjects list to include prePrimarySubjects
subject_def_old = """    const primarySubjects = ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಪರಿಸರ ಅಧ್ಯಯನ / Environment"];
    const middleSubjects = ["ಕನ್ನಡ / Kannada", "English", "ಹಿಂದಿ / Hindi", "ಸಮಾಜ ವಿಜ್ಞಾನ / Social Science", "ವಿಜ್ಞಾನ / Science", "ಗಣಿತ / Math"];"""

subject_def_new = """    const prePrimarySubjects = ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಸಾಮಾನ್ಯ ಜ್ಞಾನ / General Knowledge", "ರೇಖಾಚಿತ್ರ & ಚಟುವಟಿಕೆಗಳು / Drawing & Activities"];
    const primarySubjects = ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಪರಿಸರ ಅಧ್ಯಯನ / Environment"];
    const middleSubjects = ["ಕನ್ನಡ / Kannada", "English", "ಹಿಂದಿ / Hindi", "ಸಮಾಜ ವಿಜ್ಞಾನ / Social Science", "ವಿಜ್ಞಾನ / Science", "ಗಣಿತ / Math"];"""

js_code = js_code.replace(subject_def_old, subject_def_new)

# 2. Update classFilter subject population
class_filter_old = """        if (subjectFilter) {
          subjectFilter.innerHTML = '<option value="">-- ವಿಷಯ ಆಯ್ಕೆಮಾಡಿ --</option>';
          if (cls) {
            const subjects = ["1", "2", "3", "4", "5"].includes(cls) ? primarySubjects : middleSubjects;
            subjects.forEach(sub => {
              subjectFilter.innerHTML += `<option value="${sub}">${sub}</option>`;
            });
          }
        }"""

class_filter_new = """        if (subjectFilter) {
          subjectFilter.innerHTML = '<option value="">-- ವಿಷಯ ಆಯ್ಕೆಮಾಡಿ --</option>';
          if (cls) {
            let subjects = primarySubjects;
            if (['LKG', 'UKG'].includes(cls)) {
              subjects = prePrimarySubjects;
            } else if (['6', '7', '8', '9', '10'].includes(cls)) {
              subjects = middleSubjects;
            }
            subjects.forEach(sub => {
              subjectFilter.innerHTML += `<option value="${sub}">${sub}</option>`;
            });
          }
        }"""

js_code = js_code.replace(class_filter_old, class_filter_new)

# 3. Update updateCfgSubjectDropdown
cfg_sub_old = """      const cls = clsEl.value;
      const subjects = ["1", "2", "3", "4", "5"].includes(cls) ? primarySubjects : middleSubjects;"""

cfg_sub_new = """      const cls = clsEl.value;
      let subjects = primarySubjects;
      if (['LKG', 'UKG'].includes(cls)) {
        subjects = prePrimarySubjects;
      } else if (['6', '7', '8', '9', '10'].includes(cls)) {
        subjects = middleSubjects;
      }"""

js_code = js_code.replace(cfg_sub_old, cfg_sub_new)

# 4. View Mode & Filter State variables
vars_old = """    let currentLessons = [];
    let students = [];
    let evaluations = {};
    let isEditing = false;
    let originalEvaluations = {};"""

vars_new = """    let currentLessons = [];
    let students = [];
    let evaluations = {};
    let isEditing = false;
    let originalEvaluations = {};
    let currentViewMode = localStorage.getItem('lba_view_mode') || 'cards';
    let genderFilter = '';
    let searchQuery = '';"""

js_code = js_code.replace(vars_old, vars_new)

# 5. Replace onDataLoaded, renderGrid, and add renderCards, setViewMode, filter logic
render_block_old = re.search(r'function onDataLoaded\(response\)[\s\S]*?function saveData\(\)', js_code)

if render_block_old:
    render_block_new = """function onDataLoaded(response) {
      document.getElementById('loading-overlay').classList.add('hidden');
      if (!response.success) { resetToEmptyState(); return; }

      students = response.students || [];
      evaluations = response.evaluations || {};
      originalEvaluations = JSON.parse(JSON.stringify(evaluations));

      if (students.length === 0) { resetToEmptyState(); return; }

      document.getElementById('grid-subtitle').innerText = `${classFilter.value} | ವಿಷಯ: ${subjectFilter.value}`;
      document.getElementById('stats-bar').classList.remove('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.remove('hidden');
      
      if (document.getElementById('btn-save-pdf')) document.getElementById('btn-save-pdf').classList.remove('hidden');
      document.getElementById('btn-print-report').classList.remove('hidden');
      document.getElementById('btn-export-excel').classList.remove('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.remove('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.remove('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.remove('hidden');
      
      const hasSavedData = Object.keys(evaluations).length > 0;
      setMode(!hasSavedData);
      buildTableHeader();
      setViewMode(currentViewMode, false);
      renderActiveView();
    }

    function onDataLoadFailed(err) {
      document.getElementById('loading-overlay').classList.add('hidden');
      showToast("ಡೇಟಾ ಲೋಡ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ: " + (err.message || err), "error");
      resetToEmptyState();
    }

    function setViewMode(mode, triggerRender = true) {
      currentViewMode = mode || 'cards';
      localStorage.setItem('lba_view_mode', currentViewMode);

      const btnCards = document.getElementById('btn-view-cards');
      const btnTable = document.getElementById('btn-view-table');

      if (currentViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveView();
      }
    }

    function setGenderFilter(val) {
      genderFilter = val || '';
      const btnAll = document.getElementById('gen-btn-all');
      const btnBoy = document.getElementById('gen-btn-boy');
      const btnGirl = document.getElementById('gen-btn-girl');

      const activeClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer';
      const inactiveClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer';

      if (btnAll) btnAll.className = genderFilter === '' ? activeClass : inactiveClass;
      if (btnBoy) btnBoy.className = genderFilter === 'Boy' ? activeClass : inactiveClass;
      if (btnGirl) btnGirl.className = genderFilter === 'Girl' ? activeClass : inactiveClass;

      renderActiveView();
    }

    function applyFiltersAndRender() {
      const searchInput = document.getElementById('search-student-input');
      searchQuery = (searchInput ? searchInput.value : '').toLowerCase().trim();
      renderActiveView();
    }

    function getFilteredStudents() {
      return students.filter(s => {
        if (genderFilter && s.gender !== genderFilter) return false;
        if (searchQuery) {
          const nameEn = (s.name_english || '').toLowerCase();
          const nameKn = (s.student_name_kn || s.student_name || '').toLowerCase();
          const sts = (s.adminNo || s.app_no || s.id || '').toLowerCase();
          const father = (s.father_name_az || s.father_name_kn || '').toLowerCase();
          return nameEn.includes(searchQuery) || nameKn.includes(searchQuery) || sts.includes(searchQuery) || father.includes(searchQuery);
        }
        return true;
      });
    }

    function renderActiveView() {
      const tableEl = document.getElementById('competency-table');
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
    }

    function buildTableHeader() {
      const thead = document.getElementById('table-head');
      if (!thead) return;
      let lessonHeadersHtml = '';
      let subLabelsHtml = '';

      const numLessons = currentLessons.length || 1;
      const totalLessonCols = numLessons * 2;
      const pctPerLessonCol = (100 - 58) / totalLessonCols;

      currentLessons.forEach((lesson, index) => {
        lessonHeadersHtml += `<th colspan="2" class="p-2 text-center border-r border-slate-200 font-bold max-w-[120px] truncate" title="${lesson}" style="width: ${(pctPerLessonCol * 2).toFixed(2)}%;">${lesson}</th>`;
        subLabelsHtml += `
          <th class="p-1.5 text-center border-r border-slate-200" style="width: ${pctPerLessonCol.toFixed(2)}%;">Mark</th>
          <th class="p-1.5 text-center border-r border-slate-200" style="width: ${pctPerLessonCol.toFixed(2)}%;">Grade</th>
        `;
      });

      thead.innerHTML = `
        <tr class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-b border-slate-200 dark:border-slate-700 font-bold">
          <th rowspan="2" class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 4%;">ಕ್ರ.ಸಂ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 10%;">STS ಸಂಖ್ಯೆ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 18%;">ಹೆಸರು</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 16%;">ತಂದೆಯ ಹೆಸರು</th>
          ${lessonHeadersHtml}
          <th colspan="2" class="p-2 text-center font-bold" style="width: 10%;">ಒಟ್ಟು ಶ್ರೇಣಿ ಕೌಂಟ್</th>
        </tr>
        <tr class="bg-slate-50 dark:bg-slate-850 text-[10px] text-slate-500 uppercase border-b border-slate-200 dark:border-slate-700 font-bold">
          ${subLabelsHtml}
          <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-400 font-bold" style="width: 5%;">Total A+,A</th>
          <th class="p-1.5 text-center bg-blue-50 dark:bg-blue-950/30 text-blue-800 dark:text-blue-400 font-bold" style="width: 5%;">Others</th>
        </tr>
      `;
    }

    function renderGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = getFilteredStudents();
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${4 + (currentLessons.length * 2) + 2}" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50 dark:hover:bg-slate-800/50 transition border-b border-slate-200 dark:border-slate-800 text-xs";
        const sId = student.id;
        tr.setAttribute('data-student-id', sId);

        if (!evaluations[sId]) {
          evaluations[sId] = {};
          currentLessons.forEach((_, i) => {
            evaluations[sId]["les_" + i + "_mark"] = "";
            evaluations[sId]["les_" + i + "_grade"] = "-";
          });
        }
        
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        let nameHtml = '';
        if (nameEn && nameKn) {
          nameHtml = `<div class="font-bold text-slate-800 dark:text-slate-100 text-[11px]">${nameEn}</div><div class="text-[10px] text-slate-500 font-medium">${nameKn}</div>`;
        } else {
          nameHtml = `<span class="font-bold text-slate-800 dark:text-slate-100 text-[11px]">${nameEn || nameKn || '-'}</span>`;
        }

        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        let fatherHtml = '';
        if (fatherEn && fatherKn) {
          fatherHtml = `<div class="font-bold text-slate-700 dark:text-slate-300 text-[11px]">${fatherEn}</div><div class="text-[10px] text-slate-500 font-medium">${fatherKn}</div>`;
        } else {
          fatherHtml = `<span class="font-semibold text-slate-700 dark:text-slate-300 text-[11px]">${fatherEn || fatherKn || '-'}</span>`;
        }

        let rowHtml = `
          <td class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold">${index + 1}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700 font-mono text-slate-500 dark:text-slate-400 font-bold">${student.adminNo || student.id}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700">${nameHtml}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700">${fatherHtml}</td>
        `;

        currentLessons.forEach((_, i) => {
          const m = evalData["les_" + i + "_mark"] !== undefined ? evalData["les_" + i + "_mark"] : '';
          const g = evalData["les_" + i + "_grade"] || '-';

          if (isEditing) {
            rowHtml += `
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center">
                <input type="number" min="0" max="10" step="0.5" value="${m}" oninput="onMarkChange('${sId}', ${i}, this.value, this)" class="w-12 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-1 text-center font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 dark:text-white">
              </td>
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center font-bold bg-slate-50/50 dark:bg-slate-900/50">
                <span id="grade-${sId}-${i}" class="text-xs ${getGradeBadgeClass(g)}">${g}</span>
              </td>
            `;
          } else {
            rowHtml += `
              <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold text-slate-800 dark:text-slate-200">${m !== '' ? m : '-'}</td>
              <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                <span class="${getGradeBadgeClass(g)} badge-print">${g}</span>
              </td>
            `;
          }
        });

        rowHtml += `
          <td id="row-total-a-${sId}" class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-400 text-xs">0</td>
          <td id="row-total-b-${sId}" class="p-3 text-center font-black bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-400 text-xs">0</td>
        `;

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
      });
    }

    function getGradeBadgeClass(g) {
      if (g === 'A+') return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300 rounded px-2 py-0.5 font-black';
      if (g === 'A') return 'bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-300 rounded px-2 py-0.5 font-bold';
      if (g === 'B+') return 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300 rounded px-2 py-0.5 font-bold';
      if (g === 'B') return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300 rounded px-2 py-0.5 font-bold';
      if (g === 'C') return 'bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300 rounded px-2 py-0.5 font-bold';
      return 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 rounded px-2 py-0.5 font-bold';
    }

    function renderCards() {
      const container = document.getElementById('student-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const filtered = getFilteredStudents();
      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) {
          evaluations[sId] = {};
          currentLessons.forEach((_, i) => {
            evaluations[sId]["les_" + i + "_mark"] = "";
            evaluations[sId]["les_" + i + "_grade"] = "-";
          });
        }
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        const isBoy = student.gender === 'Boy';

        let lessonsCardsHtml = '';
        currentLessons.forEach((lesson, i) => {
          const m = evalData["les_" + i + "_mark"] !== undefined ? evalData["les_" + i + "_mark"] : '';
          const g = evalData["les_" + i + "_grade"] || '-';

          lessonsCardsHtml += `
            <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-800 dark:text-slate-200 truncate max-w-[170px]" title="${lesson}">${lesson}</span>
                <span id="card-grade-${sId}-${i}" class="text-[11px] ${getGradeBadgeClass(g)}">${g}</span>
              </div>
              ${isEditing ? `
                <div class="flex items-center gap-1.5">
                  <button type="button" onclick="stepMark('${sId}', ${i}, -0.5)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer transition active:scale-95">-</button>
                  <input type="number" min="0" max="10" step="0.5" id="card-input-${sId}-${i}" value="${m}" oninput="onMarkChange('${sId}', ${i}, this.value, this)" class="flex-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-black text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 dark:text-white" placeholder="0-10">
                  <button type="button" onclick="stepMark('${sId}', ${i}, 0.5)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer transition active:scale-95">+</button>
                </div>
                <!-- Quick Preset Chips -->
                <div class="flex items-center gap-1 justify-between pt-0.5">
                  ${[10, 9, 8, 7, 5, 0].map(sc => `
                    <button type="button" onclick="quickSetMark('${sId}', ${i}, ${sc})" class="px-1.5 py-0.5 rounded bg-slate-200/60 dark:bg-slate-700/60 hover:bg-indigo-600 hover:text-white text-[10px] font-bold text-slate-600 dark:text-slate-300 transition cursor-pointer border-0">${sc}</button>
                  `).join('')}
                </div>
              ` : `
                <div class="flex items-center justify-between pt-1">
                  <span class="text-xs text-slate-500">ಅಂಕ:</span>
                  <span class="text-sm font-black text-slate-800 dark:text-slate-100">${m !== '' ? m : '-'} / 10</span>
                </div>
              `}
            </div>
          `;
        });

        const cardHtml = `
          <div class="bg-white dark:bg-slate-850 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-3.5" data-card-student-id="${sId}">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isBoy ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' : 'bg-pink-100 text-pink-700 dark:bg-pink-900/50 dark:text-pink-300'} shadow-xs">
                  ${index + 1}
                </div>
                <div>
                  <h4 class="text-xs font-black text-slate-900 dark:text-white leading-tight">${nameEn || nameKn}</h4>
                  ${nameKn && nameEn ? `<p class="text-[10px] text-slate-500 font-semibold">${nameKn}</p>` : ''}
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${isBoy ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-400' : 'bg-pink-50 text-pink-700 dark:bg-pink-950/40 dark:text-pink-400'}">
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧 ಬಾಲಕಿ'}
                </span>
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${student.adminNo || student.id}</span>
              </div>
            </div>

            <!-- Father Details -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- Lessons Grid -->
            <div class="space-y-2 pt-1 flex-1">
              ${lessonsCardsHtml}
            </div>

            <!-- Card Footer -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 px-2 py-0.5 rounded">A+,A: <strong id="card-total-a-${sId}">0</strong></span>
                <span class="text-[10px] font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 rounded">ಇತರ: <strong id="card-total-b-${sId}">0</strong></span>
              </div>
              ${!isEditing ? `
                <button type="button" onclick="enableEditing()" class="text-indigo-600 dark:text-indigo-400 hover:underline font-bold text-[11px] flex items-center gap-1 border-0 bg-transparent cursor-pointer">
                  <i class="fa-solid fa-pen-to-square"></i> ತಿದ್ದು / Edit
                </button>
              ` : ''}
            </div>
          </div>
        `;

        container.innerHTML += cardHtml;
      });
    }

    function stepMark(studentId, lessonIdx, delta) {
      const currentVal = evaluations[studentId] && evaluations[studentId]["les_" + lessonIdx + "_mark"] !== undefined && evaluations[studentId]["les_" + lessonIdx + "_mark"] !== '' ? parseFloat(evaluations[studentId]["les_" + lessonIdx + "_mark"]) : 0;
      let newVal = Math.max(0, Math.min(10, currentVal + delta));
      quickSetMark(studentId, lessonIdx, newVal);
    }

    function quickSetMark(studentId, lessonIdx, markVal) {
      if (!evaluations[studentId]) evaluations[studentId] = {};
      evaluations[studentId]["les_" + lessonIdx + "_mark"] = markVal;
      const gradeVal = determineGrade(markVal);
      evaluations[studentId]["les_" + lessonIdx + "_grade"] = gradeVal;

      // Update Card input and grade badge
      const cardInput = document.getElementById(`card-input-${studentId}-${lessonIdx}`);
      if (cardInput) cardInput.value = markVal;
      const cardGrade = document.getElementById(`card-grade-${studentId}-${lessonIdx}`);
      if (cardGrade) {
        cardGrade.innerText = gradeVal;
        cardGrade.className = `text-[11px] ${getGradeBadgeClass(gradeVal)}`;
      }

      // Update Table grade badge
      const tableGrade = document.getElementById(`grade-${studentId}-${lessonIdx}`);
      if (tableGrade) {
        tableGrade.innerText = gradeVal;
        tableGrade.className = `text-xs ${getGradeBadgeClass(gradeVal)}`;
      }

      updateTotals();
    }

    function onMarkChange(studentId, lessonIdx, val, inputEl) {
      let markVal = val.trim() === '' ? '' : parseFloat(val);
      if (markVal > 10) {
        markVal = 10;
        if (inputEl) inputEl.value = 10;
      } else if (markVal < 0) {
        markVal = 0;
        if (inputEl) inputEl.value = 0;
      }

      quickSetMark(studentId, lessonIdx, markVal);
    }

    function updateTotals() {
      let grandTotalA = 0;
      let grandTotalOthers = 0;

      students.forEach(student => {
        const sId = student.id;
        const evalData = evaluations[sId] || {};
        let rowA = 0;
        let rowOthers = 0;

        currentLessons.forEach((_, i) => {
          const g = evalData["les_" + i + "_grade"] || '-';
          if (g === '-') return;
          if (['A+', 'A'].includes(g)) { rowA++; } else { rowOthers++; }
        });

        // Table totals
        const rowTotalAEl = document.getElementById(`row-total-a-${sId}`);
        const rowTotalBEl = document.getElementById(`row-total-b-${sId}`);
        if (rowTotalAEl) rowTotalAEl.innerText = rowA;
        if (rowTotalBEl) rowTotalBEl.innerText = rowOthers;

        // Card totals
        const cardTotalAEl = document.getElementById(`card-total-a-${sId}`);
        const cardTotalBEl = document.getElementById(`card-total-b-${sId}`);
        if (cardTotalAEl) cardTotalAEl.innerText = rowA;
        if (cardTotalBEl) cardTotalBEl.innerText = rowOthers;

        grandTotalA += rowA;
        grandTotalOthers += rowOthers;
      });

      const statTotalStudents = document.getElementById('stat-total-students');
      const statTotalA = document.getElementById('stat-total-a');
      const statTotalB = document.getElementById('stat-total-b');
      if (statTotalStudents) statTotalStudents.innerText = students.length;
      if (statTotalA) statTotalA.innerText = grandTotalA;
      if (statTotalB) statTotalB.innerText = grandTotalOthers;
    }

    function setMode(editing) {
      isEditing = editing;
      const modeTag = document.getElementById('grid-mode-tag');
      if (editing) {
        if (modeTag) {
          modeTag.innerText = "Edit Mode";
          modeTag.className = "px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 font-bold uppercase tracking-wider text-[10px]";
          modeTag.classList.remove('hidden');
        }
        const btnEdit = document.getElementById('btn-edit');
        const btnSave = document.getElementById('btn-save');
        const btnCancel = document.getElementById('btn-cancel');
        if (btnEdit) btnEdit.classList.add('hidden');
        if (btnSave) btnSave.classList.remove('hidden');
        if (btnCancel) btnCancel.classList.remove('hidden');
      } else {
        if (modeTag) {
          modeTag.innerText = "View Mode";
          modeTag.className = "px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-bold uppercase tracking-wider text-[10px]";
          modeTag.classList.remove('hidden');
        }
        const btnEdit = document.getElementById('btn-edit');
        const btnSave = document.getElementById('btn-save');
        const btnCancel = document.getElementById('btn-cancel');
        if (btnEdit) btnEdit.classList.remove('hidden');
        if (btnSave) btnSave.classList.add('hidden');
        if (btnCancel) btnCancel.classList.add('hidden');
      }
    }

    function hideActionButtons() {
      const modeTag = document.getElementById('grid-mode-tag');
      if (modeTag) modeTag.classList.add('hidden');
      const btnEdit = document.getElementById('btn-edit');
      const btnSave = document.getElementById('btn-save');
      const btnCancel = document.getElementById('btn-cancel');
      if (btnEdit) btnEdit.classList.add('hidden');
      if (btnSave) btnSave.classList.add('hidden');
      if (btnCancel) btnCancel.classList.add('hidden');
    }

    function resetToEmptyState() {
      document.getElementById('empty-state').classList.remove('hidden');
      document.getElementById('competency-table').classList.add('hidden');
      const cardsEl = document.getElementById('student-cards-container');
      if (cardsEl) cardsEl.classList.add('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.add('hidden');

      document.getElementById('grid-subtitle').innerText = "ಯಾವುದೇ ತರಗತಿ ಅಥವಾ ವಿಷಯವನ್ನು ಆರಿಸಲಾಗಿಲ್ಲ";
      hideActionButtons();
      document.getElementById('stats-bar').classList.add('hidden');
      if (document.getElementById('btn-save-pdf')) document.getElementById('btn-save-pdf').classList.add('hidden');
      document.getElementById('btn-print-report').classList.add('hidden');
      document.getElementById('btn-export-excel').classList.add('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.add('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.add('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.add('hidden');
      document.getElementById('rules-note-card').classList.add('hidden');
    }

    function enableEditing() { setMode(true); renderActiveView(); }
    
    function cancelEditing() {
      evaluations = JSON.parse(JSON.stringify(originalEvaluations));
      setMode(Object.keys(originalEvaluations).length === 0);
      renderActiveView();
    }

    function saveData()"""

    js_code = js_code[:render_block_old.start()] + render_block_new + js_code[render_block_old.end():]

# Also update onDataSaved to call renderActiveView()
js_code = js_code.replace("renderGrid();\n    }", "renderActiveView();\n    }")

with open('LbaAssessment.html', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Successfully integrated Premium Card View and Filter Engine into LbaAssessment.html")
