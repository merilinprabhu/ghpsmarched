import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('UniformDistribution.html', 'r', encoding='utf-8') as f:
    u_code = f.read()

# Add view switcher into export buttons area
export_old = """        <!-- Export Buttons / Bulk Action -->
        <div class="flex gap-2 items-center flex-wrap">"""

export_new = """        <!-- Export Buttons / Bulk Action -->
        <div class="flex gap-2 items-center flex-wrap">
          <!-- View Mode Switcher -->
          <div class="flex items-center gap-1 p-1 bg-black/40 border border-white/5 rounded-xl">
            <button type="button" id="btn-u-cards" onclick="setUniformViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
              <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
            </button>
            <button type="button" id="btn-u-table" onclick="setUniformViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent">
              <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
            </button>
          </div>"""

u_code = u_code.replace(export_old, export_new, 1)

# Add cards container right above uniform-table container
table_cont_old = """      <!-- Main entry table -->
      <div class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

table_cont_new = """      <!-- Mobile Cards View for Uniform -->
      <div id="uniform-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

      <!-- Main entry table -->
      <div id="uniform-table-container" class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

u_code = u_code.replace(table_cont_old, table_cont_new, 1)

# Add JS state variables
js_state_old = "    let entrySortCol = 'name_english';"
js_state_new = """    let entrySortCol = 'name_english';
    let currentUniformViewMode = localStorage.getItem('uniform_view_mode') || 'cards';
    let currentUniformStudents = [];
    let currentUniformRecordsMap = {};"""

u_code = u_code.replace(js_state_old, js_state_new, 1)

# Replace renderTable with dual view engine
render_target = r'function renderTable\(students, recordsMap\)[\s\S]*?async function autoSaveRecord\(studentId\)'

