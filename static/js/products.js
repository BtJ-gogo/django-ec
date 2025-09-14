const classRow = document.querySelector(".row");
let page = 2;
let loading = false;
let hasNext = true;

window.addEventListener("scroll", async () => {
  if (!hasNext || loading) {
    return;
  }

  if (window.scrollY + window.innerHeight >= document.body.offsetHeight - 200) {
    loading = true;
    const urlstring = window.location.pathname;
    const category = decodeURIComponent(urlstring.split("/")[3]);
    try {
      let res;
      if (category) {
        res = await fetch(`/products/books/${category}/load/?page=${page}`);
      } else {
        res = await fetch(`/products/books/load/?page=${page}`);
      }
      const data = await res.json();
      if (!data.html) {
        hasNext = data.has_next;
        return
      }

      classRow.insertAdjacentHTML("beforeend", data.html);
      page++;
      hasNext = data.has_next;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }
});
