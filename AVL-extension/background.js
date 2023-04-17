chrome.tabs.onUpdated.addListener(function() {
});

// chrome.contextMenus.create({
//     id: "avl-checker",
//     title: "avl-checker",
//     contexts: ["selection", "link"]
// });

// chrome.contextMenus.onClicked.addListener(function(info, tab) {
//     if (info.menuItemId === "avl-checker") {
//         var selectedText = info.selectionText;
//         var url = chrome.runtime.getURL("popup.html") + "?check_url=" + encodeURIComponent(selectedText);
//         chrome.windows.create({
//             url: url,
//             type: "popup",
//             focused: true,
//             width: 30,
//             height: 30,
//         });
//     }
// });

