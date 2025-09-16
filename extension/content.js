chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_PAGE_CONTENT") {
    setTimeout(() => {
      const bodyText = document.body.innerText || "No content found.";
      sendResponse({ content: bodyText });
    }, 2000);
    return true;
  }
});
