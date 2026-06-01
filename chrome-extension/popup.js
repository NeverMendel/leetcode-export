document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get(['github_token', 'github_repo', 'last_sync'], (res) => {
    if (res.github_token) document.getElementById('pat').value = res.github_token;
    if (res.github_repo) document.getElementById('repo').value = res.github_repo;
    if (res.last_sync) document.getElementById('status').innerText = "Last sync: " + res.last_sync;
  });

  document.getElementById('save').addEventListener('click', () => {
    chrome.storage.local.set({
      github_token: document.getElementById('pat').value,
      github_repo: document.getElementById('repo').value
    }, () => {
      document.getElementById('status').innerText = "Settings saved! Extension is ready.";
    });
  });

  document.getElementById('sync').addEventListener('click', () => {
    document.getElementById('status').innerText = "Fetching cookie and pushing to GitHub...";
    chrome.runtime.sendMessage({ action: "sync_now" }, (res) => {
      if (res && res.status === "ok") {
        document.getElementById('status').innerText = "Success! GitHub Secret Updated. \nYour daily GitHub Action will now run flawlessly.";
      } else {
        document.getElementById('status').innerText = "Error: " + (res ? res.msg : "Unknown error");
      }
    });
  });
});
