const classRow = document.querySelector(".row");
let page = 2;
let loading = false;
let hasNext = true;

function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

window.addEventListener("scroll", async () => {
  if (!hasNext || loading) {
    return;
  }

  if (window.scrollY + window.innerHeight >= document.body.offsetHeight - 200) {
    loading = true;
    const urlString = window.location.pathname;
    const category = decodeURIComponent(urlString.split("/")[3]);
    const search = getQueryParam("search");
    
    let fetchUrl;
    if (category) {
      fetchUrl = `/products/books/${category}/load/?page=${page}`;
    }

    if (search) {
      fetchUrl = `/products/books/load/?page=${page}&search=${search}`;
    }

    if (!category && !search) {
      fetchUrl = `/products/books/load/?page=${page}`;
    }

    try {
      const res = await fetch(fetchUrl);
      const data = await res.json();
      if (!data.html) {
        hasNext = data.has_next;
        return;
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
