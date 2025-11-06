let lastNotified = 0;
let pollIntervalMs = 1200;
let serverUrl = 'http://127.0.0.1:5000/status';

async function getStatus(){
  try {
    const r = await fetch(serverUrl);
    if (!r.ok) return { focused: true };
    return await r.json();
  } catch (e) {
    return { focused: true };
  }
}

function isFocusTab(url, domains){
  if (!url) return false;
  for (let d of domains) if (url.includes(d)) return true;
  return false;
}

async function checkFocus(){
  const status = await getStatus();
  const tabs = await chrome.tabs.query({active:true,currentWindow:true});
  const tab = tabs && tabs[0];
  let focusDomains = await new Promise(res => chrome.storage.local.get(['focusDomains'], (r)=> res(r.focusDomains || ['docs.google.com'])));
  let tabOk = tab && tab.url && isFocusTab(tab.url, focusDomains);

  if ((!status.focused || !tabOk) && Date.now() - lastNotified > 4000){
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon.png',
      title: 'Gaze',
      message: !status.focused ? 'You looked away — time to refocus.' : 'Looks like you switched away from your task.'
    });
    lastNotified = Date.now();
  }
}

setInterval(checkFocus, pollIntervalMs);
