'use strict';
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'verityweave-review-selection',
    title: 'Review selection with VerityWeave',
    contexts: ['selection']
  });
});
chrome.contextMenus.onClicked.addListener(async (info) => {
  if (info.menuItemId !== 'verityweave-review-selection') return;
  await chrome.storage.session.set({
    verityweaveSelection: info.selectionText || '',
    verityweaveSourceUrl: info.pageUrl || '',
    verityweaveCapturedAt: new Date().toISOString()
  });
  await chrome.tabs.create({url: chrome.runtime.getURL('review.html')});
});
