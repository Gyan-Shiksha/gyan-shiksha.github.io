(() => {
  "use strict";
  const list = document.getElementById("material-results");
  if (!list) return;
  const search = document.getElementById("material-search");
  const standard = document.getElementById("material-standard");
  const category = document.getElementById("material-category");
  const provider = document.getElementById("material-provider");
  const empty = document.getElementById("material-empty");
  const error = document.getElementById("material-error");
  const count = document.getElementById("material-result-count");
  const reset = document.getElementById("material-reset");
  const clean = value => String(value ?? "").trim();
  const hosts = Object.freeze({"drive.google.com":"Google Drive", "docs.google.com":"Google Drive", "mega.nz":"MEGA", "mega.io":"MEGA"});
  function source(url) {
    try {
      const u = new URL(url);
      const h = u.hostname.toLowerCase().replace(/^www\./, "");
      // Only direct, approved individual files—not shared master folders.
      const driveFile = h === "drive.google.com" && /^\/file\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname);
      const docsFile = h === "docs.google.com" && /^\/(?:document|spreadsheets|presentation)\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname);
      const megaFile = ["mega.nz", "mega.io"].includes(h) && /^\/file\/[A-Za-z0-9_-]+(?:\/|$)/.test(u.pathname);
      return u.protocol === "https:" && hosts[h] && !u.username && !u.password &&
        (driveFile || docsFile || megaFile) ? hosts[h] : "";
    } catch { return ""; }
  }
  function normalize(row) {
    if (!row || row.status !== "Approved") return null;
    const url = clean(row.url), title = clean(row.title), src = source(url);
    if (!title || !src) return null;
    const allowed = ["Textbook", "Notes", "Question Paper", "Worksheet", "Model Paper", "Other"];
    return {title:title.slice(0,180), url, source:src,
      standard:clean(row.standard), subject:clean(row.subject).slice(0,70),
      category:allowed.includes(row.category) ? row.category : "Other",
      description:clean(row.description).slice(0,450), updated_at:clean(row.updated_at)};
  }
  const label = {Textbook:"પાઠ્યપુસ્તક",Notes:"નોટ્સ","Question Paper":"પ્રશ્નપત્ર",Worksheet:"વર્કશીટ","Model Paper":"મોડેલ પેપર",Other:"અન્ય"};
  const el = (tag, className, text) => { const n = document.createElement(tag); if (className) n.className = className; if (text !== undefined) n.textContent = text; return n; };
  function renderCard(item) {
    const card = el("article", "material-item");
    const badges = el("div", "material-badges");
    badges.append(el("span", "material-badge", label[item.category]));
    badges.append(el("span", "material-badge source", item.source));
    card.append(badges);
    card.append(el("h3", "", item.title));
    if (item.description) card.append(el("p", "", item.description));
    const meta = [];
    if (item.standard) meta.push(item.standard === "Other" ? "અન્ય ધોરણ" : `ધોરણ ${item.standard}`);
    if (item.subject) meta.push(item.subject);
    if (/^\d{4}-\d{2}-\d{2}$/.test(item.updated_at)) meta.push(item.updated_at);
    if (meta.length) card.append(el("div", "material-meta", meta.join(" · ")));
    const a = el("a", "material-action", "ફાઇલ ખોલો / ડાઉનલોડ ↗");
    a.href = item.url; a.target = "_blank"; a.rel = "noopener noreferrer nofollow";
    a.setAttribute("aria-label", `${item.title} — ${item.source} પર ખોલો`);
    card.append(a);return card;
  }
  let all = [];
  function update() {
    const q = clean(search.value).toLocaleLowerCase("gu-IN");
    const filtered = all.filter(row =>
      (!standard.value || row.standard === standard.value) &&
      (!category.value || row.category === category.value) &&
      (!provider.value || row.source === provider.value) &&
      (!q || [row.title,row.subject,row.description,row.standard,row.category].join(" ").toLocaleLowerCase("gu-IN").includes(q)));
    list.replaceChildren(...filtered.map(renderCard));
    empty.hidden = filtered.length > 0;
    error.hidden = true;
    count.textContent = `${filtered.length} સામગ્રી મળી`;
    list.setAttribute("aria-busy", "false");
  }
  for (const node of [search,standard,category,provider]) node.addEventListener(node === search ? "input" : "change",update);
  reset.addEventListener("click",()=>{search.value="";standard.value="";category.value="";provider.value="";update();search.focus();});
  fetch("data/materials.json", {cache:"no-store"}).then(response=>{
    if (!response.ok) throw new Error("feed unavailable");return response.json();
  }).then(data=>{
    if (!Array.isArray(data)) throw new Error("invalid list");
    all = data.map(normalize).filter(Boolean).sort((a,b)=>b.updated_at.localeCompare(a.updated_at));
    update();
  }).catch(()=>{
    error.hidden=false;empty.hidden=true;count.textContent="";list.setAttribute("aria-busy","false");
  });
})();
