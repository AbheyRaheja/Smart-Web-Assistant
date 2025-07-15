chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_PAGE_CONTENT") {
    const bodyText = document.body.innerText;
    sendResponse({ content: bodyText });
  }
});
