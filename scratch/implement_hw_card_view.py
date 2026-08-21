import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('HeightWeightTracker.html', 'r', encoding='utf-8') as f:
    hw_code = f.read()

# Add view mode buttons in export buttons bar
export_btns_old = """        <!-- Export Buttons -->
        <div class="flex gap-2 items-center flex-wrap">"""

export_btns_new = """        <!-- View Mode Switcher -->
        <div class="flex items-center gap-1 p-1 bg-black/40 border border-white/5 rounded-xl">
          <button type="button" id="btn-hw-cards" onclick="setHwViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
            <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
          </button>
          <button type="button" id="btn-hw-table" onclick="setHwViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent">
            <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
          </button>
        </div>

        <!-- Export Buttons -->
        <div class="flex gap-2 items-center flex-wrap">"""

hw_code = hw_code.replace(export_btns_old, export_btns_new, 1)

# Add #hw-cards-container right above #height-weight-table container
table_container_old = """      <!-- Main entry table -->
      <div class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

table_container_new = """      <!-- Mobile Cards View for Height Weight -->
      <div id="hw-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

      <!-- Main entry table -->
      <div id="hw-table-container" class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

hw_code = hw_code.replace(table_container_old, table_container_new, 1)

# Add JS state variables
js_state_old = "    let currentData = [];"
js_state_new = """    let currentData = [];
    let currentHwViewMode = localStorage.getItem('hw_view_mode') || 'cards';"""

hw_code = hw_code.replace(js_state_old, js_state_new, 1)

# Find renderTable function and replace to support dual view
render_target = r'function renderTable\(data\)[\s\S]*?function renderRow\(student, index\)'

