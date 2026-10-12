(() => {
  "use strict";
  const results = document.getElementById("material-results");
  const summary = document.getElementById("material-summary");
  const controls = document.getElementById("material-browse-controls");
  const grade = document.getElementById("material-standard");
  const subject = document.getElementById("material-subject");
  const search = document.getElementById("material-search");
  const reset = document.getElementById("material-reset");
  const empty = document.getElementById("material-empty");
  const emptyTitle = document.getElementById("material-empty-title");
  const emptyMessage = document.getElementById("material-empty-message");
  const error = document.getElementById("material-error");
  const more = document.getElementById("material-load-more");
  const kindButtons = [...document.querySelectorAll("[data-material-kind]")];
  if (!results || !summary || !controls || !grade || !subject || !search || !reset) return;

  const types = Object.freeze({
    "Notes": "📝 નોટ્સ", "Question Paper": "📋 પ્રશ્નપત્ર",
    "Worksheet": "✏️ વર્કશીટ", "Textbook": "📘 પુસ્તક",
    "PDF": "📄 PDF", "Image": "🖼️ ફોટો / ચાર્ટ",
    "Presentation": "📊 પ્રેઝન્ટેશન", "Video": "🎬 વિડિયો",
    "Audio": "🎧 ઑડિયો", "Other": "📂 અન્ય"
  });
  const clean = value => String(value == null ? "" : value).trim();
  const providers = Object.freeze({
    "drive.google.com": "Google Drive",
    "docs.google.com": "Google Drive",
    "mega.nz": "MEGA",
    "mega.io": "MEGA"
  });

  // Accept ONLY individual Google Drive, Docs and MEGA files.
  // A public share link can still be redistributed; access is not protected by this site.
  function fileProvider(value) {
    try {
      const u = new URL(value);
      const host = u.hostname.toLowerCase();
      if (u.protocol !== "https:" || u.username || u.password || !providers[host]) return "";
      const driveFile = host === "drive.google.com" &&
        (/^\/file\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname) ||
         (u.pathname === "/open" && /^[A-Za-z0-9_-]+$/.test(u.searchParams.get("id") || "")));
      const docFile = host === "docs.google.com" &&
        /^\/(?:document|spreadsheets|presentation)\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname);
      const megaFile = (host === "mega.nz" || host === "mega.io") &&
        /^\/file\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname);
      return (driveFile || docFile || megaFile) ? providers[host] : "";
    } catch {
      return "";
    }
  }

  function safeItem(entry) {
    if (!entry || entry.status !== "Approved" || entry.rights_verified !== true) return null;
    const url = clean(entry.url);
    const provider = fileProvider(url);
    const title = clean(entry.title).slice(0, 180);
    const standard = clean(entry.standard).slice(0, 60);
    const subject = clean(entry.subject).slice(0, 80);
    const category = Object.prototype.hasOwnProperty.call(types, entry.category)
      ? entry.category : "Other";
    if (!provider || !title || !standard || !subject) return null;
    return {
      title, url, provider, standard, subject, category,
      description: clean(entry.description).slice(0, 500),
      date: /^\d{4}-\d{2}-\d{2}$/.test(clean(entry.updated_at)) ? clean(entry.updated_at) : ""
    };
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function fileCard(item) {
    const card = el("article", "material-resource-card");
    const top = el("div", "material-resource-top");
    top.append(el("span", "material-format", types[item.category]));
    top.append(el("span", "material-provider", item.provider));
    const title = el("h3", "", item.title);
    const desc = el("p", "material-resource-description", item.description ||
      "આ ફાઇલની વિગતો જોવા માટે નીચેની લિંક ખોલો.");
    const meta = el("div", "material-resource-meta",
      [item.standard === "General" ? "સામાન્ય" : item.standard, item.subject, item.date].filter(Boolean).join(" · "));
    const open = el("a", "material-action", "ફાઇલ જુઓ ↗");
    open.href = item.url; open.target = "_blank"; open.rel = "noopener noreferrer nofollow";
    open.setAttribute("aria-label", item.title + " — " + item.provider + " પર ફાઇલ જુઓ");
    card.append(top, title, desc, meta, open);
    return card;
  }

  let all = [], selectedKind = "", visibleCount = 12;
  const norm = str => clean(str).toLocaleLowerCase("gu-IN");

  function fillSelect(select, values, firstLabel, preferred) {
    const options = [el("option", "", firstLabel)];
    options[0].value = "";
    for (const value of values) {
      const option = el("option", "", value === "General" ? "સામાન્ય" : value);
      option.value = value;
      options.push(option);
    }
    select.replaceChildren(...options);
    select.value = values.includes(preferred) ? preferred : "";
  }

  function updateSubjectOptions() {
    const previous = subject.value;
    const subset = all.filter(item => !grade.value || item.standard === grade.value);
    fillSelect(subject, [...new Set(subset.map(x => x.subject))].sort((a,b)=>a.localeCompare(b,"gu")), "બધા વિષય", previous);
  }

  function filteredItems() {
    const term = norm(search.value);
    return all.filter(item =>
      (!selectedKind || selectedKind === item.category) &&
      (!grade.value || grade.value === item.standard) &&
      (!subject.value || subject.value === item.subject) &&
      (!term || norm([item.title, item.description, item.standard, item.subject,
        types[item.category]].join(" ")).includes(term)));
  }

  function update() {
    const filtered = filteredItems();
    results.replaceChildren(...filtered.slice(0,visibleCount).map(fileCard));
    results.setAttribute("aria-busy", "false");
    const noMatch = all.length && !filtered.length;
    empty.hidden = !noMatch;
    if (noMatch) {
      emptyTitle.textContent = "આ પસંદગીમાં સામગ્રી નથી";
      emptyMessage.textContent = "બીજો વિષય અથવા ધોરણ પસંદ કરો, અથવા ‘બધું ફરી જુઓ’ દબાવો.";
    }
    summary.textContent = filtered.length === all.length
      ? "કુલ " + all.length + " મંજૂર ફાઇલો"
      : filtered.length + " સામગ્રી મળી · કુલ " + all.length;
    if (more) more.hidden = filtered.length <= visibleCount;
    error.hidden = true;
  }

  kindButtons.forEach(button => {
    button.addEventListener("click", () => {
      selectedKind = button.dataset.materialKind || "";
      for (const b of kindButtons) {
        const active = b === button;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-pressed", String(active));
      }
      visibleCount = 12;
      update();
    });
  });
  grade.addEventListener("change", () => {updateSubjectOptions();visibleCount=12;update();});
  subject.addEventListener("change", () => {visibleCount=12;update();});
  search.addEventListener("input", () => {visibleCount=12;update();});
  reset.addEventListener("click", () => {
    grade.value = ""; search.value = ""; selectedKind = ""; visibleCount=12;
    updateSubjectOptions();subject.value="";
    for (const button of kindButtons) {
      const active = !button.dataset.materialKind;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    }
    update();
  });
  if (more) more.addEventListener("click", () => { visibleCount+=12;update(); });

  results.setAttribute("aria-busy", "true");
  fetch("data/materials.json", {cache:"no-store"})
    .then(res => {if (!res.ok) throw new Error("material catalogue unavailable");return res.json();})
    .then(rows => {
      if (!Array.isArray(rows)) throw new Error("invalid material catalogue");
      const seen = new Set();
      all = rows.map(safeItem).filter(item => {
        if (!item || seen.has(item.url)) return false;
        seen.add(item.url);return true;
      }).sort((a,b)=>b.date.localeCompare(a.date));
      if (!all.length) {
        summary.textContent = "હાલ પ્રકાશિત કરવા યોગ્ય ફાઇલ ઉપલબ્ધ નથી";
        empty.hidden = false;
        emptyTitle.textContent = "મંજૂર ફાઇલો આવતાં અહીં દેખાશે";
        emptyMessage.textContent = "PDF, ફોટો, Notes અને બીજા દસ્તાવેજો ચકાસણી બાદ ઉમેરવામાં આવશે. હાલ નીચેના શૈક્ષણિક માર્ગદર્શન વાંચી શકો છો અથવા સામગ્રીની વિનંતી મોકલો.";
        results.setAttribute("aria-busy","false");
        return;
      }
      controls.hidden = false;
      fillSelect(grade, [...new Set(all.map(x=>x.standard))].sort((a,b)=>
        /^\d+$/.test(a) && /^\d+$/.test(b) ? Number(a)-Number(b) : a.localeCompare(b,"gu")), "બધાં ધોરણ", "");
      updateSubjectOptions();
      const present = new Set(all.map(item => item.category));
      for (const button of kindButtons) {
        button.hidden = !!button.dataset.materialKind && !present.has(button.dataset.materialKind);
      }
      update();
    })
    .catch(() => {
      results.setAttribute("aria-busy","false");
      summary.textContent = "સામગ્રીની સૂચિ ઉપલબ્ધ નથી";
      error.hidden = false;empty.hidden=true;
    });
})();
