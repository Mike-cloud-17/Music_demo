// helper ------------------------------------------------
async function postJSON(url, data = {}) {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return r.ok ? r.json() : null;
  }
  function toast(txt, cls = "success") {
    const html = `
     <div class="toast align-items-center text-bg-${cls}" role="alert">
       <div class="d-flex"><div class="toast-body">${txt}</div>
         <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
       </div>
     </div>`;
    const box = document.querySelector(".toast-container");
    box.insertAdjacentHTML("beforeend", html);
    new bootstrap.Toast(box.lastElementChild, { delay: 1800 }).show();
  }
  
  // update card -------------------------------------------
  function updateCard(j) {
    if (!j) return;
    document.querySelector("#title").innerText  = j.title;
    document.querySelector("#artist").innerText = j.artist;
    document.querySelector("#genre").innerText  = j.genre;
    if (j.sp_url) document.querySelector("#sp_iframe").src = j.sp_url;
    if (j.yt_url) document.querySelector("#yt_iframe").src = j.yt_url;
  }
  
  // buttons -----------------------------------------------
  document.querySelector("#btn_next").onclick = () =>
    postJSON("/api/next").then(updateCard);
  
  document.querySelector("#btn_genre").onclick = () => {
    const g = prompt("Genre?", "Pop");
    if (g) postJSON("/api/genre", { genre: g }).then(updateCard);
  };
  
  document.querySelector("#btn_like").onclick = () => {
    fetch("/api/like", { method: "POST" });
    toast("Saved ❤️", "success");
  };
  document.querySelector("#btn_dislike").onclick = () => {
    fetch("/api/dislike", { method: "POST" });
    toast("Skipped 👎", "danger");
  };
  