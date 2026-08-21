import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('EggBananaDistribution.html', 'r', encoding='utf-8') as f:
    eb_code = f.read()

target_pattern = r'function renderActiveEggBananaView\(\)[\s\S]*?async function autoSaveRecord\(studentId\)'

replacement = """function renderActiveEggBananaView() {
      const tableEl = document.getElementById('eggbanana-table-container');
      const cardsEl = document.getElementById('eggbanana-cards-container');

      // Always render both so that DOM elements exist for auto-saving and print drawers
      renderEggBananaCards(currentEggBananaStudents, currentEggBananaRecordsMap);
      renderEggBananaTable(currentEggBananaStudents, currentEggBananaRecordsMap);

      if (currentEggBananaViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) cardsEl.classList.remove('hidden');
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) tableEl.classList.remove('hidden');
      }
    }

    function renderTable(students, recordsMap) {
      currentEggBananaStudents = students;
      currentEggBananaRecordsMap = recordsMap;
      setEggBananaViewMode(currentEggBananaViewMode, false);
      renderActiveEggBananaView();
    }

    function renderEggBananaCards(students, recordsMap) {
      const container = document.getElementById('eggbanana-cards-container');
      if (!container) return;
      container.innerHTML = '';

      if (students.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold glass-card rounded-2xl border border-white/5"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-500"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const pref = vals.food_preference || 'Egg';
        const isDist = vals.distributed_status === true || vals.distributed_status === 'true';

        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const isBoy = !isGirl;

        const cardHtml = `
          <div class="glass-card rounded-2xl p-4 border border-white/10 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5" data-card-eb-id="${s.id}">
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

            <!-- Food Choice Pills -->
            <div class="space-y-1.5">
              <span class="text-[10px] font-extrabold text-slate-300 uppercase tracking-wider block">ಆಹಾರ ಆಯ್ಕೆ / Food Choice:</span>
              <div class="grid grid-cols-3 gap-1.5">
                <button type="button" onclick="setEggBananaCardPref('${s.id}', 'Egg')" id="card-pref-egg-${s.id}" class="py-1.5 px-2 rounded-xl text-xs font-black transition cursor-pointer border-0 ${pref === 'Egg' ? 'bg-amber-500 text-slate-950 shadow-md' : 'bg-black/40 text-slate-400 border border-white/10'}">
                  🥚 ಮೊಟ್ಟೆ
                </button>
                <button type="button" onclick="setEggBananaCardPref('${s.id}', 'Banana')" id="card-pref-banana-${s.id}" class="py-1.5 px-2 rounded-xl text-xs font-black transition cursor-pointer border-0 ${pref === 'Banana' ? 'bg-yellow-400 text-slate-950 shadow-md' : 'bg-black/40 text-slate-400 border border-white/10'}">
                  🍌 ಬಾಳೆಹಣ್ಣು
                </button>
                <button type="button" onclick="setEggBananaCardPref('${s.id}', 'Chikki')" id="card-pref-chikki-${s.id}" class="py-1.5 px-2 rounded-xl text-xs font-black transition cursor-pointer border-0 ${pref === 'Chikki' ? 'bg-orange-500 text-white shadow-md' : 'bg-black/40 text-slate-400 border border-white/10'}">
                  🥜 ಚಿಕ್ಕಿ
                </button>
              </div>
            </div>

            <!-- Distribution Toggle Button -->
            <button type="button" onclick="toggleEggBananaDist('${s.id}')" id="card-eb-dist-btn-${s.id}" class="w-full py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-2 ${isDist ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-black/50 text-slate-400 border border-white/10'}">
              <i class="fa-solid fa-circle-check text-sm"></i> <span>${isDist ? 'ವಿತರಿಸಲಾಗಿದೆ (Distributed) ✓' : 'ವಿತರಣೆ ಬಾಕಿ (Pending) ✗'}</span>
            </button>

            <!-- Footer Save Status -->
            <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
              <span class="text-[10px] text-slate-400">ಆಯ್ಕೆ: <strong id="card-eb-pref-text-${s.id}" class="text-white">${pref}</strong></span>
              <span id="card-eb-save-status-${s.id}" class="text-[10px] text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> Saved</span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function setEggBananaCardPref(studentId, prefVal) {
      const tblSelect = document.getElementById(`pref-${studentId}`);
      if (tblSelect) tblSelect.value = prefVal;

      // Update Card buttons
      ['Egg', 'Banana', 'Chikki'].forEach(p => {
        const btn = document.getElementById(`card-pref-${p.toLowerCase()}-${studentId}`);
        if (btn) {
          if (p === prefVal) {
            const activeBg = p === 'Egg' ? 'bg-amber-500 text-slate-950 shadow-md' : (p === 'Banana' ? 'bg-yellow-400 text-slate-950 shadow-md' : 'bg-orange-500 text-white shadow-md');
            btn.className = `py-1.5 px-2 rounded-xl text-xs font-black transition cursor-pointer border-0 ${activeBg}`;
          } else {
            btn.className = 'py-1.5 px-2 rounded-xl text-xs font-black transition cursor-pointer border-0 bg-black/40 text-slate-400 border border-white/10';
          }
        }
      });

      const prefText = document.getElementById(`card-eb-pref-text-${studentId}`);
      if (prefText) prefText.innerText = prefVal;

      autoSaveRecord(studentId);
    }

    function toggleEggBananaDist(studentId) {
      const chk = document.getElementById(`status-${studentId}`);
      let isChecked = false;
      if (chk) {
        chk.checked = !chk.checked;
        isChecked = chk.checked;
      }
      
      const btn = document.getElementById(`card-eb-dist-btn-${studentId}`);
      if (btn) {
        if (isChecked) {
          btn.className = "w-full py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-2 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
          btn.innerHTML = `<i class="fa-solid fa-circle-check text-sm"></i> <span>ವಿತರಿಸಲಾಗಿದೆ (Distributed) ✓</span>`;
        } else {
          btn.className = "w-full py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-2 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<i class="fa-solid fa-circle-check text-sm"></i> <span>ವಿತರಣೆ ಬಾಕಿ (Pending) ✗</span>`;
        }
      }
      autoSaveRecord(studentId);
    }

    function renderEggBananaTable(students, recordsMap) {
      const tbody = document.getElementById('distributionTableBody');
      if (!tbody) return;
      if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-slate-500 font-semibold bg-slate-50/5"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> No records match these filters.</td></tr>`;
        return;
      }

      const options = ['Egg', 'Banana', 'Chikki', 'None'];

      let html = '';
      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const pref = vals.food_preference || 'Egg';
        const isDist = vals.distributed_status === true || vals.distributed_status === 'true';

        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const displayGender = isGirl ? 'Girl / ಹೆಣ್ಣು' : 'Boy / ಗಂಡು';

        const prefOptions = options.map(opt => `<option value="${opt}" ${opt === pref ? 'selected' : ''}>${opt}</option>`).join('');

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
              <select id="pref-${s.id}" onchange="handleTablePrefChange('${s.id}', this.value)" class="bg-black/60 border border-white/10 rounded-xl px-2.5 py-1 text-xs font-bold text-indigo-300 focus:outline-none cursor-pointer">
                ${prefOptions}
              </select>
            </td>

            <td class="p-2.5 bg-emerald-500/[0.01] border-x border-white/5 text-center">
              <input type="checkbox" id="status-${s.id}" onchange="handleTableDistChange('${s.id}', this.checked)" ${isDist ? 'checked' : ''} class="w-5 h-5 rounded text-emerald-600 bg-black border-white/10 cursor-pointer transform scale-110">
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

    function handleTablePrefChange(studentId, prefVal) {
      setEggBananaCardPref(studentId, prefVal);
    }

    function handleTableDistChange(studentId, isChecked) {
      const btn = document.getElementById(`card-eb-dist-btn-${studentId}`);
      if (btn) {
        if (isChecked) {
          btn.className = "w-full py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-2 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
          btn.innerHTML = `<i class="fa-solid fa-circle-check text-sm"></i> <span>ವಿತರಿಸಲಾಗಿದೆ (Distributed) ✓</span>`;
        } else {
          btn.className = "w-full py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-2 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<i class="fa-solid fa-circle-check text-sm"></i> <span>ವಿತರಣೆ ಬಾಕಿ (Pending) ✗</span>`;
        }
      }
      autoSaveRecord(studentId);
    }

    async function autoSaveRecord(studentId)"""

eb_code = re.sub(target_pattern, replacement, eb_code)

with open('EggBananaDistribution.html', 'w', encoding='utf-8') as f:
    f.write(eb_code)

print("Synchronized and fixed EggBananaDistribution.html card view")
