import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Replace onDataLoaded through cancelEditing
target_pattern = r'function onDataLoaded\(response\)[\s\S]*?function saveData\(\)'

replacement_code = """function onDataLoaded(response) {
      document.getElementById('loading-overlay').classList.add('hidden');
      if (!response.success) { resetToEmptyState(); return; }

      students = response.students || [];
      evaluations = response.evaluations || {};
      originalEvaluations = JSON.parse(JSON.stringify(evaluations));

      if (students.length === 0) { resetToEmptyState(); return; }

      const gridSubtitle = document.getElementById('grid-subtitle');
      if (gridSubtitle) gridSubtitle.innerText = `${classFilter.value} | Exam: ${examTypeFilter.value}`;
      
      const statsBar = document.getElementById('stats-bar');
      if (statsBar) statsBar.classList.remove('hidden');

      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.remove('hidden');

      if (document.getElementById('btn-export-pdf')) document.getElementById('btn-export-pdf').classList.remove('hidden');
      if (document.getElementById('btn-export-excel')) document.getElementById('btn-export-excel').classList.remove('hidden');
      if (document.getElementById('btn-print')) document.getElementById('btn-print').classList.remove('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.remove('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.remove('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.remove('hidden');
      
      if (classFilter.value === "ALL") {
        setMode(false);
        const btnEdit = document.getElementById('btn-edit');
        if (btnEdit) btnEdit.classList.add('hidden');
      } else {
        setMode(Object.keys(evaluations).length === 0);
      }
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
      localStorage.setItem('cce_view_mode', currentViewMode);

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
    }

    function buildTableHeader() {
      const thead = document.getElementById('table-head');
      if (!thead) return;
      const selectedSub = subjectFilter.value;
      const isSA = examTypeFilter.value.startsWith("SA");
      
      let subHeadersHtml = ''; let subLabelsHtml = '';
      let numVisibleSubs = 0;
      currentSubjects.forEach(sub => { if (selectedSub === "ALL" || sub.id === selectedSub) numVisibleSubs++; });

      const colsPerSub = isSA ? 4 : 2;
      const totalSubCols = numVisibleSubs * colsPerSub;
      const pctPerSubCol = (100 - 54) / totalSubCols;

      currentSubjects.forEach(sub => {
        if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
        if (isSA) {
          subHeadersHtml += `<th colspan="4" class="p-2 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${(pctPerSubCol * 4).toFixed(2)}%;">${sub.name}</th>`;
          subLabelsHtml += `
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-amber-50/20" style="width: ${pctPerSubCol.toFixed(2)}%;">W</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-amber-50/20" style="width: ${pctPerSubCol.toFixed(2)}%;">O</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 font-bold bg-amber-100/20" style="width: ${pctPerSubCol.toFixed(2)}%;">Total</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700" style="width: ${pctPerSubCol.toFixed(2)}%;">Grade</th>
          `;
        } else {
          subHeadersHtml += `<th colspan="2" class="p-2 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${(pctPerSubCol * 2).toFixed(2)}%;">${sub.name}</th>`;
          subLabelsHtml += `
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700" style="width: ${pctPerSubCol.toFixed(2)}%;">Mark</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700" style="width: ${pctPerSubCol.toFixed(2)}%;">Grade</th>
          `;
        }
      });

      thead.innerHTML = `
        <tr class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-b border-slate-200 dark:border-slate-700 font-bold">
          <th rowspan="2" class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 4%;">ಕ್ರ.ಸಂ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 10%;">STS ಸಂಖ್ಯೆ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 16%;">ಹೆಸರು</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 14%;">ತಂದೆಯ ಹೆಸರು</th>
          ${subHeadersHtml}
          <th colspan="2" class="p-2 text-center font-bold" style="width: 10%;">ಒಟ್ಟು ಕೌಂಟ್</th>
        </tr>
        <tr class="bg-slate-50 dark:bg-slate-850 text-[10px] text-slate-500 uppercase border-b border-slate-200 dark:border-slate-700">
          ${subLabelsHtml}
          <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300 font-bold" style="width: 5%;">Total A+,A</th>
          <th class="p-1.5 text-center bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-300 font-bold" style="width: 5%;">Others</th>
        </tr>
      `;
    }

    function renderGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      
      const selectedSub = subjectFilter.value;
      const isSA = examType.startsWith("SA");
      const filtered = getFilteredStudents();

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="20" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50 dark:hover:bg-slate-800/50 transition border-b border-slate-200 dark:border-slate-800";
        const sId = student.id;
        tr.setAttribute('data-student-id', sId);

        if (!evaluations[sId]) {
          evaluations[sId] = {};
          currentSubjects.forEach(s => {
            evaluations[sId][s.id + "_mark"] = "";
            evaluations[sId][s.id + "_grade"] = "-";
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

        currentSubjects.forEach(sub => {
          if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
          const sKey = sub.id;

          if (isSA) {
            const wVal = evalData[sKey + "_w"] !== undefined ? evalData[sKey + "_w"] : '';
            const oVal = evalData[sKey + "_o"] !== undefined ? evalData[sKey + "_o"] : '';
            const totalVal = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = evalData[sKey + "_grade"] || '-';

            if (isEditing) {
              rowHtml += `
                <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center">
                  <input type="number" value="${wVal}" oninput="onSAMarkChange('${sId}', '${sKey}', 'w', this.value)" class="w-10 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-0.5 text-center font-bold text-xs focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-white">
                </td>
                <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center">
                  <input type="number" value="${oVal}" oninput="onSAMarkChange('${sId}', '${sKey}', 'o', this.value)" class="w-10 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-0.5 text-center font-bold text-xs focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-white">
                </td>
                <td id="total-${sId}-${sKey}" class="p-2 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-slate-50/50 dark:bg-slate-850 text-xs">${totalVal}</td>
                <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                  <span id="grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </td>
              `;
            } else {
              rowHtml += `
                <td class="p-2 border-r border-slate-200 dark:border-slate-700 text-center">${wVal !== '' ? wVal : '-'}</td>
                <td class="p-2 border-r border-slate-200 dark:border-slate-700 text-center">${oVal !== '' ? oVal : '-'}</td>
                <td class="p-2 border-r border-slate-200 dark:border-slate-700 text-center font-black">${totalVal !== '' ? totalVal : '-'}</td>
                <td class="p-2 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                  <span class="${getCceGradeBadgeClass(g)} badge-print">${g}</span>
                </td>
              `;
            }
          } else {
            const m = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = evalData[sKey + "_grade"] || '-';

            if (isEditing) {
              rowHtml += `
                <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center">
                  <input type="number" value="${m}" oninput="onFAMarkChange('${sId}', '${sKey}', this.value, this)" class="w-12 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-1 text-center font-bold focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-white">
                </td>
                <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center font-bold bg-slate-50/50 dark:bg-slate-850">
                  <span id="grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </td>
              `;
            } else {
              rowHtml += `
                <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold">${m !== '' ? m : '-'}</td>
                <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                  <span class="${getCceGradeBadgeClass(g)} badge-print">${g}</span>
                </td>
              `;
            }
          }
        });

        rowHtml += `
          <td id="row-total-a-${sId}" class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300 text-xs">0</td>
          <td id="row-total-b-${sId}" class="p-3 text-center font-black bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-300 text-xs">0</td>
        `;

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
      });
    }

    function getCceGradeBadgeClass(g) {
      if (g === 'A+') return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300 rounded px-2 py-0.5 font-black text-xs';
      if (g === 'A') return 'bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-300 rounded px-2 py-0.5 font-bold text-xs';
      if (g === 'B+') return 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300 rounded px-2 py-0.5 font-bold text-xs';
      if (g === 'B') return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300 rounded px-2 py-0.5 font-bold text-xs';
      if (g === 'C+' || g === 'C') return 'bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300 rounded px-2 py-0.5 font-bold text-xs';
      return 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 rounded px-2 py-0.5 font-bold text-xs';
    }

    function renderCards() {
      const container = document.getElementById('student-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const selectedSub = subjectFilter.value;
      const isSA = examType.startsWith("SA");
      const filtered = getFilteredStudents();

      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) evaluations[sId] = {};
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        const isBoy = student.gender === 'Boy';

        let subCardsHtml = '';
        currentSubjects.forEach(sub => {
          if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
          const sKey = sub.id;

          if (isSA) {
            const wVal = evalData[sKey + "_w"] !== undefined ? evalData[sKey + "_w"] : '';
            const oVal = evalData[sKey + "_o"] !== undefined ? evalData[sKey + "_o"] : '';
            const totalVal = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = evalData[sKey + "_grade"] || '-';

            subCardsHtml += `
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black text-slate-800 dark:text-slate-200 truncate max-w-[160px]">${sub.name}</span>
                  <span id="card-grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </div>
                ${isEditing ? `
                  <div class="grid grid-cols-3 gap-1.5 items-center">
                    <div>
                      <span class="text-[9px] text-slate-400 font-bold block mb-0.5">ಬರಹ (W)</span>
                      <input type="number" value="${wVal}" oninput="onSAMarkChange('${sId}', '${sKey}', 'w', this.value)" class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-bold text-xs text-slate-900 dark:text-white" placeholder="W">
                    </div>
                    <div>
                      <span class="text-[9px] text-slate-400 font-bold block mb-0.5">ಮೌಖಿಕ (O)</span>
                      <input type="number" value="${oVal}" oninput="onSAMarkChange('${sId}', '${sKey}', 'o', this.value)" class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-bold text-xs text-slate-900 dark:text-white" placeholder="O">
                    </div>
                    <div>
                      <span class="text-[9px] text-indigo-500 font-black block mb-0.5">ಒಟ್ಟು (Total)</span>
                      <div id="card-total-${sId}-${sKey}" class="w-full bg-indigo-50 dark:bg-slate-950 border border-indigo-200 dark:border-indigo-900/50 rounded-lg py-1 text-center font-black text-xs text-indigo-700 dark:text-indigo-300">${totalVal !== '' ? totalVal : '-'}</div>
                    </div>
                  </div>
                ` : `
                  <div class="flex items-center justify-between text-xs pt-1">
                    <span class="text-slate-500">W: <strong>${wVal !== '' ? wVal : '-'}</strong> | O: <strong>${oVal !== '' ? oVal : '-'}</strong></span>
                    <span class="font-black text-slate-800 dark:text-slate-100">ಒಟ್ಟು: ${totalVal !== '' ? totalVal : '-'}</span>
                  </div>
                `}
              </div>
            `;
          } else {
            const m = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = evalData[sKey + "_grade"] || '-';

            subCardsHtml += `
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black text-slate-800 dark:text-slate-200 truncate max-w-[160px]">${sub.name}</span>
                  <span id="card-grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </div>
                ${isEditing ? `
                  <div class="flex items-center gap-1.5">
                    <button type="button" onclick="stepCceFAMark('${sId}', '${sKey}', -1)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">-</button>
                    <input type="number" id="card-input-${sId}-${sKey}" value="${m}" oninput="onFAMarkChange('${sId}', '${sKey}', this.value, this)" class="flex-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-black text-sm text-slate-900 dark:text-white" placeholder="0-20">
                    <button type="button" onclick="stepCceFAMark('${sId}', '${sKey}', 1)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">+</button>
                  </div>
                  <!-- Preset Chips -->
                  <div class="flex items-center gap-1 justify-between pt-0.5">
                    ${[20, 18, 15, 10, 5, 0].map(sc => `
                      <button type="button" onclick="quickSetCceFAMark('${sId}', '${sKey}', ${sc})" class="px-1.5 py-0.5 rounded bg-slate-200/60 dark:bg-slate-700/60 hover:bg-indigo-600 hover:text-white text-[10px] font-bold text-slate-600 dark:text-slate-300 transition cursor-pointer border-0">${sc}</button>
                    `).join('')}
                  </div>
                ` : `
                  <div class="flex items-center justify-between pt-1">
                    <span class="text-xs text-slate-500">ಅಂಕ:</span>
                    <span class="text-sm font-black text-slate-800 dark:text-slate-100">${m !== '' ? m : '-'}</span>
                  </div>
                `}
              </div>
            `;
          }
        });

        const cardHtml = `
          <div class="bg-white dark:bg-slate-850 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-3.5">
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

            <!-- Father -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- Subject Grid -->
            <div class="space-y-2 pt-1 flex-1">
              ${subCardsHtml}
            </div>

            <!-- Footer -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 px-2 py-0.5 rounded">A+,A: <strong id="card-total-a-${sId}">0</strong></span>
                <span class="text-[10px] font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 rounded">ಇತರ: <strong id="card-total-b-${sId}">0</strong></span>
              </div>
              ${!isEditing && classFilter.value !== "ALL" ? `
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

    function stepCceFAMark(studentId, subKey, delta) {
      const currentVal = evaluations[studentId] && evaluations[studentId][subKey + "_mark"] !== undefined && evaluations[studentId][subKey + "_mark"] !== '' ? parseFloat(evaluations[studentId][subKey + "_mark"]) : 0;
      let newVal = Math.max(0, currentVal + delta);
      quickSetCceFAMark(studentId, subKey, newVal);
    }

    function quickSetCceFAMark(studentId, subKey, markVal) {
      onFAMarkChange(studentId, subKey, markVal.toString());
      const cardInput = document.getElementById(`card-input-${studentId}-${subKey}`);
      if (cardInput) cardInput.value = markVal;
    }

    function updateTotals() {
      let grandTotalA = 0;
      let grandTotalOthers = 0;
      let apCount = 0, aCount = 0, bpCount = 0, bCount = 0, cCount = 0;

      students.forEach(student => {
        const sId = student.id;
        const evalData = evaluations[sId] || {};
        let rowA = 0;
        let rowOthers = 0;

        currentSubjects.forEach(sub => {
          const g = evalData[sub.id + "_grade"] || '-';
          if (g === '-') return;
          if (g === 'A+') { apCount++; rowA++; }
          else if (g === 'A') { aCount++; rowA++; }
          else if (g === 'B+') { bpCount++; rowOthers++; }
          else if (g === 'B') { bCount++; rowOthers++; }
          else if (['C+', 'C', 'D'].includes(g)) { cCount++; rowOthers++; }
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
      if (statTotalStudents) statTotalStudents.innerText = students.length;

      const statAP = document.getElementById('stat-grade-ap');
      const statA = document.getElementById('stat-grade-a');
      const statBP = document.getElementById('stat-grade-bp');
      const statB = document.getElementById('stat-grade-b');
      const statC = document.getElementById('stat-grade-c');
      if (statAP) statAP.innerText = apCount;
      if (statA) statA.innerText = aCount;
      if (statBP) statBP.innerText = bpCount;
      if (statB) statB.innerText = bCount;
      if (statC) statC.innerText = cCount;
    }

    function setMode(editing) {
      isEditing = editing;
      const btnEdit = document.getElementById('btn-edit');
      const btnSave = document.getElementById('btn-save');
      const btnCancel = document.getElementById('btn-cancel');

      if (editing) {
        if (btnEdit) btnEdit.classList.add('hidden');
        if (btnSave) btnSave.classList.remove('hidden');
        if (btnCancel) btnCancel.classList.remove('hidden');
      } else {
        if (btnEdit && classFilter.value !== "ALL") btnEdit.classList.remove('hidden');
        if (btnSave) btnSave.classList.add('hidden');
        if (btnCancel) btnCancel.classList.add('hidden');
      }
    }

    function resetToEmptyState() {
      const emptyState = document.getElementById('empty-state');
      if (emptyState) emptyState.classList.remove('hidden');
      const compTable = document.getElementById('competency-table');
      if (compTable) compTable.classList.add('hidden');
      const cardsEl = document.getElementById('student-cards-container');
      if (cardsEl) cardsEl.classList.add('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.add('hidden');
      const statsBar = document.getElementById('stats-bar');
      if (statsBar) statsBar.classList.add('hidden');

      const btnEdit = document.getElementById('btn-edit');
      const btnSave = document.getElementById('btn-save');
      const btnCancel = document.getElementById('btn-cancel');
      if (btnEdit) btnEdit.classList.add('hidden');
      if (btnSave) btnSave.classList.add('hidden');
      if (btnCancel) btnCancel.classList.add('hidden');
    }

    function enableEditing() { setMode(true); renderActiveView(); }
    
    function cancelEditing() {
      evaluations = JSON.parse(JSON.stringify(originalEvaluations));
      setMode(Object.keys(originalEvaluations).length === 0);
      renderActiveView();
    }

    function saveData()"""

