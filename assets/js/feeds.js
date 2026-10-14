(() => {
  "use strict";
  const source = { news: "data/news.json", jobs: "data/jobs.json" };
  const safeUrl = value => {
    try { const u = new URL(String(value || "")); return u.protocol === "https:" ? u.href : ""; }
    catch { return ""; }
  };
  const clean = value => String(value ?? "").trim();
  const dateText = value => {
    const s = clean(value); if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return "";
    const d = new Date(s + "T00:00:00Z");
    return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === s ? d.toLocaleDateString("gu-IN", {day:"numeric",month:"short",year:"numeric",timeZone:"UTC"}) : "";
  };
  const make = (name, cls, txt) => { const el = document.createElement(name); if(cls)el.className=cls;if(txt!==undefined)el.textContent=txt;return el; };
  function link(label, href){ const a = make("a", "", label); a.href=href; a.target="_blank"; a.rel="noopener noreferrer";return a; }
  async function fetchFeed(type){
    const resp = await fetch(source[type], {cache:"no-store"});
    if(!resp.ok) throw new Error("feed unavailable");
    const data = await resp.json();
    if (!Array.isArray(data)) throw new Error("invalid data");
    return data.filter(entry => entry && entry.status === "Approved" && clean(entry.title) && (type === "news" ? (safeUrl(entry.source_url) || safeUrl(entry.image_url) || safeUrl(entry.pdf_url)) : safeUrl(entry.source_url)))
      .filter(entry => type !== "jobs" || !entry.deadline || (/^\d{4}-\d{2}-\d{2}$/.test(clean(entry.deadline)) && clean(entry.deadline) >= new Date().toISOString().slice(0,10)))
      .sort((a,b) => clean(b.date).localeCompare(clean(a.date)))
      .slice(0,150);
  }
  function renderEntry(entry, type) {
    const article=make("article","feed-card");
    const meta=make("div","feed-meta");
    meta.append(make("span","feed-tag",clean(entry.category) || "Education"));
    const date=dateText(entry.date); if(date) meta.append(make("span","",date));
    if(type === "jobs" && entry.deadline){ const due=dateText(entry.deadline);if(due) meta.append(make("span","",`અરજીની છેલ્લી તારીખ: ${due}`)); }
    article.append(meta);
    const primaryUrl=safeUrl(entry.source_url)||safeUrl(entry.image_url)||safeUrl(entry.pdf_url);
    const h2=make("h2");h2.append(link(clean(entry.title).slice(0,170),primaryUrl));article.append(h2);
    if(entry.summary) article.append(make("p","",clean(entry.summary).slice(0,950)));
    const actions=make("div","feed-actions");
    const sourceUrl=safeUrl(entry.source_url);if(sourceUrl)actions.append(link("મૂળ જાહેરાત જુઓ ↗",sourceUrl));
    const photo=safeUrl(entry.image_url);if(photo)actions.append(link("📷 ફોટો જુઓ ↗",photo));
    const pdf=safeUrl(entry.pdf_url);if(pdf)actions.append(link("સત્તાવાર PDF ↗",pdf));article.append(actions);
    return article;
  }
  const dataset={};
  async function initialize(type){
    const list=document.querySelector(`[data-feed-list][data-feed-type="${type}"]`);
    const controls=document.querySelector(`[data-feed-controls][data-feed-type="${type}"]`);
    const home=document.querySelector(`[data-feed-home="${type}"]`);
    if(!list&&!home) return;
    const count=list?.parentElement.querySelector("[data-feed-count]");
    const empty=list?.parentElement.querySelector("[data-feed-empty]");
    const error=list?.parentElement.querySelector("[data-feed-error]");
    try {
      const items=await fetchFeed(type);dataset[type]=items;
      if(home){home.replaceChildren(); if(!items.length)home.append(make("p","feed-subtext","હાલ કોઈ નવી ચકાસેલી માહિતી પ્રકાશિત થયેલી નથી."));
        else items.slice(0,3).forEach(entry=>{const a=make("a","home-news-link",clean(entry.title).slice(0,105)+" →");a.href=type==="jobs"?"jobs.html":"updates.html";home.append(a);});}
      if(list){
        const redraw=()=>{
          const q=clean(controls?.querySelector("[data-feed-search]")?.value).toLocaleLowerCase();
          const cat=controls?.querySelector("[data-feed-category]")?.value || "all";
          const shown=items.filter(entry=>(cat==="all"||clean(entry.category)===cat) && (!q||(clean(entry.title)+" "+clean(entry.summary)+" "+clean(entry.category)).toLocaleLowerCase().includes(q)));
          list.replaceChildren(...shown.map(entry=>renderEntry(entry,type)));
          if(empty) empty.hidden=shown.length!==0;
          if(count) count.textContent=`${shown.length} ચકાસેલી નોંધ${shown.length===1?"":"ો"}`;
        };
        controls?.querySelector("[data-feed-search]")?.addEventListener("input",redraw);
        controls?.querySelector("[data-feed-category]")?.addEventListener("change",redraw);
        redraw();
      }
    } catch {
      if(list){if(count)count.textContent="";if(error)error.hidden=false;if(empty)empty.hidden=true;}
      if(home){home.replaceChildren(make("p","feed-subtext","માહિતી હાલ લોડ કરી શકાય તેમ નથી."));}
    }
  }
  initialize("news");initialize("jobs");
})();