render_replacement = """function setUniformViewMode(mode, triggerRender = true) {
      currentUniformViewMode = mode || 'cards';
      localStorage.setItem('uniform_view_mode', currentUniformViewMode);

      const btnCards = document.getElementById('btn-u-cards');
      const btnTable = document.getElementById('btn-u-table');

      if (currentUniformViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveUniformView();
      }
    }

    function renderActiveUniformView() {
      const tableEl = document.getElementById('uniform-table-container');
      const cardsEl = document.getElementById('uniform-cards-container');

      if (currentUniformViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderUniformCards(currentUniformStudents, currentUniformRecordsMap);
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderUniformTable(currentUniformStudents, currentUniformRecordsMap);
        }
      }
    }

    function renderTable(students, recordsMap) {
      currentUniformStudents = students;
      currentUniformRecordsMap = recordsMap;
      setUniformViewMode(currentUniformViewMode, false);
      renderActiveUniformView();
    }

    function renderUniformCards(students, recordsMap) {
      const container = document.getElementById('uniform-cards-container');
      if (!container) return;
      container.innerHTML = '';

      if (students.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold glass-card rounded-2xl border border-white/5"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-500"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      const sizes = ['22', '24', '26', '28', '30', '32', '34', '36', '38', '40'];

      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const cleanClass = normalizeClass(s.enroll_class);
        const recommendedSize = vals.uniform_size || defaultClassSizes[cleanClass] || '28';
        const s1 = vals.set1_status === true || vals.set1_status === 'true';
        const s2 = vals.set2_status === true || vals.set2_status === 'true';

        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const isBoy = !isGirl;

        const sizeOptions = sizes.map(sz => `<option value="${sz}" ${sz === recommendedSize ? 'selected' : ''}>Size ${sz}</option>`).join('');

        const cardHtml = `
          <div class="glass-card rounded-2xl p-4 border border-white/10 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5" data-card-u-id="${s.id}">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-white/10 pb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isBoy ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'bg-pink-600/20 text-pink-400 border border-pink-500/30'}">
                  ${idx + 1}
                </div>
                <div>
                  <h4 class="text-xs font-black text-white leading-tight">${s.name_english || s.student_name}</h4>
                  ${s.student_name && s.name_english ? `<p class="text-[10px] text-slate-400 font-semibold">${s.student_name}</p>` : ''}
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${isBoy ? 'bg-blue-900/40 text-blue-300' : 'bg-pink-900/40 text-pink-300'}">
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧 ಬಾಲಕಿ'}
                </span>
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${s.app_no || s.id}</span>
              </div>
            </div>

            <!-- Size Selector -->
            <div class="flex items-center justify-between bg-black/40 border border-white/5 rounded-xl p-2 px-3 text-xs">
              <span class="text-slate-300 font-bold">ಸಮವಸ್ತ್ರ ಗಾತ್ರ (Size):</span>
              <select id="card-size-${s.id}" onchange="handleCardSizeChange('${s.id}', this.value)" class="bg-indigo-950/80 border border-indigo-500/40 rounded-lg px-2.5 py-1 text-xs font-black text-indigo-300 focus:outline-none cursor-pointer">
                ${sizeOptions}
              </select>
            </div>

            <!-- Set 1 & Set 2 Touch Toggle Pills -->
            <div class="grid grid-cols-2 gap-2 pt-0.5">
              <!-- Set 1 -->
              <button type="button" onclick="toggleUniformSet('${s.id}', 1)" id="card-set1-btn-${s.id}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${s1 ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-black/50 text-slate-400 border border-white/10'}">
                <i class="fa-solid fa-shirt text-sm"></i> <span>Set 1 ${s1 ? '✓' : '✗'}</span>
              </button>
              <!-- Set 2 -->
              <button type="button" onclick="toggleUniformSet('${s.id}', 2)" id="card-set2-btn-${s.id}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${s2 ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-black/50 text-slate-400 border border-white/10'}">
                <i class="fa-solid fa-shirt text-sm"></i> <span>Set 2 ${s2 ? '✓' : '✗'}</span>
              </button>
            </div>

            <!-- Footer Save Status -->
            <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
              <span class="text-[10px] text-slate-400">ಸ್ಥಿತಿ: <strong class="${(s1 && s2) ? 'text-emerald-400' : 'text-amber-400'}">${(s1 && s2) ? 'ಎರಡೂ ನೀಡಲಾಗಿದೆ' : (s1 || s2 ? '1 Set ನೀಡಲಾಗಿದೆ' : 'ಬಾಕಿ')}</strong></span>
              <span id="card-save-status-${s.id}" class="text-[10px] text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> Saved</span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function handleCardSizeChange(studentId, sizeVal) {
      const tblSelect = document.getElementById(`size-${studentId}`);
      if (tblSelect) tblSelect.value = sizeVal;
      autoSaveRecord(studentId);
    }

    function toggleUniformSet(studentId, setNum) {
      const chk = document.getElementById(`set${setNum}-${studentId}`);
      if (chk) {
        chk.checked = !chk.checked;
        const btn = document.getElementById(`card-set${setNum}-btn-${studentId}`);
        if (btn) {
          if (chk.checked) {
            btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
            btn.innerHTML = `<i class="fa-solid fa-shirt text-sm"></i> <span>Set ${setNum} ✓</span>`;
          } else {
            btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-black/50 text-slate-400 border border-white/10";
            btn.innerHTML = `<i class="fa-solid fa-shirt text-sm"></i> <span>Set ${setNum} ✗</span>`;
          }
        }
        autoSaveRecord(studentId);
      }
    }

    function renderUniformTable(students, recordsMap) {
      const tbody = document.getElementById('distributionTableBody');
      if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-8 text-center text-slate-500 font-semibold bg-slate-50/5"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> No records match these filters.</td></tr>`;
        return;
      }

      const sizes = ['22', '24', '26', '28', '30', '32', '34', '36', '38', '40'];

      let html = '';
      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const cleanClass = normalizeClass(s.enroll_class);
        const recommendedSize = vals.uniform_size || defaultClassSizes[cleanClass] || '28';
        const s1 = vals.set1_status === true || vals.set1_status === 'true';
        const s2 = vals.set2_status === true || vals.set2_status === 'true';

        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const displayGender = isGirl ? 'Girl / ಹೆಣ್ಣು' : 'Boy / ಗಂಡು';

        const sizeOptions = sizes.map(sz => `<option value="${sz}" ${sz === recommendedSize ? 'selected' : ''}>Size ${sz}</option>`).join('');

        html += `
          <tr class="hover:bg-slate-50/5 border-b border-white/5 text-slate-300 font-medium">
            <td class="p-2.5 font-bold text-slate-500">${idx + 1}</td>
            <td class="p-2.5 font-mono text-center">${s.app_no || '-'}</td>
            <td class="p-2.5 text-left text-white">
              <div class="font-bold text-xs">${s.name_english || '-'}</div>
              <div class="text-[9px] text-slate-400">${s.student_name || '-'}</div>
            </td>
            <td class="p-2.5 text-center text-[10px]">${displayGender}</td>
            
            <td class="p-2.5 bg-indigo-500/[0.01]">
              <select id="size-${s.id}" onchange="autoSaveRecord('${s.id}')" class="bg-black/60 border border-white/10 rounded-xl px-2.5 py-1 text-xs font-bold text-indigo-300 focus:outline-none cursor-pointer">
                ${sizeOptions}
              </select>
            </td>

            <td class="p-2.5 bg-indigo-500/[0.01] border-x border-white/5 text-center">
              <input type="checkbox" id="set1-${s.id}" onchange="autoSaveRecord('${s.id}')" ${s1 ? 'checked' : ''} class="w-5 h-5 rounded text-indigo-650 bg-black border-white/10 cursor-pointer transform scale-110">
            </td>

            <td class="p-2.5 bg-indigo-500/[0.01] border-x border-white/5 text-center">
              <input type="checkbox" id="set2-${s.id}" onchange="autoSaveRecord('${s.id}')" ${s2 ? 'checked' : ''} class="w-5 h-5 rounded text-indigo-650 bg-black border-white/10 cursor-pointer transform scale-110">
            </td>

            <td class="p-2.5 no-print" id="status-container-${s.id}">
              <div id="save-indicator-${s.id}" class="text-[10px] text-emerald-400 font-bold flex items-center justify-center gap-1">
                <i class="fa-solid fa-circle-check"></i> Saved
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    async function autoSaveRecord(studentId)"""

u_code = re.sub(render_target, render_replacement, u_code)

with open('UniformDistribution.html', 'w', encoding='utf-8') as f:
    f.write(u_code)

print("Successfully integrated Mobile Card View into UniformDistribution.html")