# Replace in js_code
js_code = re.sub(target_pattern, replacement_code, js_code)

# In onFAMarkChange and onSAMarkChange, also update the Card elements
fa_mark_change_old = """      const gradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (gradeEl) {
        gradeEl.innerText = gradeVal;
        if (['A+', 'A'].includes(gradeVal)) {
          gradeEl.className = "text-xs font-bold text-emerald-800 dark:text-emerald-400";
        } else {
          gradeEl.className = "text-xs font-bold text-slate-600 dark:text-slate-400";
        }
      }"""

fa_mark_change_new = """      const gradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (gradeEl) {
        gradeEl.innerText = gradeVal;
        gradeEl.className = getCceGradeBadgeClass(gradeVal);
      }
      const cardGradeEl = document.getElementById(`card-grade-${studentId}-${subKey}`);
      if (cardGradeEl) {
        cardGradeEl.innerText = gradeVal;
        cardGradeEl.className = getCceGradeBadgeClass(gradeVal);
      }"""

js_code = js_code.replace(fa_mark_change_old, fa_mark_change_new)

sa_mark_change_old = """      const gradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (gradeEl) {
        gradeEl.innerText = gradeVal;
      }"""

sa_mark_change_new = """      const gradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (gradeEl) {
        gradeEl.innerText = gradeVal;
        gradeEl.className = getCceGradeBadgeClass(gradeVal);
      }
      const cardGradeEl = document.getElementById(`card-grade-${studentId}-${subKey}`);
      if (cardGradeEl) {
        cardGradeEl.innerText = gradeVal;
        cardGradeEl.className = getCceGradeBadgeClass(gradeVal);
      }
      const cardTotalEl = document.getElementById(`card-total-${studentId}-${subKey}`);
      if (cardTotalEl) {
        cardTotalEl.innerText = totalVal !== '' ? totalVal : '-';
      }"""

js_code = js_code.replace(sa_mark_change_old, sa_mark_change_new)

# Also in onDataSaved
js_code = js_code.replace("renderGrid();\n    }", "renderActiveView();\n    }")

with open('CceAssessmet.html', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Successfully integrated Mobile Card View into CceAssessmet.html")
