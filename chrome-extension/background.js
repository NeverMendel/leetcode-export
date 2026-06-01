importScripts('nacl.min.js', 'nacl-util.min.js', 'sealedbox.js');

const SECRET_NAME = "LEETCODE_COOKIE";

async function updateGitHubSecret() {
  try {
    const data = await chrome.storage.local.get(['github_token', 'github_repo']);
    if (!data.github_token || !data.github_repo) {
      return {status: "error", msg: "No GitHub token or repo configured."};
    }
    
    const [owner, repo] = data.github_repo.trim().split('/');
    if (!owner || !repo) return {status: "error", msg: "Invalid repo format. Use owner/repo."};

    const cookies = await chrome.cookies.getAll({ domain: "leetcode.com" });
    if (cookies.length === 0) return {status: "error", msg: "No cookies found for leetcode.com!"};
    
    let cookieStr = cookies.map(c => c.name + "=" + c.value).join("; ");
    if (!cookieStr.includes("LEETCODE_SESSION")) {
      return {status: "error", msg: "No LEETCODE_SESSION found. Are you logged in?"};
    }

    const keyRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/actions/secrets/public-key`, {
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${data.github_token.trim()}`,
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    
    if (!keyRes.ok) {
      const errTxt = await keyRes.text();
      return {status: "error", msg: `Failed to fetch public key. Status: ${keyRes.status}. ${errTxt}`};
    }
    const keyData = await keyRes.json();
    
    const messageBytes = nacl.util.decodeUTF8(cookieStr);
    const keyBytes = nacl.util.decodeBase64(keyData.key);
    
    const encryptedBytes = sealedBox.seal(messageBytes, keyBytes);
    const encryptedBase64 = nacl.util.encodeBase64(encryptedBytes);
    
    const uploadRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/actions/secrets/${SECRET_NAME}`, {
      method: "PUT",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": `Bearer ${data.github_token.trim()}`,
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        encrypted_value: encryptedBase64,
        key_id: keyData.key_id
      })
    });
    
    if (uploadRes.ok || uploadRes.status === 201 || uploadRes.status === 204) {
      chrome.storage.local.set({ last_sync: new Date().toLocaleString() });
      return {status: "ok", msg: "Success!"};
    } else {
      const errTxt = await uploadRes.text();
      return {status: "error", msg: `Failed to upload secret. Status: ${uploadRes.status}. ${errTxt}`};
    }
  } catch (e) {
    return {status: "error", msg: "Exception: " + e.message};
  }
}

// Run when alarm fires
chrome.alarms.create("syncAlarm", { periodInMinutes: 60 * 12 }); // Every 12 hours
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "syncAlarm") {
    updateGitHubSecret();
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "sync_now") {
    updateGitHubSecret().then((result) => {
      sendResponse(result);
    });
    return true; // Keep message channel open for async response
  }
});
