function openSearch() {
  const searchBar = document.getElementById("search-bar")
  const resultContainer = document.getElementById("results-container")
  const searchContainer = document.getElementById("search-container")
  if (searchContainer.style.display === "none" || searchContainer.style.display === "") {
    searchBar.value = ""
    resultContainer.innerHTML = ""
    searchContainer.style.display = "block"
    searchBar.focus()
  } else {
    searchContainer.style.display = "none"
  }
}

function closeSearch() {
  const searchContainer = document.getElementById("search-container")
  searchContainer.style.display = "none"
}

function registerHandlers(onInputFn) {
  const searchBar = document.getElementById("search-bar")
  const searchContainer = document.getElementById("search-container")
  //searchBar.addEventListener("keyup", (e) => {
  //  if (e.key === "Enter") {
  //    const anchor = document.getElementsByClassName("result-card")[0]
  //    // TODO: open url
  //  }
  //})
  searchBar.addEventListener("input", onInputFn)
  document.addEventListener("keydown", (event) => {
    if (event.key === "k" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault()
      openSearch()
    }
    if (event.key === "Escape") {
      event.preventDefault()
      closeSearch()
    }
  })

  const searchButton = document.getElementById("search-icon")
  searchButton.addEventListener("click", (_) => {
    openSearch()
  })
  searchButton.addEventListener("keydown", (_) => {
    openSearch()
  })
  searchContainer.addEventListener("click", (_) => {
    closeSearch()
  })
  document.getElementById("search-space").addEventListener("click", (evt) => {
    evt.stopPropagation()
  })
}

function displayResults(term, finalResults) {
  const results = document.getElementById("results-container")
  if (finalResults.length === 0) {
    results.innerHTML = `<div class="result-card"><p>No results.</p></div>`
  } else {
    results.innerHTML = finalResults
      .map((result) => {
        const linebreak = result.content.indexOf('\n')
        return `<div class="result-card">
          <a href="${result.url}" class="result-title"><h3>${result.title}</h3></a>
          <p><span class="result-meta">${result.modified_at}</span><span> · </span><span class="result-meta">${result.id}</span><span> · </span><span>${result.content.slice(0, Math.min(linebreak, 120))}</span></p>
        </div>`
      })
      .join("\n")
  }
}

async function downloadIndex() {
  const response = await fetch("/index.json")
  return await response.json()
}

(async function() {
  const encoder = (str) => str.toLowerCase().split(/([^a-z]|[^\x00-\x7F])/)
  const searchIndex = new FlexSearch.Document({
    cache: true,
    charset: "latin:extra",
    optimize: true,
    index: [
      {
        field: "title",
        tokenize: "forward",  // try: "full"
        encode: encoder,
        //encode: "advanced",
      },
      {
        field: "content",
        tokenize: "reverse",  // try: "full"
        encode: encoder,
        //encode: "advanced",
      },
    ],
  })

  const content = await downloadIndex()
  for (const [key, value] of Object.entries(content)) {
    searchIndex.add({
      id: key,
      title: value.title,
      content: value.content,
      url: value.url,
    })
  }

  const formatForDisplay = (id) => ({
    id,
    url: content[id].url,
    title: content[id].title,
    content: content[id].content,
    modified_at: content[id].modified_at,
  })

  registerHandlers((e) => {
    const term = e.target.value
    const searchResults = searchIndex.search(term, [
      {
        field: "title",
        limit: 5,
      },
      {
        field: "content",
        limit: 10,
      },
    ])
    const getByField = (field) => {
      const results = searchResults.filter((x) => x.field === field)
      if (results.length === 0) {
        return []
      } else {
        return [...results[0].result]
      }
    }
    const allIds = new Set([...getByField("title"), ...getByField("content")])
    const finalResults = [...allIds].map(formatForDisplay)
    displayResults(term, finalResults)
  })
})()
