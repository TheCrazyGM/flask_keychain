function getCurrentUTCDateTime() {
  const now = new Date();
  return now.toISOString();
}
document
  .getElementById("loginForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const status = document.getElementById("status");
    status.textContent = "";
    if (!username) {
      status.textContent = "Please enter your Hive username.";
      return;
    }
    if (typeof window.hive_keychain === "undefined") {
      status.textContent = "Hive Keychain extension not detected!";
      return;
    }
    const datetimeToSign = getCurrentUTCDateTime();
    window.hive_keychain.requestSignBuffer(
      username,
      datetimeToSign,
      "Posting",
      function (response) {
        if (response.success) {
          status.textContent = "Posting signed! Sending to API...";
          const proof = response.result;
          const pubkey =
            response.publicKey ||
            (response.data && response.data.publicKey) ||
            null;
          if (!pubkey) {
            status.textContent =
              "Could not retrieve public key from Keychain response.";
            return;
          }
          const payload = {
            challenge: proof,
            username: username,
            pubkey: pubkey,
            proof: datetimeToSign,
          };
          fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          })
            .then((r) => r.json())
            .then((data) => {
              if (data.success) {
                let msg = "Login successful! <br>";
                if (data.token) {
                  localStorage.setItem("token", data.token);
                  msg += ` Token: <code>${data.token}</code> <br>`;
                }
                status.innerHTML = msg;
              } else {
                status.textContent = data.error || "Login failed.";
              }
            })
            .catch((err) => {
              status.textContent = "API error: " + err;
            });
        } else {
          status.textContent = "Keychain signature failed.";
        }
      },
    );
  });
