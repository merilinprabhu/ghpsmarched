import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('ShoeSocksDistribution.html', 'r', encoding='utf-8') as f:
    ss_code = f.read()

target_pattern = r'function renderActiveShoeSocksView\(\)[\s\S]*?async function autoSaveRecord\(studentId\)'

replacement = """function renderActiveShoeSocksView() {
      const tableEl = document.getElementById('shoesocks-table-container');
      const cardsEl = document.getElementById('shoesocks-cards-container');

      // Always render both so that DOM elements exist for auto-saving and print drawers
      renderShoeSocksCards(currentShoeSocksStudents, currentShoeSocksRecordsMap);
      renderShoeSocksTable(currentShoeSocksStudents, currentShoeSocksRecordsMap);

      if (currentShoeSocksViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) cardsEl.classList.remove('hidden');
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) tableEl.classList.remove('hidden');
      }
    }

    function renderTable(students, recordsMap) {
      currentShoeSocksStudents = students;
      currentShoeSocksRecordsMap = recordsMap;
      setShoeSocksViewMode(currentShoeSocksViewMode, false);
      renderActiveShoeSocksView();
    }

    function renderShoeSocksCards(students, recordsMap) {
      const container = document.getElementById('shoesocks-cards-container');
      if (!container) return;
      container.innerHTML = '';

      if (students.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold glass-card rounded-2xl border border-white/5"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-500"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      const sizes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'];

      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const cleanClass = normalizeClass(s.enroll_class);
        const recommendedSize = vals.shoe_size || defaultClassSizes[cleanClass] || '5';
        const shoeDist = vals.shoe_distributed === true || vals.shoe_distributed === 'true';
        const socksDist = vals.socks_distributed === true || vals.socks_distributed === 'true';

        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const isBoy = !isGirl;

        const sizeOptions = sizes.map(sz => `<option value="${sz}" ${sz === recommendedSize ? 'selected' : ''}>Size ${sz}</option>`).join('');

        const cardHtml = `
          <div class="glass-card rounded-2xl p-4 border border-white/10 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5" data-card-ss-id="${s.id}">
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
              <span class="text-slate-300 font-bold">ಶೂ ಅಳತೆ (Shoe Size):</span>
              <select id="card-ss-size-${s.id}" onchange="handleCardShoeSizeChange('${s.id}', this.value)" class="bg-indigo-950/80 border border-indigo-500/40 rounded-lg px-2.5 py-1 text-xs font-black text-indigo-300 focus:outline-none cursor-pointer">
                ${sizeOptions}
              </select>
            </div>

            <!-- Shoe & Socks Touch Toggle Pills -->
            <div class="grid grid-cols-2 gap-2 pt-0.5">
              <!-- Shoe -->
              <button type="button" onclick="toggleShoeSocksItem('${s.id}', 'shoe')" id="card-shoe-btn-${s.id}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${shoeDist ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-black/50 text-slate-400 border border-white/10'}">
                <i class="fa-solid fa-shoe-prints text-sm"></i> <span>ಶೂ ${shoeDist ? '✓' : '✗'}</span>
              </button>
              <!-- Socks -->
              <button type="button" onclick="toggleShoeSocksItem('${s.id}', 'socks')" id="card-socks-btn-${s.id}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${socksDist ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-black/50 text-slate-400 border border-white/10'}">
                <i class="fa-solid fa-socks text-sm"></i> <span>ಸಾಕ್ಸ್ ${socksDist ? '✓' : '✗'}</span>
              </button>
            </div>

            <!-- Footer Save Status -->
            <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
              <span class="text-[10px] text-slate-400">ಸ್ಥಿತಿ: <strong id="card-ss-status-text-${s.id}" class="${(shoeDist && socksDist) ? 'text-emerald-400' : 'text-amber-400'}">${(shoeDist && socksDist) ? 'ಎರಡೂ ನೀಡಲಾಗಿದೆ' : (shoeDist || socksDist ? 'ಭಾಗಶಃ ನೀಡಲಾಗಿದೆ' : 'ಬಾಕಿ')}</strong></span>
              <span id="card-ss-save-status-${s.id}" class="text-[10px] text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> Saved</span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function handleCardShoeSizeChange(studentId, sizeVal) {
      const tblSelect = document.getElementById(`shoe-size-${studentId}`);
      if (tblSelect) tblSelect.value = sizeVal;
      autoSaveRecord(studentId);
    }

    function toggleShoeSocksItem(studentId, itemType) {
      const chk = document.getElementById(`${itemType}-${studentId}`);
      let isChecked = false;
      if (chk) {
        chk.checked = !chk.checked;
        isChecked = chk.checked;
      }
      
      const btn = document.getElementById(`card-${itemType}-btn-${studentId}`);
      if (btn) {
        const icon = itemType === 'shoe' ? 'fa-shoe-prints' : 'fa-socks';
        const label = itemType === 'shoe' ? 'ಶೂ' : 'ಸಾಕ್ಸ್';
        if (isChecked) {
          btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
          btn.innerHTML = `<i class="fa-solid ${icon} text-sm"></i> <span>${label} ✓</span>`;
        } else {
          btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<i class="fa-solid ${icon} text-sm"></i> <span>${label} ✗</span>`;
        }
      }

      const sShoe = document.getElementById(`shoe-${studentId}`)?.checked;
      const sSocks = document.getElementById(`socks-${studentId}`)?.checked;
      const statText = document.getElementById(`card-ss-status-text-${studentId}`);
      if (statText) {
        statText.className = (sShoe && sSocks) ? 'text-emerald-400' : 'text-amber-400';
        statText.innerText = (sShoe && sSocks) ? 'ಎರಡೂ ನೀಡಲಾಗಿದೆ' : (sShoe || sSocks ? 'ಭಾಗಶಃ ನೀಡಲಾಗಿದೆ' : 'ಬಾಕಿ');
      }

      autoSaveRecord(studentId);
    }

    function renderShoeSocksTable(students, recordsMap) {
      const tbody = document.getElementById('distributionTableBody');
      if (!tbody) return;
      if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-8 text-center text-slate-500 font-semibold bg-slate-50/5"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> No records match these filters.</td></tr>`;
        return;
      }

      const sizes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'];

      let html = '';
      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const cleanClass = normalizeClass(s.enroll_class);
        const recommendedSize = vals.shoe_size || defaultClassSizes[cleanClass] || '5';
        const shoeDist = vals.shoe_distributed === true || vals.shoe_distributed === 'true';
        const socksDist = vals.socks_distributed === true || vals.socks_distributed === 'true';

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
              <select id="shoe-size-${s.id}" onchange="handleTableShoeSizeChange('${s.id}', this.value)" class="bg-black/60 border border-white/10 rounded-xl px-2.5 py-1 text-xs font-bold text-indigo-300 focus:outline-none cursor-pointer">
                ${sizeOptions}
              </select>
            </td>

            <td class="p-2.5 bg-indigo-500/[0.01] border-x border-white/5 text-center">
              <input type="checkbox" id="shoe-${s.id}" onchange="handleTableShoeItemChange('${s.id}', 'shoe', this.checked)" ${shoeDist ? 'checked' : ''} class="w-5 h-5 rounded text-indigo-650 bg-black border-white/10 cursor-pointer transform scale-110">
            </td>

            <td class="p-2.5 bg-pink-500/[0.01] border-x border-white/5 text-center">
              <input type="checkbox" id="socks-${s.id}" onchange="handleTableShoeItemChange('${s.id}', 'socks', this.checked)" ${socksDist ? 'checked' : ''} class="w-5 h-5 rounded text-pink-650 bg-black border-white/10 cursor-pointer transform scale-110">
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

    function handleTableShoeSizeChange(studentId, sizeVal) {
      const cardSelect = document.getElementById(`card-ss-size-${studentId}`);
      if (cardSelect) cardSelect.value = sizeVal;
      autoSaveRecord(studentId);
    }

    function handleTableShoeItemChange(studentId, itemType, isChecked) {
      const btn = document.getElementById(`card-${itemType}-btn-${studentId}`);
      if (btn) {
        const icon = itemType === 'shoe' ? 'fa-shoe-prints' : 'fa-socks';
        const label = itemType === 'shoe' ? 'ಶೂ' : 'ಸಾಕ್ಸ್';
        if (isChecked) {
          btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
          btn.innerHTML = `<i class="fa-solid ${icon} text-sm"></i> <span>${label} ✓</span>`;
        } else {
          btn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<i class="fa-solid ${icon} text-sm"></i> <span>${label} ✗</span>`;
        }
      }
      autoSaveRecord(studentId);
    }

    async function autoSaveRecord(studentId)"""

ss_code = re.sub(target_pattern, replacement, ss_code)

with open('ShoeSocksDistribution.html', 'w', encoding='utf-8') as f:
    f.write(ss_code)

print("Synchronized and fixed ShoeSocksDistribution.html card view")