render_replacement = """function setHwViewMode(mode, triggerRender = true) {
      currentHwViewMode = mode || 'cards';
      localStorage.setItem('hw_view_mode', currentHwViewMode);

      const btnCards = document.getElementById('btn-hw-cards');
      const btnTable = document.getElementById('btn-hw-table');

      if (currentHwViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveHwView();
      }
    }

    function renderActiveHwView() {
      const tableEl = document.getElementById('hw-table-container');
      const cardsEl = document.getElementById('hw-cards-container');

      if (currentHwViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderHwCards(currentFilteredData);
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderHwTable(currentFilteredData);
        }
      }
    }

    function renderTable(data) {
      currentFilteredData = data;
      setHwViewMode(currentHwViewMode, false);
      renderActiveHwView();
    }

    function renderHwCards(data) {
      const container = document.getElementById('hw-cards-container');
      if (!container) return;
      container.innerHTML = '';

      if (!data || data.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold glass-card rounded-2xl border border-white/5"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-500"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      data.forEach((student, index) => {
        const isBoy = student.gender === 'Boy';
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name || student.student_name_kn || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        const height = student.height_cm || '';
        const weight = student.weight_kg || '';
        const bmi = calculateBMI(height, weight);
        const status = getBMIStatus(bmi, student.gender, student.enroll_class);

        const cardHtml = `
          <div class="glass-card rounded-2xl p-4 border border-white/10 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5" data-card-hw-id="${student.id}">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-white/10 pb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isBoy ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'bg-pink-600/20 text-pink-400 border border-pink-500/30'}">
                  ${index + 1}
                </div>
                <div>
                  <h4 class="text-xs font-black text-white leading-tight">${nameEn || nameKn}</h4>
                  ${nameKn && nameEn ? `<p class="text-[10px] text-slate-400 font-semibold">${nameKn}</p>` : ''}
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${isBoy ? 'bg-blue-900/40 text-blue-300' : 'bg-pink-900/40 text-pink-300'}">
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧 ಬಾಲಕಿ'}
                </span>
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${student.app_no || student.id}</span>
              </div>
            </div>

            <!-- Father & Class -->
            <div class="flex items-center justify-between text-[11px] text-slate-300 px-1">
              <span>ತಂದೆ: <strong class="text-white">${fatherEn || fatherKn || '-'}</strong></span>
              <span class="bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded text-[10px] font-bold">Class ${student.enroll_class}</span>
            </div>

            <!-- Height & Weight Touch Inputs -->
            <div class="grid grid-cols-2 gap-3 pt-1">
              <!-- Height -->
              <div class="bg-indigo-950/40 border border-indigo-500/20 rounded-xl p-2.5 space-y-1.5">
                <span class="text-[10px] font-extrabold text-indigo-300 uppercase tracking-wider block">📏 ಎತ್ತರ / Height (cm)</span>
                <div class="flex items-center gap-1">
                  <button type="button" onclick="stepHwValue('${student.id}', 'height', -1)" class="w-7 h-7 rounded-lg bg-indigo-900/60 text-indigo-200 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">-</button>
                  <input type="number" id="card-height-${student.id}" value="${height}" oninput="handleCardHwChange('${student.id}')" class="flex-1 bg-black/50 border border-indigo-500/30 rounded-lg py-1 text-center font-black text-sm text-white focus:outline-none focus:ring-1 focus:ring-indigo-400" placeholder="cm">
                  <button type="button" onclick="stepHwValue('${student.id}', 'height', 1)" class="w-7 h-7 rounded-lg bg-indigo-900/60 text-indigo-200 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">+</button>
                </div>
              </div>

              <!-- Weight -->
              <div class="bg-pink-950/40 border border-pink-500/20 rounded-xl p-2.5 space-y-1.5">
                <span class="text-[10px] font-extrabold text-pink-300 uppercase tracking-wider block">⚖️ ತೂಕ / Weight (kg)</span>
                <div class="flex items-center gap-1">
                  <button type="button" onclick="stepHwValue('${student.id}', 'weight', -0.5)" class="w-7 h-7 rounded-lg bg-pink-900/60 text-pink-200 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">-</button>
                  <input type="number" id="card-weight-${student.id}" value="${weight}" step="0.5" oninput="handleCardHwChange('${student.id}')" class="flex-1 bg-black/50 border border-pink-500/30 rounded-lg py-1 text-center font-black text-sm text-white focus:outline-none focus:ring-1 focus:ring-pink-400" placeholder="kg">
                  <button type="button" onclick="stepHwValue('${student.id}', 'weight', 0.5)" class="w-7 h-7 rounded-lg bg-pink-900/60 text-pink-200 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">+</button>
                </div>
              </div>
            </div>

            <!-- BMI & Health Status Footer -->
            <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] text-slate-400 font-bold">BMI: <strong id="card-bmi-${student.id}" class="text-white font-mono">${bmi || '-'}</strong></span>
                <span id="card-status-${student.id}" class="${status.badgeClass} text-[10px] font-bold px-2 py-0.5 rounded">${status.label}</span>
              </div>
              <span id="card-save-status-${student.id}" class="text-[9px] text-emerald-400 font-mono"><i class="fa-solid fa-cloud-check"></i></span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function stepHwValue(studentId, field, delta) {
      const student = currentData.find(s => s.id === studentId);
      if (!student) return;
      if (field === 'height') {
        const cur = parseFloat(student.height_cm) || 120;
        const nxt = Math.max(50, Math.min(220, cur + delta));
        student.height_cm = nxt;
        const cardIn = document.getElementById(`card-height-${studentId}`);
        const tblIn = document.getElementById(`height-${studentId}`);
        if (cardIn) cardIn.value = nxt;
        if (tblIn) tblIn.value = nxt;
      } else {
        const cur = parseFloat(student.weight_kg) || 25;
        const nxt = Math.max(10, Math.min(150, cur + delta));
        student.weight_kg = nxt;
        const cardIn = document.getElementById(`card-weight-${studentId}`);
        const tblIn = document.getElementById(`weight-${studentId}`);
        if (cardIn) cardIn.value = nxt;
        if (tblIn) tblIn.value = nxt;
      }
      recalcStudentBMI(studentId);
      autoSaveStudent(studentId);
    }

    function handleCardHwChange(studentId) {
      const student = currentData.find(s => s.id === studentId);
      if (!student) return;
      const cardH = document.getElementById(`card-height-${studentId}`);
      const cardW = document.getElementById(`card-weight-${studentId}`);
      if (cardH) student.height_cm = cardH.value;
      if (cardW) student.weight_kg = cardW.value;
      
      const tblH = document.getElementById(`height-${studentId}`);
      const tblW = document.getElementById(`weight-${studentId}`);
      if (tblH && cardH) tblH.value = cardH.value;
      if (tblW && cardW) tblW.value = cardW.value;

      recalcStudentBMI(studentId);
      autoSaveStudent(studentId);
    }

    function recalcStudentBMI(studentId) {
      const student = currentData.find(s => s.id === studentId);
      if (!student) return;
      const bmi = calculateBMI(student.height_cm, student.weight_kg);
      const status = getBMIStatus(bmi, student.gender, student.enroll_class);

      const cardBmi = document.getElementById(`card-bmi-${studentId}`);
      const cardStatus = document.getElementById(`card-status-${studentId}`);
      if (cardBmi) cardBmi.innerText = bmi || '-';
      if (cardStatus) {
        cardStatus.className = `${status.badgeClass} text-[10px] font-bold px-2 py-0.5 rounded`;
        cardStatus.innerText = status.label;
      }

      const tblBmi = document.getElementById(`bmi-${studentId}`);
      const tblStatus = document.getElementById(`status-${studentId}`);
      if (tblBmi) tblBmi.innerText = bmi || '-';
      if (tblStatus) {
        tblStatus.className = `${status.badgeClass} text-[10px] font-bold px-2 py-0.5 rounded`;
        tblStatus.innerText = status.label;
      }
    }

    function renderHwTable(data) {
      const tbody = document.getElementById('distributionTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';
      if (!data || data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="p-8 text-center text-slate-500 font-bold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ವಿವರಗಳು ಲಭ್ಯವಿಲ್ಲ</td></tr>`;
        return;
      }
      data.forEach((student, index) => {
        tbody.appendChild(renderRow(student, index));
      });
    }

    function renderRow(student, index)"""

hw_code = re.sub(render_target, render_replacement, hw_code)

with open('HeightWeightTracker.html', 'w', encoding='utf-8') as f:
    f.write(hw_code)

print("Successfully integrated Mobile Card View into HeightWeightTracker.html")
