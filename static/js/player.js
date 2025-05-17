// helper: POST → JSON ----------------------------------
async function postJSON(url, data = {}) {
  const r = await fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(data)
  });
  return r.ok ? r.json() : null;
}

// toast -------------------------------------------------
function toast(msg, cls = "success") {
  const html = `
   <div class="toast align-items-center text-white bg-${cls}" role="alert" aria-live="assertive" aria-atomic="true">
     <div class="d-flex">
       <div class="toast-body">${msg}</div>
       <button type="button" class="btn-close btn-close-white me-2 m-auto"
               data-bs-dismiss="toast"></button>
     </div>
   </div>`;
  const box = document.querySelector(".toast-container");
  box.insertAdjacentHTML("beforeend", html);
  const toastEl = box.lastElementChild;
  const bsToast = new bootstrap.Toast(toastEl, {
    delay: 3000,      // 3 секунды
    autohide: true    // автоматическое скрытие
  });
  bsToast.show();
  // по завершении — чистим DOM
  toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
}

// обновить карточку -------------------------------------
function updateCard(d) {
  if (!d) return;
  document.querySelector("#title").innerText  = d.title;
  document.querySelector("#artist").innerText = d.artist;
  document.querySelector("#genre").innerText  = d.genre;
  if (d.sp_url) document.querySelector("#sp_iframe").src = d.sp_url;
  if (d.vk_url) document.querySelector("#vk_iframe").src = d.vk_url;
}

// NEXT --------------------------------------------------
document.querySelector("#btn_next").onclick =
  () => postJSON("/api/next").then(updateCard);

// BY GENRE — без prompt, просто следующий трек того же жанра
document.querySelector("#btn_genre").onclick = async () => {
  const d = await postJSON("/api/genre");
  toast(`Another ${d.genre} track`, "info");
  updateCard(d);
};

// Like / Dislike ----------------------------------------
document.querySelector("#btn_like").onclick = () => {
  fetch("/api/like", { method:"POST" });
  toast("We'll remember you appreciate this song 👍", "success");
};
document.querySelector("#btn_dislike").onclick = () => {
  fetch("/api/dislike", { method:"POST" });
  toast("We'll remember you don't like this song 👎", "danger");
};